#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Go/No-Go 과제 — 한국어 로컬판 (gng_ko.py)

원본: PsychoPy3 Builder v2023.2.3 산출물 (gng_lastrun.py, 2023-12-13)
정본 기준: gng.js (nReps=10, 자극 0.2, 예시 아이콘 ±0.1)

[측정 알고리즘 무변경 보증]
  자극 2000ms / 반응창 2000ms / 피드백 500ms / ITI 없음
  허용키 space / RT 원점 = 자극 flip / method='random'(4시행 묶음 셔플)
  채점: 반응시 keys==corr_ans, 무반응시 corr_ans가 None이면 정답

  키보드 백엔드는 원본대로 iohub 를 유지한다. Keyboard._backend 가 클래스
  속성이라 key_resp 의 RT 측정도 iohub 경로로 이뤄지므로, ptb 로 바꾸면
  계측기가 달라진다.

  변경된 것은 확정 파라미터 3개(.psyexp 원본 대조 완료), 표시 언어,
  실행 경로 처리, 종료화면 버그 수정, 시드 기록뿐.

원 저작권 고지 (PsychoPy):
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019)
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195.
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins

plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# 실행 기준 폴더: exe로 패키징된 경우 exe 옆, 스크립트 실행이면 스크립트 옆
if getattr(sys, 'frozen', False):
    _thisDir = os.path.dirname(os.path.abspath(sys.executable))
else:
    _thisDir = os.path.dirname(os.path.abspath(__file__))

# --- 자산 파일 경로 (exe 옆에 함께 배치) ---
CONDITIONS_FILE = os.path.join(_thisDir, 'conditions.xlsx')
GO_IMAGE = os.path.join(_thisDir, 'go.png')
NOGO_IMAGE = os.path.join(_thisDir, 'nogo.png')

# --- 한글 폰트 ---
# NanumGothic.ttf 를 동봉하면 그것을 쓰고, 없으면 시스템 폰트로 폴백.
# 루트와 fonts/ 하위 둘 다 탐색한다.
KO_FONT = 'Malgun Gothic'  # Windows 기본 한글 폰트
_fontFile = None
for _cand in (os.path.join(_thisDir, 'NanumGothic.ttf'),
              os.path.join(_thisDir, 'fonts', 'NanumGothic.ttf')):
    if os.path.isfile(_cand):
        _fontFile = _cand
        break
if _fontFile:
    try:
        from psychopy.visual.textbox2 import allFonts
        import freetype as _ft

        allFonts.addFontFile(_fontFile)
        _fam = _ft.Face(str(_fontFile)).family_name
        if isinstance(_fam, bytes):
            _fam = _fam.decode('utf-8', 'ignore')
        if _fam:
            KO_FONT = _fam
    except Exception as _e:
        logging.warning('동봉 폰트 로드 실패, 시스템 폰트로 진행합니다: %s' % _e)

# --- 시작 전 자산 파일 존재 확인 ---
_missing = [p for p in (CONDITIONS_FILE, GO_IMAGE, NOGO_IMAGE) if not os.path.isfile(p)]
if _missing:
    _msg = '다음 파일을 찾을 수 없습니다.\n\n' + '\n'.join(_missing) + \
           '\n\n실행 파일과 같은 폴더에 두어야 합니다.'
    try:
        from psychopy import gui as _gui

        _gui.warnDlg(prompt=_msg, title='파일 없음')
    except Exception:
        print(_msg)
    core.quit()
# Store info about the experiment session
psychopyVersion = '2023.2.3'
expName = 'gng'  # from the Builder filename that created this script
expInfo = {
    'participant': '',  # 검사자가 직접 입력. 비워두면 실행 시 경고.
    'session': '001',
    'date': data.getDateStr(),  # add a simple timestamp
    'expName': expName,
    'psychopyVersion': psychopyVersion,
}


def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.

    Returns
    ==========
    dict
        Information about this experiment.
    """
    # temporarily remove keys which the dialog doesn't need to show
    poppedKeys = {
        'date': expInfo.pop('date', data.getDateStr()),
        'expName': expInfo.pop('expName', expName),
        'psychopyVersion': expInfo.pop('psychopyVersion', psychopyVersion),
    }
    # show participant info dialog
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False,
                          title='Go/No-Go 검사 - 참가자 정보')
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # 참가자 ID 미입력 방지
    while not str(expInfo.get('participant', '')).strip():
        gui.warnDlg(prompt='참가자 ID를 입력해야 합니다.', title='입력 필요')
        dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False,
                              title='Go/No-Go 검사 - 참가자 정보')
        if dlg.OK == False:
            core.quit()
    # restore hidden keys
    expInfo.update(poppedKeys)
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.

    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    """

    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    # 결과 저장 폴더 (실행 파일 옆 data/)
    filename = os.path.join('data', u'%s_%s_%s' % (
        expInfo['participant'], expName, expInfo['date']))
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)

    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/becca/Documents/newdemos/Experiments/Go NoGo/gng_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.

    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.

    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # this outputs to the screen, not a file
    logging.console.setLevel(logging.EXP)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename + '.log', level=logging.EXP)

    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window

    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.

    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=[1440, 900], fullscr=True, screen=0,
            winType='pyglet', allowStencil=True,
            monitor='testMonitor', color=[-1, -1, -1], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height'
        )
        if expInfo is not None:
            # store frame rate of monitor if we can measure it
            expInfo['frameRate'] = win.getActualFrameRate()
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [-1, -1, -1]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    win.mouseVisible = False
    win.hideMessage()
    return win


def setupInputs(expInfo, thisExp, win):
    """
    Setup whatever inputs are available (mouse, keyboard, eyetracker, etc.)

    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    dict
        Dictionary of input devices by name.
    """
    # --- Setup input devices ---
    # [원본 유지] gng.psyexp 의 keyboardBackend='ioHub' 설정을 그대로 따른다.
    #   Keyboard._backend 는 클래스 속성이므로, 여기서 iohub 로 고정되면
    #   이후 생성되는 key_resp / start_resp 도 모두 iohub 백엔드를 쓴다.
    #   즉 RT 측정 계측기가 iohub 다. 절대 ptb 로 바꾸지 말 것.
    inputs = {}
    ioConfig = {}

    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')

    ioSession = '1'
    if 'session' in expInfo:
        ioSession = str(expInfo['session'])
    ioServer = io.launchHubServer(window=win, **ioConfig)
    eyetracker = None

    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard(backend='iohub')
    # return inputs dict
    return {
        'ioServer': ioServer,
        'defaultKeyboard': defaultKeyboard,
        'eyetracker': eyetracker,
    }


def pauseExperiment(thisExp, inputs=None, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.

    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return

    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # prevent components from auto-drawing
    win.stashAutoDraw()
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # make sure we have a keyboard
        if inputs is None:
            inputs = {
                'defaultKeyboard': keyboard.Keyboard(backend='ioHub')
            }
        # check for quit (typically the Esc key)
        if inputs['defaultKeyboard'].getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win, inputs=inputs)
        # flip the screen
        win.flip()
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, inputs=inputs, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # restore auto-drawn components
    win.retrieveAutoDraw()
    # reset any timers
    for timer in timers:
        timer.reset()


def run(expInfo, thisExp, win, inputs, globalClock=None, thisSession=None):
    """
    Run the experiment flow.

    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    inputs : dict
        Dictionary of input devices by name.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = inputs['ioServer']
    defaultKeyboard = inputs['defaultKeyboard']
    eyetracker = inputs['eyetracker']
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess

    # Start Code - component code to be run after the window creation

    # --- Initialize components for Routine "intro" ---
    introtxt = visual.TextBox2(
        win,
        text='화면에 체크 표시가 나타나면 스페이스바를 누르세요.\n\n엑스 표시가 나타나면 아무것도 누르지 마세요.\n\n최대한 빠르고 정확하게 반응해 주세요.\n\n준비가 되면 S 키를 눌러 시작하세요.',
        placeholder='', font=KO_FONT,
        pos=(0, 0), letterHeight=0.055,
        size=(1, 0.5), borderWidth=2.0,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=False, italic=False,
        lineSpacing=1.0, speechPoint=None,
        padding=0.0, alignment='center',
        anchor='center', overflow='visible',
        fillColor=None, borderColor=None,
        flipHoriz=False, flipVert=False, languageStyle='LTR',
        editable=False,
        name='introtxt',
        depth=0, autoLog=True,
    )
    start_resp = keyboard.Keyboard()
    go_example = visual.ImageStim(
        win=win,
        name='go_example',
        image=GO_IMAGE, mask=None, anchor='center',
        ori=0.0, pos=(0.6, 0.1), size=(0.1, 0.1),
        color=[1, 1, 1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-2.0)
    nogo_example = visual.ImageStim(
        win=win,
        name='nogo_example',
        image=NOGO_IMAGE, mask=None, anchor='center',
        ori=0.0, pos=(0.6, -0.1), size=(0.1, 0.1),
        color=[1, 1, 1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)

    # --- Initialize components for Routine "trial" ---
    image = visual.ImageStim(
        win=win,
        name='image',
        image=GO_IMAGE, mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(0.2, 0.2),
        color=[1, 1, 1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    key_resp = keyboard.Keyboard()

    # --- Initialize components for Routine "feedback" ---
    # Run 'Begin Experiment' code from code
    correct_counter = 0
    fbtxt = visual.TextBox2(
        win, text='', placeholder='', font=KO_FONT,
        pos=(0, 0), letterHeight=0.055,
        size=(0.5, 0.5), borderWidth=2.0,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=False, italic=False,
        lineSpacing=1.0, speechPoint=None,
        padding=0.0, alignment='center',
        anchor='center', overflow='visible',
        fillColor=None, borderColor=None,
        flipHoriz=False, flipVert=False, languageStyle='LTR',
        editable=False,
        name='fbtxt',
        depth=-1, autoLog=True,
    )

    # --- Initialize components for Routine "end" ---
    end_resp = keyboard.Keyboard()  # [버그 수정] 종료 키 수신용
    textbox = visual.TextBox2(
        win, text='', placeholder='', font=KO_FONT,
        pos=(0, 0), letterHeight=0.055,
        size=(0.7, 0.5), borderWidth=2.0,
        color='white', colorSpace='rgb',
        opacity=None,
        bold=False, italic=False,
        lineSpacing=1.0, speechPoint=None,
        padding=0.0, alignment='center',
        anchor='center', overflow='visible',
        fillColor=None, borderColor=None,
        flipHoriz=False, flipVert=False, languageStyle='LTR',
        editable=False,
        name='textbox',
        depth=-1, autoLog=True,
    )

    # create some handy timers
    if globalClock is None:
        globalClock = core.Clock()  # to track the time since experiment started
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6)

    # --- Prepare to start Routine "intro" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('intro.started', globalClock.getTime())
    introtxt.reset()
    start_resp.keys = []
    start_resp.rt = []
    _start_resp_allKeys = []
    # keep track of which components have finished
    introComponents = [introtxt, start_resp, go_example, nogo_example]
    for thisComponent in introComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1

    # --- Run Routine "intro" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *introtxt* updates

        # if introtxt is starting this frame...
        if introtxt.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            introtxt.frameNStart = frameN  # exact frame index
            introtxt.tStart = t  # local t and not account for scr refresh
            introtxt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(introtxt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'introtxt.started')
            # update status
            introtxt.status = STARTED
            introtxt.setAutoDraw(True)

        # if introtxt is active this frame...
        if introtxt.status == STARTED:
            # update params
            pass

        # *start_resp* updates
        waitOnFlip = False

        # if start_resp is starting this frame...
        if start_resp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            start_resp.frameNStart = frameN  # exact frame index
            start_resp.tStart = t  # local t and not account for scr refresh
            start_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_resp.started')
            # update status
            start_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(start_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(start_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if start_resp.status == STARTED and not waitOnFlip:
            theseKeys = start_resp.getKeys(keyList=['s'], ignoreKeys=["escape"], waitRelease=False)
            _start_resp_allKeys.extend(theseKeys)
            if len(_start_resp_allKeys):
                start_resp.keys = _start_resp_allKeys[-1].name  # just the last key pressed
                start_resp.rt = _start_resp_allKeys[-1].rt
                start_resp.duration = _start_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False

        # *go_example* updates

        # if go_example is starting this frame...
        if go_example.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            go_example.frameNStart = frameN  # exact frame index
            go_example.tStart = t  # local t and not account for scr refresh
            go_example.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(go_example, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'go_example.started')
            # update status
            go_example.status = STARTED
            go_example.setAutoDraw(True)

        # if go_example is active this frame...
        if go_example.status == STARTED:
            # update params
            pass

        # *nogo_example* updates

        # if nogo_example is starting this frame...
        if nogo_example.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            nogo_example.frameNStart = frameN  # exact frame index
            nogo_example.tStart = t  # local t and not account for scr refresh
            nogo_example.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(nogo_example, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'nogo_example.started')
            # update status
            nogo_example.status = STARTED
            nogo_example.setAutoDraw(True)

        # if nogo_example is active this frame...
        if nogo_example.status == STARTED:
            # update params
            pass

        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in introComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "intro" ---
    for thisComponent in introComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('intro.stopped', globalClock.getTime())
    # check responses
    if start_resp.keys in ['', [], None]:  # No response was made
        start_resp.keys = None
    thisExp.addData('start_resp.keys', start_resp.keys)
    if start_resp.keys != None:  # we had a response
        thisExp.addData('start_resp.rt', start_resp.rt)
        thisExp.addData('start_resp.duration', start_resp.duration)
    thisExp.nextEntry()
    # the Routine "intro" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # --- 무작위 시드 생성 및 기록 ---
    # 참가자마다 새 시드를 뽑되 반드시 데이터 파일에 남긴다.
    # 전 참가자 고정 시드는 모두가 같은 순서를 받게 되므로 금지.
    trialSeed = int(randint(0, 2 ** 31 - 1))
    expInfo['trialSeed'] = trialSeed
    logging.exp('trialSeed = %d' % trialSeed)

    # --- 프레임률 품질 점검 ---
    _fr = expInfo.get('frameRate', None)
    if _fr is None:
        logging.critical('프레임률 측정 실패. 60Hz로 가정하여 진행합니다. '
                         'RT 정확도 검증이 필요합니다.')
    else:
        logging.exp('측정된 프레임률: %.2f Hz' % _fr)
        if abs(_fr - 60.0) > 2.0:
            logging.warning('모니터 주사율이 60Hz가 아닙니다 (%.2f Hz). '
                            '자극 제시 시간이 프레임 단위로 반올림됩니다.' % _fr)

    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=10.0, method='random',
                               extraInfo=expInfo, originPath=-1,
                               trialList=data.importConditions(CONDITIONS_FILE),
                               seed=trialSeed, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]

    for thisTrial in trials:
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t')
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp,
                inputs=inputs,
                win=win,
                timers=[routineTimer],
                playbackComponents=[]
            )
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]

        # --- Prepare to start Routine "trial" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('trial.started', globalClock.getTime())
        image.setImage(os.path.join(_thisDir, str(this_image)))
        key_resp.keys = []
        key_resp.rt = []
        key_resp.corr = None  # [방어] 이전 시행 값 유입 차단
        _key_resp_allKeys = []
        # keep track of which components have finished
        trialComponents = [image, key_resp]
        for thisComponent in trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1

        # --- Run Routine "trial" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 2.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *image* updates

            # if image is starting this frame...
            if image.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                image.frameNStart = frameN  # exact frame index
                image.tStart = t  # local t and not account for scr refresh
                image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'image.started')
                # update status
                image.status = STARTED
                image.setAutoDraw(True)

            # if image is active this frame...
            if image.status == STARTED:
                # update params
                pass

            # if image is stopping this frame...
            if image.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > image.tStartRefresh + 2 - frameTolerance:
                    # keep track of stop time/frame for later
                    image.tStop = t  # not accounting for scr refresh
                    image.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'image.stopped')
                    # update status
                    image.status = FINISHED
                    image.setAutoDraw(False)

            # *key_resp* updates
            waitOnFlip = False

            # if key_resp is starting this frame...
            if key_resp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.started')
                # update status
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip

            # if key_resp is stopping this frame...
            if key_resp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > key_resp.tStartRefresh + 2 - frameTolerance:
                    # keep track of stop time/frame for later
                    key_resp.tStop = t  # not accounting for scr refresh
                    key_resp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_resp.stopped')
                    # update status
                    key_resp.status = FINISHED
                    key_resp.status = FINISHED
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    key_resp.duration = _key_resp_allKeys[-1].duration
                    # was this correct?
                    if (key_resp.keys == str(corr_ans)) or (key_resp.keys == corr_ans):
                        key_resp.corr = 1
                    else:
                        key_resp.corr = 0
                    # a response ends the routine
                    continueRoutine = False

            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # --- Ending Routine "trial" ---
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('trial.stopped', globalClock.getTime())
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
            # was no response the correct answer?!
            if str(corr_ans).lower() == 'none':
                key_resp.corr = 1;  # correct non-response
            else:
                key_resp.corr = 0;  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('key_resp.keys', key_resp.keys)
        trials.addData('key_resp.corr', key_resp.corr)
        if key_resp.keys != None:  # we had a response
            trials.addData('key_resp.rt', key_resp.rt)
            trials.addData('key_resp.duration', key_resp.duration)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-2.000000)

        # --- Prepare to start Routine "feedback" ---
        continueRoutine = True
        # update component parameters for each repeat
        thisExp.addData('feedback.started', globalClock.getTime())
        # Run 'Begin Routine' code from code
        # [방어] corr가 할당되지 않은 채 여기 도달하면 데이터가 오염된다.
        if key_resp.corr is None:
            logging.critical('key_resp.corr 미할당 상태로 feedback 진입 (trial %s)'
                             % trials.thisN)
            key_resp.corr = 0
            thisExp.addData('corr_fallback', 1)

        if key_resp.corr:
            fb = '정답'
        else:
            fb = '오답'

        correct_counter += key_resp.corr
        fbtxt.reset()
        fbtxt.setText(fb)
        # keep track of which components have finished
        feedbackComponents = [fbtxt]
        for thisComponent in feedbackComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1

        # --- Run Routine "feedback" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 0.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *fbtxt* updates

            # if fbtxt is starting this frame...
            if fbtxt.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                fbtxt.frameNStart = frameN  # exact frame index
                fbtxt.tStart = t  # local t and not account for scr refresh
                fbtxt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fbtxt, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fbtxt.started')
                # update status
                fbtxt.status = STARTED
                fbtxt.setAutoDraw(True)

            # if fbtxt is active this frame...
            if fbtxt.status == STARTED:
                # update params
                pass

            # if fbtxt is stopping this frame...
            if fbtxt.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fbtxt.tStartRefresh + 0.5 - frameTolerance:
                    # keep track of stop time/frame for later
                    fbtxt.tStop = t  # not accounting for scr refresh
                    fbtxt.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fbtxt.stopped')
                    # update status
                    fbtxt.status = FINISHED
                    fbtxt.setAutoDraw(False)

            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, inputs=inputs, win=win)
                return

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # --- Ending Routine "feedback" ---
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.addData('feedback.stopped', globalClock.getTime())
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-0.500000)
        thisExp.nextEntry()

        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 1.0 repeats of 'trials'

    # --- Prepare to start Routine "end" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('end.started', globalClock.getTime())
    # Run 'Begin Routine' code from set_endtxt
    endtxt = ('검사가 끝났습니다.\n\n총 ' + str(trials.nTotal) + '문항 중 '
              + str(correct_counter) + '문항 정답\n\n스페이스바를 누르면 종료됩니다.')
    textbox.reset()
    textbox.setText(endtxt)
    # [버그 수정] 원본에는 종료 키 컴포넌트가 없어 Esc 외에는 종료가 불가능했다.
    end_resp.keys = []
    end_resp.rt = []
    _end_resp_allKeys = []
    # keep track of which components have finished
    endComponents = [textbox, end_resp]
    for thisComponent in endComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1

    # --- Run Routine "end" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *textbox* updates

        # if textbox is starting this frame...
        if textbox.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            textbox.frameNStart = frameN  # exact frame index
            textbox.tStart = t  # local t and not account for scr refresh
            textbox.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(textbox, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'textbox.started')
            # update status
            textbox.status = STARTED
            textbox.setAutoDraw(True)

        # if textbox is active this frame...
        if textbox.status == STARTED:
            # update params
            pass

        # *end_resp* updates  [버그 수정]
        waitOnFlip = False
        if end_resp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            end_resp.frameNStart = frameN
            end_resp.tStart = t
            end_resp.tStartRefresh = tThisFlipGlobal
            win.timeOnFlip(end_resp, 'tStartRefresh')
            thisExp.timestampOnFlip(win, 'end_resp.started')
            end_resp.status = STARTED
            waitOnFlip = True
            win.callOnFlip(end_resp.clock.reset)
            win.callOnFlip(end_resp.clearEvents, eventType='keyboard')
        if end_resp.status == STARTED and not waitOnFlip:
            theseKeys = end_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _end_resp_allKeys.extend(theseKeys)
            if len(_end_resp_allKeys):
                end_resp.keys = _end_resp_allKeys[-1].name
                continueRoutine = False

        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, inputs=inputs, win=win)
            return

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in endComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "end" ---
    for thisComponent in endComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('end.stopped', globalClock.getTime())
    # the Routine "end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # mark experiment as finished
    endExperiment(thisExp, win=win, inputs=inputs)


def saveData(thisExp):
    """
    Save data from this experiment

    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, inputs=None, win=None):
    """
    End this experiment, performing final shut down operations.

    This function does NOT close the window or end the Python process - use `quit` for this.

    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    inputs : dict
        Dictionary of input devices by name.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip()
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # shut down eyetracker, if there is one
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()


def quit(thisExp, win=None, inputs=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.

    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    inputs : dict
        Dictionary of input devices by name.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip()
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    if inputs is not None:
        if 'eyetracker' in inputs and inputs['eyetracker'] is not None:
            inputs['eyetracker'].setConnectionState(False)
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    inputs = setupInputs(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo,
        thisExp=thisExp,
        win=win,
        inputs=inputs
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win, inputs=inputs)