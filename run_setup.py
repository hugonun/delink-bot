import os
x=input("What is your discord bot Token: ")
with open('token.txt', 'w') as token_file:
    token_file.write(x)

os.system("python3 -m pip install -r requirements.txt")

os.system("python3 init.py")