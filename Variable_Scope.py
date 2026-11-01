# L - Local → E - Enclosing → G - Global → B - Built-in 

#L - Local

print("Local")

def order():
    laptop = "19 14 generation Windows 11 laptop"
    print(f"Your Order is : {laptop}")

order()

#print(laptop) #:Error

print("Enclosing")

#E - Enclosing

def cart():
    discount = "90%"
    def checkout():
        print(f"applying discount : {discount}")

    checkout()
cart()

print("Global")

#Global

user_id = "S.Harshal"

def homepage():
    print(f"Welcome, {user_id}!")

def profilpage():
    print(f"Welcome to the profile page: {user_id}")

homepage()
profilpage()

# Built-in
#Example

print("Built - in")

#Variable:
print(__file__)

#Function
print("S. Harshal".upper())