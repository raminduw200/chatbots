import pyautogui as pag
from time import sleep

while True:
    posXY = pag.position()
    print(posXY, pag.pixel(posXY[0], posXY[1]))
    sleep(1)

    if posXY[0] == 0:
        break
