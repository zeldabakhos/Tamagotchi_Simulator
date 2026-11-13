import json

from tamagotchi import Tamagotchi


def save_game(pets, filename="savegame.json"):
    data = []
    for pet in pets:
        data.append({
            "name": pet.name,
            "hunger": pet.hunger,
            "health": pet.health,
            "boredom": pet.boredom,
            "exhaustion": pet.exhaustion,
            "is_alive": pet.is_alive(),
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_game(filename="savegame.json"):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list) or len(data) != 3:
        raise ValueError("Invalid save file: expected exactly three pets.")

    pets = []
    for pet_data in data:
        if not isinstance(pet_data, dict):
            raise ValueError("Invalid save file: each pet must be a dictionary.")

        for key in ("name", "hunger", "health", "boredom", "exhaustion", "is_alive"):
            if key not in pet_data:
                raise ValueError(f"Invalid save file: missing {key}.")

        if not isinstance(pet_data["name"], str) or not pet_data["name"].strip():
            raise ValueError("Invalid save file: pet names must be nonempty text.")

        pet = Tamagotchi(
            pet_data["name"],
            pet_data["hunger"],
            pet_data["health"],
            pet_data["boredom"],
            pet_data["exhaustion"],
        )

        # Health and the saved living/dead status must agree.
        if type(pet_data["is_alive"]) is not bool or pet_data["is_alive"] != pet.is_alive():
            raise ValueError("Invalid save file: living/dead status does not match health.")

        pets.append(pet)

    return pets
