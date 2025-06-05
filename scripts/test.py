def factorial(n):
    for i in range(1, int(n) + 1):
        print("esse eh i:",i)
        if i == 1:
            result = 1
        else:
            result = result * i

    return result

print("insira seu numero")
n = input()
print(factorial(n))