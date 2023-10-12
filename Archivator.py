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
        tree, data_compressed = HuffmanAlgorythm.build_huffman_tree(
            data_uncompressed)
        bytes_array = Archivator.get_byte_array(data_compressed)
        return ArchiveData(name, bytes_array, tree)

    def get_byte_array(bit_string):
        while len(bit_string) % 8 != 0:
            bit_string += '0'
        # Конвертируем битовую строку в байтовую
        bytes_list = [int(bit_string[i:i+8], 2)
                      for i in range(0, len(bit_string), 8)]
        return bytes(bytes_list)

    def make_archive(path_to_old, path_to_folder_of_new, name):
        if os.path.exists(path_to_old) and os.path.exists(path_to_folder_of_new):
            os.mkdir(f"{path_to_folder_of_new}\\{name}.hfmn")
            archive_data = Archivator.get_archive_data(path_to_old)
            with open(f"{path_to_folder_of_new}\\{name}\\data.bin", "wb") as file:
                data = archive_data.data
                pickle.dump(data, file)

            with open(f"{path_to_folder_of_new}\\{name}\\data_to_unarchive.txt", "wb") as file:
                to_pickle = [archive_data.file_name, archive_data.tree]
                pickle.dump(to_pickle, file)

            #pickle.dump(Archivator.get_archive_data(path_to_old), file)
