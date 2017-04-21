n = int(input('n: '))
x, y = 1, 1
for _ in range(n):
    print(x)
    x, y = y, x + y
