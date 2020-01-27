from sys import exit as exit_script
import os

bot_secret_file = "bot_secret.txt"

def get_secret():
    # Allow fuction to access variable
    global bot_secret_file
    # Check if the file even exists before trying to open it.
    if os.path.isfile( bot_secret_file ):
        # Open the file.
        f = open( bot_secret_file, "r" )
        # Make sure the file was opened in READ mode.
        if f.mode == "r":
            data = f.read()
            # Dirty way to clean output, I know.
            data = data.replace( "\n", "" )
            data = data.replace( "\t", "" )
            data = data.replace( " ", "" )
            if len( data ):
                return data
            else:
                print( "Bot secret file is empty!" )
                exit_script( 1 )
        # Show error and close if file is not in READ mode.
        else:
            print( "Bot secret file wasn't opened in read mode! Aborting ..." )
            exit_script( 1 )
    # Show error and exit if file is not found.
    else:
        print( f"Bot secret file not found! Please make a file named {bot_secret_file} in the same directory as this script with your secret!" )
        exit_script( 1 )