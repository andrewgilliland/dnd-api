"""Spell generation service"""

import random
from app.models.spell import Spell, SpellSchool, SpellComponent


_SCHOOL_DESCRIPTIONS = {
    SpellSchool.EVOCATION: "You channel raw magical energy to create a powerful effect",
    SpellSchool.ABJURATION: "Protective magical energy surrounds the target",
    SpellSchool.CONJURATION: "You summon or teleport matter across space",
    SpellSchool.DIVINATION: "Magical insight reveals hidden truths",
    SpellSchool.ENCHANTMENT: "You weave magic that influences the mind",
    SpellSchool.ILLUSION: "A magical figment deceives the senses",
    SpellSchool.NECROMANCY: "Dark energy manipulates the essence of life",
    SpellSchool.TRANSMUTATION: "You alter the physical properties of a creature or object",
}

_SCHOOL_CLASSES = {
    SpellSchool.EVOCATION: ["Sorcerer", "Wizard", "Cleric"],
    SpellSchool.ABJURATION: ["Wizard", "Paladin", "Cleric"],
    SpellSchool.CONJURATION: ["Wizard", "Sorcerer", "Druid"],
    SpellSchool.DIVINATION: ["Wizard", "Cleric", "Ranger"],
    SpellSchool.ENCHANTMENT: ["Bard", "Wizard", "Sorcerer", "Warlock"],
    SpellSchool.ILLUSION: ["Wizard", "Sorcerer", "Bard"],
    SpellSchool.NECROMANCY: ["Wizard", "Cleric", "Warlock"],
    SpellSchool.TRANSMUTATION: ["Wizard", "Druid", "Sorcerer"],
}

_LEVEL_CASTING_TIMES = {
    0: ["1 action"],
    1: ["1 action", "1 bonus action", "1 reaction"],
    2: ["1 action", "1 bonus action"],
    3: ["1 action", "1 minute"],
    4: ["1 action"],
    5: ["1 action"],
    6: ["1 action"],
    7: ["1 action", "10 minutes"],
    8: ["1 action"],
    9: ["1 action", "1 minute"],
}

_LEVEL_RANGES = {
    0: ["60 feet", "30 feet", "120 feet", "Touch"],
    1: ["60 feet", "30 feet", "120 feet", "Touch", "Self"],
    2: ["60 feet", "120 feet", "Touch", "Self", "30 feet"],
    3: ["120 feet", "150 feet", "60 feet", "Self"],
    4: ["60 feet", "120 feet", "Touch"],
    5: ["90 feet", "60 feet", "150 feet", "Self"],
    6: ["60 feet", "120 feet", "Touch"],
    7: ["60 feet", "90 feet", "Touch", "Self"],
    8: ["60 feet", "120 feet", "150 feet"],
    9: ["Self", "Touch", "60 feet"],
}


def generate_random_spell(
    school: SpellSchool | None = None,
    level: int | None = None,
    spell_class: str | None = None,
) -> Spell:
    """Generate a random D&D spell with optional constraints."""
    chosen_school = school or random.choice(list(SpellSchool))
    chosen_level = level if level is not None else random.randint(0, 9)

    level_label = "cantrip" if chosen_level == 0 else f"level {chosen_level}"
    description = (
        f"{_SCHOOL_DESCRIPTIONS[chosen_school]}. "
        f"This is a {level_label} {chosen_school.value.lower()} spell."
    )

    components = [SpellComponent.VERBAL, SpellComponent.SOMATIC]
    if chosen_level >= 2 and random.random() > 0.5:
        components.append(SpellComponent.MATERIAL)

    concentration = chosen_level >= 2 and random.random() > 0.6
    ritual = chosen_level <= 3 and not concentration and random.random() > 0.8

    classes = list(_SCHOOL_CLASSES[chosen_school])
    if spell_class and spell_class not in classes:
        classes = [spell_class] + classes[:2]

    return Spell(
        id=0,
        name=f"Random {chosen_school.value} {'Cantrip' if chosen_level == 0 else f'Spell (Level {chosen_level})'}",
        level=chosen_level,
        school=chosen_school,
        casting_time=random.choice(
            _LEVEL_CASTING_TIMES.get(chosen_level, ["1 action"])
        ),
        range=random.choice(_LEVEL_RANGES.get(chosen_level, ["60 feet"])),
        components=components,
        duration="1 minute" if concentration else "Instantaneous",
        concentration=concentration,
        ritual=ritual,
        description=description,
        classes=classes,
    )
