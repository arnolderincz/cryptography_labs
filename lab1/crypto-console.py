#!/usr/bin/env python3
"""Run a console menu to interact with cryptographic ciphers.
"""
import random

from crypto import (decrypt_rail_fence, encrypt_caesar, decrypt_caesar, encrypt_rail_fence,
                    encrypt_vigenere, decrypt_vigenere,
                    encrypt_scytale, decrypt_scytale)

HEADER = r"""
   ___________ __ __ ___   ______                 __                               __             ______                       __
  / ____/ ___// // /<  /  / ____/______  ______  / /_____  ____ __________ _____  / /_  __  __   / ____/___  ____  _________  / /__
 / /    \__ \/ // /_/ /  / /   / ___/ / / / __ \/ __/ __ \/ __ `/ ___/ __ `/ __ \/ __ \/ / / /  / /   / __ \/ __ \/ ___/ __ \/ / _ \
/ /___ ___/ /__  __/ /  / /___/ /  / /_/ / /_/ / /_/ /_/ / /_/ / /  / /_/ / /_/ / / / / /_/ /  / /___/ /_/ / / / (__  ) /_/ / /  __/
\____//____/  /_/ /_/   \____/_/   \__, / .___/\__/\____/\__, /_/   \__,_/ .___/_/ /_/\__, /   \____/\____/_/ /_/____/\____/_/\___/
                                  /____/_/              /____/          /_/          /____/
"""


#############################
# GENERAL CONSOLE UTILITIES #
#############################


def get_cryptosystem():
    """Ask the user which cryptosystem to use. Always returns a letter in `"CVM"`."""
    print("* Cryptosystem *")
    return _get_selection("(C)aesar, (V)igenere, (S)cytale or (R)ail Fence? ", "CVSR")


def get_action():
    """Ask the user whether to encrypt or decrypt text. Always returns a letter in `"ED"`."""
    print("* Action *")
    return _get_selection("(E)ncrypt or (D)ecrypt? ", "ED")


def get_filename():
    """Ask the user for a filename, reprompting for nonempty input.

    Doesn't check that the file exists.
    """
    filename = input("Filename? ")
    while not filename:
        filename = input("Filename? ")
    return filename


def get_input(binary=False):
    """Prompt the user for input data, optionally read as bytes."""
    print("* Input *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        text = input("Enter a string: ").strip().upper()
        while not text:
            text = input("Enter a string: ").strip().upper()
        if binary:
            return bytes(text, encoding='utf8')
        return text
    else:
        filename = get_filename()
        flags = 'r'
        if binary:
            flags += 'b'
        with open(filename, flags) as infile:
            return infile.read()


def set_output(output, binary=False):
    """Write output to a user-specified location."""
    print("* Output *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        print(output)
    else:
        filename = get_filename()
        flags = 'w'
        if binary:
            flags += 'b'
        with open(filename, flags) as outfile:
            print("Writing data to {}...".format(filename))
            outfile.write(output)


def _get_selection(prompt, options):
    choice = input(prompt).upper()
    while not choice or choice[0] not in options:
        choice = input("Please enter one of {}. {}".format('/'.join(options), prompt)).upper()
    return choice[0]


def get_yes_or_no(prompt, reprompt=None):
    """Ask the user whether they would like to continue.

    Responses that begin with a `Y` return True. (case-insensitively)
    Responses that begin with a `N` return False. (case-insensitively)
    All other responses (including '') cause a reprompt.
    """
    if not reprompt:
        reprompt = prompt

    choice = input("{} (Y/N) ".format(prompt)).upper()
    while not choice or choice[0] not in ['Y', 'N']:
        choice = input("Please enter either 'Y' or 'N'. {} (Y/N)? ".format(reprompt)).upper()
    return choice[0] == 'Y'


def clean_caesar(text):
    """Convert text to a form compatible with the preconditions imposed by Caesar cipher."""
    return text.upper()


def clean_vigenere(text):
    """Convert text to a form compatible with the preconditions imposed by Vigenere cipher."""
    return ''.join(ch for ch in text.upper() if ch.isupper())


def run_caesar(encrypting, data):
    """Run the Caesar cipher cryptosystem."""
    data = clean_caesar(data)

    print("* Transform *")
    print("{}crypting {} using Caesar cipher...".format('En' if encrypting else 'De', data))

    return (encrypt_caesar if encrypting else decrypt_caesar)(data)


def run_vigenere(encrypting, data):
    """Run the Vigenere cipher cryptosystem."""
    data = clean_vigenere(data)

    print("* Transform *")
    keyword = clean_vigenere(input("Keyword? "))
    while not keyword:
        keyword = clean_vigenere(input("Keyword? "))

    print("{}crypting {} using Vigenere cipher and keyword {}...".format('En' if encrypting else 'De', data, keyword))

    return (encrypt_vigenere if encrypting else decrypt_vigenere)(data, keyword)


def run_scytale(encrypting, data):
    print("* Transform *")
    data = clean_caesar(data)
    
    print("{}crypting {} using Scytale cipher...".format('En' if encrypting else 'De', data))

    if encrypting:  # Encrypt  
        return encrypt_scytale(data)
    else:  # Decrypt
        return decrypt_scytale(data)

def run_rail_fence(encrypting, data):
    print("* Transform *")
    data = clean_caesar(data)
    
    print("{}crypting {} using Rail Fence cipher...".format('En' if encrypting else 'De', data))

    if encrypting:  # Encrypt  
        return encrypt_rail_fence(3, data)
    else:  # Decrypt
        return decrypt_rail_fence(3, data)


def run_suite():
    """Run a single iteration of the cryptography suite.

    Asks the user a type of cryptosystem to use, whether to encrypt or decrypt,
    input text from a string or file, and where to show the output, dispatching
    the actual work to a helper function.
    """
    print('-' * 34)
    system = get_cryptosystem()
    action = get_action()
    encrypting = action == 'E'
    if system == 'M' and encrypting:
        data = get_input(binary=True)
    else:
        data = get_input(binary=False)


    # This isn't the cleanest way to implement functional control flow, but I
    # thought it was too cool to not sneak in here!
    commands = {
        'C': run_caesar,         # Caesar Cipher
        'V': run_vigenere,       # Vigenere Cipher
        'S': run_scytale,         # Scytale Cipher
        'R': run_rail_fence      # Rail Fence Cipher
    }
    output = commands[system](encrypting, data)
    set_output(output)


def main():
    """Run the main interactive console for Assignment 1: Cryptography."""
    print(HEADER)
    print("Welcome to the Cryptography Suite!")
    run_suite()
    while get_yes_or_no("Again?"):
        run_suite()
    print("Goodbye!")


if __name__ == '__main__':
    main()
