"""
  Author : Gabriel Andres Avendaño
  username : gavendanoc
"""

import numpy as np
import math
import string
import argparse

def alphabetical(s):
  s = s.upper()
  allowedSymbols = string.ascii_uppercase + " "
  isAllowed = all(letter in allowedSymbols for letter in s)
  if not isAllowed:
    msg = ("%r must contain only letters or spaces" % s)
    raise argparse.ArgumentTypeError(msg)
  return s

def putSpaces(characters, t, space=" "):
  characters_spaces = []
  for i, ch in enumerate(characters):
    characters_spaces.append(space + ch if i % t == 0 else ch)
  return ("".join(characters_spaces)).strip()

def preprocess(plaintext, padding=0, paddingCharacter="X"):
  plaincharacters = plaintext.replace(" ", "")
  if padding == 0: return plaincharacters
  newLength = math.ceil(len(plaincharacters) / padding) * padding
  return plaincharacters.ljust(newLength, paddingCharacter)

# found in https://stackoverflow.com/questions/2706605/sorting-a-2d-numpy-array-by-multiple-axes
def sortPoints(points):
  ind = np.lexsort((points[:,1],points[:,0])) 
  return points[ind]

clockwise = lambda row, column, size: (column, size - row - 1)
counterClockwise = lambda row, column, size : (size - column - 1, row)
rotateClockwise = lambda points, size: np.vstack(clockwise(points[:, 0], points[:, 1], size)).T
rotateCounterClockwise = lambda points, size: np.vstack(counterClockwise(points[:, 0], points[:, 1], size)).T

def removeDuplicates(points):
  _, idx = np.unique(points, return_index=True, axis=0)
  return points[np.sort(idx)]

def makeFullRotation(points, rotate, size):
  points = sortPoints(points)
  availablePoints = []
  for _ in range(4):
    availablePoints.append(points)
    points = sortPoints(rotate(points, size))
  availablePoints = np.vstack(availablePoints)
  return removeDuplicates(availablePoints)


def cipher(plaintext, markedPoints, rotate, size, paddingCharacter="_"):
  plaintext = np.array(list(plaintext), dtype='S1')
  canvas = np.empty((size, size), dtype = "S1")
  canvas[:] = paddingCharacter
  points = makeFullRotation(markedPoints, rotate, size)
  canvas[points[:, 0], points[:, 1]] = plaintext[:points.shape[0]]
  return (b''.join(canvas.ravel())).decode("utf-8")

def decipher(ciphertext, markedPoints, rotate, size):
  ciphertext = np.array(list(ciphertext), dtype='S1')
  canvas = ciphertext.reshape((size, size))
  size = canvas.shape[0]
  selected = []
  for i in range(4):
    selected.extend(canvas[markedPoints[:, 0], markedPoints[:, 1]])
    markedPoints = sortPoints(rotate(markedPoints, size))
  return (b''.join(selected)).decode("utf-8")

description = "This is a turning grille cipher and decipher. Use with caution"
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-a", "--action", help="select decipher/cipher mode", choices=["cipher", "decipher"], required=True)
parser.add_argument("-r", "--rotation", help="totate grill clockwise or counterclockwise", choices=["cw", "ccw"], required=True)
parser.add_argument("-m", "--message", help="contains ciphertext or plaintext", type=alphabetical, required=True)
parser.add_argument("-s", "--size", help="The size of the output and grille matrix", type=int, required=True)
parser.add_argument("-p", "--point", help="opened points in the grille", action='append', nargs=2, type=int, required=True)
args = parser.parse_args()

totalPoints = len(args.point)
markedPoints = sortPoints(np.array(args.point))
markedPoints = markedPoints - 1
size = args.size

if args.action == "cipher":
  processedtext = preprocess(args.message, 4 * totalPoints)
  if args.rotation == 'cw':
    ciphertext = cipher(processedtext, markedPoints, rotateClockwise, size)
  else:
    ciphertext = cipher(processedtext, markedPoints, rotateCounterClockwise, size)
  print (putSpaces(ciphertext, size))
else:
  ciphertext = preprocess(args.message)
  if args.rotation == 'cw':
    plaintext = decipher(ciphertext, markedPoints, counterClockwise, size)
  else:
    plaintext = decipher(ciphertext, markedPoints, rotateCounterClockwise, size)
  print (putSpaces(plaintext, size))
