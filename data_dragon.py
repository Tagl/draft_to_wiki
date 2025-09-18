import urllib.request

from json import loads


def get_current_lol_version() -> str:
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    response = urllib.request.urlopen(url).read().decode("utf-8")
    obj = loads(response)
    return obj[0]


DDVERSION = get_current_lol_version()


def get_champion_data():
    url = (
        "https://ddragon.leagueoflegends.com/cdn/%s/data/en_US/champion.json"
        % DDVERSION
    )
    response = urllib.request.urlopen(url).read().decode("utf-8")
    obj = loads(response)
    return obj


obj = get_champion_data()
# NOTE: ID and KEY are swapped in json, key in json is numerical id, id is string
champ_id_to_name = {int(v["key"]): v["name"] for k, v in obj["data"].items()}
champ_id_to_key = {int(v["key"]): v["id"] for k, v in obj["data"].items()}
champ_key_to_name = {
    champ_id_to_key[i]: champ_id_to_name[i] for i in champ_id_to_name.keys()
}
