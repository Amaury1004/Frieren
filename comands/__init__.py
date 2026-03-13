arr = list(range(1, 21))  

for i in range(len(arr)):
    num = arr[i]

    low = num & 0xFFFF
    high = (num >> 16) & 0xFFFF

    arr[i] = high + low

print(arr)