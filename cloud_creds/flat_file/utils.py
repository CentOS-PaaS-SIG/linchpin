import glob
from os import listdir
from os.path import isfile, join


def list_files(path):
    onlyfiles = glob.glob(path+"/*.*")
    return onlyfiles
