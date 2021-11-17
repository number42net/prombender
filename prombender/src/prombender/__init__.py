def pad(in_file, out_file, kbits, top=False, bottom=False, hex_val=False, dec_val=False):
    # Check top and bottom
    if top and bottom:
        raise ValueError("bottom cannot be combined with top")
    if hex_val and dec_val:
        raise ValueError("hex cannot be combined with dec")

    if not top and not bottom:
        bottom = True
    
    # Check hex and dec val
    if not hex_val and not dec_val:
        dec_val = 0
    elif hex_val:
        dec_val = int(hex_val, base=16)

    # Read file check size
    data = in_file.read()
    if len(data) >= kbits / 8 * 1024:
        raise ValueError(f"File size {len(data) * 8 / 1024} already equal to or greater than kbits: {kbits}")

    output = bytearray()

    if bottom:
        output = bytearray(data)

    for i in range(int(kbits / 8 * 1024  - len(data))):
        output.append(dec_val)

    if top:
        output = output + data

    out_file.write(output)

def combine(out_file, in_files=False, even_file=False, odd_file=False):
    if in_files and (even_file or odd_file):
        raise ValueError("in_files cannot be combined with even_file or odd_file")
    elif in_files:
        for file in in_files:
            out_file.write(file.read())
            file.close()
        out_file.close()
        return
    elif not in_files and not even_file and not odd_file:
        raise ValueError("Either in_file or even_file and odd_file need to be specified")
    elif not (even_file and odd_file):
        raise ValueError("both even_file and odd_file are required to do odd / even combine")

    # Add odd and even files
    file1 = even_file.read()
    file2 = odd_file.read()
    file3 = bytearray()

    for i in range(len(file1)):
        file3.append(file1[i])
        file3.append(file2[i])

    out_file.write(file3)

    # Close files and present result
    odd_file.close()
    even_file.close()
    out_file.close()

def split(in_file, out_file=False, count=2, odd_file=False, even_file=False):
    if not count:
        count = 2

    if out_file and (odd_file or even_file):
        raise ValueError("out_files cannot be combined with even_file or odd_file")
    elif not out_file and not odd_file and not even_file:
        raise ValueError("Use either out_files for regular split or even_file and odd_file for even / odd split")

    # Regular split
    elif out_file:
        data = in_file.read()
        if not len(data) % count == 0:
            raise ValueError(f"File size: {len(data)} bytes is not devisable by count: {count}")

        # Create file name template
        if "." in out_file:
            file_start = ".".join(out_file.split(".")[:-1])
            file_end = out_file.split(".")[-1]
        else:
            file_start = out_file
            file_end = ""

        for i in range(count):
            filename = f"{file_start}_{i+1}.{file_end}"
            start = int(i * (len(data) / count))
            end = int((i + 1) * (len(data) / count))
            with open(filename, "wb") as file:
                file.write(data[start:end])

        return
    
    # odd / even split
    elif not out_file and not (odd_file and even_file):
        raise ValueError("even_file and odd_file are required for even / odd split")

    data = in_file.read()
    odd = data[1::2] # Elements from data starting from 1 iterating by 2
    even = data[::2] # Elements from data starting from 0 iterating by 2

    odd_file.write(odd)
    even_file.write(even)

    # Close files and present result
    odd_file.close()
    even_file.close()
    in_file.close()

def concatenate(in_file, out_file, kbits=False, copies=False):
    # Do not allow specifying both kbits and copies
    if kbits and copies:
        raise ValueError("Both kbits or copies specified")
    # If neither kbits or copies was specified, default to 2 copies
    elif not copies and not kbits:
        copies = 2
    
    data = in_file.read()
    
    # Ensure kbits is devisable by data size
    if kbits and not kbits * 1024 % (len(data)*8) == 0:
        raise ValueError(
            f"kbits specified: {kbits * 1024} bits is not devisable by size of input file: {len(data) * 8} bits.")
    # If kbits was specified, convert to copies
    elif kbits:
        copies = int(1024 * kbits / (len(data) * 8))

    for _ in range(copies):
        out_file.write(data)

    # Close files and report result
    in_file.close()
    out_file.close()