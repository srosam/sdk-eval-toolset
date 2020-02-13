import logging
import os
import shutil


def getDirectoryFiles(inputDirectory):
    # Return a list of file paths from a given directory
    fileList = list()
    for root, _, files in os.walk(u"" + inputDirectory):
        for eachFile in files:
            fileList.append(os.path.join(root, eachFile))
    return fileList


def emptyOutput(directory):
    for root, dirs, files in os.walk(directory):
        shutil.rmtree(os.path.join(root))


def writeText(fileName, outputDir, text):
    f = open(os.path.join(outputDir, fileName), "wb")
    f.write(text.encode("utf8"))
    f.close()


def writeFile(fileName, outputDir, content):
    status = False
    fileOpenSuccess = False
    fileHandler = None

    try:
        fileHandler = open(os.path.join(outputDir, fileName), "wb")
        fileOpenSuccess = True
    except IOError:
        status = False

    if fileOpenSuccess:
        if content:
            fileHandler.write(content)
        fileHandler.close()
        status = True

    return status


def getFileType(key):
    return {
        16: "pdf",
        17: "doc",
        18: "docx",
        19: "ppt",
        20: "pptx",
        21: "xls",
        22: "xlsx",
        23: "png",
        24: "jpg",
        25: "gif",
        26: "emf",
        27: "wmf",
        28: "rtf",
        29: "bmp",
        30: "tiff",
        31: "pe",
        32: "macho",
        33: "elf",
        34: "mp4",
        35: "mp3",
        36: "mp2",
        37: "wav",
        38: "mpg",
        39: "coff",

    }.get(key, "ft_unknown")


# noinspection PyBroadException
def mirrorDirectoryStructure(outdir, indir, infile):
    absInPath = os.path.abspath(infile)
    relInPath = os.path.relpath(absInPath, indir)

    _, pathWithNoDrive = os.path.splitdrive(relInPath)
    _, outPathWithNoDrive = os.path.splitdrive(outdir)
    commonPathElements = os.path.commonprefix([os.path.normpath(pathWithNoDrive),
                                               os.path.normpath(outPathWithNoDrive)])

    if commonPathElements:
        lastChar = commonPathElements[len(commonPathElements) - 1]
        if lastChar is not "\\":
            commonPathElements = commonPathElements.rpartition('\\')[0]
    newPath = pathWithNoDrive.replace(commonPathElements, "")

    if newPath[0] == "\\" or newPath[0] == '/':
        outputLocation = os.path.join(outdir, newPath[1:])
    else:
        outputLocation = os.path.join(outdir, newPath)

    return outputLocation
