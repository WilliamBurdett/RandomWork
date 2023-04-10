#NoTrayIcon
#SingleInstance Force

SetTitleMatchMode, 2

#If WinActive("TowerDefense")
    getProperties() {
        Send {Alt down}p{Alt up}
    }


    #NumpadEnd::
        getProperties()
    return

    #NumpadClear::
        Send {F6}
        Send {F7}
    return
#If
