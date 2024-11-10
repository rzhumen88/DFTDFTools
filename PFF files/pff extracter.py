import os

def bToKb(b):
    return str(b/1000)[:5]+"kb"

def main():
    #deffile = "small.pff"
    #deffolder = "small"
    deffile = input("Input pff file name:\t")
    if not os.path.isfile(deffile):
        input("File does not exist")
        return 1
    deffolder = deffile.replace(".pff","")
    if not os.path.isdir(deffolder):
        os.mkdir(deffolder)
    with open(deffile, "rb") as f:
        f = f.read()
        filesOffset = int.from_bytes(f[:4], byteorder="little")
        header = f[4:8]
        if header != b"PFF3":
            input("not supported PFF3 file")
            return 1
        crcfile = open(deffolder+"/"+"CRC", "wb")
        fileorder = open(deffolder+"/"+"FILEORDER", "w")
        totalFiles = int.from_bytes(f[8:12], byteorder="little")
        pffFormat = int.from_bytes(f[12:16], byteorder="little")
        dirOffset = int.from_bytes(f[16:20], byteorder="little")
        print(f"{deffile} recognized! Version {pffFormat} | {totalFiles} files inside.")
        for file in range(totalFiles):
            dummy = int.from_bytes(f[dirOffset+36*file+0:dirOffset+36*file+4], byteorder="little")
            offset = int.from_bytes(f[dirOffset+36*file+4:dirOffset+36*file+8], byteorder="little")
            size = int.from_bytes(f[dirOffset+36*file+8:dirOffset+36*file+12], byteorder="little")
            sizeInKb = bToKb(size)
            dummy = int.from_bytes(f[dirOffset+36*file+8:dirOffset+36*file+12], byteorder="little")
            crc = f[dirOffset+36*file+12:dirOffset+36*file+16]
            bytestr = f[dirOffset+36*file+16:dirOffset+36*file+32]
            filename = bytestr.replace(b'\x00', b'').decode('ANSI')
            with open(deffolder+"/"+filename, "wb") as f2:
                f2.write(f[offset:offset+size])
                crcfile.write(crc)
                fileorder.write(filename+"\n")
                print(f"{filename} extracted! Size {sizeInKb} | CRC = {crc}.")
        crcfile.close()
        fileorder.close()
        input("Done!")
        return 0
if  __name__ == "__main__":
    main()
