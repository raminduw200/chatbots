import pyautogui as pog
import requests
from textblob import TextBlob
from time import sleep
import pyperclip
# import keyboard
import os
from os.path import join, dirname
from dotenv import load_dotenv

# import brainshop credentials
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BID = os.environ.get("BID")
KEY = os.environ.get("KEY")

# Locate send location
pos_send_stkr = pog.locateOnScreen("ss/send_sticker.jpg", confidence=0.6)
x_send_stkr = pos_send_stkr[0]  # Position of laptop screen - 2350
y_send_stkr = pos_send_stkr[1]  # Position of laptop screen - 1803

# Locate first conversation location
pos_top_location = pog.locateOnScreen("ss/top_location.jpg", confidence=0.7)


def get_message():
    global x_send_stkr, y_send_stkr

    pog.moveTo(x_send_stkr, y_send_stkr)
    pog.moveTo(x_send_stkr + 80, y_send_stkr - 55)

    # select last message and copy
    pog.tripleClick()
    pog.hotkey('ctrl', 'c')

    # deselect selected text
    pog.click()

    return pyperclip.paste()


def send_message(message):
    global x_send_stkr, y_send_stkr

    pog.moveTo(x_send_stkr + 150, y_send_stkr + 13)
    pog.click()

    pog.typewrite(message, interval=0.01)
    pog.typewrite("\n")


def check_new_messages():
    global pos_top_location
    while True:
        try:
            position = pog.locateOnScreen("ss/inbox_mssg.jpg", confidence=0.9)
            if position is not None:
                pog.moveTo(position)
                pog.moveRel(-100, 0)
                pog.click()

                send_message(get_response())

                # Reset position
                pog.moveTo(pos_top_location)
                pog.click()

                sleep(5)

        except Exception:
            print("No new messages")


def get_response():
    msg = get_message()
    response = requests.get(
        "http://api.brainshop.ai/get?bid={}&key={}&uid=154631&msg={}".format(BID, KEY, msg))

    responseJson = response.json()

    print(responseJson['cnt'] + " - Chat bot")

    # return responseJson['cnt'] + sentiment_analysis(responseJson['cnt']) + " - AI Chat bot"
    return responseJson['cnt'] + " - Chat bot"


def sentiment_analysis(message):
    return TextBlob(message).sentiment


check_new_messages()
