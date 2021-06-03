import pyautogui as pog
import requests
from textblob import TextBlob
from time import sleep
import pyperclip
import keyboard
import os
from os.path import join, dirname
from dotenv import load_dotenv

# import brainshop credentials
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BID = os.environ.get("BID")
KEY = os.environ.get("KEY")

position1 = pog.locateOnScreen("send_sticker.jpg", confidence=0.6)
# Position laptop screen - 2350, 1803
x = position1[0]
y = position1[1]


def get_message():
    global x, y

    position = pog.locateOnScreen("send_sticker.jpg", confidence=0.7)
    x = position[0]
    y = position[1]
    pog.moveTo(x, y)
    pog.moveTo(x + 80, y - 55)

    # select last message and copy
    pog.tripleClick()
    pog.hotkey('ctrl', 'c')

    # deselect selected text
    pog.click()

    return pyperclip.paste()


def send_message(message):
    global x, y

    position = pog.locateOnScreen("send_sticker.jpg", confidence=0.7)
    # print(position, position[0], position[1])
    # x = position[0]
    # y = position[1]
    # print(x, y + " TESTING")

    pog.moveTo(position[0] + 150, position[1] + 13)
    pog.click()

    pog.typewrite(message, interval=0.01)
    pog.typewrite("\n")


def check_new_messages():
    # press q to exit
    while not keyboard.is_pressed('q'):
        try:
            position = pog.locateOnScreen("inbox_mssg.jpg", confidence=0.9)

            if position is not None:
                pog.moveTo(position)
                pog.moveRel(-100, 0)
                pog.click()

                send_message(get_response())

                # Reset position
                position = pog.locateOnScreen("top_location.jpg", confidence=.9)
                pog.moveTo(position)
                pog.click()

                sleep(5)

        except Exception:
            print("No new messages")


def get_response():
    msg = get_message()
    response = requests.get(
        "http://api.brainshop.ai/get?bid={}&key={}&uid=154631&msg={}".format(BID, KEY, msg))

    responseJson = response.json()

    print(responseJson['cnt'] + " - AI Chat bot")

    # return responseJson['cnt'] + sentiment_analysis(responseJson['cnt']) + " - AI Chat bot"
    return responseJson['cnt'] + " - AI Chat bot"


def sentiment_analysis(message):
    return TextBlob(message).sentiment


check_new_messages()
