# Shin Megami Tensei V Save Editor
Shin Megami Tensei V Save Editor made in Python.

[GBATemp Thread link](https://gbatemp.net/threads/shin-megami-tensei-v-discussion-save-editor-soon.602923/)

Works with all the savefiles from Save Slot 1 through 20. (GameSave00-GameSave19) (GameSave00 = Slot 1, GameSave19 = Slot 20)

Features
* Game's Mode (Game Difficulty)
* Money
* Glory
* Character Stats & Skills
* Demon Stats & Skills
* Items
* Essences 
* Names
* EXP
* Level
* Demon ID

## Prerequisites
* [Python 3](https://www.python.org/downloads/) (Tested with Python 3.10.0)
* PyQt5, can be installed through `pip`. (`pip install PyQt5`)
* A **decrypted** SMT V save file from your Nintendo Switch (through a save utility such as [Checkpoint](https://github.com/FlagBrew/Checkpoint/releases)) or your Switch emulator of choice. 
* You can decrypt your save file with [smtv.saveutil](https://github.com/zarroboogs/smtv.saveutil), for example: `smtv.saveutil.exe -i GameSave**` will output `GameSave**_dec` in the folder where `smtv.saveutil.exe` is. For more info, check out the tool's own [README](https://github.com/zarroboogs/smtv.saveutil/blob/master/README.md#Usage).

## How to use
Run the script: `python shinv.py`.