#SingleInstance Force

if (not A_IsAdmin) {
;    Run *RunAs "%A_ScriptFullPath%"  ; Requires v1.0.92.01+
    MsgBox, Not Admin
    ExitApp
}

#If WinActive("Diablo II")

    sendFKey(counter) {
        fkeys := []
    ;    MsgBox % fkeys
        fkeyCount := 0
        if (!GetKeyState("A")) {
            fkeyCount++
            fkeys.push("{F10}")
        }
        if (!GetKeyState("S")) {
            fkeyCount++
            fkeys.push("{F11}")
        }
        if (!GetKeyState("D")) {
            fkeyCount++
            fkeys.push("{F12}")
        }
        if (GetKeyState("F")) {
            fkeyCount := 1
            fkeys := ["{F9}"]
        }
        mod_value := Mod(counter, fkeyCount)
        Send % fkeys[mod_value + 1]
    }

    SendRightClick() {
        Click
    }


    ScrollLock::
;        d2_counter++
;        if (d2_counter >= 100) {
;             d2_counter = 33
;        }
;        sendFKey(d2_counter)
        SendRightClick()
    return

    Space::
        if(GetKeyState("CapsLock", "T")) {
            SendRightClick()
        }
        if(!GetKeyState("CapsLock", "T")) {
            Send {Space}
        }
    return


    Numpad1::
        Send 1
    return

    Numpad2::
        Send 2
    return

    Numpad3::
        Send 3
    return

    Numpad4::
        Send 4
    return

    #NumpadEnd::
        Send 1
    return

    #NumpadDown::
        Send 2
    return

    #NumpadPgDn::
        Send 3
    return

    #NumpadLeft::
        Send 4
    return

    #NumpadClear::
        MouseGetPos, xpos, ypos
        Click, 903, 806
        MouseMove, %xpos%, %ypos%8
    return

    #NumpadHome::
        MouseGetPos, xpos, ypos
        Click, 1091, 1112
        MsgBox, The Bcursor is at X%xpos% Y%ypos%.
        MouseMove, %xpos%, %ypos%
    return

    #NumpadRight::
        MouseGetPos, xpos, ypos
        MsgBox, The cursor is at X%xpos% Y%ypos%.
    return

#If
