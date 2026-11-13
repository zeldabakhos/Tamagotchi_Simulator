class Tamagotchi:
    """A virtual pet whose status values range from 0 to 100."""

    def __init__(self, name, hunger=50, health=100, boredom=50, exhaustion=0):
        for value in (hunger, health, boredom, exhaustion):
            if type(value) is not int or not 0 <= value <= 100:
                raise ValueError("Status values must be integers between 0 and 100.")

        self.name = name
        self.hunger = hunger
        self.health = health
        self.boredom = boredom
        self.exhaustion = exhaustion

    def is_alive(self):
        """Health determines whether the pet is alive."""
        return self.health > 0

    def _check_alive(self):
        if not self.is_alive():
            raise ValueError(f"{self.name} is deceased and cannot perform actions.")

    def feed(self):
        self._check_alive()
        self.hunger = max(0, self.hunger - 20)

    def play(self):
        self._check_alive()
        self.boredom = max(0, self.boredom - 20)
        self.hunger = min(100, self.hunger + 10)
        self.exhaustion = min(100, self.exhaustion + 15)

    def sleep(self):
        self._check_alive()
        self.exhaustion = max(0, self.exhaustion - 30)

    def heal(self):
        self._check_alive()
        self.health = min(100, self.health + 20)

    def display_status(self):
        state = "Alive" if self.is_alive() else "Dead"
        print(f"{self.name} ({state})")
        print(f"Hunger: {self.hunger}/100")
        print(f"Health: {self.health}/100")
        print(f"Boredom: {self.boredom}/100")
        print(f"Exhaustion: {self.exhaustion}/100")
