import unittest

from dotsecrets.utils import CopyTemplate


class TestUtils(unittest.TestCase):

    def test_copytemplate(self):
        """Test copy template"""
        t = CopyTemplate()
        l = "This is a line"
        return self.assertEqual(l, t.sub(l))


if __name__ == '__main__':
    unittest.main()
