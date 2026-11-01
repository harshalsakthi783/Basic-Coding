age = int(input("Enter your age: "))
student = input("Are you are a student(Type yes or no): ")

if age >= 60 or student == "yes".lower():
    print("Discount applied")
else:
    print("No Discount")