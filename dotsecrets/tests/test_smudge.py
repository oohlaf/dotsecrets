import logging
import unittest

from dotsecrets.smudge import SmudgeFilter


class TestSmudgeFilter(unittest.TestCase):

    def setUp(self):
        logging.basicConfig()
        self.secrets = {}
        self.secrets['password'] = 's3cr3t'
        self.secrets['question'] = 'h1dd3n 4g3nd4'
        self.filters = []
        self.filters.append(SmudgeFilter('name', self.secrets))

    def test_nosecret_sub(self):
        self.assertEqual(self.filters[0].sub('password = hi # comment'),
                         'password = hi # comment')

    def test_nokey_sub(self):
        self.assertEqual(self.filters[0].sub('password = '
                                             '$DotSecrets: $ # comment'),
                         'password = $DotSecrets: $ # comment')

    def test_nomatch_sub(self):
        self.assertEqual(self.filters[0].sub('password = '
                                             '$DotSecrets: notfound$ '
                                             '# comment'),
                         'password = $DotSecrets: notfound$ # comment')

    def test_single_sub(self):
        self.assertEqual(self.filters[0].sub('password = '
                                             '$DotSecrets: password$ '
                                             '# comment'),
                         'password = s3cr3t # comment')

    def test_double_sub(self):
        self.assertEqual(self.filters[0].sub('password = '
                                             '$DotSecrets: password$; '
                                             'security question = '
                                             '$DotSecrets: question$ '
                                             '# comment'),
                         'password = s3cr3t; security question = '
                         'h1dd3n 4g3nd4 # comment')

if __name__ == '__main__':
    unittest.main()
