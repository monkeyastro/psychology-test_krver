# -*- mode: python ; coding: utf-8 -*-
"""
Go/No-Go 한국어판 PyInstaller 빌드 명세
사용법:  pyinstaller gng_ko.spec --noconfirm

주의:
  - onedir 고정. iohub 가 별도 프로세스를 띄우므로 onefile 과 궁합이 나쁘다.
  - psychopy / psychopy.iohub 는 데이터 파일(yaml 설정, 폰트)을 런타임에 읽는다.
    collect_all 로 통째로 담지 않으면 실행 즉시 죽는다.
"""

from PyInstaller.utils.hooks import collect_all, collect_dynamic_libs

datas, binaries, hiddenimports = [], [], []

# --- PsychoPy 본체: 설정 파일, 기본 폰트, 리소스 전부 필요 ---
for pkg in ('psychopy', 'psychopy.iohub', 'psychtoolbox', 'freetype', 'questplus'):
    try:
        d, b, h = collect_all(pkg)
        datas += d; binaries += b; hiddenimports += h
    except Exception as e:
        print(f'[spec] collect_all({pkg}) 건너뜀: {e}')

binaries += collect_dynamic_libs('psychtoolbox')

# --- 정적 분석으로 안 잡히는 모듈들 ---
hiddenimports += [
    # 창 생성 / OpenGL (pyglet 1.4.11)
    'pyglet.window.win32',
    'pyglet.gl.wgl',
    'pyglet.gl.wglext_arb',
    'pyglet.media.drivers.directsound',
    'pyglet.canvas.win32',
    # iohub 스택
    'gevent', 'gevent.monkey', 'gevent.socket',
    'zmq', 'msgpack', 'msgpack_numpy', 'ujson', 'yaml',
    'tables', 'psutil',
    'pyWinhook', 'pywinhook',        # 패키지명/모듈명이 달라 둘 다 시도
    # 텍스트 렌더링
    'freetype', 'bidi', 'arabic_reshaper',
    # 조건파일
    'openpyxl', 'pandas', 'scipy',
]

excludes = [
    'wx', 'wxPython',                # Builder GUI 전용. 수백 MB 절약
    'matplotlib.tests', 'numpy.tests', 'scipy.spatial.cKDTree',
    'tkinter', 'IPython', 'pytest', 'jedi',
    'cv2', 'ffpyplayer', 'moviepy',  # 동영상 백엔드 미사용
    'psychopy.app',                  # Coder/Builder 앱
]

a = Analysis(
    ['gng_ko.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GoNoGo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,          # UPX 압축은 백신 오탐을 유발한다. 끄는 편이 안전.
    console=True,       # 최초 검증용. 안정화되면 False 로.
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='GoNoGo',
)
