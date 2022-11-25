########################################################################################################################
#                                                                                                                      #
# SMOKE                                                                                                                #
#                                                                                                                      #
# This tool is used to verify whether a specified Steam user owns a particular game on Steam.                          #
#                                                                                                                      #
# It WILL NOT WORK until the included .env file has been amended to contain information required by Valve's API. The   #
# required values have placeholders in secrets.env. Check the GitHub repo if you have any questions about using Smoke. #
#                                                                                                                      #
# https://github.com/MrSarno/Smoke                                                                                     #
#                                                                                                                      #
########################################################################################################################


import os


def clear_screen():
    """Clears the screen, regardless of the OS."""
    os.system("cls" if os.name == "nt" else "clear")
    print("\n")
