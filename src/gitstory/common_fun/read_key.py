import os


# catches the key
def read_key(cur_folder) -> str:
    try:
        key_path = cur_folder + "/data/key.txt"
        with open(key_path, "r") as key_f:
            if os.path.getsize(key_path) > 250:
                raise ValueError(f"File {key_path} too large to be reasonable!")
            ret = key_f.read()
            return ret
    except:
        raise
