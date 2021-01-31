import PyInstaller.__main__
from os.path import abspath, isfile, dirname, join, splitext
from os import rename
import sys


def getDirName(path):
    return dirname(path)


def getAbsolutePath(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = abspath(".")
    return join(basePath, relativePath)


print(getAbsolutePath('fonts\\Ubuntu-Regular.ttf'))

settings = ['--onefile', '--windowed']
pythonFile = input('Enter the Python file: ')
while not isfile(pythonFile):
    print('Sorry we can\'t find that file\n')
    pythonFile = input('Enter the Python file: ')

isAddData = input('Would you like to add extra data? (y/n): ').lower()
while isAddData != 'n' and isAddData != 'y':
    print('Please enter a \'y\' or a \'n\'\n')
while isAddData == 'y':
    dataFile = input('Enter the data file: ')
    while not isfile(dataFile):
        print('Sorry we can\'t find that file\n')
        dataFile = input('Enter the data file: ')
    settings.append('--add-data=' + getAbsolutePath(dataFile) +
                    ';' + getDirName(dataFile))
    isAddData = input('Would you like to add extra data? (y/n): ').lower()
    while isAddData != 'n' and isAddData != 'y':
        print('Please enter a \'y\' or a \'n\'\n')

settings.append(pythonFile)

print(settings)

PyInstaller.__main__.run(settings)

resultFilename = splitext(pythonFile)[0] + '.exe'
screenFilename = splitext(pythonFile)[0] + '.scr'

rename('dist\\' + resultFilename, 'dist\\' + screenFilename)
