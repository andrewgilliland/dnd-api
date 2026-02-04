"""Monster service for business logic and monster generation"""

import random
from app.models import Monster, MonsterType, Size, Alignment, Stats, Action, DamageType


def generate_random_monster_name(monster_type: MonsterType) -> str:
    """Generate a random monster name based on type"""

    name_prefixes = {
        MonsterType.DRAGON: ["Ancient", "Young", "Adult", "Elder", "Wyrm"],
        MonsterType.UNDEAD: ["Cursed", "Haunted", "Restless", "Dread", "Fallen"],
        MonsterType.FIEND: ["Infernal", "Abyssal", "Hellish", "Burning", "Dark"],
        MonsterType.CELESTIAL: ["Radiant", "Divine", "Holy", "Blessed", "Sacred"],
        MonsterType.ABERRATION: [
            "Twisted",
            "Corrupted",
            "Mind-Bending",
            "Eldritch",
            "Strange",
        ],
        MonsterType.BEAST: ["Wild", "Savage", "Primal", "Feral", "Great"],
        MonsterType.CONSTRUCT: ["Animated", "Mechanical", "Arcane", "Stone", "Iron"],
        MonsterType.ELEMENTAL: ["Raging", "Primordial", "Pure", "Eternal", "Chaos"],
        MonsterType.FEY: ["Enchanted", "Twilight", "Mystical", "Trickster", "Wild"],
        MonsterType.GIANT: ["Towering", "Mighty", "Hill", "Stone", "Frost"],
        MonsterType.HUMANOID: ["Savage", "Tribal", "Raiding", "War", "Blood"],
        MonsterType.MONSTROSITY: [
            "Monstrous",
            "Hybrid",
            "Chimeric",
            "Cursed",
            "Mutant",
        ],
        MonsterType.OOZE: ["Gelatinous", "Acidic", "Hungry", "Slithering", "Black"],
        MonsterType.PLANT: ["Carnivorous", "Strangling", "Thorned", "Awakened", "Vine"],
    }

    name_suffixes = {
        MonsterType.DRAGON: ["Dragon", "Drake", "Wyrm", "Dragonling"],
        MonsterType.UNDEAD: ["Wraith", "Zombie", "Skeleton", "Specter", "Ghoul"],
        MonsterType.FIEND: ["Demon", "Devil", "Imp", "Hellhound", "Fiend"],
        MonsterType.CELESTIAL: ["Angel", "Archon", "Deva", "Pegasus"],
        MonsterType.ABERRATION: ["Horror", "Beholder", "Mind Flayer", "Aboleth"],
        MonsterType.BEAST: ["Bear", "Wolf", "Tiger", "Spider", "Serpent"],
        MonsterType.CONSTRUCT: ["Golem", "Guardian", "Sentinel", "Automaton"],
        MonsterType.ELEMENTAL: ["Elemental", "Mephit", "Salamander", "Djinni"],
        MonsterType.FEY: ["Pixie", "Sprite", "Dryad", "Satyr", "Hag"],
        MonsterType.GIANT: ["Giant", "Ogre", "Troll", "Ettin"],
        MonsterType.HUMANOID: ["Orc", "Goblin", "Kobold", "Hobgoblin", "Gnoll"],
        MonsterType.MONSTROSITY: [
            "Chimera",
            "Manticore",
            "Griffon",
            "Hydra",
            "Basilisk",
        ],
        MonsterType.OOZE: ["Ooze", "Pudding", "Slime", "Jelly", "Cube"],
        MonsterType.PLANT: ["Treant", "Shambler", "Vine", "Blight"],
    }

    prefix = random.choice(name_prefixes[monster_type])
    suffix = random.choice(name_suffixes[monster_type])

    return f"{prefix} {suffix}"


def generate_random_monster_stats(challenge_rating: float) -> Stats:
    """Generate monster stats based on challenge rating"""
    # Base stats scale with CR
    base_stat = 10 + int(challenge_rating * 1.5)
    variation = int(challenge_rating / 2) + 1

    return Stats(
        strength=base_stat + random.randint(-variation, variation),
        dexterity=base_stat + random.randint(-variation, variation),
        constitution=base_stat + random.randint(-variation, variation),
        intelligence=base_stat + random.randint(-variation, variation),
        wisdom=base_stat + random.randint(-variation, variation),
        charisma=base_stat + random.randint(-variation, variation),
    )


def calculate_hp_from_cr(challenge_rating: float, size: Size) -> tuple[int, str]:
    """Calculate HP and hit dice based on CR and size"""

    # Hit die by size
    hit_dice_map = {
        Size.TINY: 4,
        Size.SMALL: 6,
        Size.MEDIUM: 8,
        Size.LARGE: 10,
        Size.HUGE: 12,
        Size.GARGANTUAN: 20,
    }

    die_size = hit_dice_map[size]
    num_dice = max(1, int(challenge_rating * 3) + random.randint(1, 6))
    constitution_bonus = int(challenge_rating)

    # Calculate HP: (num_dice * (die_size / 2 + 0.5)) + (num_dice * con_bonus)
    average_roll = (die_size / 2) + 0.5
    hit_points = int((num_dice * average_roll) + (num_dice * constitution_bonus))
    hit_dice = f"{num_dice}d{die_size}+{num_dice * constitution_bonus}"

    return hit_points, hit_dice


def calculate_ac_from_cr(challenge_rating: float) -> int:
    """Calculate armor class based on challenge rating"""
    return 10 + int(challenge_rating * 1.2) + random.randint(0, 3)


def calculate_xp_from_cr(challenge_rating: float) -> int:
    """Calculate XP reward based on challenge rating"""
    xp_table = {
        0: 10,
        0.125: 25,
        0.25: 50,
        0.5: 100,
        1: 200,
        2: 450,
        3: 700,
        4: 1100,
        5: 1800,
        6: 2300,
        7: 2900,
        8: 3900,
        9: 5000,
        10: 5900,
        11: 7200,
        12: 8400,
        13: 10000,
        14: 11500,
        15: 13000,
        16: 15000,
        17: 18000,
        18: 20000,
        19: 22000,
        20: 25000,
    }
    return xp_table.get(challenge_rating, int(challenge_rating * 1000))


def generate_special_abilities(
    monster_type: MonsterType, challenge_rating: float
) -> list[Action] | None:
    """Generate passive abilities and traits based on monster type"""

    abilities_map = {
        MonsterType.DRAGON: [
            Action(
                name="Frightful Presence",
                description="Each creature within 60 feet that is aware of the dragon must succeed on a Wisdom saving throw or become frightened for 1 minute",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ],
        MonsterType.UNDEAD: [
            Action(
                name="Undead Fortitude",
                description="If damage reduces the creature to 0 hit points, it can make a Constitution saving throw to drop to 1 hit point instead",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ],
        MonsterType.ABERRATION: [
            Action(
                name="Telepathy",
                description="The creature can communicate telepathically with any creature within 120 feet that has a language",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ],
        MonsterType.FIEND: [
            Action(
                name="Magic Resistance",
                description="The creature has advantage on saving throws against spells and other magical effects",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ],
        MonsterType.CELESTIAL: [
            Action(
                name="Divine Blessing",
                description="The creature's weapon attacks are magical and deal an extra 2d8 radiant damage",
                attack_bonus=None,
                damage_dice="2d8",
                damage_type=DamageType.RADIANT,
            ),
        ],
        MonsterType.FEY: [
            Action(
                name="Fey Ancestry",
                description="The creature has advantage on saving throws against being charmed, and magic can't put it to sleep",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ],
        MonsterType.ELEMENTAL: [
            Action(
                name="Elemental Body",
                description="The creature can move through spaces as narrow as 1 inch wide without squeezing",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ],
        MonsterType.CONSTRUCT: [
            Action(
                name="Immutable Form",
                description="The creature is immune to any spell or effect that would alter its form",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ],
        MonsterType.OOZE: [
            Action(
                name="Amorphous",
                description="The creature can move through spaces as narrow as 1 inch wide without squeezing",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ],
        MonsterType.PLANT: [
            Action(
                name="False Appearance",
                description="While motionless, the creature is indistinguishable from a normal plant",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ],
        MonsterType.BEAST: [
            Action(
                name="Keen Senses",
                description="The creature has advantage on Wisdom (Perception) checks that rely on sight, hearing, or smell",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ]
        if challenge_rating >= 2
        else None,
        MonsterType.GIANT: [
            Action(
                name="Powerful Build",
                description="The creature counts as one size larger when determining its carrying capacity and the weight it can push, drag, or lift",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            ),
        ],
    }

    abilities = abilities_map.get(monster_type)

    # Add legendary resistance for high CR monsters
    if challenge_rating >= 10 and abilities:
        abilities.append(
            Action(
                name="Legendary Resistance (3/Day)",
                description="If the creature fails a saving throw, it can choose to succeed instead",
                attack_bonus=None,
                damage_dice=None,
                damage_type=None,
            )
        )

    return abilities


def generate_monster_actions(
    monster_type: MonsterType, challenge_rating: float
) -> list[Action]:
    """Generate monster actions based on type and CR"""

    action_templates = {
        MonsterType.DRAGON: [
            Action(
                name="Bite",
                description="Melee Weapon Attack",
                attack_bonus=int(2 + challenge_rating),
                damage_dice=f"{max(1, int(challenge_rating))}d10+{int(challenge_rating)}",
                damage_type=DamageType.PIERCING,
            ),
            Action(
                name="Breath Weapon",
                description="Exhales destructive energy in a cone",
                damage_dice=f"{int(challenge_rating * 2)}d6",
                damage_type=random.choice(
                    [DamageType.FIRE, DamageType.COLD, DamageType.LIGHTNING]
                ),
            ),
        ],
        MonsterType.UNDEAD: [
            Action(
                name="Life Drain",
                description="Melee Weapon Attack that drains life force",
                attack_bonus=int(2 + challenge_rating),
                damage_dice=f"{max(1, int(challenge_rating / 2))}d6+{int(challenge_rating / 2)}",
                damage_type=DamageType.NECROTIC,
            ),
        ],
        MonsterType.BEAST: [
            Action(
                name="Claw",
                description="Melee Weapon Attack",
                attack_bonus=int(2 + challenge_rating),
                damage_dice=f"{max(1, int(challenge_rating / 2))}d6+{int(challenge_rating)}",
                damage_type=DamageType.SLASHING,
            ),
        ],
    }

    # Return type-specific actions or generic attack
    actions = action_templates.get(
        monster_type,
        [
            Action(
                name="Strike",
                description="Melee Weapon Attack",
                attack_bonus=int(2 + challenge_rating),
                damage_dice=f"{max(1, int(challenge_rating / 2))}d8+{int(challenge_rating)}",
                damage_type=random.choice(
                    [DamageType.BLUDGEONING, DamageType.PIERCING, DamageType.SLASHING]
                ),
            ),
        ],
    )

    return actions


def generate_random_monster(
    monster_type: MonsterType | None = None,
    size: Size | None = None,
    min_cr: float | None = None,
    max_cr: float | None = None,
) -> Monster:
    """Generate a random monster with optional constraints"""

    # Random selections
    if monster_type is None:
        monster_type = random.choice(list(MonsterType))

    if size is None:
        size = random.choice(list(Size))

    # Generate CR within constraints
    if min_cr is None:
        min_cr = 0
    if max_cr is None:
        max_cr = 20

    cr_options = [0, 0.125, 0.25, 0.5] + list(range(1, 21))
    valid_crs = [cr for cr in cr_options if min_cr <= cr <= max_cr]
    challenge_rating = random.choice(valid_crs if valid_crs else [1])

    alignment = random.choice(list(Alignment))
    name = generate_random_monster_name(monster_type)
    stats = generate_random_monster_stats(challenge_rating)
    hit_points, hit_dice = calculate_hp_from_cr(challenge_rating, size)
    armor_class = calculate_ac_from_cr(challenge_rating)
    experience_points = calculate_xp_from_cr(challenge_rating)
    special_abilities = generate_special_abilities(monster_type, challenge_rating)
    actions = generate_monster_actions(monster_type, challenge_rating)

    # Generate speed based on type
    speed = {"walk": 30}
    if monster_type in [MonsterType.DRAGON, MonsterType.FEY, MonsterType.CELESTIAL]:
        speed["fly"] = 60
    if monster_type in [MonsterType.BEAST, MonsterType.ELEMENTAL]:
        if random.random() > 0.5:
            speed["swim"] = 30

    # Generate random ID
    monster_id = random.randint(1000, 9999)

    return Monster(
        id=monster_id,
        name=name,
        size=size,
        type=monster_type,
        alignment=alignment,
        armor_class=armor_class,
        hit_points=hit_points,
        hit_dice=hit_dice,
        speed=speed,
        stats=stats,
        challenge_rating=challenge_rating,
        special_abilities=special_abilities,
        experience_points=experience_points,
        actions=actions,
    )
