"""Assignment 2

Name: Erincz Arnold

"""
import math
from typing import Collection

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
    if (rows == 1):
        return text
    
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

#####################
# RAIL FENCE CIPHER #
#####################

def encrypt_rail_fence(rows, text):
    if (rows == 1):
        return text

    n = len(text)
    columns = int(n / (rows - 1))

    matrix = create_rail_fence_matrix(n, columns, rows, text)

    result = []
    for i in range(0, rows):
        for j in range(0, columns):
            if matrix[i][j] != '#':
                result.append(matrix[i][j])
    
    return ''.join(result)


def decrypt_rail_fence(rows, cipher):
    if (rows == 1):
        return cipher

    n = len(cipher)
    columns = int(n / (rows - 1))

    structure_matrix = create_rail_fence_matrix(n, columns, rows, cipher)
 
    text_index = 0
    for i in range(0, rows):
        for j in range(0, columns):
            if structure_matrix[i][j] != '#':
                structure_matrix[i][j] = cipher[text_index]
                text_index += 1
        

    result = []
    dir_down = True
    act_row = 0
    act_col = 0

    for i in range(0, n):
        result.append(structure_matrix[act_row][act_col])

        if (dir_down):
            if(act_row == rows - 1):
                act_col += 1
                dir_down = False
                act_row = rows - 2
            else:
                act_row += 1
        else:
            if (act_row == 0):
                act_col += 1
                dir_down = True
                act_row += 1
            else:
                act_row -= 1
    
    return ''.join(result)

def create_rail_fence_matrix(n, columns, rows, text):
    matrix = [['#' for i in range(0, columns)] for j in range(0, rows)]

    dir_down = True
    act_row = 0
    act_col = 0

    for i in range(0, n):
        matrix[act_row][act_col] = text[i]

        if (dir_down):
            if(act_row == rows - 1):
                act_col += 1
                dir_down = False
                act_row = rows - 2
            else:
                act_row += 1
        else:
            if (act_row == 0):
                act_col += 1
                dir_down = True
                act_row += 1
            else:
                act_row -= 1

    return matrix
