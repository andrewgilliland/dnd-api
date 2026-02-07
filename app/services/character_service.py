"""Character service for business logic and character generation"""

import random
from app.models import Character, Class, Race, Alignment, Stats
from app.services.data_loader import load_character_names, load_character_traits
from app.utils import roll_ability_score


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
    names_data = load_character_names()
    return random.choice(names_data.get(race.value, ["Adventurer"]))


def generate_random_description(
    name: str, race: Race, class_: Class, alignment: Alignment
) -> str:
    """Generate a character description using race, class, and alignment"""

    traits_data = load_character_traits()

    # Build the description using data from JSON
    trait = random.choice(
        traits_data["class_traits"].get(class_.value, ["adventurous"])
    )
    motivation = random.choice(
        traits_data["alignment_motivations"].get(
            alignment.value, ["seeks their destiny"]
        )
    )
    background = random.choice(
        traits_data["race_backgrounds"].get(race.value, ["from distant lands"])
    )

    # Format the template
    template = random.choice(traits_data["description_templates"])
    return template.format(
        name=name,
        trait=trait,
        race=race.value,
        class_=class_.value,
        background=background,
        motivation=motivation,
    )


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
        **{"class": class_},  # Use dict unpacking to handle the alias
    )
