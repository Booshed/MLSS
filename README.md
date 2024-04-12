Intended Use: This is a beginner-friendly Python program intended to be used to modify the SRAM/.sav file for Mario & Luigi: Superstar Saga.

Description: This program will allow the user to permanently modify stats for Slot 1 of MLSS. This program will also update the checksum whether or not you change any stats. 

How to Use: This program must be run from the command line: "python3 [filename]"

- Example: "python3 MLSS_CustomizeSave.py"

After the program starts, follow the prompts to select your save file and make customization changes. Make sure to type "EXIT" or "BACK", as the prompt says, in order to update the checksum after you finish customizing your stats. For the changes to take place, you must restart your emulator or run the program while the emulator is not running MLSS.

Dependencies: You must have Python 3 as well as tkinter (a python library). On UNIX, these can be easily installed using homebrew.

Notes: The python code contains all of the offsets for these stats as well as the checksum calculation if you want to pull them and use them for your own programs. If you want to modify a different save slot, add additional categories, or alter different stats, you will have to go into the code yourself to change the offsets to their appropriate values. To change to a different slot, I believe you simply have to add "0x06F8" to each address in the dictionaries at the top of the file. I may add this functionality in a future version.
