import os

def cbinDecrypt(filename):
    newFile = []
    with open(filename, 'rb') as f:
        f =  f.read()
        if f[:4] != b'CBIN':
            input("Wrong header")
            return 1
        newFile.append(f[:16])
        f = f[16:]
        max_int = 4294967295
        nor = max_int
        i = 0
        for int32 in range(0, len(f), 4):
            i += 1
            int32 = int.from_bytes(f[int32 : int32+4])
            int32 = int32 ^ i + int32
            if int32 > max_int:
                int32 = int32 - max_int
            if int32 < 0:
                int32 = int32 + max_int
            newFile.append(int32.to_bytes(4, byteorder='little'))

        with open(filename, 'wb') as f:
            for e in newFile:
                f.write(e)
            input("Done!")
            
if __name__ == '__main__':
    filename = input("Input path to CBIN file: ")
    if os.path.isfile(filename):
        cbinDecrypt(filename)
    else:
        input("File does not exist.")
    
