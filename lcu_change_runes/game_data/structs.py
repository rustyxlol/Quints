import attr

from lcu_change_runes.game_data.utils import remove_spaces


@attr.s(frozen=True, order=True)
class Champion:
    id: int = attr.ib(converter=int)
    name: str = attr.ib(converter=remove_spaces)


@attr.s()
class Champions:
    champions: list[Champion] = attr.ib(factory=list)

    def add(self, champion: Champion):
        self.champions.append(champion)

    def from_id(self, champ_id):
        for champion in self.champions:
            if champion.id == champ_id:
                return champion
        return None
        # return [champion for champion in self.champions if champion.id == champ_id]

    def from_name(self, name):
        for champion in self.champions:
            if champion.name.lower() == remove_spaces(name.lower()):
                return champion
        return None

    def all_champion_ids(self):
        return [champion.id for champion in self.champions]

    def all_champion_names(self):
        return [champion.name for champion in self.champions]


@attr.s(frozen=True)
class Rune:
    id: int = attr.ib(converter=int)
    name: str = attr.ib(converter=remove_spaces)


@attr.s()
class Runes:
    runes: list[Rune] = attr.ib(factory=list)

    def add(self, rune: Rune):
        self.runes.append(rune)

    def from_id(self, rune_id):
        return [rune for rune in self.runes if rune.id == rune_id]

    def from_name(self, name):
        return [
            rune
            for rune in self.runes
            if rune.name.lower() == remove_spaces(name.lower())
        ]

    def all_rune_ids(self):
        return [rune.id for rune in self.runes]

    def all_rune_names(self):
        return [rune.name for rune in self.runes]


@attr.s()
class RunePayLoad:
    name: str = attr.ib()
    primary: int = attr.ib()
    secondary: int = attr.ib()
    runes: list[int] = attr.ib()
    current: bool = attr.ib()
