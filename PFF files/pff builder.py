import os

def main(deffile):
    filesOffset = 20
    pffFormat = 36
    fileEnd = b'C0\xA8\x00\x03\x00\x00\x00\x00\x4B\x49\x4E\x47'
    deffolder = deffile.replace(".PFF","")
    deffile = deffile + ".PFF"
    if not os.path.isfile(deffolder+"/"+"FILEORDER") or not os.path.isfile(deffolder+"/"+"CRC"):
        input("Files FILEORDER or CRC cannot be found in the folder, archive cannot be created.")
        return 1
    fileorder = open(deffolder+"/"+"FILEORDER", "r")
    fileorder = fileorder.read().splitlines()
    size = filesOffset
    sizeList = []
    offsetCounter = filesOffset
    offsetList = [filesOffset, ]
    for file in fileorder:
        with open(deffolder+"/"+file, "rb") as f2:
            f2 = f2.read()
            size = size + len(f2)
            sizeList.append(len(f2))
            offsetCounter = offsetCounter + len(f2)
            offsetList.append(offsetCounter)
    crcfile = open(deffolder+"/"+"CRC", "rb")
    crcfile = crcfile.read()
    with open(deffile, 'wb') as f:
        f.write(int.to_bytes(filesOffset, 4, byteorder="little"))
        f.write(b"PFF3")
        f.write(int.to_bytes(len(fileorder), 4, byteorder="little"))
        f.write(int.to_bytes(pffFormat, 4, byteorder="little"))
        f.write(int.to_bytes(size, 4, byteorder="little"))
        counterCRC = 0
        counterFile = 0
        for file in fileorder:
            with open(deffolder+"/"+file, "rb") as f2:
                f2 = f2.read()
                f.write(f2)
        for file in fileorder:
            f.write(b"\x00"*4)
            f.write(int.to_bytes(offsetList[counterFile], 4, byteorder="little"))
            f.write(int.to_bytes(sizeList[counterFile], 4, byteorder="little"))
            f.write(crcfile[counterCRC:counterCRC+4])
            counterCRC = counterCRC+4
            f.write(bytes(fileorder[counterFile],'ANSI')+b'\x00'*(16 - len(fileorder[counterFile])))
            f.write(b"\x00"*4)
            print(f"Imported: {file} Size: {sizeList[counterFile]} Offset: {offsetList[counterFile]}")
            counterFile = counterFile + 1
        f.write(fileEnd)
    print(f"Files imported: {counterFile}")
    
if  __name__ == "__main__":
    folder = ''
    while not os.path.isdir(folder):
        folder = input('Enter path to pack into PFF file:  ')
    main(folder)
    input("Done!")
