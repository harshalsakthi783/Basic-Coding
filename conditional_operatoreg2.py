"""This code is developed by S. Harshal
This Code is About Grades"""

Mark = int(input("Enter your mark(Do not use words): "))

if Mark >= 80 and Mark <= 100:
    print("Grade A")
elif Mark >= 70 and Mark <= 70:
    print("Grade B")
elif Mark >= 60 and Mark <= 60:
    print("Grade C")
elif Mark >= 50 and Mark <= 50:
    print("Grade D")
elif Mark >= 40 and Mark <= 40:
    print("Fail")
elif Mark == 0:
    print("Fail")
else:
    print("Invalid Input")