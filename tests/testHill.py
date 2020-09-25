import unittest
import random
import string
import numpy as np
from hillcypher import hill

class TestHill(unittest.TestCase):
  def get_random_string(self, length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
  
  def test_inverse (self):
    count = 0
    side = np.random.randint(2, 10)
    while count < 500:
      keyMatrix = np.random.randint(26, size=(side, side))
      inverse = hill.get_modular_inverse(keyMatrix)
      if inverse is not None:
        count += 1
        identical = keyMatrix.dot(inverse) % 26
        isEqual = np.all(identical == np.eye(side))
        with self.subTest(i=count):
          self.assertTrue(isEqual, f"Error with matrix {str(keyMatrix)} and inverse {inverse}")


  def test_cipher(self):
    # 
    # keyMatrix = np.array([[11, 8], [3, 7]])
    count = 0
    side = np.random.randint(2, 10)
    while count < 500:
      keyMatrix = np.random.randint(26, size=(side, side))
      plaintext = hill.preprocess(self.get_random_string(30), padding=side)
      ciphertext = hill.cipher(plaintext, keyMatrix)
      originaltext, _ = hill.decipher(ciphertext, keyMatrix)

      # print (plaintext, originaltext, keyMatrix.ravel())

      if originaltext is not None: # Menor tamaño posible, aqui no se detectan errores
        count += 1
        with self.subTest(i=count):
          self.assertEqual(plaintext, originaltext, f"Error with matrix {str(keyMatrix)}")

if __name__ == "__main__":
  unittest.main()