print("Don't' use words")

num1 = int(input("Enter number 1 : "))
num2 = int(input("Enter number 2 : "))

operation = input("Enter the Operation: ")

if operation == "+":
    print(num1 + num2)
elif operation == "-":
    print(num1 - num2)
elif operation == "x" or "*":
    print(num1 * num2)
elif operation == "/":
    print(round(num1 / num2))
else:
    print("Invalid operation")