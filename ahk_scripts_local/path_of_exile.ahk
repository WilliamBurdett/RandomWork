#SingleInstance Force
#NoTrayIcon
;#InstallKeybdHook
#IfWinActive ahk_exe PathOfExileSteam.exe
    F11::
        Send 1
    return

    F12::
        Send 2
    return

    F13::
        Send 3
    return

    F14::
        Send 4
    return

    F15::
        Send 5
    return

    ScrollLock::
        Send {Space}
    return

    F21::
        Loop
        {
            Send ^{Click}
            Sleep, 125
            if !GetKeyState("F21")
                break
        }
    Return

#If
