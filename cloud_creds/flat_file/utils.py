import glob
from os import listdir
from os.path import isfile, join

def list_files(path):
    #onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] 
    onlyfiles = glob.glob(path+"/*.*")
    return onlyfiles
