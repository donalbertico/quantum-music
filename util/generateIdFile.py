import os
import csv
import numpy as np

for folder in os.walk('./assets/'):
    if(folder[2]) :
        folderName = folder[0].split('./assets/')[1]
        if(folderName != 'filenames'):
            with open('./assets/filenames/'+folderName+'.csv','w') as f:
                write = csv.writer(f)
                write.writerows([folder[2]])
