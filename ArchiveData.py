class ArchiveData:
    def __init__(self, file_name : str, data : bytearray, tree):
        self.file_name = file_name
        self.data = data
        self.tree = tree