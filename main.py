#!/usr/bin/env python3


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


# imports

import requests
import sys

from pathlib import Path
from utils import clear_screen


# consts

VERSION = "1.0"
INDENT = "     "


# init


def greet_user():
    clear_screen()
    print(INDENT + "Smoke v" + VERSION)
    print(INDENT + "----------\n")


# prompt user for Steam User ID


def id_prompt():
    steam_user_id = input(INDENT + "Please enter Steam User ID: ")
    return steam_user_id


# obtain publisher secret et al


def secrets_reader():
    f = open(Path(__file__).parent / "secrets.env", "r")
    lines = []
    for line in f:
        lines.append(line)
    f.close()

    pub_auth_key = lines[0]
    pub_auth_key = pub_auth_key[15:]
    pub_auth_key = pub_auth_key.strip()

    app_id = lines[1]
    app_id = app_id[9:]
    app_id = app_id.strip()

    send_request(pub_auth_key, steam_user_id, app_id)


# send GET request to Valve


def send_request(pub_auth_key, steam_user_id, app_id):
    steam_url = "https://partner.steam-api.com/ISteamUser/CheckAppOwnership/v2/"
    steam_url_params = {"key": pub_auth_key, "steamid": steam_user_id, "appid": app_id}

    try:
        r = requests.get(url=steam_url, params=steam_url_params, timeout=3.5)
    except requests.exceptions.ConnectTimeout:
        print("\n")
        print(INDENT + "[ERROR] Could not connect to the Steam servers.")
        print(
            INDENT
            + "Please verify you are currently connected to the internet, then try again.\n\n"
        )
        print(
            INDENT
            + "If the issue persists, see if https://steamstat.us suggests Valve are having problems."
        )
        print(INDENT + "The website is unofficial, but is usually very reliable.")
        end_smoke()
    except requests.exceptions.SSLError:
        print("\n")
        print(INDENT + "[ERROR] Could not establish a secure connection.")
        print(INDENT + "Aborting.")
        end_smoke()
    except requests.exceptions.ConnectionError:
        print("\n")
        print(INDENT + "[ERROR] Could not connect to Valve's servers.")
        print(
            INDENT
            + "Are they having problems? It's not official, but you could try checking https://steamstat.us"
        )
        end_smoke()
    except requests.exceptions.HTTPError:
        print("\n")
        print(INDENT + "[ERROR] A HTTP error occurred.")
        end_smoke()
    except (requests.exceptions.InvalidURL, requests.exceptions.URLRequired):
        print("\n")
        print(INDENT + "[ERROR] A valid URL was not provided for your request.")
        print(INDENT + "If this keeps happening, delete Smoke & re-download it.")
        end_smoke()
    except requests.exceptions.ReadTimeout:
        print("\n")
        print(
            INDENT
            + "[ERROR] The Steam server received the request, but failed to respond in a timely fashion."
        )
        end_smoke()

    quit_if_error(r)


# abort in cases where the status code is not set to 200 (OK)


def quit_if_error(r):
    if r.status_code != 200:
        print("\n")
        print(INDENT + "[ERROR] Request failed.")
        print(INDENT + "Valve's server sent the following information;\n")
        print(INDENT + "Status code: " + str(r.status_code))
        print(INDENT + "More information: " + str(r.text))

        end_smoke()

    parse_reply(r)


# interpret the response


def parse_reply(r):
    valves_response = str(r.text[27:])
    print("\n")
    if valves_response.startswith("true"):
        print(INDENT + "This user DOES indeed own the game on Steam!")
    elif valves_response.startswith("false"):
        print(INDENT + "This user does NOT currently own the game on Steam.")
    else:
        print(
            INDENT
            + "[ERROR] Smoke was unable to determine whether this user owns the game on Steam."
        )


# bring the program to an end


def end_smoke():
    print("\n")
    input(INDENT + "Press Enter to close...")
    sys.exit()


# run

if __name__ == "__main__":
    greet_user()
    steam_user_id = id_prompt()
    secrets_reader()
    end_smoke()
