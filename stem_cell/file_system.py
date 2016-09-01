import os
import stat


class FileSystem(object):
    def write_file(self, file_name, contents):
        self.write_close_and_set_permissions(contents, file_name)

    def write_close_and_set_permissions(self, contents, file_name):
        self.write_and_close(contents, self.file_handle(file_name))
        self.chmod_to_owner_read_only(file_name)

    def chmod_to_owner_read_only(self, file_name):
        os.chmod(file_name, stat.S_IRUSR)

    def write_and_close(self, contents, file_handle):
        file_handle.write(contents)
        file_handle.close()

    def file_handle(self, file_name):
        return open(file_name, 'w')
