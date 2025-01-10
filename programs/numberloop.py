# original source: programs/numberloop.wb
# created by gen_python.py (work in progress)
def mod(x, n):
    d = (x // n)
    return (x - (d * n))

def pow(x, n):
    out = 1
    i = 0
    while (i < n):
        out = (out * x)
        i = (i + 1)
    return out

def lennum(num):
    i = 1
    scale = 10
    while (scale < (num + 1)):
        scale = (scale * 10)
        i = (i + 1)
    return i

def concat(a, b):
    scale = pow(10, lennum(b))
    return ((scale * a) + b)

def digitn(num, n):
    x = pow(10, n)
    return ((mod(num, x) - mod(num, (x // 10))) // (x // 10))

def mergedigits(n):
    len = lennum(n)
    i = 1
    out = 0
    if (len == 1):
        return n
    else:
        pass
    while (i < len):
        right = digitn(n, i)
        left = digitn(n, (i + 1))
        sum = (left + right)
        if (i == 1):
            out = sum
        else:
            out = concat(sum, out)
        i = (i + 1)
    return out

def mergeloop(n):
    if (n < 0):
        return -1
    else:
        pass
    prev = 0
    endloop = 0
    loops = 0
    while (endloop == 0):
        print(n)
        prev = n
        n = mergedigits(n)
        loops = (loops + 1)
        if (prev == n):
            endloop = 1
        else:
            len = lennum(n)
            if (len >= 8):
                endloop = 2
            else:
                if (loops > 20):
                    endloop = 3
                else:
                    endloop = 0
    return endloop

def main():
    runtests = 0
    if (runtests != 0):
        print(pow(2, 5))
        print(pow(3, 1))
        print(mod(13, 3))
        print(concat(12, 345))
        print(lennum(9))
        print(lennum(10))
        xa = 123456
        print(123456)
        print(lennum(xa))
        print(digitn(xa, 1))
        print(digitn(xa, 5))
        x = 4396
        print(x)
        print(mergedigits(x))
        print(mergedigits(7))
    else:
        print(mergeloop(1467))
        print(mergeloop(1792))
        print(mergeloop(1537))
    return 0

if __name__ == "__main__":
    main()
