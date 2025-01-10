# original source: programs/pow.wb
# created by gen_python.py (work in progress)
def pow(x, n):
    out = 1
    i = 0
    while (i < n):
        out = (out * x)
        i = (i + 1)
    return out

def main():
    x = pow(3, 4)
    print(x)
    return 0

if __name__ == "__main__":
    main()
