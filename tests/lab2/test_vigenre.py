import unittest

from src.lab2.vigenre import decrypt_vigenere, encrypt_vigenere


class VigenereTestCase(unittest.TestCase):
    def test_decryption(self):
        self.assertEqual("Python3.6", decrypt_vigenere("Kglpca3.6", "vision"))

    def test_decryption_with_empty_string(self):
        self.assertEqual("", decrypt_vigenere("", "empty"))

    def test_encryption(self):
        self.assertEqual("Kglpca3.6", encrypt_vigenere("Python3.6", "vision"))

    def test_encryption_with_empty_string(self):
        self.assertEqual("", encrypt_vigenere("", "empty"))

    def test_encryption_with_keywoard(self):
        self.assertEqual("u zkhi lkxvkz", encrypt_vigenere("i love python", "meow"))

    def test_decryption_with_keywoard(self):
        self.assertEqual("i love python", decrypt_vigenere("u zkhi lkxvkz", "meow"))
