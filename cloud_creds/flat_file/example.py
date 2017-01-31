import utils


class Example:
    def __init__(self):
        pass

    def search_creds(self, path, name, profile=None):
        # resolves by name
        for file_path in utils.list_files(path):
            if name == file_path.split("/").strip(".yml").strip(".yaml"):
                return file_path
        # if not found by name searches each profile in the file

    def get_creds(self):
        pass

    def get_default_creds(self):
        pass
