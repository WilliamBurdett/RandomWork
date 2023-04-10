from pytube import Playlist

playlist = Playlist("https://music.youtube.com/playlist?list=PLCm4zcMW1nhVTig-MvHJo2BiOc5S_FLTA")
for video in playlist:
    print("video")
