import json
import os
import sys

def save_liquids(liquids, file_name="liquids.json"):
    """
    Saves a list of liquid names to a JSON file.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, file_name)

    try:
        with open(file_path, "w") as file:
            json.dump({"liquids": liquids}, file, indent=4)
    except IOError as e:
        print(f"Error saving liquids: {e}")


def load_liquids(file_name="liquids.json"):
    """
    Loads a list of liquid names from a JSON file.
    If the file does not exist or is invalid, returns a list of 6 empty strings.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, file_name)

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data.get("liquids", [""] * 6)
    except (IOError, json.JSONDecodeError):
        return [""] * 6  # Default to 6 empty strings


def save_drinks(drinks, file_name="drinks.json"):
    """
    Saves the list of drinks to a JSON file.
    """
    # Ensure the file is saved in the same directory as the executable/script
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, file_name)

    try:
        with open(file_path, "w") as file:
            json.dump(drinks, file, indent=4)
    except IOError as e:
        print(f"Error saving drinks: {e}")

def load_drinks(file_name="drinks.json"):
    """
    Loads the list of drinks from a JSON file.
    Returns an empty list if the file doesn't exist or is invalid.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, file_name)

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError):
        return []  # Return an empty list if the file is missing or corrupt


def add_drink(name, amounts):
    drinks = load_drinks()  # Load existing drinks at program start
    drinks[name] = amounts
    save_drinks(drinks)

def remove_drink(drink_name, file_name="drinks.json"):
    """
    Removes a drink from the saved list by name.
    Returns True if the drink was removed, False if the drink was not found.
    """
    # Load the current list of drinks
    drinks = load_drinks(file_name)

    # Check if drink name exists
    if drink_name not in drinks:
        return False  # No drink removed, name not found
    
    drinks.pop(drink_name)
    # Save the updated list back to the file
    save_drinks(drinks, file_name)
    return True

#save_liquids(["1", "2", "3", "4", "5", "6"])
remove_drink("liquids")