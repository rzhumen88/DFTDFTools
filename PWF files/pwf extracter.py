from PWF import PWFExtracter

def main():
    filename = input("What file do you want to extract?\n")
    pwf = PWFExtracter(filename)
    #pwf.print_info()
    pwf.extractWAV()
    
if __name__ == '__main__':
    main()
    input("Done!")
        
