"""
  Author : Gabriel Andres Avendaño
  username : gavendanoc
"""

import argparse
import string

def vigenere_encrypt (plain_letter, key_letter):
  alphabet_letters = 26
  A_ascii = ord("A")
  plain_pos = ord(plain_letter) - A_ascii
  key_pos = ord(key_letter) - A_ascii
 
  cipher_pos = (plain_pos + key_pos) % alphabet_letters
  return chr(cipher_pos + A_ascii)

def vigenere_decrypt (cipher_letter, key_letter):
  alphabet_letters = 26
  A_ascii = ord("A")
  cipher_pos = ord(cipher_letter) - A_ascii
  key_pos = ord(key_letter) - A_ascii
 
  plain_pos = (cipher_pos - key_pos) % alphabet_letters
  return chr(plain_pos + A_ascii)

def putSpaces(characters, t, space=" "):
  characters_spaces = []
  for i, ch in enumerate(characters):
    characters_spaces.append(space + ch if i % t == 0 else ch)
  return ("".join(characters_spaces)).strip()


def translate(function, key, characters):
  translatedletters = []
  key_length = len(key)

  for i, plain_letter in enumerate(characters):
    key_letter = key[i % key_length]
    translated_letter = function(plain_letter, key_letter)
    translatedletters.append(translated_letter)
  return translatedletters

def alphabetical (s):
  s = s.upper()
  allowed_symbols = string.ascii_uppercase + " "
  for letter in s:
    if letter not in allowed_symbols:
      msg = ("%r must contain only letters or spaces" % s)
      raise argparse.ArgumentTypeError(msg)
  return s

description = "This is a vigenere cipher and decipher. Use with caution"
parser = argparse.ArgumentParser(description=description)

parser.add_argument("-a", "--action", help="select decipher/cipher mode", choices=["cipher", "decipher"], required=True)
parser.add_argument("-te", "--text", help="contains ciphertext or plaintext", required=True, type=alphabetical)
parser.add_argument("-k", "--key", help="keyword for the vigenere cipher", required=True, type=alphabetical)
parser.add_argument("-t", help="styling : used for grouping blocks of size 't'", type=int, required=True)

args = parser.parse_args()

key = args.key.replace(" ", "")
t = args.t

if args.action == "cipher":
  plain_characters = list(args.text.replace(" ", ""))
  cipher_characters = translate(vigenere_encrypt, key, plain_characters)

  print("Action : encrypt\n")
  print("key : ", key)
  print("t : ", t)
  print("plaintext :  ", putSpaces(plain_characters, t))
  print("ciphertext : ", putSpaces(cipher_characters, t))
else:
  cipher_characters= list(args.text.replace(" ", ""))
  plain_characters = translate(vigenere_decrypt, key, cipher_characters)

  print(plain_characters)

  print("Action : decrypt\n")
  print("key : ", key)
  print("t : ", t)
  print("ciphertext : ", putSpaces(cipher_characters, t))
  print("plaintext :  ", putSpaces(plain_characters, t))

