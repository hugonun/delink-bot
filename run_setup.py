import os
"""Ask for secret token and then write to token.txt file"""
x=input("What is your discord bot Token: ")
with open('token.txt', 'w') as token_file:
    token_file.write(x)

"""Install all rewuirred rewuirements"""
os.system("python3 -m pip install -r requirements.txt")

"""Start bot"""
os.system("python3 init.py")