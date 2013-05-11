import unittest

from dotbriefs.clean import CleanSecret


class TestCleanSecret(unittest.TestCase):

    def setUp(self):
        self.secrets = []
        self.secrets.append(CleanSecret('passwd',
            r'password(\s*)=(\s*)(?#UpToHash)',
            r'password\1=\2(?#Key)',
            'Mutt passwords',
            True))

    def test_state(self):
        state = self.secrets[0].__getstate__()
        other_secret = CleanSecret('', '', '')
        other_secret.__setstate__(state)
        self.assertEqual(self.secrets[0].__dict__, other_secret.__dict__)


if __name__ == '__main__':
    unittest.main()
