from PWF import PWFBuilder

def main():
    foldername = input("What folder do you want to build into container?\n")
    pwf = PWFBuilder(foldername)
    pwf.buildWAV()
            
if __name__ == '__main__':
    main()
    input("Done!")
        
