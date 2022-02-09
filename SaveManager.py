# SaveManager.py - allows saving/loading of multiple quick saves created in Teardown
# XxLegitOPxX
# 08/02/2022

import shutil
import sys
import os

#global path

# copied from stackoverflow lolol
def set_list(l, i, v):
      try:
          l[i] = v
      except IndexError:
          for _ in range(i-len(l)+1):
              l.append(None)
          l[i] = v

# main class
class SaveManager:
    def __init__(self, fileWithPath): # initial execution checks if required files exist
        pathFile = None
        try:
            pathFile = open(fileWithPath, "r")
            self.path = pathFile.readlines()[0]
            print("Found path.txt")

            isFile = os.path.isfile(self.path) 
            if isFile:
                print("quicksave.bin found in [" + self.path + "]")
            else:
                print("quicksave.bin was not found.")
        except FileNotFoundError:
            print("path.txt not found")
            input("Press ENTER to exit...")
            sys.exit(1)
        except Exception as e:
            print("An exception occurred: " + str(e))
            input("Press ENTER to exit...")
            sys.exit(1)
        finally:
            if pathFile:
                  #print("CLOSING PATHFILE...")
                  pathFile.close()
    
    # the startup prompt
    def AskForCommand(self):
        print("")
        letter = input("Do you want to SAVE FILE (s) or LOAD FILE (l)?: ")

        if letter == "s": # Execute SAVE FILE protocol
            print("\n") # double newline for distinguishing between active protocols
            print("==========[SAVE FILE]==========")
            saveName = input("Save as (don't include .bin): ") + ".bin"
            # "Are you sure" dialog
            print("")
            print("Name selected: " + saveName)
            proceed = input("Are you sure you want to save this file as the name above? (y/n): ")

            if proceed == "y":
                self.SaveFile(saveName)
            elif proceed == "n":
                print("")
                print("SAVE FILE operation cancelled.")
                input("Press ENTER to exit...")

        elif letter == "l": # Execute LOAD FILE protocol
            print("\n") # double newline for distinguishing between active protocols
            print("==========[LOAD FILE]==========")
            fileList = self.GetFilesInDirectory(".bin")

            def recurse(): # Ask for file (by number)
                print("")
                number = input("Select a file (by number): ")

                try: # Confirm file selection
                    # "Are you sure" dialog
                    fileSelected = fileList[int(number)]
                    print("")
                    print("File selected: " + fileSelected)
                    proceed = input("Are you sure you want to load this file? (y/n): ")

                    if proceed == "y":
                        self.LoadFile(fileSelected)
                    elif proceed == "n":
                        print("")
                        print("LOAD FILE operation cancelled.")
                        input("Press ENTER to exit...")
                except IndexError: # if index is out of range
                    print("Invalid number. Try again.")
                    recurse()
                except ValueError: # if index is not a number
                    print("Invalid number. Try again.")
                    recurse()

            recurse() # initial run
        else:
            print("Incorrect option. Try again.")
            self.AskForCommand()


    # these functions can be ran manually and they won't check for confirmation.
    # Saves a file with name "saveAsName"
    def SaveFile(self, saveAsName):
        try:
            shutil.copyfile(self.path, f"{saveAsName}")
            print("")
            print("File saved successfully.")
        except Exception as e:
            print("An error occurred: " + str(e))
        finally:
            input("Press ENTER to exit...")
    
    # Loads a file with name "fileName"
    def LoadFile(self, fileName):
        try:
            shutil.copyfile(f"{fileName}", self.path)
            print("")
            print("File loaded successfully.")
        except Exception as e:
            print("An error occurred: " + str(e))
        finally:
            input("Press ENTER to exit...")

    # prints all files in current working directory and returns a list 
    def GetFilesInDirectory(self, extension):
        index = -1
        fileList = []
        for file in os.scandir(os.getcwd()):
            if file.is_file():
                if file.name.endswith(".bin"):
                    index += 1
                    # it's a .bin file which is what we need
                    print(f"[{index}] " + file.name)
                    set_list(fileList, index, file.name)

        return fileList

#print("\n"*3)
manager = SaveManager("path.txt")
manager.AskForCommand()

#input()

#shutil.copyfile('/Users/datagy/Desktop/file.py', '/Users/datagy/Desktop/file2.py')
