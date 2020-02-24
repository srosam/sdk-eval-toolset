import argparse
import sys


def argParser(parser):
    # Parser command line arguments

    parser.parse_args()
    args = parser.parse_args()

    if str(args.InputDirectory) != 'None':
        input_location = str(args.InputDirectory)
    else:
        print("No input directory given.\n")
        parser.print_help()
        sys.exit()

    if str(args.OutputDirectory) != 'None':
        output_location = str(args.OutputDirectory)
    else:
        print("No output directory given.\n")
        parser.print_help()
        sys.exit()

    if str(args.PathToConfig) != 'None':
        path_to_config = str(args.PathToConfig)
    else:
        print("Path to the Config file was not specified.\n")
        parser.print_help()
        sys.exit()

    if str(args.PathToLib) != 'None':
        path_to_lib = str(args.PathToLib)
    else:
        print("Path to the report File was not specified.\n")
        parser.print_help()
        sys.exit()

    return input_location, output_location, path_to_config, path_to_lib


def getCommandLineArgs():
    # Command Line Help Options

    parser = argparse.ArgumentParser()

    parser.add_argument("-i,", dest="InputDirectory", help="[Required] Input directory.", type=str)
    parser.add_argument("-o,", dest="OutputDirectory", help="[Required] Directory to store output packages.", type=str)
    parser.add_argument("-c,", dest="PathToConfig", help="[Required] Full path to Log folder.", type=str)
    parser.add_argument("-l", dest="PathToLib", help="[Required] Full path to core2 library.", type=str)

    return argParser(parser)