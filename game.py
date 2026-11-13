import random

from storage import load_game, save_game
from tamagotchi import Tamagotchi


def calculate_statistics(pets):
    living = 0
    total_health = 0
    total_hunger = 0
    total_boredom = 0
    total_exhaustion = 0

    for pet in pets:
        if pet.is_alive():
            living += 1
            total_health += pet.health
        total_hunger += pet.hunger
        total_boredom += pet.boredom
        total_exhaustion += pet.exhaustion

    average_health = 0
    if living > 0:
        average_health = total_health / living

    average_hunger = 0
    average_boredom = 0
    average_exhaustion = 0
    if len(pets) > 0:
        average_hunger = total_hunger / len(pets)
        average_boredom = total_boredom / len(pets)
        average_exhaustion = total_exhaustion / len(pets)

    return {
        "living": living,
        "dead": len(pets) - living,
        "average_health": average_health,
        "average_hunger": average_hunger,
        "average_boredom": average_boredom,
        "average_exhaustion": average_exhaustion,
    }


def display_statistics(pets):
    statistics = calculate_statistics(pets)
    print("\nGame statistics")
    print(f"Living pets: {statistics['living']}")
    print(f"Dead pets: {statistics['dead']}")
    print(f"Average health (living pets): {statistics['average_health']:.1f}/100")
    print(f"Average hunger (all pets): {statistics['average_hunger']:.1f}/100")
    print(f"Average boredom (all pets): {statistics['average_boredom']:.1f}/100")
    print(f"Average exhaustion (all pets): {statistics['average_exhaustion']:.1f}/100")


def random_event(pets):
    living_pets = []
    for pet in pets:
        if pet.is_alive():
            living_pets.append(pet)

    # One event has a 25% chance of occurring after each turn.
    if not living_pets or random.randint(1, 4) != 1:
        return

    pet = random.choice(living_pets)
    event = random.choice(["sickness", "food", "health_bonus"])

    if event == "sickness":
        pet.health = max(0, pet.health - 15)
        print(f"Oh no! {pet.name} became sick and lost 15 health.")
    elif event == "food":
        pet.hunger = max(0, pet.hunger - 15)
        print(f"Look! {pet.name} found food! Hunger decreased by 15.")
    else:
        pet.health = min(100, pet.health + 10)
        print(f"Great! {pet.name} received a 10 health bonus!")

    if not pet.is_alive():
        print(f"I am so sorry... {pet.name} has died.")


def update_game(pets):
    for pet in pets:
        if pet.is_alive():
            pet.update_status()
            if not pet.is_alive():
                print(f"{pet.name} has died.")

    random_event(pets)


def select_pet(pets, current_pet):
    print("\nYour Tamagotchis:")
    for index, pet in enumerate(pets, start=1):
        state = "Alive" if pet.is_alive() else "Deceased"
        print(f"{index}. {pet.name} ({state})")

    try:
        number = int(input("Select a pet (1-3): "))
    except ValueError:
        print("Please enter a number between 1 and 3.")
        return current_pet

    if 1 <= number <= len(pets):
        return pets[number - 1]

    print("That pet does not exist.")
    return current_pet


def display_menu(selected_pet):
    print(f"\nSelected pet: {selected_pet.name}")
    print("1. Select a Tamagotchi")
    print("2. Feed")
    print("3. Play")
    print("4. Sleep")
    print("5. Heal")
    print("6. Display status")
    print("7. Display game statistics")
    print("8. Save game")
    print("9. Load game")
    print("0. Quit")


def run_game():
    pets = [Tamagotchi("Mochi"), Tamagotchi("Luna"), Tamagotchi("Pip")]
    selected_pet = pets[0]
    print("Ready to play with your Tamagotchi?")

    while True:
        display_menu(selected_pet)
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        try:
            if choice == "1":
                selected_pet = select_pet(pets, selected_pet)
            elif choice == "2":
                selected_pet.feed()
            elif choice == "3":
                selected_pet.play()
            elif choice == "4":
                selected_pet.sleep()
            elif choice == "5":
                selected_pet.heal()
            elif choice == "6":
                selected_pet.display_status()
            elif choice == "7":
                display_statistics(pets)
            elif choice == "8":
                save_game(pets)
                print("Game saved to savegame.json.")
            elif choice == "9":
                pets = load_game()
                selected_pet = pets[0]
                print("Game loaded from savegame.json. The first pet is selected.")
            else:
                print("Invalid option. Choose a number from the menu.")

            if choice in ("2", "3", "4", "5"):
                update_game(pets)
                selected_pet.display_status()
        except ValueError as error:
            print(error)
        except FileNotFoundError:
            print("No save file found. Save a game before loading.")
        except OSError as error:
            print(f"Could not access the save file: {error}")
