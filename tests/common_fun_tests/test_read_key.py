from gitstory.common_fun.read_key import read_key
import os

def write_file(cur_folder, key):
    cur_folder = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isdir(cur_folder + "/data"):
        os.mkdir(cur_folder + "/data")
    key_path = cur_folder + "/data/key.txt"
    with open(key_path, "w") as key_f:
        key_f.write(key)
    

class TestReadKey:
    def test_basic_read:
        cwd = os.getcwd()
        write_file(cwd, "test")
        assert read_file(cwd) == "test"