"""
  Simple DES implementation

  Author : Gabriel Andres Avendaño Casadiego
"""

import pyDes
import base64
import argparse

def byteArray(s):
  if (len(s) != 8):
    msg = ("key %r must be 8 characters long" % s)
    raise argparse.ArgumentTypeError(msg)
  return bytes(s, 'utf-8')

description = "This is an image cipher with DES. Use with caution"
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-a", "--action", help="select decipher/cipher mode", choices=["cipher", "decipher"], required=True)
parser.add_argument("-k", "--key", help="key to cipher / decipher. Must be 8 characters long", type=byteArray, required=True)
parser.add_argument("-img", "--imgname", help="image file", type=str, required=True)
parser.add_argument("-fn", "--filename", help="text file (default: cipherfile.txt)", type=str, default="cipherfile.txt")
args = parser.parse_args()

k = pyDes.des(args.key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

if args.action == 'cipher':
  with open(args.imgname, "rb") as imageFile:
    img = imageFile.read()
  cipherdata = k.encrypt(img)
  encoded_b64 = base64.b64encode(cipherdata)
  encoded_str = encoded_b64.decode("utf-8")
  with open(args.filename, 'w') as file:
    file.write(encoded_str)
  print (f"{encoded_str[0:100]}...")
  print (f"View the entire log in {args.filename}")
else:
  with open(args.filename, 'r', encoding='utf-8') as cipherFile:
    encoded_b64 = cipherFile.read()
  cipherdata = base64.b64decode(encoded_b64)
  plaindata = k.decrypt(cipherdata)
  with open(args.imgname, "wb") as imageFile:
    imageFile.write(plaindata)