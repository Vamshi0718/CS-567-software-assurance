import unittest
from unittest.mock import patch, MagicMock

from main import Player, Game, Ability, ShieldAbility, CriticalStrikeAbility, HealthPotion, Ammunition

class TestPlayer(unittest.TestCase):
    def test_take_damage(self):
        player = Player("TestPlayer")
        player.take_damage(30)
        self.assertEqual(player.health, 70)

    def test_attack(self):
        player1 = Player("Attacker", abilities=[CriticalStrikeAbility()])
        player2 = Player("Defender")
        player1.attack(player2)
        self.assertGreater(player2.health, 0)
        self.assertGreater(player1.total_damage_dealt, 0)

    def test_ability_modify_damage(self):
        player1 = Player("Attacker", abilities=[CriticalStrikeAbility()])
        player2 = Player("Defender")
        ability = CriticalStrikeAbility()
        damage_before = 15
        damage_after = ability.modify_damage(damage_before)
        self.assertGreater(damage_after, damage_before)

    def test_pick_up_item(self):
        player = Player("TestPlayer")
        player.pick_up_item(HealthPotion())
        self.assertIn("Health Potion", player.inventory)

    def test_show_inventory(self):
        player = Player("TestPlayer")
        player.pick_up_item(HealthPotion())
        player.pick_up_item(Ammunition())
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            player.show_inventory()
            expected_output = "TestPlayer's Inventory:\nHealth Potion: 1\nAmmunition: 1"
            mock_stdout.assert_called_with(expected_output)

    def test_use_health_potion(self):
        player1 = Player("User")
        player1.pick_up_item(HealthPotion())
        initial_health = player1.health
        player1.use_item("Health Potion")
        self.assertGreater(player1.health, initial_health)

    def test_use_ammunition(self):
        player1 = Player("User")
        player2 = Player("OtherPlayer")
        player1.pick_up_item(Ammunition())
        initial_health = player2.health
        player1.use_item("Ammunition", player2)
        self.assertLess(player2.health, initial_health)

    # Add more tests as needed...

class TestGame(unittest.TestCase):
    def test_play_round(self):
        player1 = Player("Player 1")
        player2 = Player("Player 2")
        game = Game(player1, player2)
        game.play_round()
        # Add assertions for the round outcome

    def test_play_game(self):
        player1 = Player("Player 1")
        player2 = Player("Player 2")
        game = Game(player1, player2)
        game.play_game()
        # Add assertions for the game outcome

if _name_ == '_main_':
    unittest.main()