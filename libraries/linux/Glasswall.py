import ctypes as ct
import os
import logging


"""
    Linux Dependencies
    ==================

    Run the following commands to setup the library

        sudo ln -s {X}/libglasswall_core2.so /usr/lib/libglasswall_core2.so.1
        sudo ln -s {X}/libQt5Concurrent.so /usr/lib/libQt5Concurrent.so.5
        sudo ln -s {X}/libQt5Core.so /usr/lib/libQt5Core.so.5
        sudo ln -s {X}/libquazip.so /usr/lib/libquazip.so.1
        sudo ln -s {X}/libQt5Xml.so /usr/lib/libQt5Xml.so.5
        sudo ln -s {X}/libicui18n.so /usr/lib/libicui18n.so.56
        sudo ln -s {X}/libicuuc.so /usr/lib/libicuuc.so.56
        sudo ln -s {X}/libicudata.so /usr/lib/libicudata.so.56
        sudo ln -s {X}/libQt5Gui.so /usr/lib/libQt5Gui.so.5
        sudo ldconfig

    Where {X} is the directory containing Glasswall

"""


class GwStringReturnObj:
    """A result from Glasswall containing a text string"""

    def __abs__(self):
        pass

    text = None  # type: str or None


class GwStatusReturnObj:
    """A result from Glasswall containing the return status."""

    def __init__(self):
        pass

    returnStatus = 0  # type: int


class GwMemReturnObj:
    """A result from Glasswall containing the return status along with the file buffer"""

    def __init__(self):
        pass

    returnStatus = 0  # type: int
    fileBuffer = None  # type: bytearray or bytes or None
    Buffer = 0  # type: bytes
    BufferLength = 0  # type: bytes


class GwFileTypeEnum:
    """A result from Glasswall containing the determined file type value."""
    def __init__(self):
        pass

    enumValue = 0  # type: int
    fileBuffer = None  # type: bytearray or None


class Interface_GwCore2:
    """
        A Python API wrapper around the Glasswall Core-2 library.
    """

    gwLibrary = None

    """Python dictionaries keeping track of memory buffers"""
    sessionExportMemoryTracker = dict()
    sessionOutputMemoryTracker = dict()
    sessionAnalysisMemoryTracker = dict()
    sessionPolicyMemoryTracker = dict()

    # sessionId = 0

    def __init__(self, pathToLib):
        """
            Constructor for the Glasswall library

            :param str pathToLib: The file path to the Glasswall library.
        """

        try:
            # Change working directory to lib directory to find dependencies in Windows
            cwd = os.getcwd()
            os.chdir(os.path.dirname(pathToLib))

            print(pathToLib)

            self.gwLibrary = ct.cdll.LoadLibrary(pathToLib)

            # Revert to original working directory after loading lib
            os.chdir(cwd)

        except Exception as e:
            raise Exception("Failed to load Glasswall library. Exception: {0}".format(e))

    def CreateArrayFromBuffer(self, buffer, bufferLength):
        if buffer == 0 or bufferLength == 0:
            return 0

        gwReturn = GwMemReturnObj

        fileBuffer = (ct.c_byte * bufferLength.value)()
        ct.memmove(fileBuffer, buffer.value, bufferLength.value)

        gwReturn.fileBuffer = bytearray(fileBuffer)

        return gwReturn

    def AssignExportBuffer(self, session):

        returnObj = self.GW2RegisterExportMemory(session)
        gwReturn = GwMemReturnObj()

        gwReturn.Buffer = returnObj.Buffer
        gwReturn.BufferLength = returnObj.BufferLength

        self.sessionExportMemoryTracker[session] = gwReturn

    def AssignOutputBuffer(self, session):
        returnObj = self.GW2RegisterOutputMemory(session)
        gwReturn = GwMemReturnObj()

        gwReturn.Buffer = returnObj.Buffer
        gwReturn.BufferLength = returnObj.BufferLength

        self.sessionOutputMemoryTracker[session] = gwReturn
        # return returnObj

    def AssignAnalysisBuffer(self, session):
        returnObj = self.GW2RegisterAnalysisMemory(session)
        gwReturn = GwMemReturnObj()

        gwReturn.Buffer = returnObj.Buffer
        gwReturn.BufferLength = returnObj.BufferLength

        self.sessionAnalysisMemoryTracker[session] = gwReturn

    def AssignPoliciesMemory(self, session):
        returnObj = self.GW2RegisterPoliciesMemory(session)
        gwReturn = GwMemReturnObj()

        gwReturn.Buffer = returnObj.Buffer
        gwReturn.BufferLength = returnObj.BufferLength

        self.sessionPolicyMemoryTracker[session] = gwReturn

    def GetExportBytes(self, session):

        if session in self.sessionExportMemoryTracker:
            returnObj = self.sessionExportMemoryTracker[session]
            array = self.CreateArrayFromBuffer(returnObj.Buffer, returnObj.BufferLength)

            data = self.sessionExportMemoryTracker.pop(session)
            return array
        else:
            return None

    def GetOutputBytes(self, session):

        if session in self.sessionOutputMemoryTracker:
            returnObj = self.sessionOutputMemoryTracker[session]
            array = self.CreateArrayFromBuffer(returnObj.Buffer, returnObj.BufferLength)

            self.sessionOutputMemoryTracker.pop(session)
            return array
        else:
            return None

    def GetAnalysisBytes(self, session):

        if session in self.sessionAnalysisMemoryTracker:
            returnObj = self.sessionAnalysisMemoryTracker[session]
            array = self.CreateArrayFromBuffer(returnObj.Buffer, returnObj.BufferLength)

            # self.sessionAnalysisMemoryTracker.pop(session)
            return array
        else:
            return None

    def GetPolicyBuffer(self, session):

        if session in self.sessionPolicyMemoryTracker:
            returnObj = self.sessionPolicyMemoryTracker[session]
            array = self.CreateArrayFromBuffer(returnObj.Buffer, returnObj.BufferLength)

            return array
        else:
            return None

    def GW2DetermineFileTypeFromFile(self, filePath):
        """Returns a vaue indicaing th file type determined by glasswall.

        :param: str filephath: The file path to the input file.
        :return: A result indicating the determined file type
        :rtype: GwFiletypeEnum"""

        # API function declaration
        self.gwLibrary.GW2DetermineFileTypeFromFile.argtype = [ct.c_char_p]

        # Variable initialisation
        c_path = ct.c_char_p(filePath.encode("utf-8"))

        # Return Object
        gwReturn = GwFileTypeEnum()

        # API call
        gwReturn.enumValue = self.gwLibrary.GW2DetermineFileTypeFromFile(c_path)

        return gwReturn

    def GW2DetermineFileTypeFromMemory(self, inputFileBuffer, inputLength):
        """Returns a vaue indicaing th file type determined by glasswall.

        :param: bytearray inputFileBuffer: The input buffer containing the file to be determined
        :param: inputLength: length of the input file buffer data.
        :return: A result indicating the determined file type
        :rtype: GwFiletypeEnum"""

        # API function declaration
        self.gwLibrary.GW2DetermineFileTypeFromMemory.argtypes = [
            ct.c_char_p,
            ct.c_size_t
        ]

        # Variable function declaration
        inBuff = ct.c_char_p(inputFileBuffer)
        inLen = ct.c_size_t(inputLength)

        # Return Object
        gwReturn = GwFileTypeEnum()

        # API Call
        gwReturn.enumValue = self.gwLibrary.GW2DetermineFileTypeFromMemory(inBuff, inLen)

        return gwReturn

    def GW2LibVersion(self):
        """Returns the Glasswall library version

        :return: A result with the Glasswall library version
        :rtype: GwStringReturnObj"""

        # Declare the return type
        self.gwLibrary.GW2LibVersion.restype = ct.c_char_p

        # Return Object
        gwReturn = GwStringReturnObj()

        # API Call
        version = self.gwLibrary.GW2LibVersion()

        gwReturn.text = ct.string_at(version).decode()

        return gwReturn

    def GW2OpenSession(self):
        """
            Open a new Glasswall session
        """

        # API Call
        session = self.gwLibrary.GW2OpenSession()

        return session

    def GW2CloseSession(self, session):
        """
            Close the Glasswall session
        """

        # API function declaration
        self.gwLibrary.GW2CloseSession.argtypes = [ct.c_size_t]

        # Variable initialisation
        c_session_id = ct.c_size_t(session)

        # API Call
        sesh_status = self.gwLibrary.GW2CloseSession(c_session_id)

        return sesh_status

    def GW2RegisterPoliciesFile(self, session, policyPath, policyFormat):
        """Registers the policies to be used by Glasswall when processing files

        :param: policyPath: A pointer to the policies data
        :param: policyFormat: format of the policies data
        :rtype: GwStatusReturnObj"""

        # API function declaration
        self.gwLibrary.GW2RegisterPoliciesFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p,
            ct.c_int,
        ]

        # Variable initialisation
        c_sessions_id = ct.c_size_t(session)
        c_char_str = ct.c_char_p(policyPath.encode("utf-8"))
        c_pol_buff = ct.c_int(policyFormat)

        # Return Object
        gwReturn = GwStatusReturnObj()

        gwReturn.returnStatus = self.gwLibrary.GW2RegisterPoliciesFile(c_sessions_id, c_char_str, c_pol_buff)

        logging.warning("GW2RegisterPoliciesFile = {0}".format(gwReturn.returnStatus))

        return gwReturn

    def GW2RegisterPoliciesMemory(self, session):
        """Registers the policies in memory to be used bt Glasswall when processing files

        :param: policies: A pointer to the policies data
        :param: policies length: Specifies the size in bytes of the data"""

        # API function declaration
        self.gwLibrary.GW2RegisterPoliciesMemory.argtype = [
            ct.c_size_t,
            ct.c_char_p
        ]

        # Variable initialisation
        c_session_id = ct.c_size_t(session)
        pol = ct.c_char_p()
        pol_len = ct.c_size_t(0)
        pol_fmt = ct.c_int(0)

        # Return Object
        gwReturn = GwMemReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GW2RegisterPoliciesMemory(c_session_id, pol, pol_len, pol_fmt)
        logging.warning("GW2RegisterPoliciesMemory = {0}".format(gwReturn.returnStatus))

        gwReturn.Buffer = pol
        gwReturn.BufferLength = pol_len

        return gwReturn

    def GW2GetPolicySettings(self, session):
        """Retrieves policy settings used by Glasswall for the session

        :param: policiesBuffer: A pointer to an object containing a pointer to the information
        :param: A pointer to an object containing the size in bytes of the data
        :return: TODO
        :rtype: GwMemReturnObj"""

        self.gwLibrary.GW2GetPolicySettings.argtypes = [
            ct.c_size_t,
            ct.POINTER(ct.c_void_p),
        ]

        # Variable initialisation
        c_session_id = ct.c_size_t(session)
        policyBuffer = ct.c_void_p()
        policyBufferLength = ct.c_size_t(0)

        # Return Object
        gwReturn = GwMemReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GW2GetPolicySettings(c_session_id, ct.byref(policyBuffer), ct.byref(policyBufferLength))

        gwReturn.Buffer = policyBuffer
        gwReturn.BufferLength = policyBufferLength

        return gwReturn

    def GW2RegisterInputFile(self, session, inputFilePath):
        """Register an input file with the session

        :param: str inputFilePath: The file path to the file to be processed
        :rtype: GwStatusReturnObj """

        # API function declaration
        self.gwLibrary.GW2RegisterInputFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p
        ]

        # Variable initialisation
        c_session_id = ct.c_size_t(session)
        inputPath = ct.c_char_p(inputFilePath.encode("utf-8"))

        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GW2RegisterInputFile(c_session_id, inputPath)

        return gwReturn

    def GW2RegisterInputMemory(self, session, inputFileBuffer, inputFileBufferLength):
        """Registers the input file in memory

        :param: bytearray inputFileBuffer: The input buffer containing the file to be processed
        :param: intputFileBufferLength: length of the input file buffer data """

        # API function declaration
        self.gwLibrary.GW2RegisterInputMemory.argtypes = [
            ct.c_size_t,
            ct.c_char_p,
            ct.c_size_t
        ]

        # Variable initialisation
        c_session_id = ct.c_size_t(session)
        inputBuffer = ct.c_char_p(inputFileBuffer)
        inputBufferLength = ct.c_size_t(inputFileBufferLength)

        gwReturn = GwMemReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GW2RegisterInputMemory(c_session_id, inputBuffer, inputBufferLength)
        gwReturn.Buffer = inputBuffer
        gwReturn.BufferLength = inputBufferLength

        return gwReturn

    def GW2RegisterOutFile(self, session, outputFilePath):
        """ Register an output file location with the session (Where to store the output file)

        :param: str outputFilePath: the file path where the file containing the Glasswall output is placed
        :return: an output file from Glasswall
        :rtype: GwStatusReturnObj
        """

        # API function declaration
        self.gwLibrary.GW2RegisterOutFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p
        ]

        # Variable initialisation
        c_session_id = ct.c_size_t(session)
        outPath = ct.c_char_p(outputFilePath.encode("utf-8"))

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GW2RegisterOutFile(c_session_id, outPath)

        return gwReturn

    def GW2RegisterOutputMemory(self, session):
        """Registers a block of memory where the managed export content is to be placed.

        :param: """

        self.gwLibrary.GW2RegisterOutputMemory.argtypes = [
            ct.c_size_t,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        c_session_id = ct.c_size_t(session)
        outputBuffer = ct.c_void_p()
        outputBufferLength = ct.c_size_t(0)

        gwReturn = GwMemReturnObj()

        gwReturn.returnStatus = self.gwLibrary.GW2RegisterOutputMemory(c_session_id, ct.byref(outputBuffer),
                                                                       ct.byref(outputBufferLength))

        gwReturn.Buffer = outputBuffer
        gwReturn.BufferLength = outputBufferLength

        return gwReturn

    def GW2RegisterAnalysisFile(self, session, formatFilePath):

        self.gwLibrary.GW2RegisterAnalysisFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p,
            ct.c_int,
        ]

        c_session_id = ct.c_size_t(session)
        c_path_name = ct.c_char_p(formatFilePath.encode("utf-8"))
        c_ana_fmt = ct.c_int(0)

        analysis = self.gwLibrary.GW2RegisterAnalysisFile(c_session_id, c_path_name, c_ana_fmt)
        logging.warning("GW2RegisterAnalysisFile = {0}".format(analysis))

        return analysis

    def GW2RegisterAnalysisMemory(self, session):

        self.gwLibrary.GW2RegisterAnalysisMemory.argtypes = [
            ct.c_size_t,
            ct.POINTER(ct.c_void_p),
        ]

        c_session_id = ct.c_size_t(session)
        c_ana_file_buff = ct.c_void_p()
        c_ana_out_len = ct.c_size_t(0)

        gwReturn = GwMemReturnObj()

        gwReturn.status = self.gwLibrary.GW2RegisterAnalysisMemory(c_session_id, ct.byref(c_ana_file_buff), ct.byref(c_ana_out_len))
        logging.warning("GW2RegisterAnalysisMemory = {0}".format(gwReturn.status))

        gwReturn.Buffer = c_ana_file_buff
        gwReturn.BufferLength = c_ana_out_len

        return gwReturn

    def GW2RegisterImportFile(self, session, inputFilePath):
        """
            Register an input package file with the session
            (Where to find the (exported) package)
        """

        # API function declaration
        self.gwLibrary.GW2RegisterImportFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p
        ]

        # Variable initialisation
        c_session_id = ct.c_size_t(session)
        c_path = ct.c_char_p(inputFilePath.encode("utf-8"))

        # API Call
        impFile = self.gwLibrary.GW2RegisterImportFile(c_session_id, c_path)

        return impFile

    def GW2RegisterImportMemory(self, session, importBuffer, bufferLength):

        self.gwLibrary.GW2RegisterImportMemory.argtypes = [
            ct.c_size_t,
            ct.c_char_p,
        ]

        c_session_id = ct.c_size_t(session)
        c_imp_file_buff = ct.c_char_p(importBuffer)
        c_imp_len = ct.c_size_t(bufferLength)

        status = self.gwLibrary.GW2RegisterImportMemory(c_session_id, c_imp_file_buff, c_imp_len)
        logging.warning("GW2RegisterImportMemory =  {0}".format(status))

        # fileBuffer = (ct.c_byte * c_imp_file_buff.value)()
        # status.buffer = bytearray(fileBuffer)

        return status

    def GW2RegisterExportFile(self, session, exportFilePath):
        """
            Register an output export package location with the session
            (Where to store exported package)
        """

        # API function declaration
        self.gwLibrary.GW2RegisterExportFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p
        ]

        # Variable initialisation
        c_session_id = ct.c_size_t(session)
        c_outpath = ct.c_char_p(exportFilePath.encode("utf-8"))

        # API Call
        regExFile = self.gwLibrary.GW2RegisterExportFile(c_session_id, c_outpath)

        logging.warning("GW2RegisterExportFile = {0}".format(regExFile))

        return regExFile

    def GW2RegisterExportMemory(self, session):

        self.gwLibrary.GW2RegisterExportMemory.argtypes = [
            ct.c_size_t,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        c_session_id = ct.c_size_t(session)
        c_exp_file_buff = ct.c_void_p()
        c_exp_len = ct.c_size_t(0)

        gwReturn = GwMemReturnObj()

        gwReturn.returnStatus = self.gwLibrary.GW2RegisterExportMemory(c_session_id, ct.byref(c_exp_file_buff), ct.byref(c_exp_len))

        gwReturn.Buffer = c_exp_file_buff
        gwReturn.BufferLength = c_exp_len

        return gwReturn

    def GW2RegisterReportFile(self, session, reportFilePath):

        self.gwLibrary.GW2RegisterReportFile.argtypes = [
            ct.c_size_t,
            ct.c_char_p,
        ]

        c_session_id = ct.c_size_t(session)
        c_rep_file_path = ct.c_char_p(reportFilePath.encode("utf-8"))

        regExFile = self.gwLibrary.GW2RegisterReportFile(c_session_id, c_rep_file_path)
        logging.warning("GW2RegisterReportFile = {0}".format(regExFile))

        return regExFile

    def GW2RunSession(self, session):
        """
            Run the Glasswall session (start processing the file)
        """

        # API function declaration
        self.gwLibrary.GW2CloseSession.argtypes = [ct.c_size_t]

        # Variable initialisation
        c_session_id = ct.c_size_t(session)

        # API Call
        status = self.gwLibrary.GW2RunSession(c_session_id)
        logging.warning("GW2RunSession = {0}".format(status))

        return status

    def GW2GetIdInfo(self, session, issueID, bufferLength, outputBuffer):

        self.gwLibrary.GW2GetIdInfo.argtypes = [
            ct.c_size_t,
            ct.c_void_p,
        ]

        c_session_id = ct.c_size_t(session)
        c_iss_id = ct.c_size_t(issueID)
        c_buff_len = ct.c_size_t(bufferLength)
        c_out_buff = ct.c_void_p(outputBuffer)

        return self.gwLibrary.GW2GetIdInfo(c_session_id, c_iss_id, c_buff_len, c_out_buff)

    def GW2GetAllIdInfo(self, session, bufferLength, outputBuffer):

        self.gwLibrary.GW2GetAllIdInfo.argtypes = [
            ct.c_size_t,
            ct.c_void_p,
        ]

        c_session_id = ct.c_size_t(session)
        c_buff_len = ct.c_size_t(bufferLength)
        c_out_buff = ct.c_void_p(outputBuffer)

        return self.gwLibrary.GW2GetAllIdInfo(c_session_id, c_buff_len, c_out_buff)

    def GW2FileSessionStatus(self, session, glasswallSessionStatus, ):

        self.gwLibrary.GW2FileSessionStatus.argtypes = [
            ct.c_size_t,
            ct.c_uint,
        ]

        c_session_id = ct.c_size_t(session)
        c_gw_sesh_stat = ct.c_uint(glasswallSessionStatus)

        return self.gwLibrary.GW2FileSessionStatus(c_session_id, c_gw_sesh_stat)

    def GW2FileErrorMsg(self, session):

        self.gwLibrary.GW2FileErrorMsg.argtype = [
            ct.c_size_t]
        self.gwLibrary.GW2FileErrorMsg.restypes = [ct.POINTER(ct.c_void_p), ct.c_size_t]

        gwReturn = GwStringReturnObj

        c_session_id = ct.c_size_t(session)

        ct_string = self.gwLibrary.GW2FileErrorMsg(c_session_id)

        gwReturn.text = ct.string_at(ct_string)

        return gwReturn
