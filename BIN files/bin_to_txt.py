import os

def binToTxt(filename):
    
    with open(filename, 'rb') as f:
        f = f.read()
        if f[:4] != b'RTXT':
            print("Error: Wrong File Header")
            return 1
        
        tkeyTablePointer = int.from_bytes(f[4:8], byteorder='little')
        unkTableLen = int.from_bytes(f[tkeyTablePointer : tkeyTablePointer+4], byteorder='little') * 2
        unkValues = []
        tkeyTableLen = int.from_bytes(f[8:12], byteorder='little')
        linesTotal = int.from_bytes(f[12:16], byteorder='little')
        lines = []
        tkeyTxt = []
        tkey = ''
        line = ''
        binTkey = f[tkeyTablePointer+4+(unkTableLen*4):]
        binTxt = f[16+(linesTotal*16):-len(binTkey)]
        datafile = filename.replace(".BIN", "_DATA.TXT")
        textfile = filename.replace(".BIN", "_TEXT.TXT")
        datafile = open(datafile, 'w')
        textfile = open(textfile, 'w')
        
        for b in binTkey:
            if not b == 0:
                tkey = tkey + b.to_bytes(1, byteorder='little').decode('ANSI')
            else:
                tkeyTxt.append(tkey)
                tkey = ''

        binTkey = None
        datafile.write('\n'.join(tkeyTxt))
        datafile.write('\n')
        
        for line in range(0, linesTotal):
            pointer = int.from_bytes(f[16+(line*16):20+(line*16)], byteorder='little')
            group = int.from_bytes(f[16+8+(line*16):20+8+(line*16)], byteorder='little')
            i = 0
            line = ''
            while True:
                if binTxt[pointer+i] == 0:
                    textfile.write("group="+str(group)+", "+line+'\n')
                    break
                line = line + binTxt[pointer+i].to_bytes(1, byteorder='little').decode('ANSI')
                i += 1

        for value in range(0, unkTableLen):
            value = int.from_bytes(f[tkeyTablePointer+4+(value*4):tkeyTablePointer+4+(value*4)+4], byteorder='little')
            unkValues.append(str(value))

        datafile.write(", ".join(unkValues))
        
        datafile.close()
        textfile.close()

if __name__ == '__main__':
    input_ = input("Enter path to .bin file: ")
    binToTxt(input_)
    input("Done!")

  
