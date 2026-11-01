delivery_partner = "Flipkart"

def Flipkart():
    item1 = "Windows 11 14 generatin 19 Laptop"
    item2 = "Android mobile"
    
    def order_now():
        quantity_for_laptop = 1
        quantity_for_mobile = 1
        print(f"ordering {quantity_for_laptop} {item1}, {quantity_for_mobile} {item2} in {delivery_partner}")

    order_now()

Flipkart()

print(f"Code File link(For this computer only): {__file__}")

#In this code your usig all variable scope