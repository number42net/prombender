# PromBender

![logo](https://raw.githubusercontent.com/number42net/prombender/main/images/mini.png)

Bend programmable ROM images to your will using PromBender! 

+ Combine and split ROM images, either in sequence or in odd / even pairs
+ Concatenate images to fill a ROM of a specfic size
+ Pad your own images with any value to fill a ROM of a specific size

## Requirements

+ Windows / Linux / Unix / MacOS
+ Python 3.6
+ Pip (for installation)

## Installation

The easiest way to install PromBender is by using pip:

```
pip3 install git+https://github.com/number42net/prombender.git
```

## Usage

### Combine
Combine two or more files into a single ROM, either in sequence or in odd / even order.

```
usage: prombender combine --out FILE [--in FILE [FILE ...]] [--even FILE] [--odd FILE]

required arguments:
  --out FILE            Output file

required arguments for regular combine:
  --in FILE [FILE ...]  List of files to combine

required arguments for odd / even combine:
  --even FILE           Source file with even bytes
  --odd FILE            Source file with odd bytes
```
### Split
Split a single file into multiple ROMs, either in sequence or in an odd / even order.
```
usage: prombender split --in FILE [--out PATTERN] [--count NUMBER] [--even FILE] [--odd FILE]

required arguments:
  --in FILE       Input file
  --out PATTERN   Output file pattern. Example: output.bin will result in output-1.bin, output-2.bin, etc.

optional arguments for regular split:
  --count NUMBER  Number of files to split the ROM into

required arguments for odd / even split:
  --even FILE     Source file with even bytes
  --odd FILE      Source file with odd bytes
```
### Concatenate
Concatenate a single file multiple times to fill a larger ROM.
```
usage: prombender concatenate --in FILE --out FILE [--kbits KILO_BITS | --copies NUMBER]

required arguments:
  --in FILE          Input file
  --out FILE         Output file

optional arguments:
  --kbits KILO_BITS  Final size in kilobits. Example: for a 27C256 EPROM, set this to 256
  --copies NUMBER    Number of copies to make. Example: to fill a 256k EPROM with a 64k file set this to 4
```
### Pad
Add padding to a file to create a ROM of a specific size.
```
usage: prombender pad --in FILE --out FILE --kbits INTEGER [--hex HEX | --dec INTEGER] [--bottom | --top]

required arguments:
  --in FILE        Input file
  --out FILE       Output file
  --kbits INTEGER  Final size in kbits

optional arguments:
  --hex HEX        Use the hex value for padding
  --dec INTEGER    Use the decimal value for padding
  --bottom         Pad the bottom, data stays at the beginning of the file
  --top            Pad the top, data moves to the end of the file
```
