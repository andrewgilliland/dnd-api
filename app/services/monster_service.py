"""Monster service for business logic and monster generation"""

import random
from app.models import Monster, MonsterType, Size, Alignment, Stats, Action, DamageType
from app.config.constants import XP_BY_CR
from app.services.data_loader import load_monster_names
from app.utils import calculate_hp_from_cr, calculate_ac_from_cr, get_xp_by_cr


def generate_random_monster_name(monster_type: MonsterType) -> str:
    """Generate a random monster name based on type"""
    names_data = load_monster_names()

    prefix = random.choice(names_data["prefixes"].get(monster_type.value, ["Unknown"]))
    suffix = random.choice(names_data["suffixes"].get(monster_type.value, ["Creature"]))

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
    experience_points = XP_BY_CR.get(challenge_rating, int(challenge_rating * 1000))
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
