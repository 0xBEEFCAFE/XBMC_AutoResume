# XBMC_AutoResume
An XBMC script for original Xbox to save the current playlist and shutdown, then resume playback on bootup

Version 2 (12/28/2007)

To install, copy the AutoResumer folder to the Q:\Scripts\ folder. Then all you need to do is run it.

To execute on startup, add this to autoexec.py:
```
xbmc.executescript("Q:\scripts\autoresume.py")
```

To call this scipt from the fullscreen visualizations (or anywhere else), add this keymap.xml
```
XBMC.RunScript(Q:\scripts\autoresume.py)
```