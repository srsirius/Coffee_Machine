from dataclasses import dataclass


class CoffeeMachine:
    class State:
        MAIN = "main"
        BUY = "buy"
        FILL_WATER = "fill_water"
        FILL_MILK = "fill_milk"
        FILL_BEANS = "fill_beans"
        FILL_CUPS = "fill_cups"
        EXIT = "exit"

    @dataclass
    class Drink:
        name: str
        water: int
        milk: int
        beans: int
        cups: int
        money: int

    def __init__(self):
        self.state = self.State.MAIN
        self.water = 400
        self.milk = 540
        self.coffee_beans = 120
        self.cups = 9
        self.money = 550
        self.DRINKS = {
            '1': self.Drink(name="espresso", water=250, milk=0, beans=16, cups=1, money=4),
            '2': self.Drink(name="latte", water=350, milk=75, beans=20, cups=1, money=7),
            '3': self.Drink(name="cappuccino", water=200, milk=100, beans=12, cups=1, money=6)}

    def __repr__(self):
        return (
            f"CoffeeMachine(state={self.state!r}, "
            f"water={self.water}, milk={self.milk}, "
            f"beans={self.coffee_beans}, cups={self.cups}, "
            f"money={self.money})"
        )

    def _check_resources(self, w: int, m: int, b: int, cups_needed=1):
        if self.water < w:
            return False, "Sorry, not enough water!\n"
        elif self.milk < m:
            return False, "Sorry, not enough milk!\n"
        elif self.coffee_beans < b:
            return False, "Sorry, not enough coffee beans!\n"
        elif self.cups < cups_needed:
            return False, "Sorry, not enough cups!\n"
        else:
            return True, "I have enough resources, making you a coffee!\n"

    def _handle_buy(self, choice: str):
        if choice == "back":
            self.state = self.State.MAIN
            return ""

        if choice in self.DRINKS:
            drink = self.DRINKS[choice]
            ok, request = self._check_resources(drink.water, drink.milk, drink.beans)
            if ok:
                self.water -= drink.water
                self.milk -= drink.milk
                self.coffee_beans -= drink.beans
                self.cups -= drink.cups
                self.money += drink.money
            self.state = self.State.MAIN
            return request

        else:
            self.state = self.State.BUY
            return self._handle_main(self.state)

    def _check_val_isdigit(self, val: str):
        if val.isdigit() and int(val) > 0:
            return True
        else:
            return False

    def _handle_fill_water(self, val='0'):
        if self._check_val_isdigit(val):
            self.water += int(val)

    def _handle_fill_milk(self, val='0'):
        if self._check_val_isdigit(val):
            self.milk += int(val)

    def _handle_fill_beans(self, val='0'):
        if self._check_val_isdigit(val):
            self.coffee_beans += int(val)

    def _handle_fill_cups(self, val='0'):
        if self._check_val_isdigit(val):
            self.cups += int(val)

    def _status(self):
        return (
            f"\nThe coffee machine has:\n"
            f"{self.water} ml of water\n"
            f"{self.milk} ml of milk\n"
            f"{self.coffee_beans} g of coffee beans\n"
            f"{self.cups} disposable cups\n"
            f"${self.money} money\n")

    def _handle_main(self, cmd: str):
        if cmd == "buy":
            return f"\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:"
        elif cmd == "fill":
            return "\nWrite how many ml of water you want to add:"
        elif self.state in (self.State.FILL_MILK, self.State.FILL_BEANS, self.State.FILL_CUPS):
            prompts = {
                self.State.FILL_MILK: "Write how many ml of milk you want to add:",
                self.State.FILL_BEANS: "Write how many grams of coffee beans you want to add:",
                self.State.FILL_CUPS: "Write how many disposable cups you want to add:"
            }
            return prompts[self.state]
        else:
            return ""

    def process_input(self, input_str: str):
        s = input_str.strip()
        if self.state == self.State.MAIN:
            if s == "buy":
                self.state = self.State.BUY
                return self._handle_main(s)
            elif s == "fill":
                self.state = self.State.FILL_WATER
                return self._handle_main(s)
            elif s == "take":
                amount = self.money
                self.money = 0
                return f"\nI gave you ${amount}\n"
            elif s == "remaining":
                return self._status()
            elif s == "exit":
                self.state = self.State.EXIT
                return self.state
            else:
                return ""
        elif self.state == self.State.BUY:
            if s == "back":
                self.state = self.State.MAIN
                return self._handle_main(s)
            return self._handle_buy(s)
        elif self.state == self.State.FILL_WATER:
            self._handle_fill_water(s)
            self.state = self.State.FILL_MILK
            return self._handle_main(self.state)
        elif self.state == self.State.FILL_MILK:
            self._handle_main(s)
            self.state = self.State.FILL_BEANS
            return self._handle_main(s)
        elif self.state == self.State.FILL_BEANS:
            self._handle_fill_beans(s)
            self.state = self.State.FILL_CUPS
            return self._handle_main(s)
        elif self.state == self.State.FILL_CUPS:
            self._handle_fill_cups(s)
            self.state = self.State.MAIN
            return self._handle_main(s)
        else:
            self.state = self.State.MAIN
            return ""


if __name__ == "__main__":
    machine = CoffeeMachine()
    while machine.state != machine.State.EXIT:
        if machine.state == machine.State.MAIN:
            user_input = input(f"Write action (buy, fill, take, remaining, exit):\n")
        else:
            user_input = input()

        response = machine.process_input(user_input)
        if machine.state == machine.State.EXIT:
            break
        print(response)
