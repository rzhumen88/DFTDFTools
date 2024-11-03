import os
import wave

class PWFExtracter():
    
    tableLen = 52
    headerLen = 20
    
    def __init__(self, filename):
        
        with open(filename, 'rb') as file:
            self.file = file.read()
            self.filename = filename.split("/")[-1]
            self.folder = self.filename[:-4]
            self.version = int.from_bytes(self.file[0:4], byteorder='little')
            self.header = self.file[4:8]
            self.n_files = int.from_bytes(self.file[8:12], byteorder='little')
            self.containerLength = int.from_bytes(self.file[16:20], byteorder='little')
            self.fileNames = []
            self.offsets = []
            self.lengths = []
            for f in range(0, self.n_files):
                self.fileNames.append(self.file[8+self.headerLen+(self.tableLen*f):8+self.headerLen+(self.tableLen*f)+24].replace(b'\x00', b'').decode('ANSI'))
                self.offsets.append(int.from_bytes(self.file[32+self.headerLen+(self.tableLen*f):36+self.headerLen+(self.tableLen*f)], byteorder='little'))
                self.lengths.append(int.from_bytes(self.file[36+self.headerLen+(self.tableLen*f):40+self.headerLen+(self.tableLen*f)], byteorder='little')-28)

    def print_info(self):
        
        print(f"Filename: {self.filename}")
        print(f"Header: {self.header.decode('ANSI')}")
        print(f"Version: {self.version}")
        print(f"Files inside: {self.n_files}")
        print(f"Size: {self.containerLength+20}")

    def extractRaw(self):
        
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
            
        for f in range(0, self.n_files):
            with open(self.folder + "/" + self.fileNames[f]+".samp", 'wb') as samp:
                samp.write(self.file[self.offsets[f]:self.offsets[f]+self.lengths[f]])
                print(f"Extracted: {self.fileNames[f]} | Size: {self.lengths[f]}")

    def extractWAV(self):

        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
            
        for f in range(0, self.n_files):
            with wave.open(self.folder + "/" + self.fileNames[f]+".wav", 'wb') as wav:
                wav.setnchannels(1)
                wav.setsampwidth(1)
                wav.setframerate(22050.0)
                wav.writeframesraw(self.file[self.offsets[f]+16:self.offsets[f]+self.lengths[f]])
                print(f"Extracted: {self.fileNames[f]} | Size: {self.lengths[f]}")


class PWFBuilder():
    
    tableLen = 52
    headerLen = 20
    
    def __init__(self, folderName):
        
        self.folderName = folderName
        self.version = 28
        self.header = b'PWF2'
        self.fileNames = []
        self.fileNamesNoExt = []
        
        for file in os.listdir(folderName):
            if file.endswith(".wav"):
                self.fileNames.append(file)
                self.fileNamesNoExt.append(file.replace(".wav", ""))
                
        self.lengths = []
        self.offsets = []

        self.n_files = len(self.fileNames)
        self.tableLen = (self.tableLen*self.n_files) + self.headerLen + 8
        self.offset = self.tableLen
        self.containerLength = self.tableLen
        print(self.tableLen)
        self.offsets.insert(0, self.tableLen)
        
        for files in self.fileNames:
            with wave.open(folderName + "/" + files, 'rb') as self.f:
                (self.nchannels, self.sampwidth, self.framerate, self.nframes, self.comptype, self.compname) = self.f.getparams()
                self.audioData = self.f.readframes(self.nframes)
                self.audioSize = len(self.audioData) + 16
                self.containerLength += self.audioSize
                self.offset = self.offset + self.audioSize
                self.offsets.append(self.offset)
                self.lengths.append(self.audioSize)   
        
    def buildWAV(self):
        with open(self.folderName+".PWF", "wb") as f:
            
            f.write(int.to_bytes(self.version, 4, byteorder='little'))
            f.write(self.header)
            f.write(int.to_bytes(self.n_files, 4, byteorder='little'))
            f.write(b'\x00'*4)
            f.write(int.to_bytes(self.containerLength - self.headerLen, 4, byteorder='little'))

            for file in range(0, self.n_files):
                f.write(b'\x00'*8)
                f.write(bytes(self.fileNamesNoExt[file],'ANSI')+b'\x00'*(24 - len(self.fileNamesNoExt[file])))
                f.write(int.to_bytes(self.offsets[file], 4, byteorder='little'))
                f.write(int.to_bytes(self.lengths[file], 4, byteorder='little'))
                f.write(b'\x00\xBE')
                f.write(b'\x00'*10)

            f.write(b'\x00'*8)

            for file in self.fileNames:
                with wave.open(self.folderName + "/" + file, 'rb') as self.wav:
                    (self.nchannels, self.sampwidth, self.framerate, self.nframes, self.comptype, self.compname) = self.wav.getparams()
                    self.audioData = self.wav.readframes(self.nframes)
                    f.write(b'SAMP')
                    f.write(int.to_bytes(len(self.audioData)+16, 4, byteorder='little'))
                    f.write(b'\x00\x00\x00\x10\x00\x01\x74\x20')
                    f.write(self.audioData)
                    print(f'Imported: {file} | Size {len(self.audioData)}')

