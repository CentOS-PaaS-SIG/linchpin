

class RepositoryControl(object):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def list_files(self):
        pass

    @abstractmethod
    def fetch_files(self):
        pass
