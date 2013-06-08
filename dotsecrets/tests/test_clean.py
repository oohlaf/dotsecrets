import unittest

from dotsecrets.clean import CleanSecret


class TestCleanSecret(unittest.TestCase):

    def setUp(self):
        self.secrets = []
        self.secrets.append(CleanSecret('passwd',
            r'password(\s*)=(\s*)(?#UpToHash)',
            r'password\1=\2(?#Key)',
            'Mutt passwords',
            True))
        self.secrets.append(CleanSecret('passwd',
            r'password(\s*)=(\s*)(?#QuotedString)',
            r'password\1=\2(?#Key)',
            'Mutt passwords',
            True))
        self.secrets.append(CleanSecret('abc',
            r'password(\s*)=(\s*)(?#DoesNotExist)',
            r'password\1=\2(?#Key)',
            'Mutt passwords',
            True))

    def test_state(self):
        """Test getting and setting state"""
        state = self.secrets[0].__getstate__()
        other_secret = CleanSecret('', '', '')
        other_secret.__setstate__(state)
        self.assertEqual(self.secrets[0].__dict__, other_secret.__dict__)

    def test_regex_sub(self):
        """Test regex substitution with predefined short cuts"""
        self.assertEqual(self.secrets[0].regex.pattern,
                r'password(\s*)=(\s*)([^\s#]+(?:[ \t\v\f]*[^\s#]+)+)')
        self.assertEqual(self.secrets[1].regex.pattern,
                r'password(\s*)=(\s*)("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')')
        self.assertEqual(self.secrets[2].regex.pattern,
                r'password(\s*)=(\s*)(?#DoesNotExist)')

    def test_sub_uth_no_match(self):
        """Test uptohash copy line on no match"""
        line = 'paaasword = df35@$^%ds'
        out = self.secrets[0].sub(line)
        self.assertEqual(out, line)

    def test_sub_uth_single_match(self):
        """Test uptohash single match"""
        line = 'password =   df35@$^%ds'
        out = self.secrets[0].sub(line)
        self.assertEqual(out, 'password =   $DotSecrets: passwd_1$')

    def test_sub_uth_single_match_comment(self):
        """Test uptohash single match with comment"""
        line = 'password =   df35@$^%ds    # comment'
        out = self.secrets[0].sub(line)
        self.assertEqual(out, 'password =   $DotSecrets: passwd_1$    # comment')

    def test_sub_uth_single_match_inside_comment(self):
        """Test uptohash single match inside comment"""
        line = '#password =   df35@$^%ds    # comment'
        out = self.secrets[0].sub(line)
        self.assertEqual(out, '#password =   $DotSecrets: passwd_1$    # comment')

    def test_sub_uth_double_match_in_comment(self):
        """Test uptohash one match before comment, other match inside comment"""
        line = 'password =   df35@$^%ds    # comment password = qsd&t63 # comment'
        out = self.secrets[0].sub(line)
        self.assertEqual(out, 'password =   $DotSecrets: passwd_1$    # comment password = $DotSecrets: passwd_2$ # comment')

    def test_sub_qs_single_match(self):
        """Test quotedstring single match two times"""
        line = 'password = "df35@$^%ds"'
        out = self.secrets[1].sub(line)
        self.assertEqual(out, 'password = $DotSecrets: passwd_1$')
        line = "password = 'df35@$^%ds'"
        out = self.secrets[1].sub(line)
        self.assertEqual(out, 'password = $DotSecrets: passwd_2$')

    def test_sub_qs_single_match_inner_dquotes(self):
        """Test quotedstring single match with inner double quotes"""
        line = 'password = "df35\\"@\\"$^%ds"'
        out = self.secrets[1].sub(line)
        self.assertEqual(out, 'password = $DotSecrets: passwd_1$')

    def test_sub_qs_single_match_inner_squotes(self):
        """Test quotedstring single match with inner single quotes"""
        line = 'password = "df35\'@\'$^%ds"'
        out = self.secrets[1].sub(line)
        self.assertEqual(out, 'password = $DotSecrets: passwd_1$')


if __name__ == '__main__':
    unittest.main()
