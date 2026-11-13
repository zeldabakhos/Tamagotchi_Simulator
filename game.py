from tamagotchi import Tamagotchi

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
            else:
                print("Invalid option. Choose a number from the menu.")

            if choice in ("2", "3", "4", "5"):
                selected_pet.display_status()
        except ValueError as error:
            print(error)
