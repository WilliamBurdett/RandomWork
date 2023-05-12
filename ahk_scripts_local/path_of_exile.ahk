#SingleInstance Force
;#NoTrayIcon
;#InstallKeybdHook
#include %A_WorkingDir%\..\ahk_scripts_local\global.ahk

#IfWinActive ahk_exe PathOfExileSteam.exe

drag_start_x = 970
drag_start_y = 1062
drag_end_x = 891
drag_end_y = 1066
click_x = 830
click_y = 1148
reset_x = 1258
reset_y = 1162

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

    F16::
        MouseGetPos, x_pos, y_pos
        ;poe_click_x = %x_pos%
        ;poe_click_y = %y_pos%
        MsgBox, Saved position to X%x_pos% Y%y_pos%.
    return

    F17::
        MouseGetPos, initial_x_pos, initial_y_pos
        Click, %click_x%, %click_y%
        MouseMove, %initial_x_pos%, %initial_y_pos%
    return

    F20::
        MouseGetPos, x_pos, y_pos
        MsgBox, Mouse position is X%x_pos% Y%y_pos%.
    return

    F18::
        MouseGetPos, initial_x_pos, initial_y_pos
        Click, %initial_x_pos%, %initial_y_pos%
        MouseMove, %drag_start_x%, %drag_start_y%
        MouseClickDrag, left, %drag_start_x%, %drag_start_y%, %drag_end_x%, %drag_end_y%, 5
        Click, %click_x%, %click_y%
        MouseMove, %initial_x_pos%, %initial_y_pos%
    return

    F19::
        MouseGetPos, initial_x_pos, initial_y_pos
        Click, %reset_x%, %reset_y%
        MouseMove, %initial_x_pos%, %initial_y_pos%
    return

    F4::
        Send, {Enter}
        fast_paste("/F5-hideout | F6-Invite | F8-Leave")
        Send, {Enter}
    return


    F5::
        Send, {Enter}
        fast_paste("/hideout")
        Send, {Enter}
    return

    F6::
        Send, {Enter}
        fast_paste("/invite @last")
        Send, {Enter}
    return

    F7::
        Send, {Enter}
        fast_paste("/kick Agathos_CR_WandGoesBurr")
        Send, {Enter}
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
