import json
import os
import getpass
from pathlib import Path
from PIL import Image
import InfiniteApi


def save_data(data: {}):
    filename = create_main_directory() + "/user.json"
    #print("filename : " +  filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def load_data() -> {}:
    filename = create_main_directory() + "/user.json"
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

    if os.path.exists(f"{document_path}/Infinite_data"):
        #print("main directory already exists")
        return str(Path(f"C:/Users/{username}/Documents/Infinite_data"))
    else:
        os.mkdir(Path(f"C:/Users/{username}/Documents/Infinite_data"))
        return str(Path(f"C:/Users/{username}/Documents/Infinite_data"))


def create_sub_directory():
    main_directory = Path(create_main_directory())
    if os.path.exists(f"{main_directory}/Medals"):
        #print("sub directory already exists")
        return str(Path(f"{main_directory}/Medals"))
    else:
        os.mkdir(Path(f"{main_directory}/Medals"))
        return str(Path(f"{main_directory}/Medals"))


def medal_exists_in_local(id_medal=None) -> bool:
    return os.path.exists(f"{create_sub_directory()}/{id_medal}.png")
      

def save_medal_in_local(id_medal=None,size=80):
    img_medal = InfiniteApi.url_to_image(InfiniteApi.medal_url(id_medal,size))
    if img_medal is not None and id_medal is not None:
        if not medal_exists_in_local(id_medal):
            img_medal.save(f"{create_sub_directory()}/{id_medal}.png")
            print("Saved medal in local")


def get_medal_from_local(id_medal=None,size=80):
    if id_medal is not None:
        if medal_exists_in_local(id_medal):
            return Image.open(f"{create_sub_directory()}/{id_medal}.png")
    save_medal_in_local(id_medal,size)
    return Image.open(f"{create_sub_directory()}/{id_medal}.png")




if __name__ == "__main__":
    """print(create_main_directory())
    print(create_sub_directory())
    print(load_data())"""
    #save_data({'.curim': {'gamertag': 'IceCurim'},'arthurias': {'gamertag': 'SirArthurias'}})
    #print(load_data())
    medal_exists_in_local(622331684)