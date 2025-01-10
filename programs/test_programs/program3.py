# original source: tests/program3.wb
# created by gen_python.py (work in progress)
def main():
    result = 1
    x = 1
    while (x < 10):
        result = (result * x)
        x = (x + 1)
    print(result)
    return 0

if __name__ == "__main__":
    main()
