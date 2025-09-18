class TeamDraftData:
    def __init__(self, name: str, bans: list[str], picks: list[str]):
        self.name = name
        self.bans = bans
        self.picks = picks
        assert len(self.bans) == 5, f"Incorrect length of bans: {self.bans}"
        assert len(self.picks) == 5, f"Incorrect length of picks: {self.picks}"


class DraftData:
    def __init__(self, blue: TeamDraftData, red: TeamDraftData):
        self.blue = blue
        self.red = red

    def get_order(self) -> list[str]:
        order = []
        for i in range(3):
            order.append(self.blue.bans[i])
            order.append(self.red.bans[i])
        order.append(self.blue.picks[0])
        order.append(self.red.picks[0])
        order.append(self.red.picks[1])
        order.append(self.blue.picks[1])
        order.append(self.blue.picks[2])
        order.append(self.red.picks[2])
        for i in range(3, 5):
            order.append(self.red.bans[i])
            order.append(self.blue.bans[i])
        order.append(self.red.picks[3])
        order.append(self.blue.picks[3])
        order.append(self.blue.picks[4])
        order.append(self.red.picks[4])
        return order
