import unittest

from dotsecrets.utils import CopyFilter


class TestUtils(unittest.TestCase):

    def test_copyfilter(self):
        """Test copy filter"""
        t = CopyFilter()
        line = "This is a line"
        return self.assertEqual(line, t.sub(line))


if __name__ == '__main__':
    unittest.main()
