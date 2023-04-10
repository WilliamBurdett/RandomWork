#SingleInstance Force
#NoTrayIcon
;#InstallKeybdHook
#IfWinActive ahk_exe SC2_x64.exe

;    F11::
;        MouseGetPos, xpos, ypos
;        MsgBox, The cursor is at X%xpos% Y%ypos%.
;    return

    F11::
        MouseGetPos, xpos, ypos
        Click, 496, 36
        MouseMove, %xpos%, %ypos%
    return

#If
