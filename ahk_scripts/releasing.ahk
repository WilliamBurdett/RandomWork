#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn All, StdOut  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

; Admin
;Run *RunAs "C:\Other Programs\autohotkey\ahk_scripts_local\diablo_2.exe" ; Requires v1.0.92.01+
; Standard
Run %A_AHKPath% "C:\Other Programs\autohotkey\ahk_scripts_local\factorio.ahk"
Run %A_AHKPath% "C:\Other Programs\autohotkey\ahk_scripts_local\leaf_blower.ahk"
Run %A_AHKPath% "C:\Other Programs\autohotkey\ahk_scripts_local\path_of_exile.ahk"
Run %A_AHKPath% "C:\Other Programs\autohotkey\ahk_scripts_local\unity.ahk"
Run %A_AHKPath% "C:\Other Programs\autohotkey\ahk_scripts_local\global.ahk"
Run %A_AHKPath% "C:\Other Programs\autohotkey\ahk_scripts_local\on_top.ahk"
Run %A_AHKPath% "C:\Other Programs\autohotkey\ahk_scripts_local\email.ahk"
