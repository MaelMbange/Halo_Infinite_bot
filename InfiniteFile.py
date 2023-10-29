import json
import os
import getpass
from pathlib import Path


def save_data(data: {}):
    filename = str(create_main_directory()) + "/user.json"
    #print("filename : " +  filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def load_data() -> {}:
    filename = str(create_main_directory()) + "/user.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    else:        
        with open(filename, 'w') as f:
            json.dump({".":{"gamertag":"."}}, f, indent=2)
            return {".":{"gamertag":"."}}
    

def create_main_directory():
    username = getpass.getuser()
    document_path = Path(f"C:/Users/{username}/Documents")

    if True if os.listdir(document_path).__contains__("Infinite_data") else False:
        return Path(f"C:/Users/{username}/Documents/Infinite_data")
    else:
        os.mkdir(Path(f"C:/Users/{username}/Documents/Infinite_data"))
        return Path(f"C:/Users/{username}/Documents/Infinite_data")


def create_sub_directory():
    main_directory = Path(create_main_directory())
    if True if os.listdir(main_directory).__contains__("Medals") else False:
        return Path(f"{main_directory}/Medals")
    else:
        os.mkdir(Path(f"{main_directory}/Medals"))
        return Path(f"{main_directory}/Medals")



if __name__ == "__main__":
    print(create_main_directory())
    print(create_sub_directory())
    print(load_data())
    #save_data({"test": "test"})
    #print(load_data())