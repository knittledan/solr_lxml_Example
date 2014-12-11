import os


def makeDirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)
