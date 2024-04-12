# Author: Boosh (offsets pulled from Mugg1991, Jdaster64, Biospark, and Teawater) <<-- TAS script
# Date: 4/11/2024
# IDE: VS Code
#
# Testing:      Tested in Python 3 on a Unix system. Requires tkinter (can be installed via homebrew)
#
# Description:  Python program for MLSS to change stats and update checksum for Slot 1 in a permanent fashion. Prompts user for SRAM/.sav file then provides 
#               a UI via the command line to change desired stats. This program only works for the basic stats, not the weird stuff. However, the program can
#               be easily expanded to do so by adding extra categories and updating the dictionaries/error checking. Tested on UNIX. Only works for save file #1.
#               If a different save file is required, calculate the offsets (should just be adding 0x06F8 to each dictionary entry) and update the dictionaries 
#               at the top of the file.
#               
# Future Dev:   What could be improved?
#               1. Ask which slot to save to and then update dictionaries accordingly (0x06F8 added to every offset?)
#               2. Make an actual GUI instead of just command line
#
# Instructions: Run program via the command line with "python3 [program name]" i.e. "python3 MLSSchecksum.py". You must have both python3 installed and
#               tkinter. These are both obtainable via homebrew on UNIX. Then, follow the program prompts. When you finish, Use the progam's "EXIT" and
#               "BACK" key words, do not use ^C or similar. This is because after typing "EXIT" this program will update the checksum for you to prevent
#               MLSS from disabling your save file. If this happens, your data is not gone. You just need to update the checksum. If this happens, run
#               the program again, select your file, and upon the prompt "Would you like to change the current stats? (Y/N)", type "N" and press enter.
#               This will recalculate the checksum and update your file. If your data isn't corrupted, this should 'save' your save file.
#
# Credit:       I pulled the offsets directly from a LUA script for a TAS speedrun written by Mugg1991 and his gang. I would not have been able to complete this 
#               project nearly as quickly if not for them. Thank you.

import os                       # for getting terminal width for pretty print
import tkinter as tk            # for easy file selection
from tkinter import filedialog  # ^

# Stat Locations in SRAM/.sav file for Slot 1

starting_address = 0x0010 # offset for checksum
coin_stat = 0xbe # offset for coins
mario_stats = { # offsets for mario's stats
    "LVL": 0x67,        # mario's level
    "EXP": 0x31,        # mario's experience points
    "CURR_HP": 0x38,    # mario's current HP
    "MAX_HP": 0x44,     # mario's maximum HP
    "BASE_HP": 0x46,    # mario's base HP
    "CURR_BP": 0x42,    # mario's current BP
    "MAX_BP": 0x4E,     # mario's max BP
    "BASE_BP": 0x40,    # mario's base BP
    "POW": 0x4A,        # mario's power
    "BASE_POW": 0x4C,   # mario's base power
    "DEF": 0x52,        # mario's defense
    "BASE_DEF": 0x54,   # mario's base defense
    "SPD": 0x56,        # mario's speed
    "BASE_SPD": 0x48,   # mario's base speed
    "STC": 0x5E,        # mario's stache
    "BASE_STC": 0x50    # mario's base stache
}
luigi_stats = { # offsets for luigi's stats
    "LVL": 0x9B,        # luigi's level   
    "EXP": 0x75,        # luigi's experience
    "CURR_HP": 0x7C,    # luigi's current HP
    "MAX_HP": 0x78,     # luigi's maximum HP
    "BASE_HP": 0x7A,    # luigi's base HP
    "CURR_BP": 0x86,    # luigi's current BP
    "MAX_BP": 0x82,     # luigi's maximum BP
    "BASE_BP": 0x84,    # luigi's base BP
    "POW": 0x8E,        # luigi's power
    "BASE_POW": 0x80,   # luigi's base power
    "DEF": 0x96,        # luigi's defense
    "BASE_DEF": 0x88,   # luigi's base defense
    "SPD": 0x8A,        # luigi's speed
    "BASE_SPD": 0x8C,   # luigi's base speeds
    "STC": 0x92,        # luigi's stache
    "BASE_STC": 0x94    # luigi's base stache
}
stat_byte_size = { # how many bytes to read for each of these stats
    "LVL": 1,
    "EXP": 3,
    "CURR_HP": 2,
    "MAX_HP": 2,
    "BASE_HP": 2,
    "CURR_BP": 2,
    "MAX_BP": 2,
    "BASE_BP": 2,
    "POW": 2,
    "BASE_POW": 2,
    "DEF": 2,
    "BASE_DEF": 2,
    "SPD": 2,
    "BASE_SPD": 2,
    "STC": 2,
    "BASE_STC": 2
}
def printHeader(header):
    # terminal width
    width = os.get_terminal_size().columns 
    
    # add one space to the left and right
    header_length = len(header)
    header = header.center(header_length + 2)
    
    # center header on terminal
    header = header.center(width, "=")

    print("\n" + header + "\n")

def printFooter():
    # terminal width
    width = os.get_terminal_size().columns 
    footer = "".rjust(width, '=')
    print("\n" + footer + "\n")

def displayStats(save_file):

    printHeader("Current Stats")
    
    # Money
    save_file.seek(coin_stat)
    coins = int(save_file.read(2).hex(),16)
    print(">> COINS:\t" + str(coins))
    
    # Mario Stats - Luigi Stats
    print("\n>> MARIO\t\t>> LUIGI")
    
    # Mario Level - Luigi Level
    save_file.seek(mario_stats["LVL"])
    mario_level = int(save_file.read(1).hex(),16)
    save_file.seek(luigi_stats["LVL"])
    luigi_level = int(save_file.read(1).hex(),16)
    print("\tLVL:\t" + str(mario_level),end="")
    print("\t\tLVL:\t" + str(luigi_level))
    
    # Mario Experience - Luigi Experience
    save_file.seek(mario_stats["EXP"])
    mario_experience = int(save_file.read(3).hex(),16)
    save_file.seek(luigi_stats["EXP"])
    luigi_experience = int(save_file.read(3).hex(),16)
    print("\tEXP:\t" + str(mario_experience),end="")
    print("\t\tEXP:\t" + str(luigi_experience))
    
    # Mario HP - Luigi HP
    save_file.seek(mario_stats["MAX_HP"])
    mario_hp = int(save_file.read(2).hex(),16)
    save_file.seek(luigi_stats["MAX_HP"])
    luigi_hp = int(save_file.read(2).hex(),16)
    print("\tHP:\t" + str(mario_hp),end="")
    print("\t\tHP:\t" + str(luigi_hp))
    
    # Mario BP - Luigi BP
    save_file.seek(mario_stats["MAX_BP"])
    mario_bp = int(save_file.read(2).hex(),16)
    save_file.seek(luigi_stats["MAX_BP"])
    luigi_bp = int(save_file.read(2).hex(),16)
    print("\tBP:\t" + str(mario_bp),end="")
    print("\t\tBP:\t" + str(luigi_bp))
    
    # Mario POW - Luigi POW
    save_file.seek(mario_stats["POW"])
    mario_pow = int(save_file.read(2).hex(),16)
    save_file.seek(luigi_stats["POW"])
    luigi_pow = int(save_file.read(2).hex(),16)
    print("\tPOW:\t" + str(mario_pow),end="")
    print("\t\tPOW:\t" + str(luigi_pow))
    
    # Mario DEF - Luigi DEF
    save_file.seek(mario_stats["DEF"])
    mario_def = int(save_file.read(2).hex(),16)
    save_file.seek(luigi_stats["DEF"])
    luigi_def = int(save_file.read(2).hex(),16)
    print("\tDEF:\t" + str(mario_def),end="")
    print("\t\tDEF:\t" + str(luigi_def))
    
    # Mario SPD - Luigi SPD
    save_file.seek(mario_stats["SPD"])
    mario_spd = int(save_file.read(2).hex(),16)
    save_file.seek(luigi_stats["SPD"])
    luigi_spd = int(save_file.read(2).hex(),16)
    print("\tSPD:\t" + str(mario_spd),end="")
    print("\t\tSPD:\t" + str(luigi_spd))
    
    # Mario STC - Luigi STC
    save_file.seek(mario_stats["STC"])
    mario_stc = int(save_file.read(2).hex(),16)
    save_file.seek(luigi_stats["STC"])
    luigi_stc = int(save_file.read(2).hex(),16)
    print("\tSTC:\t" + str(mario_stc),end="")
    print("\t\tSTC:\t" + str(luigi_stc))
    
    printFooter()

def changeStats(save_file):
    
    printHeader("Change Stats")
    
    user_category = input("\t>> Choose a stat category: [COINS,MARIO,LUIGI] or type \"EXIT\": ")

    while (user_category.upper().strip() != "DONE" and user_category.upper().strip() != "EXIT" and user_category.upper().strip() != "Q" and user_category.upper().strip() != "QUIT"):
        
        # Coins
        if user_category.upper().strip() == "COINS":
            user_coins = input("\t>> Enter COINS (integer): ")
            if user_coins.isnumeric():
                coins_to_add = int(user_coins)
                coins_to_add_bytes = coins_to_add.to_bytes(2,'big')
                save_file.seek(0xbe)
                coins = int(save_file.read(2).hex(),16)
                print("\t** SYS: Changing coins from " + str(coins) + " to " + str(coins_to_add))
                save_file.seek(0xbe)
                save_file.write(coins_to_add_bytes)
                
            else:
                print("\t** SYS: Invalid input. Please try again...")

        # Mario / Luigi
        elif user_category.upper().strip() == "MARIO" or user_category.upper().strip() == "LUIGI":
            # select correct stat dictionary
            current_stats = mario_stats
            if user_category.upper().strip() == "LUIGI":
                current_stats = luigi_stats
            
            # Loop for specific category until user is done
            user_stat_input = input("\t>> Enter STAT to change for " + user_category.upper().strip() + ", [LVL,EXP,HP,BP,POW,DEF,SPD,STC] or type \"BACK\": ")
            user_stat = user_stat_input.upper().strip()
            
            while (user_stat != "BACK" and user_stat != "EXIT" and user_stat != "QUIT" and user_stat != "B" and user_stat != "E" and user_stat != "Q"):
                user_value_input = input("\t>> Enter VALUE for " + user_stat + " (integer): ")
                if user_value_input.strip().isnumeric():
                    user_value = int(user_value_input.strip())
                    
                    # Set stats in save_file to value
                    
                    something_found = False

                    if user_stat in current_stats:
                        save_file.seek(current_stats[user_stat])
                        current_val = int(save_file.read(stat_byte_size[user_stat]).hex(),16)
                        save_file.seek(current_stats[user_stat])
                        save_file.write(user_value.to_bytes(stat_byte_size[user_stat],'big'))
                        print("\t\t** SYS: Changing " + user_category.upper().strip() + "\'s " + user_stat + " from " + str(current_val) + " to " + str(user_value))
                        something_found = True
                        
                    if ("BASE_" + (user_stat)) in current_stats:
                        save_file.seek(current_stats["BASE_" + (user_stat)])
                        current_val = int(save_file.read(stat_byte_size["BASE_" + user_stat]).hex(),16)
                        save_file.seek(current_stats["BASE_" + (user_stat)])
                        save_file.write(user_value.to_bytes(stat_byte_size["BASE_" + user_stat],'big'))
                        print("\t\t** SYS: Changing " + user_category.upper().strip() + "\'s BASE_" + user_stat + " from " + str(current_val) + " to " + str(user_value))
                        something_found = True
                        
                    if ("MAX_" + (user_stat)) in current_stats:
                        save_file.seek(current_stats["MAX_" + (user_stat)])
                        current_val = int(save_file.read(stat_byte_size["MAX_" + user_stat]).hex(),16)
                        save_file.seek(current_stats["MAX_" + (user_stat)])
                        save_file.write(user_value.to_bytes(stat_byte_size["MAX_" + user_stat],'big'))
                        print("\t\t** SYS: Changing " + user_category.upper().strip() + "\'s MAX_" + user_stat + " from " + str(current_val) + " to " + str(user_value))
                        something_found = True 
                        
                    if ("CURR_" + (user_stat)) in current_stats:
                        save_file.seek(current_stats["CURR_" + (user_stat)])
                        current_val = int(save_file.read(stat_byte_size["CURR_" + user_stat]).hex(),16)
                        save_file.seek(current_stats["CURR_" + (user_stat)])
                        save_file.write(user_value.to_bytes(stat_byte_size["CURR_" + user_stat],'big'))
                        print("\t\t** SYS: Changing " + user_category.upper().strip() + "\'s CURR_" + user_stat + " from " + str(current_val) + " to " + str(user_value))
                        something_found = True
                        
                    if not something_found:
                        print("\t\t** SYS: Invalid stat. Please try again...")
                else:
                    print("\t\t** SYS: Invalid value. Please try again...")

                # loop again for STATS in this category
                user_stat_input = input("\n\t>> Enter STAT to change [LVL,EXP,HP,BP,POW,DEF,SPD,STC], or type \"BACK\": ")
                user_stat = user_stat_input.upper().strip()
        else:
            print("\t**SYS: Invalid category. Please try again...")
        # loop again for categories
        displayStats(save_file)
        user_category = input("\t>> Choose a stat category: [COINS,MARIO,LUIGI,STATS] or type \"EXIT\": ")
        
    printFooter()

def checksum_mlss(save_file):
    
    # title
    printHeader("Checksum")
    # calculate checksum
    save_file.seek(0x16)
    current_checksum = save_file.read(1)
    
    # print("Current Checksum: 0x" + current_checksum.hex() + "\n")
    print("\n** SYS: Computing Checksum...\n")
    
    addedbytes = 0
    
    offset = starting_address
    save_file.seek(offset)
    for i in range(4):
        byte_to_add = int(save_file.read(1).hex(),16)
        # print("\tAdding byte " + f"{byte_to_add:#0{4}x}" + " from address (DEC): " + str(offset))
        # print(f"{byte_to_add:#0{4}x}")
        addedbytes = addedbytes + byte_to_add
        offset += 1
    print("** SYS: Step 1 - Add 0x10 -> 0x13: " + str(addedbytes))
    
    offset = starting_address + 0x08
    save_file.seek(offset)
    for i in range(1776):
        byte_to_add = int(save_file.read(1).hex(),16)
        # print("\tAdding byte " + f"{byte_to_add:#0{4}x}" + " from address (DEC): " + str(offset))
        addedbytes = addedbytes + byte_to_add
        offset += 1
    print("** SYS: Step 2 - Add 0x18 -> 0x707: " + str(addedbytes))
    
    checksum = addedbytes%256
    
    print("** SYS: Step 3 - Mod the sum " + str(addedbytes) + " by 2^8: " + str(checksum) + "\n")
    
    print("[Stored Checksum:     0x" + current_checksum.hex() + "]")
    print("[Calculated Checksum: " + f"{checksum:#0{4}x}" + "]\n")
    
    checksum_bytes = checksum.to_bytes()
    # write_to_file_check = input(">> Would you like to write this checksum to the save file? (Y/N) ")
    # if (write_to_file_check.upper().strip() == "Y"):
    #     print("\n** SYS: Writing 0x" + checksum_bytes.hex() + " to save file at offset 0x16...\n")
    #     # write checksum to file
    #     save_file.seek(0x16)
    #     save_file.write(checksum_bytes)
    #     
    #     print("** SYS: Write Successful....\n")
    print("** SYS: Writing 0x" + checksum_bytes.hex() + " to save file at offset 0x16...")
    # write checksum to file
    save_file.seek(0x16)
    save_file.write(checksum_bytes)
    
    print("** SYS: Write Successful....")
    printFooter()

def main():
    
    # GUI to get filepath
    waitForUser = input("\n>> Please select your save file (Press ENTER)...\n")
    root = tk.Tk()
    root.withdraw()
    save_file_path = filedialog.askopenfilename()
    
    # open save file
    save_file = open(save_file_path,'r+b')
    
    # display stats
    displayStats(save_file)
    
    # change stats
    change_stats_check = input(">> Would you like to change the current stats? (Y/N) ")
    if (change_stats_check.upper().strip() == "Y" or change_stats_check.upper().strip() == "YES"):
        changeStats(save_file)
    checksum_mlss(save_file)
    print("** SYS: Exiting...\n")
    save_file.close()
    
    
main()