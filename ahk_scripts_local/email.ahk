#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#NoTrayIcon
#SingleInstance Force
;SetScrollLockState, AlwaysOn
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.

F23::
    chars := "william.burdett1@gmail.com"
    Loop, parse, chars
    {
        Send, %A_LoopField%
        sleep, 2
    }
return

F24::
    chars := "will@willsapps.com"
    Loop, parse, chars
    {
        Send, %A_LoopField%
        sleep, 2
    }
return
