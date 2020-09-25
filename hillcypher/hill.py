"""
  Author : Gabriel Andres Avendaño
  username : gavendanoc
"""

import argparse
import string
import numpy as np
import math

def preprocess(plaintext, padding, paddingCharacter="X"):
    plaincharacters = plaintext.replace(" ", "")
    newLength = math.ceil(len(plaincharacters) / padding) * padding
    return plaincharacters.ljust(newLength, paddingCharacter)

def putSpaces(characters, t, space=" "):
  characters_spaces = []
  for i, ch in enumerate(characters):
    characters_spaces.append(space + ch if i % t == 0 else ch)
  return ("".join(characters_spaces)).strip()

def alphabetical(s):
  s = s.upper()
  allowedSymbols = string.ascii_uppercase + " "
  isAllowed = all(letter in allowedSymbols for letter in s)
  if not isAllowed:
    msg = ("%r must contain only letters or spaces" % s)
    raise argparse.ArgumentTypeError(msg)
  return s

def EEA(a, b):
  if b == 0: return (a, 1, 0)
  q = a // b
  d, x, y = EEA(b, a % b)
  x, y = y, x - q * y
  return (d, x, y)

def get_modular_inverse (matrix):
  det = round(np.linalg.det(matrix)) 
  if det == 0: return None
  gcd, _, det_inv = EEA(26, det % 26)
  if abs(gcd) != 1: return None
  det_inv = det_inv % 26
  inverse = np.linalg.inv(matrix)
  adjugate = inverse * det
  modular_inverse = (det_inv * adjugate)
  modular_inverse = np.rint(modular_inverse).astype('int64')
  modular_inverse = modular_inverse % 26
  return modular_inverse

def translate(text, matrix):
  A = ord('A')
  side = matrix.shape[0]
  originalNumbers = np.array([ord(ch) - A for ch in text])
  originalNumbers = originalNumbers.reshape((-1, side))
  translatedNumbers = (originalNumbers @ matrix) % 26
  translatedNumbers = translatedNumbers.ravel()
  translatedtext = "".join(chr(n + A) for n in translatedNumbers)
  return translatedtext

def cipher(plaintext, keyMatrix):
  return translate(plaintext, keyMatrix)

def decipher(ciphertext, keyMatrix):
  modular_inverse = get_modular_inverse(keyMatrix)
  if modular_inverse is None: return None, None
  return translate(ciphertext, modular_inverse), modular_inverse

def printKeyMatrix(matrix):
  for row in matrix:
    print('\t'.join(str(ele) for ele in row))
    
if __name__ == "__main__":
  description = "This is a hill cipher and decipher. Use with caution"
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument("-a", "--action", help="select decipher/cipher mode", choices=["cipher", "decipher"], required=True)
  parser.add_argument("-te", "--text", help="contains ciphertext or plaintext", required=True, type=alphabetical)
  parser.add_argument("-k", "--key", help="keyword for the vigenere cipher", nargs=4, type=int)
  args = parser.parse_args()

  keyMatrix = np.array(args.key).reshape((2, 2))

  if args.action == "cipher":
    plaintext = args.text
    processedtext = preprocess(plaintext, padding=2)
    ciphertext = cipher(processedtext, keyMatrix)
    print ("Action : cipher")
    print ("Key matrix : ")
    printKeyMatrix (keyMatrix)
    print ()
    print ("Message : ", plaintext)
    print ("plaintext :  ", putSpaces(processedtext, 2))
    print ("ciphertext : ", putSpaces(ciphertext, 2))
  else:
    ciphertext = args.text.replace(" ", "")
    plaintext, modular_inverse = decipher(ciphertext, keyMatrix)

    print ("Action : decipher")
    if plaintext is not None:
      print ("Inverse matrix : ")
      printKeyMatrix(modular_inverse)
      print ()
      print ("ciphertext : ", putSpaces(ciphertext, 2))
      print ("plaintext :  ", putSpaces(plaintext, 2))
    else:
      print ("Matrix is not reversable") 