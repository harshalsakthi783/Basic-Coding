amount = int(input("Enter th amount: "))
tax = amount * 0.18
total = amount + tax

if total > 1000:
    discount = total * 0.90
    total -= discount

print(total)