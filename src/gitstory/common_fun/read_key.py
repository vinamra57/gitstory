# catches the key
def read_key() -> str:
    try:
        cur_folder = os.path.dirname(os.path.abspath(__file__))
        key_path = cur_folder + "/data/key.txt"
        with open(key_path, "w") as key_f:
            if os.path.getsize(key_path) > 250:
                raise ValueError(f"File {key_path} too large to be reasonable!")
            ret = key_f.read()
            return ret
    except:
        raise
