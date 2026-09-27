import unittest

from base62 import encode, decode, CHARSET


class TestEncode(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(encode(0), "0")

    def test_single_digits(self):
        self.assertEqual(encode(1), "1")
        self.assertEqual(encode(9), "9")
        self.assertEqual(encode(10), "A")
        self.assertEqual(encode(35), "Z")
        self.assertEqual(encode(36), "a")
        self.assertEqual(encode(61), "z")

    def test_two_digit_boundary(self):
        # 62 -> first two-digit value: "10"
        self.assertEqual(encode(62), "10")
        self.assertEqual(encode(63), "11")

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            encode(-1)

    def test_bool_rejected(self):
        # bool is a subclass of int; accepting it would let True silently
        # encode as 1, which is a real source of bugs at call sites.
        with self.assertRaises(ValueError):
            encode(True)

    def test_non_int_raises(self):
        with self.assertRaises(ValueError):
            encode("5")
        with self.assertRaises(ValueError):
            encode(3.0)


class TestDecode(unittest.TestCase):
    def test_single_chars(self):
        self.assertEqual(decode("0"), 0)
        self.assertEqual(decode("1"), 1)
        self.assertEqual(decode("9"), 9)
        self.assertEqual(decode("A"), 10)
        self.assertEqual(decode("Z"), 35)
        self.assertEqual(decode("a"), 36)
        self.assertEqual(decode("z"), 61)

    def test_two_digit(self):
        self.assertEqual(decode("10"), 62)
        self.assertEqual(decode("11"), 63)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            decode("")

    def test_invalid_char_raises(self):
        with self.assertRaises(ValueError):
            decode("abc!")
        with self.assertRaises(ValueError):
            decode("-1")

    def test_non_str_raises(self):
        with self.assertRaises(ValueError):
            decode(123)
        with self.assertRaises(ValueError):
            decode(None)


class TestRoundTrip(unittest.TestCase):
    def test_round_trip_range(self):
        for n in [0, 1, 61, 62, 63, 3843, 3844, 100000, 2**40, 2**128]:
            self.assertEqual(decode(encode(n)), n)

    def test_charset_ordering(self):
        # The alphabet must be exactly 62 unique chars in the documented order.
        self.assertEqual(len(CHARSET), 62)
        self.assertEqual(len(set(CHARSET)), 62)
        self.assertEqual(CHARSET[:10], "0123456789")
        self.assertEqual(CHARSET[10:36], "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.assertEqual(CHARSET[36:], "abcdefghijklmnopqrstuvwxyz")


if __name__ == "__main__":
    unittest.main()
