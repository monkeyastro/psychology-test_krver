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
