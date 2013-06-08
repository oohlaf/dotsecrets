import unittest

from dotsecrets.utils import CopyFilter


class TestUtils(unittest.TestCase):

    def test_copyfilter(self):
        """Test copy filter"""
        t = CopyFilter()
        l = "This is a line"
        return self.assertEqual(l, t.sub(l))


if __name__ == '__main__':
    unittest.main()
