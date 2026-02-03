import string
# storing the given password
known_pass = "v7xUVE2e5bjUc"
# stored all the lowercase letters
letters = string.ascii_lowercase
# used to generate the wordlist
for letter_1 in letters:
    for letter_2 in letters:
        new_pass = known_pass + letter_1 + letter_2
        print(new_pass)
