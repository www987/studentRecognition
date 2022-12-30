import face_recognition
import cv2
import numpy as np
import os
import glob
from login import login
from mysqlConnect import cur
ISADMIN = 0
USERID = None
ISADMIN, USERID = login()
print(ISADMIN, USERID)

