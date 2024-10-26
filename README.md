# Rail Heist Maker
Level Maker for UFO 50's Game #28 Rail Heist.

This tool provides two main features: a basic graphical environment to edit and create rail heist levels, and an interface to UndertaleModTool to facilitate the operation of inserting and removing said levels into and from the game's data file. This lets creators focus their efforts on only the creative process of making levels and not bother with the technical overhead associated.

Before anything else the tool makes a backup of ufo 50's "data.win" file since it has modify it to insert levels, in case the game breaks restore from the backup by deleting data.win and renaming the "data.win.backup" to "data.win", note that your time records are not saved in "data.win" but instead in your save file in "appdata/local/ufo50" and the tool does not back this up, so if you care about your time records you can backup this file yourself.

### how 2 use:
- download RailHeistMaker.zip from releases and extract its contents 
- run RailHeistMaker.exe
- click the 'Setup' button and select the data.win file in UFO 50's directory, it will take a minute to load but thankfully you only need to do it once
- now you have several options, for starters you try creating a new mission by clicking 'New Mission'
- mess around with the editor, make something simple, dont forget to place outlaws and money bags, then adjust the level settings by clicking 'mission settings'
- save your level by clicking the 'save' button, levels are saved in a simple text file in the folder '/missions', you can easily share them online this way!
- you can load saved/downloaded levels by clicking 'Load Mission' from the menu, the inital setup also extracts the base missions in the folder '/base missions' if you want to check those out
- to insert the level click 'inject into game' button, specify where do you want it, then click 'inject'. you can look at the associated cmd window to follow the insertion process if you want. unfortunately this operation takes about a minute everytime so you may want to have some bushido ball or something to play while waiting
- if you want to quickly inject a level without editing/viewing use the 'load & inject' button from menu


### problems and solutions:
- sometimes a very bad level inserted into the game can break it, idk what really causes this but the fix is to restore data.win from backup and rerun the setup from menu
- inserting levels before last level removes the win state of levels at the end to prevent this only insert levels after the last level or just replace existing levels

### thanks
- to UndertaleModTool team for their gamechanging tool

### support
- create and share levels!

  
