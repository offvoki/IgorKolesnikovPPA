import unittest

from src.lab2.rsa import decrypt, encrypt, gcd, generate_keypair, is_prime, multiplicative_inverse


class RSATestCase(unittest.TestCase):
    def test_is_prime_number_for_unprime_number(self):
        self.assertEqual(is_prime(51), 0)

    def test_is_prime_number_for_prime_number(self):
        self.assertEqual(is_prime(71), 1)

    def test_gcd_for_two_prime_number(self):
        self.assertEqual(gcd(71, 53), 1)

    def test_gcd_for_two_random_number(self):
        self.assertEqual(gcd(5, 15), 5)

    def test_multiplicative_inverse(self):
        d = multiplicative_inverse(53, 71)
        self.assertEqual(d * 53 % 71, 1)

    def test_generate_keypair_with_not_prime_number(self):
        with self.assertRaises(ValueError):
            generate_keypair(4, 1)

    def test_generate_keypair_with_equal_number(self):
        with self.assertRaises(ValueError):
            generate_keypair(1, 1)

    def test_encrypt(self):
        self.assertEqual(
            "".join(map(str, encrypt((523, 3763), "I love Programming"))),
            "307196824462457119831619681981236724573524236716561352135228085943524",
        )

    def test_decrypt(self):
        self.assertEqual(
            decrypt(
                (1907, 3763),
                [
                    3071,
                    968,
                    2446,
                    2457,
                    1198,
                    3161,
                    968,
                    1981,
                    2367,
                    2457,
                    3524,
                    2367,
                    1656,
                    1352,
                    1352,
                    2808,
                    594,
                    3524,
                ],
            ),
            "I love Programming",
        )
