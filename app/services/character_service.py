"""Character service for business logic and character generation"""

import random
from app.models import Character, Class, Race, Alignment, Stats


def roll_ability_score() -> int:
    """Roll 4d6, drop lowest die (standard D&D method)"""
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.remove(min(rolls))
    return sum(rolls)


def generate_random_stats() -> Stats:
    """Generate random ability scores using 4d6 drop lowest"""
    return Stats(
        strength=roll_ability_score(),
        dexterity=roll_ability_score(),
        constitution=roll_ability_score(),
        intelligence=roll_ability_score(),
        wisdom=roll_ability_score(),
        charisma=roll_ability_score(),
    )


def generate_random_name(race: Race, class_: Class) -> str:
    """Generate a random character name based on race"""
    
    first_names = {
        Race.HUMAN: ["Alric", "Brianna", "Connor", "Diana", "Erik", "Fiona", "Garrett", "Helena"],
        Race.ELF: ["Aelrindel", "Caelynn", "Erevan", "Faelyn", "Galadriel", "Silaqui", "Theren", "Valandil"],
        Race.DWARF: ["Baern", "Dagnal", "Eberk", "Fargrim", "Gimli", "Thorin", "Ulfgar", "Vondal"],
        Race.HALFLING: ["Alton", "Cora", "Eldon", "Lily", "Merric", "Portia", "Rosco", "Seraphina"],
        Race.DRAGONBORN: ["Arjhan", "Balasar", "Donaar", "Ghesh", "Heskan", "Kriv", "Medrash", "Patrin"],
        Race.GNOME: ["Alston", "Brocc", "Dimble", "Eldon", "Fonkin", "Gimble", "Orryn", "Roondar"],
        Race.HALF_ELF: ["Arlan", "Celeste", "Damien", "Elara", "Gareth", "Lyra", "Rowan", "Selene"],
        Race.HALF_ORC: ["Dench", "Feng", "Gell", "Holg", "Imsh", "Keth", "Mhurren", "Ront"],
        Race.TIEFLING: ["Akmenios", "Damakos", "Ekemon", "Iados", "Kairon", "Leucis", "Melech", "Therai"],
    }
    
    return random.choice(first_names.get(race, ["Adventurer"]))


def generate_random_description(name: str, race: Race, class_: Class, alignment: Alignment) -> str:
    """Generate a character description"""
    personalities = [
        f"{name} is a brave and fearless warrior.",
        f"{name} is known for their cunning and wit.",
        f"{name} is a mysterious figure with a troubled past.",
        f"{name} seeks adventure and glory across the land.",
        f"{name} is devoted to protecting the innocent.",
        f"{name} is driven by an insatiable curiosity.",
        f"{name} wanders the realm in search of ancient knowledge.",
        f"{name} is a charismatic leader who inspires others.",
    ]
    
    return random.choice(personalities)


def generate_random_character() -> Character:
    """Generate a completely random D&D character"""
    
    # Random selections
    race = random.choice(list(Race))
    class_ = random.choice(list(Class))
    alignment = random.choice(list(Alignment))
    stats = generate_random_stats()
    name = generate_random_name(race, class_)
    description = generate_random_description(name, race, class_, alignment)
    
    # Generate a random ID (in production, this would come from database)
    character_id = random.randint(1000, 9999)
    
    return Character(
        id=character_id,
        name=name,
        race=race,
        alignment=alignment,
        description=description,
        stats=stats,
        **{"class": class_}  # Use dict unpacking to handle the alias
    )
