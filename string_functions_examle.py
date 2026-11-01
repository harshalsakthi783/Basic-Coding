name = "S. Harshal"

mobile = "9585414611"
masked = mobile[:2] + "******" + mobile[-2:]
print(masked)

book = "Python VS Java"
author = "HARSHAL s"

formatted = f"{book.title()} - {author.title()}"
print(formatted)

location = "Chennai"
fixed_location = location.replace("Chennai", "Ooty")
print(fixed_location)

message2 = "Your mail id in vetri vikaas public school is: 2762. Please Keep it safe"
mail_id = message2.split(":")[1].split(".")[0].strip()
print(mail_id)

promo__msg = "Use flipkart100 to get 100% off"
if "flipkart100" in promo__msg:
    print("100% offer applied")
else:
    print("No Offer")

feedback = "CreAct was Amazing!"
print(f"position of Amazing! is: {feedback.find("Amazing!")} ")

name = "Harshal Bhavanisha"
initials = " ".join([word[0].upper() for word in name.split()])
print(initials)

dirty_input = input("Enter with space example             chess      like this: ")
clean_output = dirty_input.strip()
print(clean_output)

message2 = "I like Python because it is very easy to learn and comfortable"
message2_count = len(message2.split())
print(message2_count)