import unittest

from src.lab2.caesar import decrypt_caesar, encrypt_caesar


class CaesarTestCase(unittest.TestCase):
    def test_decryption(self):
        self.assertEqual("Python3.6", decrypt_caesar("Sbwkrq3.6"))

    def test_decryption_with_empty_string(self):
        self.assertEqual("", decrypt_caesar(""))

    def test_encryption(self):
        self.assertEqual("Sbwkrq3.6", encrypt_caesar("Python3.6"))

    def test_encryption_with_empty_string(self):
        self.assertEqual("", encrypt_caesar(""))

    def test_encryption_with_shift_25(self):
        self.assertEqual("h knud oxsgnm", encrypt_caesar("i love python", 25))

    def test_decryption_with_shift_25(self):
        self.assertEqual("i love python", decrypt_caesar("h knud oxsgnm", 25))
