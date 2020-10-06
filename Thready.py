import os
import shutil
from pathlib import Path
import pandas as pd
import threading
import time
from pandas import ExcelWriter
class Checker(threading.Thread):
    def __init__(self,carpeta,masterIn,masterPath):
      threading.Thread.__init__(self)
      self.goOn = True
      self.carpeta =carpeta
      self.masterIn =masterIn
      self.masterPath =masterPath
    def run(self):
        while(True):
            change = False
            time.sleep(0.3)
            entries = os.listdir(self.carpeta)
            dirFalse =self.carpeta +'/Not_Applicable'
            dirTrue =self.carpeta + '/Processed'
            notApplicable = Path(dirFalse)
            processed = Path(dirTrue)

            notApplicable.mkdir(exist_ok=True)
            processed.mkdir(exist_ok=True)
            for entry in entries:
                if entry == 'Processed' or entry == 'Not_Applicable' or entry ==self.masterIn:
                    continue
                if entry.endswith('.xls'):
                    try:
                        os.remove(dirTrue + '/'+entry)

                    except:
                        pass
                    try:

                        shutil.move(self.carpeta+'/'+entry,dirTrue)
                        self.copyToMaster( self.masterPath,dirTrue + '/' + entry)
                        os.remove(self.carpeta+'/'+entry)
                    except:
                        continue

                else:
                    try:
                        os.remove(dirFalse + '/'+entry)
                    except:
                        pass
                    try:
                        shutil.move(self.carpeta+'/'+entry,dirFalse)
                        os.remove(self.carpeta+'/'+entry)
                    except:
                        continue

    def copyToMaster(self,master,fileNow):
        allSheetNames = []
        print('Copying: ' + fileNow + ' to ' + master)
        masterFileExist = False
        try:
            xlsMaster = pd.ExcelFile(master)
            masterFileExist =True
        except:
            pass
        xlsNow = pd.ExcelFile(fileNow)
        dfSheets = []
        if masterFileExist:
            allSheetNames =  xlsMaster.sheet_names + xlsNow.sheet_names
            self.addToList(xlsMaster.sheet_names,master,dfSheets)
            self.addToList(xlsNow.sheet_names,fileNow,dfSheets)
        else:
            allSheetNames =  xlsNow.sheet_names
            self.addToList(xlsNow.sheet_names,fileNow,dfSheets)
        try:
            os.remove(master)
        except:

            pass

        with ExcelWriter(master) as writer:
            for n, df in enumerate(dfSheets):
                df.to_excel(writer,allSheetNames[n])
            writer.save()

    def addToList(self,listName,path,allDF):
        for sheet in listName:
            dfATM = pd.read_excel(path, sheet_name=sheet)
            allDF.append(dfATM)
