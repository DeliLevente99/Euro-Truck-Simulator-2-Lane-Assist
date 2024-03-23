import numpy as np
from ETS2LA.plugins.plugin import PluginInformation
import rpyc
import time
import cv2
import copy
PluginInfo = PluginInformation(
    name="ShowImage",
    description="Will show the screen capture img.",
    version="1.0",
    author="Tumppi066"
)

cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.resizeWindow("img", 1280, 720)

def plugin(runner):
    startTime = time.time()
    img = runner.GetData(["ScreenCapture"]) # MSS image object
    endTime = time.time()
    # print(f"GetData(['ScreenCapture']) time: {round((endTime - startTime)*1000,1)}ms")
    img = img[0]
    try:
        cv2.imshow("img", img)
        cv2.waitKey(1)
    except:
        pass