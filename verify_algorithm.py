# -*- coding: utf-8 -*-
"""
Go/No-Go Korean port - algorithm verification suite

Run inside the project venv:
    .venv\\Scripts\\activate
    python verify_algorithm.py

Checks that the port preserves every measurement invariant frozen in
gng_ko_spec.md. No display needed - this does not open a window.

Output is ASCII only so it renders correctly in cp949 consoles.
"""
from __future__ import print_function
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, 'gng_ko.py')
if not os.path.isfile(SCRIPT):
    SCRIPT = os.path.join(HERE, 'main.py')
CONDITIONS = os.path.join(HERE, 'conditions.xlsx')

results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    mark = 'PASS' if ok else 'FAIL'
    print('  [%s] %-46s %s' % (mark, name, detail))
    return ok


# =====================================================================
print('\n=== 1. conditions.xlsx integrity ===')
# =====================================================================
try:
    from psychopy import data as psydata
    conds = psydata.importConditions(CONDITIONS)
except Exception as e:
    print('  Cannot import conditions:', e)
    sys.exit(1)

check('4 conditions', len(conds) == 4, 'got %d' % len(conds))
check('columns are this_image / corr_ans',
      set(conds[0].keys()) == {'this_image', 'corr_ans'},
      str(sorted(conds[0].keys())))

go = [c for c in conds if c['this_image'] == 'go.png']
nogo = [c for c in conds if c['this_image'] == 'nogo.png']
check('3 go + 1 nogo (75/25)', len(go) == 3 and len(nogo) == 1,
      '%d go, %d nogo' % (len(go), len(nogo)))
check('go corr_ans == "space"', all(c['corr_ans'] == 'space' for c in go))
check('nogo corr_ans is None', nogo[0]['corr_ans'] is None,
      repr(nogo[0]['corr_ans']))


# =====================================================================
print('\n=== 2. Trial sequence (method="random", nReps=10) ===')
# =====================================================================
def build(seed):
    return psydata.TrialHandler(nReps=10.0, method='random',
                                trialList=psydata.importConditions(CONDITIONS),
                                seed=seed, name='trials')


def sequence(handler):
    return [t['this_image'] for t in handler]


h = build(12345)
check('nTotal == 40', h.nTotal == 40, 'got %d' % h.nTotal)
seq = sequence(h)
check('40 trials delivered', len(seq) == 40, 'got %d' % len(seq))
check('30 go / 10 nogo overall',
      seq.count('go.png') == 30 and seq.count('nogo.png') == 10,
      '%d go, %d nogo' % (seq.count('go.png'), seq.count('nogo.png')))

# THE critical property: rep-level shuffle, not a global shuffle.
blocks = [seq[i:i + 4] for i in range(0, 40, 4)]
bad = [i for i, b in enumerate(blocks) if b.count('nogo.png') != 1]
check('exactly 1 nogo per 4-trial block', not bad,
      'blocks off: %s' % bad if bad else '10/10 blocks OK')

# Repeat across many seeds - a global shuffle would fail this quickly.
violations = 0
for s in range(200):
    sq = sequence(build(s))
    if any(sq[i:i + 4].count('nogo.png') != 1 for i in range(0, 40, 4)):
        violations += 1
check('block property holds over 200 seeds', violations == 0,
      '%d violations' % violations)

# Max consecutive nogo must be 2 (only across a block boundary)
worst = 0
for s in range(200):
    sq = sequence(build(s))
    run = best = 0
    for x in sq:
        run = run + 1 if x == 'nogo.png' else 0
        best = max(best, run)
    worst = max(worst, best)
check('max consecutive nogo <= 2', worst <= 2, 'observed max %d' % worst)


# =====================================================================
print('\n=== 3. Seed reproducibility ===')
# =====================================================================
a = sequence(build(473626502))
b = sequence(build(473626502))
check('same seed -> identical sequence', a == b)
c = sequence(build(999))
check('different seed -> different sequence', a != c)


# =====================================================================
print('\n=== 4. Scoring logic (4 combinations) ===')
# =====================================================================
def score(pressed, corr_ans):
    """Exact reproduction of gng_ko.py scoring branches."""
    if pressed is not None:
        # in-frame branch
        return 1 if ((pressed == str(corr_ans)) or (pressed == corr_ans)) else 0
    # routine-end branch
    return 1 if str(corr_ans).lower() == 'none' else 0


check('Go + press space   -> correct (1)', score('space', 'space') == 1)
check('Go + no response   -> omission (0)', score(None, 'space') == 0)
check('NoGo + press space -> commission (0)', score('space', None) == 0)
check('NoGo + no response -> correct (1)', score(None, None) == 1)


# =====================================================================
print('\n=== 5. Source invariants (guard against future edits) ===')
# =====================================================================
src = open(SCRIPT, encoding='utf-8').read()
print('  source: %s' % os.path.basename(SCRIPT))

guards = [
    ('nReps is 10',                r"nReps=10\.0",                       1),
    ('stimulus size 0.2',          r"size=\(0\.2, 0\.2\)",               1),
    ('go example at (0.6, 0.1)',   r"pos=\(0\.6, 0\.1\)",                1),
    ('nogo example at (0.6,-0.1)', r"pos=\(0\.6, -0\.1\)",               1),
    ('method is random',           r"method='random'",                   2),
    ('trial window 2.0 s',         r"routineTimer\.getTime\(\) < 2\.0",  1),
    ('stimulus stop at flip+2',    r"tStartRefresh \+ 2-frameTolerance", 2),
    ('feedback window 0.5 s',      r"routineTimer\.getTime\(\) < 0\.5",  1),
    ('response key is space only', r"keyList=\['space'\], ignoreKeys",   2),
    ('RT clock reset on flip',     r"callOnFlip\(key_resp\.clock\.reset\)", 1),
    ('key buffer cleared on flip', r"callOnFlip\(key_resp\.clearEvents", 1),
    ('no-response scoring',        r"str\(corr_ans\)\.lower\(\) == 'none'", 1),
    ('iohub keyboard backend',     r"backend='iohub'",                   1),
    ('countdown present',          r"countdown\.started",                1),
]
for label, pattern, expected in guards:
    n = len(re.findall(pattern, src))
    check(label, n == expected, 'found %d, expected %d' % (n, expected))


# =====================================================================
print('\n' + '=' * 60)
failed = [n for n, ok, _ in results if not ok]
print(' %d checks, %d passed, %d failed' %
      (len(results), len(results) - len(failed), len(failed)))
if failed:
    print('\n FAILED:')
    for n in failed:
        print('   - %s' % n)
    print('\n Do not collect data until these are resolved.')
    sys.exit(1)
print(' All algorithm invariants verified.')
print('=' * 60)
