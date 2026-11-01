import sys
if len(sys.argv) == 2:
    print("Usage: python_generated_code.py 'Full name and last name'")
name = "".join(sys.argv[1:])
print(name)

email = name.lower().replace("", "") + "@google.com"


print("\n --- Your Profile ---")
print("Name: ", name)
print("Email", email)
