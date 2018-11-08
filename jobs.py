from typing import Tuple,List
from os import listdir
from os.path import isfile,join
import numpy as np
import re
import everest
from shutil import copyfile

everestPath = "/home/marco/.everest2/k2/"

class Job:
    def __init__(self,name : str ,jobList : np.ndarray,doneJobs : List,jobPath : str):
        self._name = name
        self._jobList = jobList
        self._doneJobs = doneJobs
        self._jobPath = jobPath

    def run(self):
        files = [f for f in listdir(self._jobPath) if isfile(join(self._jobPath, f))]
        print(self._jobList)
        for kicID,season in tuple(map(tuple,self._jobList)):
            print(f"Running {kicID}")

            regex_fits = re.compile(rf".+{kicID}-c{season}.+\.fits") #check if job already done
            regex_pdf = re.compile(rf".+{kicID}-c{season}.+\.pdf")
            exists = list(filter(regex_fits.match, files))

            if exists != []:
                continue
            everest.missions.k2.GetData(kicID, download_only=True, season=season)
            everest.nPLD(kicID, season=season)
            everest.k2.GetCBVs(campaign=season)
            everest.nPLD(kicID, season=season).publish()

            lowerPart = kicID % 100000
            upperPart = kicID - lowerPart

            resultPath = f"{everestPath}c{season}/{upperPart}/{str(lowerPart).zfill(6)}/"

            files = [f for f in listdir(resultPath) if isfile(join(resultPath, f))]

            fits_files = list(filter(regex_fits.match, files))
            pdf_files = list(filter(regex_pdf.match, files))

            if fits_files == [] or pdf_files == []:
                print(f"Something went terribly wrong with job {kicID}")
                continue

            copyfile(f"{resultPath}{fits_files[0]}",f"{self._jobPath}{fits_files[0]}")
            copyfile(f"{resultPath}{pdf_files[0]}", f"{self._jobPath}{pdf_files[0]}")





