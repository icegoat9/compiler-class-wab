# original source: tests/fact.wb
# created by gen_python.py (work in progress)
def fact(n):
    if (n < 2):
        return 1
    else:
        x = 1
        result = 1
        while (x < n):
            result = (result * x)
            x = (x + 1)
        return (result * n)
    return 0

def main():
    x = 1
    while (x < 10):
        print(fact(x))
        x = (x + 1)
    return 0

if __name__ == "__main__":
    main()
