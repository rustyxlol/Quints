import unittest

from attr.exceptions import FrozenInstanceError

from lcu_change_runes.game_data.structs import Champion, Champions, Rune, Runes


class TestChampion(unittest.TestCase):
    def setUp(self):
        self.annie = Champion(1, "Annie")
        self.anivia = Champion("2", "Anivia")
        self.masteryi = Champion(3, "Master Yi")

    def test_champion_name(self):
        self.assertEqual(self.annie.name, "Annie")
        self.assertEqual(self.masteryi.name, "MasterYi")

    def test_champion_id(self):
        self.assertEqual(self.annie.id, 1)
        self.assertEqual(self.anivia.id, 2)

    def test_mutability(self):
        with self.assertRaises(FrozenInstanceError):
            self.masteryi.id = 10


class TestChampions(unittest.TestCase):
    def setUp(self):
        self.annie = Champion(1, "Annie")
        self.asol = Champion("2", "Aurelion Sol")
        self.champions = Champions([self.annie, self.asol])

    def test_champions(self):
        self.assertEqual(
            self.champions,
            Champions([Champion(1, "Annie"), Champion("2", "Aurelion Sol")]),
        )

    def test_from_id(self):
        self.assertEqual(self.champions.from_id(1), self.annie)
        self.assertEqual(self.champions.from_id(2), self.asol)

        self.assertEqual(self.champions.from_id(20), None)

    def test_from_name(self):
        self.assertEqual(self.champions.from_name("Annie"), self.annie)
        self.assertEqual(self.champions.from_name("annie"), self.annie)
        self.assertEqual(self.champions.from_name("Aurelion Sol"), self.asol)

        self.assertEqual(self.champions.from_name("Random Champion"), None)

    def test_all_champion_ids(self):
        self.assertEqual(self.champions.all_champion_ids(), [1, 2])

    def test_all_champion_names(self):
        self.assertEqual(self.champions.all_champion_names(), ["Annie", "AurelionSol"])

    def test_mutability(self):
        self.champions.add(Champion(3, "Alistar"))

        self.assertEqual(self.champions.from_id(3), Champion(3, "Alistar"))


class TestRune(unittest.TestCase):
    def setUp(self):
        self.triumph = Rune(5000, "Triumph")
        self.cdg = Rune("8000", "Coup De Grace")

    def test_rune_name(self):
        self.assertEqual(self.triumph.name, "Triumph")
        self.assertEqual(self.cdg.name, "CoupDeGrace")

    def test_rune_id(self):
        self.assertEqual(self.triumph.id, 5000)
        self.assertEqual(self.cdg.id, 8000)

    def test_mutability(self):
        with self.assertRaises(FrozenInstanceError):
            self.triumph.id = 8001


class TestRunes(unittest.TestCase):
    def setUp(self):
        self.triumph = Rune(1, "Triumph")
        self.cdg = Rune("2", "Coup De Grace")
        self.runes = Runes([self.triumph, self.cdg])

    def test_runes(self):
        self.assertEqual(
            self.runes,
            Runes([Rune(1, "Triumph"), Rune("2", "CoupDeGrace")]),
        )

    def test_from_id(self):
        self.assertEqual(self.runes.from_id(1), self.triumph)
        self.assertEqual(self.runes.from_id(2), self.cdg)

        self.assertEqual(self.runes.from_id(20), None)

    def test_from_name(self):
        self.assertEqual(self.runes.from_name("Triumph"), self.triumph)
        self.assertEqual(self.runes.from_name("Triumph"), self.triumph)
        self.assertEqual(self.runes.from_name("CoupDeGrace"), self.cdg)

        self.assertEqual(self.runes.from_name("Random Rune"), None)

    def test_all_rune_ids(self):
        self.assertEqual(self.runes.all_rune_ids(), [1, 2])

    def test_all_rune_names(self):
        self.assertEqual(self.runes.all_rune_names(), ["Triumph", "CoupDeGrace"])

    def test_mutability(self):
        self.runes.add(Rune(3, "Conquerer"))

        self.assertEqual(self.runes.from_id(3), Rune(3, "Conquerer"))


if __name__ == "__main__":
    unittest.main()
