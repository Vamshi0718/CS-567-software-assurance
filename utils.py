import random

class Player:
    def _init_(self, name, abilities=None):
        self.name = name
        self.max_health = 100
        self.health = self.max_health
        self.abilities = abilities if abilities else []
        self.inventory = {}
        self.total_damage_dealt = 0
        self.rounds_won = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} has been defeated!")
            return True
        return False

    def attack(self, other_player):
        damage = random.randint(10, 20)
        for ability in self.abilities:
            damage = ability.modify_damage(damage)
        defeated = other_player.take_damage(damage)
        self.total_damage_dealt += damage
        print(f"{self.name} attacked {other_player.name} for {damage} damage!")
        return defeated

    def pick_up_item(self, item):
        if item.name in self.inventory:
            self.inventory[item.name] += 1
        else:
            self.inventory[item.name] = 1
        print(f"{self.name} picked up {item.name}.")

    def show_inventory(self):
        if self.inventory:
            print(f"{self.name}'s Inventory:")
            for item, quantity in self.inventory.items():
                print(f"{item}: {quantity}")
        else:
            print(f"{self.name}'s Inventory is empty.")

    def use_item(self, item_name, other_player=None):
        if item_name in self.inventory:
            item = self.inventory[item_name]
            if isinstance(item, Consumable):
                item.apply(self)
                del self.inventory[item_name]
            elif isinstance(item, Usable):
                item.use(other_player)
            else:
                print(f"{self.name} can't use {item_name}.")
        else:
            print(f"{self.name} doesn't have {item_name} in their inventory.")

    def use_ability(self, ability, other_player):
        if ability.name in [ab.name for ab in self.abilities]:
            ability.activate(self, other_player)
        else:
            print(f"{self.name} doesn't have the {ability.name} ability.")

    def reset_health(self):
        self.health = self.max_health

class Ability:
    def _init_(self, name):
        self.name = name

    def modify_damage(self, damage):
        return damage

    def activate(self, player, other_player):
        pass

class ShieldAbility(Ability):
    def _init_(self):
        super()._init_("Shield")

    def modify_damage(self, damage):
        return damage - random.randint(5, 10)

class CriticalStrikeAbility(Ability):
    def _init_(self):
        super()._init_("Critical Strike")

    def modify_damage(self, damage):
        return damage + random.randint(5, 10)

class Item:
    def _init_(self, name):
        self.name = name

class Consumable(Item):
    def _init_(self, name):
        super()._init_(name)

    def apply(self, player):
        pass

class HealthPotion(Consumable):
    def _init_(self):
        super()._init_("Health Potion")

    def apply(self, player):
        player.health += random.randint(10, 20)
        player.health = min(player.health, player.max_health)
        print(f"{player.name} used a Health Potion and restored health.")

class Usable(Item):
    def _init_(self, name):
        super()._init_(name)

    def use(self, other_player):
        pass

class Ammunition(Usable):
    def _init_(self):
        super()._init_("Ammunition")

    def use(self, other_player):
        damage_boost = random.randint(5, 10)
        other_player.take_damage(damage_boost)
        print(f"{other_player.name} was hit by {self.name} for {damage_boost} damage.")

class Game:
    def _init_(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play_round(self):
        print("\n--- New Round ---")
        player1_defeated = self.player1.attack(self.player2)
        if not player1_defeated:
            player2_defeated = self.player2.attack(self.player1)
            if not player2_defeated:
                self.player1.pick_up_item(Ammunition())
                self.player2.pick_up_item(HealthPotion())
                self.player1.show_inventory()
                self.player2.show_inventory()
                self.player1.use_item("Health Potion")
                self.player2.use_item("Ammunition", self.player1)

    def play_game(self, rounds=3):
        for round_number in range(1, rounds + 1):
            print(f"\n--- Round {round_number} ---")
            self.play_round()
            if self.player1.health <= 0:
                print(f"{self.player2.name} wins the round!")
                self.player2.rounds_won += 1
                break
            elif self.player2.health <= 0:
                print(f"{self.player1.name} wins the round!")
                self.player1.rounds_won += 1
                break
            else:
                self.player1.reset_health()
                self.player2.reset_health()
        else:
            print("--- Game Over ---")
            if self.player1.rounds_won > self.player2.rounds_won:
                print(f"{self.player1.name} wins the game!")
            elif self.player2.rounds_won > self.player1.rounds_won:
                print(f"{self.player2.name} wins the game!")
            else:
                print("It's a tie!")

def main():
    player1 = Player("Player 1", abilities=[ShieldAbility()])
    player2 = Player("Player 2", abilities=[CriticalStrikeAbility()])

    game = Game(player1, player2)
    game.play_game()

if _name_ == "_main_":
    main()