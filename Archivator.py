import os
from ArchiveData import ArchiveData
from HuffmanAlgorythm import HuffmanAlgorythm
import pickle

class Archivator:
    def get_data_from_file(path_to_file):
        with open(path_to_file, "r") as file:
            data = file.read()
        return data
    
    def get_file_name(path_to_file):
        return os.path.basename(path_to_file)
    
    def get_archive_data(path_to_file):
        name = Archivator.get_file_name(path_to_file)
        data_uncompressed = Archivator.get_data_from_file(path_to_file)
        tree, data_compressed = HuffmanAlgorythm.build_huffman_tree(data_uncompressed)
        bytes_array = Archivator.get_byte_array(data_compressed)
        return ArchiveData(name, data_compressed, tree)
    
    
    def get_byte_array(bit_string):
        while len(bit_string) % 8 != 0:
            bit_string += '0'
        # Конвертируем битовую строку в байтовую
        bytes_list = [int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8)]
        return bytes(bytes_list)
    
    def make_archive(archive_data, path_to_folder, name):
        with open(f"{path_to_folder}/{name}.hfmn", "wb") as file:
            pickle.dump(archive_data)