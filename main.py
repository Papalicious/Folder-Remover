import os
import shutil
from pathlib import Path
import pandas as pd
import threading
import time
from pandas import ExcelWriter
from Thready import *





print('Write dir name:')
carpeta = input()
print('Write Master File name:')
masterIn = input()
masterPath = carpeta  + '/' + masterIn
threadReader = Checker(carpeta,masterIn,masterPath)
threadReader.start()
