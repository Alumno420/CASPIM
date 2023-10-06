import os


def get_image_path(imageName):
    imgDir = get_images_path()
    path = imgDir + os.path.sep + imageName
    return path


def get_images_path():
    scriptDir = os.path.dirname(os.path.realpath(__file__))
    imgDir = scriptDir + os.path.sep + 'img'
    return imgDir


def get_root_path():
    scriptDir = os.path.dirname( os.path.realpath(__file__) )
    rootDir = scriptDir
    for _ in range(0, 3):
        rootDir = rootDir + os.path.sep + '..'
    rootDir = os.path.abspath( rootDir )
    return rootDir
