"""Assignment 2

Name: Erincz Arnold

"""
import math

#################
# CAESAR CIPHER #
#################

def encrypt_caesar(plaintext):
    return vigenereCipher(plaintext, 'C', 1)
    

def decrypt_caesar(ciphertext):
    return vigenereCipher(ciphertext, 'C', -1)


###################
# VIGENERE CIPHER #
###################

def getLetterPositionObj(characters):
    charPosition = {}

    for i in range(len(characters)):
        charPosition[characters[i]] = i

    return charPosition

def vigenereCipher(plaintext, key, sign):
    characters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",  "S", "T", "U", "V",  "W", "X", "Y", "Z",  "0", "1",  "2", "3", "4", "5", "6", "7",  "8", "9", ".", ",", "?", "!", "'", "_", "-", "&", "@", "#", "$", "%", "*", "(", ")", " "];

    charPosition = getLetterPositionObj(characters)

    message = ''

    keyIndex = 0
    offset = 0
    currentIndex = 0

    for i in range(len(plaintext)):
        if keyIndex == len(key):
            keyIndex = 0
        
        offset = charPosition[key[keyIndex]]
        keyIndex += 1
        currentIndex = charPosition[plaintext[i]]

        rawIndex = currentIndex + sign * offset
        letterIndex = 0
        
        if sign >= 0:
            letterIndex = abs(len(characters) - rawIndex) if (rawIndex >= len(characters)) else rawIndex
        else:
            letterIndex =  abs(len(characters) + rawIndex) if (rawIndex < 0) else rawIndex

        message += characters[letterIndex]

    return message

def encrypt_vigenere(plaintext, keyword):
    return vigenereCipher(plaintext, keyword, 1)


def decrypt_vigenere(ciphertext, keyword):
    return vigenereCipher(ciphertext, keyword, -1)

###################
# SCYTALE CIPHER #
###################

def scytale_algorithm(rows, text):
    n = len(text)
    columns = math.ceil(n / rows)    
    cipher = ['+'] * (rows * columns)

    additions = 0
    for i in range(n):
        if(text[i] == '+'):
            additions += 1
            continue
        row = i // rows
        col = i % rows
        cipher[col * columns + row] = text[i]

    return (''.join(cipher[:-additions]) if additions else ''.join(cipher))

def encrypt_scytale(plaintext):
    return scytale_algorithm(5, plaintext)

def decrypt_scytale(cipher):
    return scytale_algorithm(math.ceil(len(cipher) / 5), cipher)
