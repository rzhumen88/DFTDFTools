import os

def txtToBin(filename):
    
    if not os.path.isfile(filename+"_data.txt"):
        print(filename+"_data.txt can't be found.")
        return 1
    if not os.path.isfile(filename+"_text.txt"):
        print(filename+"_text.txt can't be found.")
        return 1

    print("Parsing txt files...")
    with open(filename+"_text.txt", 'r') as data:
        data = data.read()
        unk_table = data.split("\n")[-1].split(", ")
        for i in range(len(unk_table)):
            unk_table[i] = int(unk_table[i])
        data = data.split("\n")[:-1]
        tkeyTableLen = (len(unk_table) * 4)
        
        for tkey in data:
            tkeyTableLen = tkeyTableLen + len(tkey) + 1 
        
        with open(filename+"_text.txt", 'r') as text:
            text = text.read()
            groups = []
            lines = []
            lines_len = [0, ]
            text = text.split("group=")[1:]
            tkeyTablePointer = 19
            pointer = 0
            for line in text:
                line = line.split(", ", 1)
                tkeyTablePointer = tkeyTablePointer + 16
                groups.append(line[0])
                lines.append(line[1])
                pointer = pointer + len(line[1])
                lines_len.append(pointer)
            for line in range(len(text)):
                text[line] = text[line].split(", ", 1)[1].replace("\n", "")
                tkeyTablePointer = tkeyTablePointer + len(text[line]) + 1

    totalLines = len(lines)
    print(totalLines+" lines found.")
    
    with open(filename+".BIN", "wb") as binfile:
        print("Creating .bin file...")
        binfile.write(b'RTXT')
        binfile.write(int.to_bytes(tkeyTablePointer, 4, byteorder='little'))
        binfile.write(int.to_bytes(tkeyTableLen, 4, byteorder='little'))
        binfile.write(int.to_bytes(totalLines, 4, byteorder='little'))
        for i in range(totalLines):
             binfile.write(int.to_bytes(lines_len[i], 4, byteorder='little'))
             binfile.write(b'\x00'*4)
             binfile.write(int.to_bytes(int(groups[i]), 4, byteorder='little'))
             binfile.write(b'\x00'*4)
        for line in text:
            binfile.write(line.encode('ANSI')+b'\x00')
        binfile.write(b'\x00'*3)
        binfile.write(int.to_bytes(len(unk_table)//2, 4, byteorder='little'))
        for v in unk_table:
            binfile.write(int.to_bytes(v, 4, byteorder='little'))
        for line in data:
            binfile.write(line.encode('ANSI')+b'\x00')
            
if __name__ == '__main__':
    inp_ = input("Input txt file names. Example: for myfile_data.txt and myfile_text.txt type 'myfile': ")
    txtToBin(inp_)
    input("Done!")
