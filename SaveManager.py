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
    def __init__(self, savePath): # initial execution checks if required files exist
        pathFile = None
        try:
            self.path = savePath
            pathFile = open(fileWithPath, "r")
            self.path = pathFile.readlines()[0].replace("{{user_name}}", os.getlogin())
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
    @classmethod
    def AskForCommand(self):
        letter = input("\nDo you want to SAVE FILE (s) or LOAD FILE (l)?: ").lower() # lower

        if letter == "s": # Execute SAVE FILE protocol
            print("\n\n==========[SAVE FILE]==========") # Easily distinguish between operations
            saveName = input("Save as (don't include .bin): ") + ".bin"
            # "Are you sure" dialog
            print("\nName selected: " + saveName)
            proceed = input("Are you sure you want to save this file as the name above? (y/n): ").lower()
            if proceed == "y":
                self.SaveFile(saveName)
            elif proceed == "n":
                print("\nSAVE FILE operation cancelled.")
                input("Press ENTER to exit...")

        elif letter == "l": # Execute LOAD FILE protocol
            print("\n\n==========[LOAD FILE]==========") # Easily distinguish between operations
            fileList = self.GetFilesInDirectory(".bin")

            def recurse(): # Ask for file (by number)
                number = input("\nSelect a file (by number): ")

                try: # Confirm file selection
                    # "Are you sure" dialog
                    fileSelected = fileList[int(number)]
                    print("\nFile selected: " + fileSelected)
                    proceed = input("Are you sure you want to load this file? (y/n): ")

                    if proceed == "y":
                        self.LoadFile(fileSelected)
                    elif proceed == "n":
                        print("\nLOAD FILE operation cancelled.")
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


    @classmethod
    def SaveFile(self, fileName):
        """
        Creates a new save file with the name `fileName`
        """
        try:
            shutil.copyfile(self.path, f"{fileName}")
            print("\nFile saved successfully.")
        except Exception as e:
            print("An error occurred: " + str(e))
        finally:
            input("Press ENTER to exit...")
    
    @classmethod
    def LoadFile(self, fileName):
        """
        Loads the file `fileName` into the game
        """
        try:
            shutil.copyfile(f"{fileName}", self.path)
            print("\nFile loaded successfully.")
        except Exception as e:
            print("An error occurred: " + str(e))
        finally:
            input("Press ENTER to exit...")

    @classmethod
    def GetFilesInDirectory(self, extension):
        """
        Print all files in the CWD and return a list
        """
        index = -1
        fileList = []
        for file in os.scandir(os.getcwd()):
            if file.is_file():
                if file.name.endswith(extension):
                    index += 1
                    # it's a .bin file which is what we need
                    print(f"[{index}] " + file.name)
                    set_list(fileList, index, file.name)

        return fileList


manager = SaveManager("path.txt")
manager.AskForCommand()
