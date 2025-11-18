from gitstory.common_fun.read_key import read_key
import os
import pytest
import shutil


# Gets the directory for a keyfile
@pytest.fixture
def test_cwd():
    return os.getcwd()


# Creates a keyfile for use in tests
@pytest.fixture
def key_file(test_cwd):
    madeFolder = False
    cur_folder = test_cwd
    data_path = cur_folder + "/data"
    if not os.path.isdir(data_path):
        madeFolder = True
        os.mkdir(data_path)
    f = open(data_path + "/key.txt", "w")
    f.close()
    yield data_path + "/key.txt"
    os.remove(data_path + "/key.txt")
    if madeFolder:
        shutil.rmtree(data_path, ignore_errors=True)


class TestReadKey:
    def test_basic_read(self, key_file, test_cwd):
        f = open(key_file, "w")
        f.write("test")
        f.close()
        assert read_key(test_cwd) == "test"

    def test_long_read(self, key_file, test_cwd):
        f = open(key_file, "w")
        for i in range(275):
            f.write("a")
        f.close()
        with pytest.raises(ValueError):
            read_key(test_cwd)

    def test_no_read(self, test_cwd):
        assert not os.path.isfile(test_cwd + "/data/key.txt")
        with pytest.raises(FileNotFoundError):
            read_key(test_cwd)
