import hashlib
import threading
from collections import Counter

def caesar_cipher(word):
    words = []
    for i in range(1,26):
        string = ""
        for j in range(0,len(word)): # Apply caesar cipher to each word 25 times (1 - 25)
            #print(word)
            #print(word[j])
            letter = ord(word[j])
            if(letter < 123 and letter > 96):
                new_letter = letter + i
                if(new_letter > 122):
                    new_letter = new_letter - 26
                string+=(chr(new_letter))
            elif(letter > 47 and letter < 58): # special case for numbers
                new_letter = letter + (i % 10)
                if(new_letter > 57):
                    new_letter = new_letter - 10
                string+=(chr(new_letter))
            elif(letter > 64 and letter < 91): # special case for capital letter
                new_letter = letter + i
                if(new_letter > 90):
                    new_letter = new_letter - 26
                string+=(chr(new_letter))
        words.append(string)
    return words

def check(dictionary): # pass in hashing algorithm as string
    matches = []
    for i in range(0,len(dictionary)):
        hash = hashlib.blake2b()
        # print(dictionary[i][0])
        input = bytes((dictionary[i][0]), 'utf-8')
        hash.update(input)
        attempt = hash.hexdigest()
        for password in hashed_passwords:
            if(password == attempt):
                matches.append([password,dictionary[i][0],i,'blake2b'])
    for i in range(0,len(dictionary)):
        hash = hashlib.blake2s()
        input = bytes((dictionary[i][0]), 'utf-8')
        hash.update(input)
        attempt = hash.hexdigest()
        for password in hashed_passwords:
            if(password == attempt):
                matches.append([password,dictionary[i][0],i,'blake2s'])
    for i in range(0,len(dictionary)):
        hash = hashlib.sha1()
        input = bytes((dictionary[i][0]), 'utf-8')
        hash.update(input)
        attempt = hash.hexdigest()
        for password in hashed_passwords:
            if(password == attempt):
                matches.append([password,dictionary[i][0],i,'1'])
    for i in range(0,len(dictionary)):
        hash = hashlib.sha256()
        input = bytes((dictionary[i][0]), 'utf-8')
        hash.update(input)
        attempt = hash.hexdigest()
        for password in hashed_passwords:
            if(password == attempt):
                matches.append([password,dictionary[i][0],i,'256'])
    for i in range(0,len(dictionary)):
        hash = hashlib.sha512()
        input = bytes((dictionary[i][0]), 'utf-8')
        hash.update(input)
        attempt = hash.hexdigest()
        for password in hashed_passwords:
            if(password == attempt):
                matches.append([password,dictionary[i][0],i,'512', (i / 26)])
    for i in range(0,len(dictionary)):
        hash = hashlib.md5()
        input = bytes((dictionary[i][0]), 'utf-8')
        hash.update(input)
        attempt = hash.hexdigest()
        for password in hashed_passwords:
            if(password == attempt):
                matches.append([password,dictionary[i][0],i,'md5'])
    return matches
    
shadow = open("shadow", "r")
hashed_passwords = []

for sentence in shadow:
    words = sentence.split(":")
    hashed_passwords.append(words[1].strip())

the_dictionary = open("dictionary.txt", "r")
dictionary = []
for word in the_dictionary:
    dictionary.append(word.split())
print(check(dictionary))

# here add 25 caesar shifted words for every word in dictionary to create a new dictionary and then check that new dictionary
words = []
for i in range(0,len(dictionary)):
    result = caesar_cipher(dictionary[i][0])
    for j in range(0,len(result)):
        #print(result)
        #print(result[j])
        words.append([result[j]])
    words.append([dictionary[i][0]])
print(check(words))

print("Checking user2:")
print(check([['cromwell55403']]))


# section of finding salted password

numbers = [str(num).zfill(5) for num in range(100000)]

def check_salt(begin,end):
    for i in range(begin,end):
        print(i)
        for j in range(0,len(numbers)):
            output = check([[dictionary[i][0]+numbers[j]]])
            if(output != []):
                print(output)
                return output
    return []



# used multithreading for checking salted versions of all passwords through all the hashing algorithms
"""
t1 = threading.Thread(target=check_salt, args=(0,700))
t2 = threading.Thread(target=check_salt, args=(700,1400))
t3 = threading.Thread(target=check_salt, args=(1400,2100))
t4 = threading.Thread(target=check_salt, args=(2800,3500))
t5 = threading.Thread(target=check_salt, args=(3500,4200))
t6 = threading.Thread(target=check_salt, args=(4200,4776))
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
"""


with open('numbers.txt') as f: # numbers.txt was file with combinations of numbers 0-7, which would be used to create different combinations of leetspeak
    numbers = []
    for line in f:
        line = line.split(",")
        if line:            
            line = [int(i) for i in line]
            numbers.append(line)

print(numbers)
ignored = [[x-1 for x in group] for group in numbers] # numbers was file with
print(ignored)
replacements = {'l':'1','e':'3', 't':'7', 'a':'4', 'o':'0', 'g':'9', 's':'5','b':'8'}
k = list(replacements.keys())
v = list(replacements.values())
leet_dictionary = []
for number in ignored:
    for i in range(0,len(dictionary)):
        my_string = ""
        for j in range(0,len(dictionary[i][0])):
            if dictionary[i][0][j] in k:
                if(k.index(dictionary[i][0][j]) in number):
                    my_string += dictionary[i][0][j]
                else:
                    my_string += replacements[dictionary[i][0][j]]
            else:
                letter = dictionary[i][0][j].lower()
                if(letter in k and k.index(letter) not in number):
                    my_string += replacements[letter]
                else:
                    my_string += dictionary[i][0][j]
        if(i % 1000 == 0):
            print(my_string)
        leet_dictionary.append([my_string])
print(leet_dictionary)
print(check(leet_dictionary))

