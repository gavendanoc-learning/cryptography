"""
  Simple AES implementation

  Author : Gabriel Andres Avendaño Casadiego
"""

import pyaes
import base64
import argparse

description = "This is an image cipher with AES. Use with caution"
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-a", "--action", help="select decipher/cipher mode", choices=["cipher", "decipher"], required=True)
parser.add_argument("-k", "--key", help="key to cipher / decipher. Must be 8 characters long", type=str, required=True)
parser.add_argument("-o", "--operation", help="key size, must be 128 bits (16 bytes), 192 bits (24 bytes) or 256 bits (32 bytes) long", choices=[128, 192, 256], type=int, required=True)
parser.add_argument("-img", "--imgname", help="image file", type=str, required=True)
parser.add_argument("-fn", "--filename", help="text file (default: cipherfile.txt)", type=str, default="cipherfile.txt")
args = parser.parse_args()

key = args.key
if len(key) * 8 != args.operation:
  parser.error(F"--key must be {args.operation} bits ({args.operation // 8} bytes) long")

k = pyaes.AESModeOfOperationCTR(key.encode())

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