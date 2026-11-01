"""This code is developed by S. Harshal
This Code is About Traffic Signals"""

colour = input("Enter a colour(red,yellow,green): ")

if colour == "Green".lower():
    print("Go")
elif colour == "Yellow".lower():
    print("Wait")
elif colour == "Red".lower():
    print("Stop")
else:
    print("Invalid Input")