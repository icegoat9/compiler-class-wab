# this program generated from Wab AST by gen_python.py (work in progress)
def main():
    x = 1
    if (x > 2):
        print(99)
    else:
        if (x == 2):
            print(2)
        else:
            if (x == 1):
                print(1)
            else:
                print(0)
    return 0

if __name__ == "__main__":
    main()
