import requests
from PIL import Image
from io import BytesIO


def get_stat_player(pseudo):
    stat = requests.get(f"https://sr-nextjs.vercel.app/api/halodotapi?path=%2Fgames%2Fhalo-infinite%2Fstats%2Fmultiplayer%2Fplayers%2F{pseudo}%2Fservice-record%2Fmatchmade%3Ffilter%3Dall")
    result = stat.json()
    return result


def get_last_game_stat(pseudo):
    game_stat = requests.get(f"https://sr-nextjs.vercel.app/api/halodotapi?path=%2Fgames%2Fhalo-infinite%2Fstats%2Fmultiplayer%2Fplayers%2F{pseudo}%2Fmatches%3Ftype%3Dmatchmaking%26count%3D1%26offset%3D0")
    result = game_stat.json()["data"][0]
    return result


def get_last_game_medals_list(pseudo):
    game_stat = requests.get(f"https://sr-nextjs.vercel.app/api/halodotapi?path=%2Fgames%2Fhalo-infinite%2Fstats%2Fmultiplayer%2Fplayers%2F{pseudo}%2Fmatches%3Ftype%3Dmatchmaking%26count%3D1%26offset%3D0")
    result = game_stat.json()["data"][0]["player"]["stats"]["core"]["breakdown"]["medals"]
    return result


def medal_url(medal_id, size=80):
        return f"https://etxvqmdrjezgtwgueiar.supabase.co/storage/v1/render/image/public/assets/games/halo-infinite/metadata/multiplayer/medals/{medal_id}.png?width={size}&height={size}"


def url_to_image(url):
	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	return img