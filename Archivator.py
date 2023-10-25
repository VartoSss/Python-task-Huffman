import os
from ArchiveData import ArchiveData
from HuffmanAlgorythm import HuffmanAlgorythm
import pickle
import binascii


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
        bytes_array, counter_added_zeros = Archivator.get_byte_array(data_compressed)
        return ArchiveData(name, bytes_array, tree, counter_added_zeros)

    def get_byte_array(bit_string):
        counter_added_zeros = 0
        while len(bit_string) % 8 != 0:
            bit_string += '0'
            counter_added_zeros += 1
            
        # Конвертируем битовую строку в байтовую
        bytes_list = [int(bit_string[i:i+8], 2)
                      for i in range(0, len(bit_string), 8)]
        return bytes(bytes_list), counter_added_zeros

    def make_archive(path_to_old, path_to_folder_of_new, name):
        if os.path.exists(path_to_old) and os.path.exists(path_to_folder_of_new):
            path_to_folder_of_new = f"{path_to_folder_of_new}\\{name}.hfmn"
            os.mkdir(path_to_folder_of_new)
            archive_data = Archivator.get_archive_data(path_to_old)
            with open(f"{path_to_folder_of_new}\\data.bin", "wb") as file:
                data = archive_data.data
                file.write(data)

            with open(f"{path_to_folder_of_new}\\data_to_unarchive.txt", "wb") as file:
                to_pickle = [archive_data.file_name, archive_data.tree, archive_data.counter_added_zeros]
                pickle.dump(to_pickle, file)

    def unarchive(path_to_archive, path_to_save):
        with open(f"{path_to_archive}\\data.bin", "rb") as data_file:
            binary_data = data_file.read()

        binary_string = bin(int(binascii.hexlify(binary_data), 16))[2:]
        with open(f"{path_to_archive}\\data_to_unarchive.txt", "rb") as name_tree_file:
            name_tree = pickle.load(name_tree_file)
        name = name_tree[0]
        tree = name_tree[1]
        counter_added_zeros = name_tree[2]
        if (counter_added_zeros != 0):
            binary_string = binary_string[:-counter_added_zeros]
        result = Archivator.decode(tree, binary_string)
        with open(f"{path_to_save}\\{name}", "w") as result_file:
            result_file.write(result)

    def decode(root, binary_string):
        ans = []
        if HuffmanAlgorythm.is_leaf(root):
            while root.freq > 0:
                ans.append(root.ch)
                root.freq = root.freq - 1
        else:
            index = -1
            while index < len(binary_string) - 1:
                index = HuffmanAlgorythm.decode(
                    root, index, binary_string, ans)
        result = ''.join(ans)
        return result
