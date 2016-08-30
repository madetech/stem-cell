import sys
import unittest

sys.path.append('..')

from stem_cell.differentiator import Differentiator


class VersionControlSystemMock:
    def __init__(self):
        self.cloned_urls = []
        self.clone_path = ''

    def clone(self, url):
        self.cloned_urls.append(url)
        return self.clone_path

    def has_cloned_url(self, url):
        return url in self.cloned_urls

    def set_clone_path(self, clone_path):
        self.clone_path = clone_path


class MockUserDataGateway:
    def __init__(self):
        self.version_control_url = ''
        self.version_control_token = ''

    def set_version_control_url(self, url):
        self.version_control_url = url

    def get_version_control_url(self):
        return self.version_control_url

    def get_version_control_token(self):
        return self.version_control_token

    def set_version_control_token(self, token):
        self.version_control_token = token


class AnsibleSpy:
    def __init__(self):
        self.playbooks_used = []

    def was_run_with_playbook(self, playbook):
        return playbook in self.playbooks_used

    def run_playbook(self, playbook):
        self.playbooks_used.append(playbook)


class TestDifferentiate(unittest.TestCase):
    def setUp(self):
        self.user_data_gateway = MockUserDataGateway()
        self.version_control_system = VersionControlSystemMock()
        self.ansible = AnsibleSpy()
        self.differentiator = Differentiator(self.user_data_gateway, self.version_control_system, self.ansible)

    def assert_version_control_system_has_cloned_url(self, version_control_url):
        self.assertTrue(self.version_control_system.has_cloned_url(version_control_url))

    def testGivenAVersionControlUrl_ThenClonesThatRepository(self):
        self.user_data_gateway.set_version_control_url("http://example.com/expected/git/repo.git")
        self.differentiator.differentiate()
        self.assert_version_control_system_has_cloned_url("http://example.com/expected/git/repo.git")

    def testGivenADifferentVersionControlUrl_ThenClonesThatRepository(self):
        self.user_data_gateway.set_version_control_url("http://madetech.com/expected/git/repo.git")
        self.differentiator.differentiate()
        self.assert_version_control_system_has_cloned_url("http://madetech.com/expected/git/repo.git")

    def testGivenAnOAuthToken_ThenIncludesInUrl(self):
        self.user_data_gateway.set_version_control_url("http://madetech.com/expected/git/repo.git")
        self.user_data_gateway.set_version_control_token("ABCDE")
        self.differentiator.differentiate()
        self.assert_version_control_system_has_cloned_url("http://ABCDE@madetech.com/expected/git/repo.git")

    def testThatItRunsAnsibleAgainstDifferentiateYml(self):
        self.user_data_gateway.set_version_control_url("http://madetech.com/expected/git/repo.git")
        self.user_data_gateway.set_version_control_token("ABCDE")
        self.version_control_system.set_clone_path('/home/ec2-user/stem-cell/repo')
        self.differentiator.differentiate()
        self.assertTrue(self.ansible.was_run_with_playbook('/home/ec2-user/stem-cell/repo/main.yml'))

    def testThatItRunsAnsibleAgainstDifferentiateYml2(self):
        self.user_data_gateway.set_version_control_url("http://madetech.com/expected/git/repo-simple.git")
        self.user_data_gateway.set_version_control_token("ABCDE")
        self.version_control_system.set_clone_path('/home/ec2-user/stem-cell/repo-simple')
        self.differentiator.differentiate()
        self.assertTrue(self.ansible.was_run_with_playbook('/home/ec2-user/stem-cell/repo-simple/main.yml'))
