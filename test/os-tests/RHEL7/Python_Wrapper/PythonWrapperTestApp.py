import os
import argparse
import sys
import shutil
import logging
import Glasswall


def argParser(parser):
    # Parser command line arguments

    parser.parse_args()
    args = parser.parse_args()

    if str(args.InputDirectory) != 'None':

        inputLocation = str(args.InputDirectory)
    else:
        print("No input directory given.\n")
        parser.print_help()
        sys.exit()

    if str(args.OutputDirectory) != 'None':

        outputLocation = str(args.OutputDirectory)
    else:
        print("No output directory given.\n")
        parser.print_help()
        sys.exit()

    if str(args.PathToConfig) != 'None':

        pathToConfig = str(args.PathToConfig)
    else:
        print("Path to the Config file was not specified.\n")
        parser.print_help()
        sys.exit()

    if str(args.PathToGwDLL) != 'None':

        pathToLib = str(args.PathToGwDLL)
    else:
        print("Path to the Glasswall DLL was not specified.\n")
        parser.print_help()
        sys.exit()

    if str(args.PathToWrapper) != 'None':

        pathToWrapper = str(args.PathToWrapper)
    else:
        print("Path to the report File was not specified.\n")
        parser.print_help()
        sys.exit()

    return inputLocation, outputLocation, pathToConfig, pathToLib, pathToWrapper


def getCommandLineArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i,", dest="InputDirectory", help="[Required] Input directory.", type=str)
    parser.add_argument("-o,", dest="OutputDirectory", help="[Required] Directory to store output packages.", type=str)
    parser.add_argument("-c,", dest="PathToConfig", help="[Required] Full path to Log folder.", type=str)
    parser.add_argument("-d,", dest="PathToGwDLL", help="[Required] Full path to Glasswall DLL or SO.", type=str)
    parser.add_argument("-w", dest="PathToWrapper", help="[Required] Full path to Python Wrapper.", type=str)

    return argParser(parser)


def getDirectoryFiles(inputDirectory):
    # Return a list of file paths from a given directory

    fileList = list()
    for root, _, files in os.walk(u"" + inputDirectory):
        for eachFile in files:
            fileList.append(os.path.join(root, eachFile))

    return fileList


def writeText(fileName, outputDir, text):
    f = open(os.path.join(outputDir, fileName), "wb")
    f.write(text.encode("utf8"))
    f.close()


def writeFile(fileName, outputDir, content):

    status = False

    fileOpenSuccess = False

    fileHandler = None

    try:
        fileHandler = open(os.path.join(outputDir,  fileName), "wb")

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

    }[key]


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

        try:
            logging.warning("debug Info: {0}".format(outputLocation))
        except:
            pass
    return outputLocation


def getGWStatusMessages(session, gw):

    return_messages = "\n  File Session Status  = Unimplemented"
    return_messages += "\n  File Session Message = Unimplemented"
    return_messages += "\n  File Session Error   = Unimplemented"

    logging.warning("return messages is {0}".format(return_messages))
    return return_messages


def processFile(filePath, inputDirectory, outputDirectory, path_to_config, gw):
    logging.warning("Running file processing API calls...")

    file_log = ""

    file_log += "> Begin processing file: " + str(filePath)

    folderName = os.path.join(outputDirectory, os.path.basename(filePath))
    # Mirror the input directory structure in the output Location
    outputLocation = folderName #mirrorDirectoryStructure(outputDirectory, inputDirectory, folderName)
    try:
        os.makedirs(outputLocation)
    except:
        pass

    inFile = open(filePath, "rb")
    input_file_Buffer = inFile.read()
    input_file_Buffer_length = len(input_file_Buffer)
    inFile.close()

    # use Glasswall to determine file type from file and memory prior to calling all other API functions
    file_type_return = gw.GW2DetermineFileTypeFromFile(filePath)
    if file_type_return.enumValue is 0:
        logging.warning("unsupported file type returned, will not call any other API functions on this file.")
        return

    memFileTypeReturn = gw.GW2DetermineFileTypeFromMemory(input_file_Buffer, input_file_Buffer_length)
    if memFileTypeReturn.enumValue is 0:
        logging.warning("unsupported file type returned, will not call any other API functions on this file.")
        return

    # Get file type for processing
    fileType = getFileType(file_type_return.enumValue)
    logging.warning("Returned file type from file {0}".format(fileType))

    memFileType = getFileType(memFileTypeReturn.enumValue)
    logging.warning("Returned file type from memory{0}".format(memFileType))

    # Begin testing procedures
    file_log += "\n***********************************************************"
    file_log += "\n> Test 01 - Determine file type from memory for file " + filePath + "..."
    file_log += "\n Returned: " + memFileType

    file_log += "\n***********************************************************"
    file_log += "\n> Test 02 - Determine file type for " + filePath + "..."
    file_log += "\n Returned: " + fileType

    # Test 03 - Input Memory -> Export Memory
    file_log += "\n***********************************************************"
    file_log += "\n> Test 03 - Input Memory -> Export Memory"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    status = gw.GW2RegisterInputMemory(session_id, input_file_Buffer, input_file_Buffer_length)
    file_log += "\n  GW2RegisterInputMemory completed with status code " + str(status.returnStatus)

    level = gw.AssignExportBuffer(session_id)

    status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    # Export the buffer contents to an appropriate file
    writeFile("03 - GW2InputFileExportMem.zip", outputLocation, gw.GetExportBytes(session_id).fileBuffer)

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 03 Complete"

    # Test 04 - Input Memory -> Export File
    file_log += "\n***********************************************************"
    file_log += "\n> Test 04 - Input Memory -> Export File"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    status = gw.GW2RegisterInputMemory(session_id, input_file_Buffer, input_file_Buffer_length)
    file_log += "\n  GW2RegisterInputMemory completed with status code " + str(status.returnStatus)

    outputFile = os.path.join(outputLocation, "04 - GW2InputMemExportFile.zip")

    return_status = gw.GW2RegisterExportFile(session_id, outputFile)
    file_log += "\n  GW2RegisterExportFile completed with status code " + str(return_status)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 04 Complete"

    # Test 05 - Input Memory -> Output Memory
    file_log += "\n***********************************************************"
    file_log += "\n> Test 05 - Input Memory -> Output Memory"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession = " + str(session_id)

    status = gw.GW2RegisterInputMemory(session_id, input_file_Buffer, input_file_Buffer_length)
    file_log += "\n  GW2RegisterInputMemory completed with status code " + str(status.returnStatus)

    gw.AssignOutputBuffer(session_id)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    file_name = "05 - GW2InputMemOutputMem." + fileType

    # Export the buffer contents to an appropriate file
    writeFile(file_name, outputLocation, gw.GetOutputBytes(session_id).fileBuffer)

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 05 Complete"

    # Test 06 - Input Memory -> Output File
    file_log += "\n***********************************************************"
    file_log += "\n> Test 06 - Input Memory -> Output File"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    status = gw.GW2RegisterInputMemory(session_id, input_file_Buffer, input_file_Buffer_length)
    file_log += "\n  GW2RegisterInputMemory completed with status code " + str(status.returnStatus)

    outputFile = os.path.join(outputLocation, "06 - GW2InputMemOutputFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 06 Complete"

    # Test 07 - Input File -> Export Memory
    file_log += "\n***********************************************************"
    file_log += "\n> Test 07 - Input File -> Export Memory"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterInputFile(session_id, filePath)
    file_log += "\n  GW2RegisterInputFile completed with status code " + str(return_status.returnStatus)

    gw.AssignExportBuffer(session_id)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    # Export the buffer contents to an appropriate file
    writeFile("07 - GW2InputFileExportMem.zip", outputLocation, gw.GetExportBytes(session_id).fileBuffer)

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 07 Complete"

    # Test 08 - Input File -> Export File
    file_log += "\n***********************************************************"
    file_log += "\n> Test 08 - Input File -> Export File"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterInputFile(session_id, filePath)
    file_log += "\n  GW2RegisterInputFile completed with status code " + str(return_status.returnStatus)

    outputFile = os.path.join(outputLocation, "08 - GW2InputFileExportFile.zip")
    return_status = gw.GW2RegisterExportFile(session_id, outputFile)
    file_log += "\n  GW2RegisterExportFile completed with status code " + str(return_status)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 08 Complete"

    # Test 09 - Input File -> Output Memory
    file_log += "\n***********************************************************"
    file_log += "\n> Test 09 - Input File -> Output Memory"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterInputFile(session_id, filePath)
    file_log += "\n  GW2RegisterInputFile completed with status code " + str(return_status.returnStatus)

    gw.AssignOutputBuffer(session_id)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    # Export the buffer contents to an appropriate file
    writeFile(("09 - GW2.InputFileOutputMem." + fileType), outputLocation, gw.GetOutputBytes(session_id).fileBuffer)

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 09 Complete"

    # Test 10 - Input File -> Output File
    file_log += "\n***********************************************************"
    file_log += "\n> Test 10 - Input File -> Output File"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterInputFile(session_id, filePath)
    file_log += "\n  GW2RegisterInputFile completed with status code " + str(return_status.returnStatus)

    outputFile = os.path.join(folderName, "10 - GW2InputFileOutputFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 10 Complete"
    logging.warning("session 10 complete")

    # Test 11 - Import Memory -> Output Memory
    file_log += "\n***********************************************************"
    file_log += "\n> Test 11 - Import Memory -> Output Memory"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    importFile = os.path.join(outputLocation, "04 - GW2InputMemExportFile.zip")
    import_file_Buffer = open(importFile, "rb").read()
    import_file_Buffer_Length = len(import_file_Buffer)

    return_status = gw.GW2RegisterImportMemory(session_id, import_file_Buffer, import_file_Buffer_Length)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    gw.AssignOutputBuffer(session_id)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    file_name = "11 - GW2.InputFileOutputMem." + fileType

    # Export the buffer contents to an appropriate file
    writeFile(file_name, outputLocation, gw.GetOutputBytes(session_id).fileBuffer)

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 11 Complete"

    # Test 12 - Import Memory -> Output file
    file_log += "\n***********************************************************"
    file_log += "\n> Test 12 - Import Memory -> Output File"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterImportMemory(session_id, import_file_Buffer, import_file_Buffer_Length)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "12 - GW2ImportMemOutputFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 12 Complete"

    # Test 13 - Import file -> Output memory
    file_log += "\n***********************************************************"
    file_log += "\n> Test 13 - Import File -> Output Memory"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterImportFile(session_id, importFile)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    gw.AssignOutputBuffer(session_id)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    file_name = "13 - GW2.ImportFileOutputMem." + fileType

    # Export the buffer contents to an appropriate file
    writeFile(file_name, outputLocation, gw.GetOutputBytes(session_id).fileBuffer)

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 13 Complete"

    # Test 14 - Import file -> Output file
    file_log += "\n***********************************************************"
    file_log += "\n> Test 14 - Import File -> Output File"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterImportFile(session_id, importFile)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "14 - GW2InputFileOutputFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 14 Complete"

    file_log += "\n***********************************************************"
    file_log += "\nInput, Import, Output, Export Testing Complete"

    # Test 15 Register Policy Settings
    file_log += "\n***********************************************************"
    file_log += "\n> Test 15 - Import File -> Output File, Register Policy Settings"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterImportFile(session_id, importFile)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "15 - GW2ImportFileOutputFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2GetPolicySettings(session_id)
    file_log += "\n  GW2GetPolicySettings completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 15 Complete"

    # Test 16 Register Policy Settings
    file_log += "\n***********************************************************"
    file_log += "\n> Test 16 - Import File -> Output File, Register Policy Settings from Memory"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterImportFile(session_id, importFile)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "16 - GW2InputMemExportFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RegisterPoliciesMemory(session_id)
    file_log += "\n  GW2RegisterPoliciesMemory completed with status code " + str(return_status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 16 Complete"

    # Test 17 - No Policy Loaded
    file_log += "\n***********************************************************"
    file_log += "\n> Test 17 - Import File -> Output File, No Policy Settings"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterImportFile(session_id, importFile)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "17 - GW2InputMemExportFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 17 Complete"

    # Test 18 - Register Analysis Memory
    file_log += "\n***********************************************************"
    file_log += "\n> Test 18 - Import File -> Output File, Register Analysis Memory"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterImportFile(session_id, importFile)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "18 - GW2ImportFileOutputFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status.returnStatus)

    gw.AssignAnalysisBuffer(session_id)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    # Export the buffer contents to an appropriate file
    writeFile("18 - GW2AnalysisMem.xml", outputLocation, gw.GetAnalysisBytes(session_id).fileBuffer)

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 18 Complete"

    # Test 19 - Register Analysis File
    file_log += "\n***********************************************************"
    file_log += "\n> Test 19 - Import File -> Output File, Register Analysis File"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterImportFile(session_id, importFile)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "19 - GW2ImportFileOutputFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "19 - GW2ImportFileOutputFile.xml")
    return_status = gw.GW2RegisterAnalysisFile(session_id, outputFile)
    file_log += "\n  GW2RegisterAnalysisFile completed with status code " + str(return_status)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 19 Complete"

    # Test 20 - Register Report File
    file_log += "\n***********************************************************"
    file_log += "\n> Test 20 - Import File -> Output File, Register Report File"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterImportFile(session_id, importFile)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "20 - GW2ImportFileOutputFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "20 - GW2ReportFile.xml")
    return_status = gw.GW2RegisterReportFile(session_id, outputFile)
    file_log += "\n  GW2RegisterReportFile completed with status code " + str(return_status)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 20 Complete"

    # Test 21 - Override File Type with specific value
    file_log += "\n***********************************************************"
    file_log += "\n> Test 21 - Import File -> Output File, Register Report File"
    session_id = gw.GW2OpenSession()
    file_log += "\n  GW2OpenSession returned SessionID = " + str(session_id)

    return_status = gw.GW2RegisterImportFile(session_id, importFile)
    file_log += "\n  GW2RegisterImportFile completed with status code " + str(return_status)

    outputFile = os.path.join(outputLocation, "21 - GW2ImportFileOutputFile." + fileType)
    status = gw.GW2RegisterOutFile(session_id, outputFile)
    file_log += "\n  GW2RegisterOutFile completed with status code " + str(status.returnStatus)

    return_status = gw.GW2RegisterPoliciesFile(session_id, path_to_config, 0)
    file_log += "\n  GW2RegisterPoliciesFile completed with status code " + str(return_status)

    return_status = gw.GW2RunSession(session_id)
    file_log += "\n  GW2RunSession completed with status code " + str(return_status)
    file_log += str(getGWStatusMessages(session_id, gw))

    return_status = gw.GW2CloseSession(session_id)
    file_log += "\n  GW2CloseSession completed with status code " + str(return_status)
    file_log += "\n> Test 21 Complete"

    file_log += "\n\n***********************************************************"
    file_log += "\n>ile: " + str(filePath) + "Processing complete"
    file_log += "\n***********************************************************"

    writeText("Local_Process_Log.txt", outputLocation, file_log)


def LoadGlassWall(pathToLib):
    from Glasswall import Interface_GwCore2
    logging.warning("Loading Library")

    gw = Interface_GwCore2(pathToLib)
    logging.warning("Done")

    return gw


def emptyOutput(directory):
    logging.warning("Removing content from output directory...")

    for root, dirs, files in os.walk(directory):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    logging.warning("done")


def main():

    inputLocation, outputLocation, pathToConfig, pathToLib, pathToWrapper = getCommandLineArgs()

    emptyOutput(outputLocation)

    sys.path.append(pathToWrapper)
    gw = LoadGlassWall(pathToLib)

    libVer = gw.GW2LibVersion()

    logging.warning("library version is " + str(libVer.text))

    logging.warning("generating process log")

    process_log = "\n iterating over input directory"

    inputFileList = getDirectoryFiles(inputLocation)

    for eachFile in inputFileList:
        processFile(eachFile, inputLocation, outputLocation, pathToConfig, gw)
        process_log += "\n> Processing file " + eachFile

    process_log += "\n> Processing file "


if __name__ == "__main__":
    main()
