# -*- coding: utf-8 -*-
"""
Go/No-Go Korean port - runtime log checker

Verifies what ACTUALLY happened during a session, from the .log file.
The offline suite proves the code is right; this proves the machine
delivered it correctly.

Usage:
    python check_log.py                    # newest log in data\\
    python check_log.py path\\to\\file.log

Output is ASCII only.
"""
from __future__ import print_function
import glob
import os
import re
import sys

TOL = 0.030   # 30 ms tolerance on the 2000 ms stimulus window


def newest_log():
    here = os.path.dirname(os.path.abspath(__file__))
    pats = [os.path.join(here, 'data', '*.log'),
            os.path.join(here, 'dist', 'GoNoGo', 'data', '*.log')]
    files = []
    for p in pats:
        files += glob.glob(p)
    if not files:
        return None
    return max(files, key=os.path.getmtime)


path = sys.argv[1] if len(sys.argv) > 1 else newest_log()
if not path or not os.path.isfile(path):
    print('No log file found. Run the experiment first, or pass a path.')
    sys.exit(1)

print('Log: %s\n' % path)
lines = open(path, encoding='utf-8', errors='replace').read().splitlines()

issues = []


def note(ok, msg):
    print('  [%s] %s' % ('PASS' if ok else 'WARN', msg))
    if not ok:
        issues.append(msg)


# ---------------------------------------------------------------- setup
print('=== Environment ===')
fr = None
for ln in lines:
    m = re.search(r'actual frame rate measured at ([\d.]+)Hz', ln)
    if m:
        fr = float(m.group(1))
print('  frame rate: %s Hz' % (('%.2f' % fr) if fr else 'not measured'))
note(fr is not None, 'frame rate was measured')

m = [ln for ln in lines if 'Created sequence' in ln]
if m:
    print('  %s' % m[0].split('\t')[-1].strip())
    note('nReps=10' in m[0], 'nReps is 10')
    note('random' in m[0], 'method is random')
    note('trialTypes=4' in m[0], '4 conditions loaded')
else:
    note(False, 'no "Created sequence" line found')

seed = [ln for ln in lines if 'trialSeed' in ln]
note(bool(seed), 'seed recorded: %s' % (seed[0].split('=')[-1].strip() if seed else 'MISSING'))

note(not any('ptb backend' in ln for ln in lines),
     'no ptb-backend fallback detected')

# ---------------------------------------------------------------- trials
print('\n=== Trial sequence ===')
trials = []
for ln in lines:
    m = re.search(r"New trial \(rep=(\d+), index=(\d+)\): "
                  r"\{'this_image': '([^']+)'", ln)
    if m:
        trials.append((int(m.group(1)), int(m.group(2)), m.group(3)))

print('  trials started: %d' % len(trials))
seq = [t[2] for t in trials]
print('  go=%d  nogo=%d' % (seq.count('go.png'), seq.count('nogo.png')))

if len(trials) == 40:
    note(True, 'all 40 trials ran')
else:
    note(False, 'only %d of 40 trials ran (session interrupted?)' % len(trials))

# block structure per rep
reps = {}
for rep, idx, img in trials:
    reps.setdefault(rep, []).append(img)
bad = [r for r, imgs in reps.items() if len(imgs) == 4 and imgs.count('nogo.png') != 1]
note(not bad, 'exactly 1 nogo per complete rep' if not bad else 'reps off: %s' % bad)

# ---------------------------------------------------------------- timing
print('\n=== Stimulus presentation timing ===')
on = None
durations = []
for ln in lines:
    parts = ln.split('\t')
    if len(parts) < 3:
        continue
    try:
        t = float(parts[0].strip())
    except ValueError:
        continue
    body = parts[-1].strip()
    if body == 'image: autoDraw = True':
        on = t
    elif body == 'image: autoDraw = False' and on is not None:
        durations.append(t - on)
        on = None

if not durations:
    print('  no stimulus intervals found')
else:
    full = [d for d in durations if d > 1.5]      # no-response trials
    early = [d for d in durations if d <= 1.5]    # ended by a keypress
    print('  intervals measured : %d' % len(durations))
    print('  full-window trials : %d' % len(full))
    print('  response-ended     : %d' % len(early))
    if full:
        print('  full-window range  : %.4f - %.4f s' % (min(full), max(full)))
        off = [d for d in full if abs(d - 2.0) > TOL]
        note(not off, '2000 ms window held (tolerance %d ms)' % int(TOL * 1000)
             if not off else '%d trials outside tolerance: %s'
             % (len(off), ['%.4f' % d for d in off[:5]]))
    if durations:
        first = durations[0]
        note(abs(first - 2.0) <= TOL or first <= 1.5,
             'first trial %.4f s (texture preload working)' % first)

# ---------------------------------------------------------------- input
print('\n=== Keyboard input ===')
presses = [ln.split('\t')[-1].strip() for ln in lines if 'Keypress' in ln
           or 'KeyPress' in ln]
space = [p for p in presses if p.lower().endswith('space')]
other = [p for p in presses if not p.lower().endswith('space')
         and 'escape' not in p.lower()]
print('  space presses: %d' % len(space))
if other:
    print('  other keys   : %s' % other[:8])
note(not any(re.search(r'[\uac00-\ud7a3\u3131-\u318e]', p) for p in other),
     'no Hangul IME artefacts in keypress log')

# ---------------------------------------------------------------- summary
print('\n' + '=' * 60)
if issues:
    print(' %d item(s) need attention:' % len(issues))
    for i in issues:
        print('   - %s' % i)
else:
    print(' Runtime behaviour matches the frozen specification.')
print('=' * 60)
