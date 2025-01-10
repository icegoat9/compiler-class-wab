# original source: tests/factre.wb
# created by gen_python.py (work in progress)
def factre(x, n):
    if (x == n):
        return n
    else:
        return (x * factre((x + 1), n))
    return 0

def fact(n):
    if (0 < n):
        return factre(1, n)
    else:
        return 1
    return 0

def main():
    x = 1
    while (x < 10):
        print(fact(x))
        x = (x + 1)
    return 0

if __name__ == "__main__":
    main()
