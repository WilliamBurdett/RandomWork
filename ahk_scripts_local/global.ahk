#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#NoTrayIcon
#SingleInstance Force
#InstallKeybdHook
;SetScrollLockState, AlwaysOn
SetNumLockState, AlwaysOn
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetTitleMatchMode, 2

#IfWinActive ahk_exe pycharm64.exe

    F19::
        Send b
    Return
#If
F22::
    WinGet, active_id, ProcessName, A
    MsgBox, The active window's ID is "%active_id%".
;    state:=GetKeyState("F21")
;    MsgBox, %state%
return
F22::
    WinGet, active_id, ProcessName, A
    MsgBox, The active window's ID is "%active_id%".
;    state:=GetKeyState("F21")
;    MsgBox, %state%
return


;#NumpadHome::
;return
;#NumpadRight::
;return
;#NumpadClear::
;return
;#NumpadLeft::
;return
;#NumpadPgDn::
;return
;#NumpadDown::
;return
;#NumpadEnd::
;return
