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
    filesToScan = []

    if args.dir:
        for root, dirs, files in os.walk(dir, topdown=False):
            for name in files:
                filesToScan.append(os.path.join(root, name))
    elif args.file:
        filesToScan = file
    else:
        parser.error("Please provide either --file or --dir")


    for f in filesToScan:
        header = readFileHeader(f)
        data = compareHeader(signatures, header)
        if args.verbose:
            print(f'Header: {header[:47]}')
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(f'File: {f} - {data['extension']}, {data['description']}')
        if not args.json:
            print('-=-=-=-=-=-=')