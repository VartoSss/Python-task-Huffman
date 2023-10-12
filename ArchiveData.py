class ArchiveData:
    def __init__(self, file_name : str, data : bytearray, tree, counter_added_zeros):
        self.file_name = file_name
        self.data = data
        self.tree = tree
        self.counter_added_zeros = counter_added_zeros