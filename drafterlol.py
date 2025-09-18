import re

from data_dragon import champ_id_to_name
from draft_data import DraftData, TeamDraftData


def get_picks_from_drafterlol_column(column) -> list[str]:
    return [x.get_text() for x in column.find_all(class_="text")]


def get_bans_from_drafterlol_row(row) -> list[str]:
    result = []
    for x in row.find_all(
        class_="w-full h-full absolute flex items-center overflow-hidden bg-card"
    ):
        image = x.find("img")
        image_url = image["src"]
        champ_id = int(re.search(r"(\d+).png", image_url).group(1))
        champ_name = champ_id_to_name[champ_id]
        result.append(champ_name)
    return result


def parse_drafterlol(parser) -> DraftData:
    blue_team_name = parser.find(class_="text-blueRole").get_text().strip()
    red_team_name = parser.find(class_="text-redRole").get_text().strip()

    pick_columns = parser.find_all(
        class_="flex flex-1 flex-col items-stretch w-full select-none"
    )
    blue_picks_column = pick_columns[0]
    red_picks_column = pick_columns[1]

    blue_bans_row = parser.find(
        class_="flex pointer-events-none gap-1 h-full w-full false"
    )
    red_bans_row = parser.find(
        class_="flex pointer-events-none gap-1 h-full w-full justify-end"
    )

    blue_team = TeamDraftData(
        blue_team_name,
        get_bans_from_drafterlol_row(blue_bans_row),
        get_picks_from_drafterlol_column(blue_picks_column),
    )

    red_team = TeamDraftData(
        red_team_name,
        get_bans_from_drafterlol_row(red_bans_row),
        get_picks_from_drafterlol_column(red_picks_column),
    )

    return DraftData(blue_team, red_team)
