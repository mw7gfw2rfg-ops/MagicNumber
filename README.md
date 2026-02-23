# Magic Number Identifier

A command-line tool that identifies file types by reading and comparing their magic number (file header bytes) against a database of known file signatures. Unlike relying on file extensions — which can be renamed or spoofed — this tool inspects the raw binary content of a file to determine its true type.

## How it works

Every file format has a unique sequence of bytes at the start of the file known as a **magic number** or **file signature**. For example, a Windows executable always begins with `4D 5A` (MZ), and a PNG image begins with `89 50 4E 47`. This tool reads the first 512 bytes of a file, converts them to hexadecimal, and compares them against a JSON database of known signatures to identify the file's true format.

## Features

- 🔍 Identifies file types by magic number, not file extension
- 📁 Supports scanning individual files or entire directory trees recursively
- 🖨️ Optional verbose mode to display the raw hex header
- 📤 JSON output mode for integration with other tools or scripts
- 🗂️ Easily extensible signature database via `FileSig.json`

## Requirements

- Python 3.10+
- No external dependencies — uses only the Python standard library

## Installation

Clone the repository:

```bash
git clone https://github.com/mw7gfw2rfg-ops/MagicNumber.git
cd MagicNumber
```

No installation or `pip install` is required.

## Usage

### Scan a single file

```bash
python FileHeader.py --file yourfile.png
```

### Scan multiple files

```bash
python FileHeader.py --file file1.pdf file2.exe file3.jpg
```

### Scan an entire directory recursively

```bash
python FileHeader.py --dir /path/to/directory
```

### Enable verbose output (shows raw hex header)

```bash
python FileHeader.py --file yourfile --verbose
```

### Output results as JSON

```bash
python FileHeader.py --file yourfile --json
```

### Combine flags

```bash
python FileHeader.py --dir /path/to/directory --verbose --json
```

## Example output

Standard output:
```
File: document.pdf - PDF, Portable Document Format
-=-=-=-=-=-=
File: archive.zip - ZIP, ZIP compressed archive
-=-=-=-=-=-=
```

Verbose output:
```
Header: 25 50 44 46 2D 31 2E 34 20 0A 25 E2 E3 CF D3 0A
File: document.pdf - PDF, Portable Document Format
-=-=-=-=-=-=
```

JSON output:
```json
[
  {
    "extension": "PDF",
    "header": "25 50 44 46",
    "description": "Portable Document Format"
  },
  {
    "extension": "ZIP",
    "header": "50 4B 03 04",
    "description": "ZIP compressed archive"
  }
]
```

## Signature database

Signatures are stored in `FileSig.json` in the following format:

```json
{
  "signatures": [
    {
      "extension": "PNG",
      "header": "89 50 4E 47 0D 0A 1A 0A",
      "description": "Portable Network Graphic"
    },
    {
      "extension": "PDF",
      "header": "25 50 44 46",
      "description": "Portable Document Format"
    }
  ]
}
```

You can add your own signatures by appending entries to this file. The more specific (longer) the header, the more accurate the match — shorter signatures are more prone to false positives.

## Arguments

| Argument | Description |
|---|---|
| `--file` | One or more file paths to scan |
| `--dir` | A directory path to scan recursively |
| `--verbose` | Print the first 16 bytes of the file header |
| `--json` | Output results as a JSON array |

Either `--file` or `--dir` must be provided.

## Known limitations

- Signature matching is based on the start of the file only — embedded file types (e.g. a ZIP inside a DOCX) won't be detected
- The accuracy of identification depends entirely on the completeness of `FileSig.json`
- Very short signatures (2–4 bytes) may occasionally produce false positives if the signature appears at the start of an unrelated format

## Contributing

Contributions are welcome, particularly additions to the signature database. Please open an issue or submit a pull request.
