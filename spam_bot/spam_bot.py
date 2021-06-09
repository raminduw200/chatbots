import pyautogui
import time
import keyboard

time.sleep(5);
f = open("spam_bot/spam_script.txt", 'r')

for word in f:
    pyautogui.typewrite(word)
    pyautogui.press('enter')
    if keyboard.is_pressed('q'):
        break
