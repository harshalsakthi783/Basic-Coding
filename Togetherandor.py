order_amount = 60000
day = "saturday"
membership = "no"

if (order_amount >= 30000 and day in["saturday", "sunday"]) or membership == "gold":
    print("90% discount")
else:
    print("no discount")