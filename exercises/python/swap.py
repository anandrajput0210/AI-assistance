# a=int(input("Enter first number: "))
# b=int(input("Enter second number: "))
# print("Before swapping:")
# print("a =", a)
# print("b =", b)
# a, b = b, a
# print("After swapping:")
# print("a =", a)
# print("b =", b)
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
num = int(input("Enter a number: "))
if is_prime(num):
    print(num, "is a prime number.")
else:
    print(num, "is not a prime number.")