# original source: tests/program4.wb
# created by gen_python.py (work in progress)
def add1(x):
    x = (x + 1)
    return x

def main():
    x = 10
    print((1035 + add1(x)))
    print(x)
    return 0

if __name__ == "__main__":
    main()
