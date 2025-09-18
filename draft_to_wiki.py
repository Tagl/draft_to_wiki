import argparse
import bs4
import requests_html

from draftlol import parse_draftlol
from drafterlol import parse_drafterlol

DRAFTLOL = "draftlol.dawe.gg"
DRAFTERLOL = "drafter.lol"

BLUE_TEAM = ["b", "blue", "left"]
RED_TEAM = ["r", "red", "right"]

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="Draft To Wiki",
        description="Takes as input a URL to draftlol.dawe.gg and converts the pick/ban process to the wiki format.",
    )
    argparser.add_argument("url")
    argparser.add_argument("--csv", action="store_true")
    argparser.add_argument("-w", "--winner")
    args = argparser.parse_args()

    url = args.url
    sess = requests_html.HTMLSession()
    r = sess.get(url)
    r.html.render(sleep=1)

    parser = bs4.BeautifulSoup(r.html.html, "html.parser")

    if DRAFTLOL in url:
        draft = parse_draftlol(parser)
    elif DRAFTERLOL in url:
        draft = parse_drafterlol(parser)
    else:
        raise NotImplementedError

    if args.csv:
        output = ",".join(draft.get_order())
    else:
        team_1_score = ""
        team_2_score = ""
        winner = ""
        if args.winner is not None:
            if args.winner.lower() in BLUE_TEAM:
                team_1_score = 1
                team_2_score = 0
                winner = 1
            elif args.winner.lower() in RED_TEAM:
                team_1_score = 0
                team_2_score = 1
                winner = 2
            else:
                raise ValueError

        output = f"""{{{{PicksAndBansS7|team1={draft.blue.name} |team2={draft.red.name}
|team1score={team_1_score} |team2score={team_2_score} |winner={winner}
|blueban1={draft.blue.bans[0]}     |red_ban1={draft.red.bans[0]}
|blueban2={draft.blue.bans[1]}     |red_ban2={draft.red.bans[1]}
|blueban3={draft.blue.bans[2]}     |red_ban3={draft.red.bans[2]}
|bluepick1={draft.blue.picks[0]}     |bluerole1=
                                           |red_pick1={draft.red.picks[0]}    |red_role1=
                                           |red_pick2={draft.red.picks[1]}    |red_role2=
|bluepick2={draft.blue.picks[1]}     |bluerole2=
|bluepick3={draft.blue.picks[2]}     |bluerole3=
                                           |red_pick3={draft.red.picks[2]}    |red_role3=
|blueban4={draft.blue.bans[3]}     |red_ban4={draft.red.bans[3]}
|blueban5={draft.blue.bans[4]}     |red_ban5={draft.red.bans[4]}
                                           |red_pick4={draft.red.picks[3]}    |red_role4=
|bluepick4={draft.blue.picks[3]}     |bluerole4=
|bluepick5={draft.blue.picks[4]}     |bluerole5=
                                           |red_pick5={draft.red.picks[4]}    |red_role5=
|game1=yes}}}}"""

    print(output)
