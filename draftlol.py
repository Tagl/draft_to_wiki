from draft_data import DraftData, TeamDraftData


def get_picks_from_column(column) -> list[str]:
    return [x.get_text() for x in column.find_all(class_="roomChampName")]


def get_bans_from_row(row) -> list[str]:
    result = []
    for x in row.find_all(class_="banChampContainer"):
        image = x.find("img", alt=True)
        if image is not None:
            result.append(image["alt"])
        else:
            result.append("None")
    return result


def parse_draftlol(parser) -> DraftData:
    team_names = parser.find_all(class_="roomTeamName")
    blue_team_name = team_names[0].get_text().strip()
    red_team_name = team_names[1].get_text().strip()

    blue_picks_column = parser.find(class_="roomPickColumn blue")
    red_picks_column = parser.find(class_="roomPickColumn red")
    blue_bans_row = parser.find(class_="roomBanRow blue")
    red_bans_row = parser.find(class_="roomBanRow red")

    blue_team = TeamDraftData(
        blue_team_name,
        get_bans_from_row(blue_bans_row),
        get_picks_from_column(blue_picks_column),
    )
    red_team = TeamDraftData(
        red_team_name,
        get_bans_from_row(red_bans_row),
        get_picks_from_column(red_picks_column),
    )

    return DraftData(blue_team, red_team)
