"""
  Author : Gabriel Andres Avendaño
  username : gavendanoc
"""
import string
import argparse
import math

class PlayFair:
  def __init__ (self, keyword):
    key = self._addAlphabetLetters(keyword)
    key = self._combine_IJ(key)
    self._keyMatrix = self._turnIntoSquareMatrix(key)
    self._keyIndex = self._createIndexOfMatrix(self._keyMatrix)

  def _addAlphabetLetters (self, keyword):
    key = list(dict.fromkeys(list(keyword)))
    for letter in string.ascii_uppercase:
      if letter not in keyword:
        key.append(letter)
    return key

  def _combine_IJ (self, key):
    found_IJ = False
    i = 0
    while i < len(key):
      if key[i] in 'IJ':
        if not found_IJ:
          key[i] = 'IJ'
          found_IJ = True
        else:
          del key[i]
      i += 1
    return key
  
  def _turnIntoSquareMatrix (self, key):
    keyMatrix = []
    squareSide = int(len(key) ** 0.5)
    for i in range (0, len(key), squareSide):
      keyMatrix.append(key[i: i+squareSide])
    return keyMatrix

  def _createIndexOfMatrix (self, keyMatrix):
    keyIndex = {}
    squareSide = len(keyMatrix)
    for i in range (squareSide):
      for j in range (squareSide):
        keyIndex[keyMatrix[i][j]] = (i, j)
        if keyMatrix[i][j] == 'IJ':
          keyIndex['I'] = (i, j)
          keyIndex['J'] = (i, j)
    return keyIndex

  def _translate (self, pair, move):
    squareSide = len(self._keyMatrix)
    row1, col1 = self._keyIndex[pair[0]]
    row2, col2 = self._keyIndex[pair[1]]
    if row1 == row2:
      col1 = (col1 + move) % squareSide
      col2 = (col2 + move) % squareSide
    elif col1 == col2:
      row1 = (row1 + move) % squareSide
      row2 = (row2 + move) % squareSide
    else:
      col1, col2 = col2, col1
    cipher1 = self._keyMatrix[row1][col1]
    cipher2 = self._keyMatrix[row2][col2]
    return cipher1 + cipher2
  
  def cipherPair (self, pair):
    encryptedpair = self._translate(pair, 1)
    if len(encryptedpair) == 3:
      return encryptedpair[0] + encryptedpair[2]
    return encryptedpair

  def decipherPair (self, pair):
    return self._translate(pair, -1)

  def preprocess (self, plaintext):
    plaincharacters = list(plaintext.replace(" ", ""))
    paddingSymbol = "X"
    alternativeSymbol = "Y"
    i = 0
    while i < len(plaincharacters) - 1:
      if plaincharacters[i] == plaincharacters[i+1]:
        symbol = alternativeSymbol if plaincharacters[i] == paddingSymbol else paddingSymbol
        plaincharacters.insert(i+1, symbol)
      i += 2
    if len(plaincharacters) % 2 != 0:
      symbol = alternativeSymbol if plaincharacters[-1] == paddingSymbol else paddingSymbol
      plaincharacters.append(symbol)
    return "".join(plaincharacters)

  def cipher(self, plaintext):
    processedtext = self.preprocess(plaintext)
    cipherPairs = []
    for i in range(0, len(processedtext), 2):
      cipherPairs.append(self.cipherPair(processedtext[i:i+2]))
    return processedtext, "".join(cipherPairs)

  def decipher(self, ciphertext):
    plainPairs = []
    for i in range(0, len(ciphertext), 2):
      plainPairs.append(self.decipherPair(ciphertext[i:i+2]))
    return plainPairs
  
  def printKeyMatrix(self):
    print("\n".join(["\t".join(row) for row in self._keyMatrix]))

def alphabetical (s):
  s = s.upper()
  allowed_symbols = string.ascii_uppercase + " "
  for letter in s:
    if letter not in allowed_symbols:
      msg = ("%r must contain only letters or spaces" % s)
      raise argparse.ArgumentTypeError(msg)
  return s

def putSpaces(characters, t, space=" "):
  characters_spaces = []
  for i, ch in enumerate(characters):
    characters_spaces.append(space + ch if i % t == 0 else ch)
  return ("".join(characters_spaces)).strip()

description = "This is a playfair cipher and decipher. Use with caution"
parser = argparse.ArgumentParser(description=description)

parser.add_argument("-a", "--action", help="select decipher/cipher mode", choices=["cipher", "decipher"], required=True)
parser.add_argument("-t", "--text", help="contains ciphertext or plaintext", required=True, type=alphabetical)
parser.add_argument("-k", "--key", help="keyword for the vigenere cipher", required=True, type=alphabetical)

args = parser.parse_args()

keyword = args.key.replace(" ", "")
pf = PlayFair(keyword)

if args.action == "cipher":
  plaintext = args.text
  processedtext, ciphertext = pf.cipher(plaintext)
  print ("Action : cipher")
  print ("Keyword : ", keyword)
  print ("Key matrix : ")
  pf.printKeyMatrix()
  print ()
  print ("Message : ", plaintext)
  print ("plaintext :  ", putSpaces(processedtext, 2))
  print ("ciphertext : ", putSpaces(ciphertext, 2))
else:
  ciphertext = args.text.replace(" ", "")
  plaintext = pf.decipher(ciphertext)
  print ("Action : decipher")
  print ("Keyword : ", keyword)
  print ("Key matrix : ")
  pf.printKeyMatrix()
  print ()
  print ("ciphertext : ", putSpaces(ciphertext, 2))
  print ("plaintext :  ", putSpaces(plaintext, 1))