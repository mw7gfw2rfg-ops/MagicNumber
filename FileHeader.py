import json
import sys
import argparse
import os

def readFileHeader(file, num_bytes=512):
    try:
        with open(file, 'rb') as f:
            file_head = f.read(num_bytes)
            file_headHex = file_head.hex().upper()
    except (FileNotFoundError):
        print("File not Found")
        sys.exit()
    except (PermissionError):
        print("Permission Error")
        sys.exit()

    return ' '.join(file_headHex[i:i+2] for i in range(0, len(file_headHex), 2))

def loadSignatures(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)['signatures']
    except (FileNotFoundError):
        print('File Not Found')
        sys.exit()

def compareHeader(signatures, header):
    for signature in signatures:
        if header.startswith(signature['header']):
            return signature
    
    return {'extension': "Unknown", 'header': "Unknown", 'description': "unknown"}

def collectFiles(args):
    if args.dir:
        files = []
        for root, dirs, filenames in os.walk(dir, topdown=False):
            for name in filenames:
                files.append(os.path.join(root, name))
        return files
    elif args.file:
        return args.file
    else:
        return None
    
def printResult(f, data, args):
    if args.verbose:
        header = readFileHeader(f)
        print(f'Header: {header[:47]}')
    elif args.json:
        print(json.dumps(data, 2))
    else:
        print('-=-=-=-=-=-=-=-=')
        print(f'File {f} - {data['extension']}, {data['description']}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Script that compare the Magic Number File Header to a dictionary of known file headers"
    )
    parser.add_argument("--file", nargs='+')
    parser.add_argument("--dir")
    parser.add_argument("--verbose", action='store_true')
    parser.add_argument("--json", action='store_true')
    args = parser.parse_args()
    dir = args.dir
    file = args.file

    signatures = loadSignatures('FileSig.json')

    filesToScan = collectFiles(args)

    if not filesToScan:
        parser.error("Please provide either --file or --dir")

    
        
    for f in filesToScan:
        data = compareHeader(signatures, readFileHeader(f))
        printResult(f, data, args)