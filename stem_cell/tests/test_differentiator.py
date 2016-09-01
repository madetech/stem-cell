import sys
import unittest

sys.path.append('..')

from stem_cell.differentiator import Differentiator


class VersionControlSystemMock:
    def __init__(self):
        self.cloned_urls = []
        self.clone_path = ''
        self.private_keys_used = []

    def clone(self, url):
        self.cloned_urls.append(url)
        return self.clone_path

    def clone_with_private_key(self, url, private_key_path):
        self.clone(url)
        self.private_keys_used.append(private_key_path)
        return self.clone_path

    def has_cloned_url(self, url):
        return url in self.cloned_urls

    def has_cloned_url_with_private_key(self, private_key, url):
        return self.has_cloned_url(url) and private_key in self.private_keys_used


class MockUserDataGateway:
    def __init__(self):
        self._version_control_url = ''
        self._version_control_token = ''
        self._version_control_private_key = ''

    @property
    def version_control_url(self):
        return self._version_control_url

    @version_control_url.setter
    def version_control_url(self, url):
        self._version_control_url = url

    @property
    def version_control_token(self):
        return self._version_control_token

    @version_control_token.setter
    def version_control_token(self, token):
        self._version_control_token = token

    @property
    def version_control_private_key(self):
        return self._version_control_private_key

    @version_control_private_key.setter
    def version_control_private_key(self, private_key):
        self._version_control_private_key = private_key


class AnsibleSpy:
    def __init__(self):
        self.playbooks_used = []

    def was_run_with_playbook(self, playbook):
        return playbook in self.playbooks_used

    def run_playbook(self, playbook):
        self.playbooks_used.append(playbook)


class FileGatewayMock:
    def __init__(self):
        self._file_contents = {}

    def write_file(self, file_name, contents):
        self._file_contents[file_name] = contents

    def file_contents(self, file_name):
        return self._file_contents[file_name]


class TestDifferentiate(unittest.TestCase):
    def setUp(self):
        self.ssh_repository_url = "git@github.com:madetech/repo-simple.git"
        self.user_data_gateway = MockUserDataGateway()
        self.version_control_system = VersionControlSystemMock()
        self.ansible = AnsibleSpy()
        self.file_gateway = FileGatewayMock()
        self.differentiator = Differentiator(self.user_data_gateway,
                                             self.version_control_system,
                                             self.ansible,
                                             self.file_gateway)

    def assert_version_control_system_has_cloned_url(self, version_control_url):
        self.assertTrue(self.version_control_system.has_cloned_url(version_control_url))

    def assert_cloned_url_with_private_key(self, private_key, repository_url):
        self.assertTrue(self.version_control_system.has_cloned_url_with_private_key(private_key, repository_url))

    def assert_file_contains_contents(self, expected_file_name, contents):
        self.assertEquals(self.file_gateway.file_contents(expected_file_name), contents)

    def testGivenAVersionControlUrl_ThenClonesThatRepository(self):
        self.user_data_gateway.version_control_url = "http://example.com/expected/git/repo.git"
        self.differentiator.differentiate()
        self.assert_version_control_system_has_cloned_url("http://example.com/expected/git/repo.git")

    def testGivenADifferentVersionControlUrl_ThenClonesThatRepository(self):
        self.user_data_gateway.version_control_url = "http://madetech.com/expected/git/repo.git"
        self.differentiator.differentiate()
        self.assert_version_control_system_has_cloned_url("http://madetech.com/expected/git/repo.git")

    def testGivenAnOAuthToken_ThenIncludesInUrl(self):
        self.user_data_gateway.version_control_url = "http://madetech.com/expected/git/repo.git"
        self.user_data_gateway.version_control_token = "ABCDE"
        self.differentiator.differentiate()
        self.assert_version_control_system_has_cloned_url("http://ABCDE@madetech.com/expected/git/repo.git")

    def testThatItRunsAnsibleAgainstDifferentiateYml(self):
        self.user_data_gateway.version_control_url = "http://madetech.com/expected/git/repo.git"
        self.user_data_gateway.version_control_token = "ABCDE"
        self.version_control_system.clone_path = '/home/ec2-user/stem-cell/repo'
        self.differentiator.differentiate()
        self.assertTrue(self.ansible.was_run_with_playbook('/home/ec2-user/stem-cell/repo/main.yml'))

    def testThatItRunsAnsibleAgainstDifferentiateYml2(self):
        self.user_data_gateway.version_control_url = "http://madetech.com/expected/git/repo-simple.git"
        self.user_data_gateway.version_control_token = "ABCDE"
        self.version_control_system.clone_path = '/home/ec2-user/stem-cell/repo-simple'
        self.differentiator.differentiate()
        self.assertTrue(self.ansible.was_run_with_playbook('/home/ec2-user/stem-cell/repo-simple/main.yml'))

    def testGivenAnSshKey_ThenCreatesFile(self):
        self.user_data_gateway.version_control_url = self.ssh_repository_url
        private_key = '''
-----BEGIN RSA PRIVATE KEY-----
qwerty
-----END RSA PRIVATE KEY-----
'''
        self.user_data_gateway.version_control_private_key = private_key

        self.differentiator.differentiate()

        self.assert_file_contains_contents('/tmp/key.pem', private_key)
        self.assert_cloned_url_with_private_key('/tmp/key.pem', self.ssh_repository_url)
