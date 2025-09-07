import argparse
import bs4
import requests_html


def get_picks_from_column(column):
    return [x.get_text() for x in column.find_all(class_="roomChampName")]


def get_bans_from_row(row):
    return [
        x.find("img", alt=True)["alt"] for x in row.find_all(class_="banChampContainer")
    ]


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="Draft To Wiki",
        description="Takes as input a URL to draftlol.dawe.gg and converts the pick/ban process to the wiki format.",
    )
    argparser.add_argument("url")
    args = argparser.parse_args()

    sess = requests_html.HTMLSession()
    r = sess.get(args.url)
    r.html.render(sleep=1)

    parser = bs4.BeautifulSoup(r.html.html, "html.parser")
    blue_picks_column = parser.find(class_="roomPickColumn blue")
    red_picks_column = parser.find(class_="roomPickColumn red")
    blue_bans_row = parser.find(class_="roomBanRow blue")
    red_bans_row = parser.find(class_="roomBanRow red")

    blue_picks = get_picks_from_column(blue_picks_column)
    red_picks = get_picks_from_column(red_picks_column)
    blue_bans = get_bans_from_row(blue_bans_row)
    red_bans = get_bans_from_row(red_bans_row)

    team_names = parser.find_all(class_="roomTeamName")
    blue_team_name = team_names[0].get_text()
    red_team_name = team_names[1].get_text()

    output = f"""{{PicksAndBansS7|team1={blue_team_name} |team2={red_team_name} |team1score= |team2score= |winner= 
|blueban1={blue_bans[0]}     |red_ban1={red_bans[0]}
|blueban2={blue_bans[1]}     |red_ban2={red_bans[1]}
|blueban3={blue_bans[2]}     |red_ban3={red_bans[2]}
|bluepick1={blue_picks[0]}     |bluerole1=
                                           |red_pick1={red_picks[0]}    |red_role1=
                                           |red_pick2={red_picks[1]}    |red_role2=
|bluepick2={blue_picks[1]}     |bluerole2=
|bluepick3={blue_picks[2]}     |bluerole3=
                                           |red_pick3={red_picks[2]}    |red_role3=
|blueban4={blue_bans[3]}     |red_ban4={red_bans[3]}
|blueban5={blue_bans[4]}     |red_ban5={red_bans[4]}
                                           |red_pick4={red_picks[3]}    |red_role4=
|bluepick4={blue_picks[3]}     |bluerole4=
|bluepick5={blue_picks[4]}     |bluerole5=
                                           |red_pick5={red_picks[4]}    |red_role5=
|game1=yes}}"""

    print(output)
