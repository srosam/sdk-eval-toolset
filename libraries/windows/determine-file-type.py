

def get_args():

    from os import path
    import sys

    program_name = sys.argv[0]
    print("Program: {0} v0.1\n".format(
            path.basename(
                path.splitext(program_name)[0])
        )
    )

    arguments = sys.argv[1:]
    count = len(arguments)

    if not count:
        print("Example Usage: {0} <directoryPath> <pathToGlasswallEngine>".format(
            path.basename(program_name))
        )
        sys.exit(-1)
        
    print (arguments)

    return path.abspath(arguments[0]), path.abspath(arguments[1])


def load_glasswall(path_to_engine):

    from Glasswall import Interface_GwCore2

    print("Loading Library")

    gw = Interface_GwCore2(path_to_engine)

    print("Done")

    return gw


def lookup_file_type(key):
    return {
        16 : "PDF",     17 : "DOC",     18 : "DOCX",
        19 : "PPT",     20 : "PPTX",    21 : "XLS",
        22 : "XLSX",    23 : "PNG",     24 : "JPEG",
        25 : "GIF",     26 : "EMF",     27 : "WMF",
        28 : "RTF",     29 : "BMP",     30 : "TIFF",
        31 : "PE",      32 : "MACH-O",  33 : "ELF",
        34 : "MP4",     35 : "MP3",     36 : "MP2",
        37 : "WAV",     38 : "MPG",     39 : "COFF",
        40 : "JSON"
    }.get(key)

def gw_determine_file_type(gw, file_path):

    ftype_enum = gw.GW2DetermineFileTypeFromFile(file_path).enumValue

    if ftype_enum:
        ftype_str = lookup_file_type(ftype_enum)
        return ftype_enum, ftype_str

    return None


def main():
    input_directory, gw_lib_path = get_args()
    from os import walk, path

    gw = load_glasswall(gw_lib_path)

    for root, dirs, files in walk(input_directory):
        for name in files:
            file_path = path.join(root, name)
            print("File Path {0}".format(file_path))
            result = gw_determine_file_type(gw, file_path)
            if result is None:
                print("\tFile type enum value is 0 and file type is UNKNOWN")
            else:
                print("\tFile type enum value is {0} and file type is {1}".format(
                    result[0], result[1]))


if __name__ == "__main__":
    main()
