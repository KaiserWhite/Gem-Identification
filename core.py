"""Core logic for gem identification and cutting workflows."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Optional, Sequence, Tuple

# ------------------------
# GEM DATA (1e DMG 25-26)
# ------------------------
GEMS = {
    "(01-25) Ornamental Stones: Base Value 10gp": [
        ("Azurite", "opaque, deep blue", 10),
        ("Banded Agate", "translucent, striped multicolor", 10),
        ("Blue Quartz", "transparent, pale blue", 10),
        ("Eye Agate", "translucent, brown/green with concentric circles", 10),
        ("Hematite", "opaque, black/gray metallic", 10),
        ("Lapis Lazuli", "opaque, light and dark blue with yellow flecks", 10),
        ("Malachite", "opaque, striated light and dark green", 10),
        ("Moss Agate", "transparent, pink or yellow-white with grayish or greenish moss markings", 10),
        ("Obsidian", "opaque, black", 10),
        ("Rhodochrosite", "opaque, light pink", 10),
        ("Tiger Eye", "translucent, rich brown with golden center under-hue", 10),
        ("Turquoise", "opaque, light blue-green", 10),
    ],
    "(26-50) Semi-Precious Stones: Base Value 50gp": [
        ("Bloodstone", "opaque, dark grey with red flecks", 50),
        ("Carnelian", "opaque, orange to reddish brown", 50),
        ("Chalcedony", "opaque, white", 50),
        ("Chrysoprase", "translucent, apple green to emerald green", 50),
        ("Citrine", "transparent, pale yellow", 50),
        ("Jasper", "blue-black to brown", 50),
        ("Moonstone", "translucent, milky with blue sheen", 50),
        ("Onyx", "opaque, bands of black and white or pure black or white", 50),
        ("Rock Crystal", "transparent, clear", 50),
        ("Sardonyx", "opaque, bands of red and onyx", 50),
        ("Smoky Quartz", "transparent, gray, yellow, or blue, all light", 50),
        ("Star Rose Quartz", "transparent, translucent rosy stone with a white 'star' center", 50),
        ("Zircon", "transparent, clear pale blue-green", 50),
    ],
    "(51-70) Fancy Stones: Base Value 100 gp": [
        ("Amber", "transparent, watery gold to rich gold", 100),
        ("Alexandrite", "transparent dark green", 100),
        ("Amethyst", "transparent, deep purple", 100),
        ("Chrysoberyl", "transparent, yellow green to green", 100),
        ("Coral", "opaque, crimson", 100),
        ("Garnet", "transparent red, brown-green", 100),
        ("Jade", "translucent, light green, deep green, green and white, white", 100),
        ("Jet", "opaque, deep black", 100),
        ("Pearl", "opaque, lustrous white, yellowish, pinkish, etc", 100),
        ("Spinel", "transparent, red, or brown", 100),
        ("Tourmaline", "transparent, pale green, brown pale, or reddish pale", 100),
    ],
    "(71-90) Fancy Stones (Precious): Base Value 500 gp": [
        ("Aquamarine", "transparent, pale blue-green", 500),
        ("Violet Garnet", "transparent violet", 500),
        ("Black Pearl", "opaque, black", 500),
        ("Blue Spinel", "transparent, blue", 500),
        ("Peridot", "rich olive green", 500),
        ("Topaz", "transparent golden brown", 500),
    ],
    "(91-99) Gem Stones: Base Value 1,000gp": [
        ("Black Opal", "transparent, dark green with black mottling and golden flecks", 1000),
        ("Emerald", "transparent, vivid green", 1000),
        ("Fire Opal", "transparent, fiery red", 1000),
        ("Opal", "translucent, pale blue with green and golden mottling", 1000),
        ("Oriental Amethyst", "transparent, rich purple", 1000),
        ("Star Ruby", "translucent, clear ruby with 'white' star center", 1000),
        ("Star Sapphire", "translucent, clear sapphire with 'white' star center", 1000),
    ],
    "(00) Gem Stones (Jewels) 5,000 gp": [
        ("Black Sapphire", "transparent, lustrous black with glowing highlights", 5000),
        ("Diamond", "transparent, blue-white", 5000),
        ("Jacinth", "fiery orange", 5000),
        ("Oriental Emerald", "transparent, clear bright green", 5000),
        ("Ruby", "transparent, deep red", 5000),
        ("Sapphire", "transparent, clear blue", 5000),
    ],
}

# ------------------------
# SIZE MODIFIERS
# ------------------------
SIZE_MODIFIERS = {
    "Very Small": 0.5,
    "Small": 0.75,
    "Average": 1.0,
    "Large": 1.25,
    "Very Large": 1.5,
    "Huge": 2.0,
}

# ------------------------
# MAGICAL PROPERTIES (DMG p.26)
# ------------------------
MAGICAL_PROPERTIES = {
    "Agate": "Restful and safe sleep",
    "Alexandrite": "Good omens",
    "Amber": "Wards off diseases",
    "Amethyst": "Prevents drunkenness or drugging",
    "Beryl": "Wards off foes",
    "Bloodstone": "Weather control",
    "Carbuncle": "Powers of dragon's sight",
    "Carnelian": "Protection from evil",
    "Cats' eye agate": "Protection from spirits",
    "Chalcedony": "Wards off undead",
    "Chrysoberyl": "Protection from possession",
    "Chrysolite": "Wards off spells",
    "Chrysoprase": "Invisibility",
    "Coral": "Calms weather, safety in river crossing, cures madness, stanches bleeding",
    "Diamond": "Invulnerability vs. undead",
    "Hematite": "Aids fighters, heals wounds",
    "Jacinth": "Luck traveling, wards off plague, protection from fire",
    "Jade": "Skill at music and musical instruments",
    "Jasper": "Protection from venom",
    "Jet": "Soul object material",
    "Lapis Lazuli": "Raises morale, courage",
    "Malachite": "Protection from falling",
    "Malachite & Sunstone": "Wards off spells, evil spirits, and poisons",
    "Moonstone": "Cures lycanthropy",
    "Olivine": "Protection from spells",
    "Onyx": "Causes discord amongst enemies",
    "Peridot": "Wards off enchantments",
    "Ruby": "Gives good luck",
    "Sapphire": "Aids understanding of problems, kills spiders, boosts magical abilities",
    "Star Sapphire": "Protection from magic",
    "Sard": "Benefits wisdom",
    "Serpentine": "Adds to wile and cunning",
    "Topaz": "Wards off evil spells",
    "Turquoise": "Aids horses in all ways (but shatters when it operates)",
}

# ------------------------
# NAME NORMALIZATION FOR MAGICAL PROPERTIES
# ------------------------
NORMALIZATION_MAP = {
    "sardonyx": "Onyx",
    "oriental amethyst": "Amethyst",
    "star ruby": "Ruby",
    "star sapphire": "Star Sapphire",
}

# ------------------------
# COLOR NOTES
# ------------------------
COLOR_NOTES = {
    "Black": "The Earth — darkness — negation",
    "Blue": "The Heavens — truth — spirituality",
    "Clear": "The Sun — luck",
    "Green": "Venus — reproduction — sight — resurrection",
    "Red": "Hemorrhage control — heat",
    "White": "The Moon — enigmatic",
    "Yellow": "Secrecy — homeopathy — jaundice",
}
COLOR_SUBSTRINGS = {
    "black": "Black",
    "blue": "Blue",
    "green": "Green",
    "red": "Red",
    "white": "White",
    "clear": "Clear",
    "yellow": "Yellow",
    "bluish": "Blue",
    "blueish": "Blue",
    "greenish": "Green",
    "reddish": "Red",
    "whitish": "White",
    "blackish": "Black",
    "yellowish": "Yellow",
    "pinkish": "Red",
    "purplish": "Blue",
    "violet": "Blue",
    "azure": "Blue",
    "cerulean": "Blue",
    "cobalt": "Blue",
    "indigo": "Blue",
    "navy": "Blue",
    "sapphire": "Blue",
    "turquoise": "Blue",
    "emerald": "Green",
    "olive": "Green",
    "teal": "Green",
    "verdant": "Green",
    "crimson": "Red",
    "scarlet": "Red",
    "ruby": "Red",
    "magenta": "Red",
    "rose": "Red",
    "rosy": "Red",
    "pink": "Red",
    "milky": "White",
    "ivory": "White",
    "snow": "White",
    "snowy": "White",
    "colorless": "Clear",
    "gold": "Yellow",
    "golden": "Yellow",
    "lemon": "Yellow",
    "saffron": "Yellow",
    "amber": "Yellow",
    "honey": "Yellow",
}
COLOR_ORDER = ["Black", "Blue", "Clear", "Green", "Red", "White", "Yellow"]

# ------------------------
# MONEY / UNITS
# ------------------------
SP_PER_GP = 20  # 20 sp = 1 gp


def gp(value_sp: int) -> str:
    """Format an SP value as 'X gp' (with decimals) or 'Y sp' if <1 gp; 0 -> 'Nil'."""
    if value_sp == 0:
        return "Nil"
    if value_sp >= SP_PER_GP:
        if value_sp % SP_PER_GP == 0:
            return f"{value_sp // SP_PER_GP:,} gp"
        return f"{value_sp / SP_PER_GP:,.2f} gp"
    return f"{value_sp} sp"


def to_sp(gp_value: float) -> int:
    return int(round(gp_value * SP_PER_GP))


# ------------------------
# CONSTANTS
# ------------------------
CUTTING_CAP_GP = 5_000
CUTTING_CAP_SP = CUTTING_CAP_GP * SP_PER_GP
APPRAISAL_FEE_BASE = 100  # gp per month (retainer unit)

# ------------------------
# VALUE LADDER in SP (strictly increasing)
# ------------------------
RUNG_VALUES_SP = [
    1,
    5,
    10,
    20,
    100,
    200,
    1_000,
    2_000,
    10_000,
    20_000,
    100_000,
    200_000,
    500_000,
    1_000_000,
    2_000_000,
    5_000_000,
    10_000_000,
    20_000_000,
]


# ------------------------
# RETAINER & BATCH DATA CLASSES
# ------------------------
@dataclass
class RetainerState:
    active: bool = False
    race: Optional[str] = None
    type_bonus: int = 0
    fee_mult: int = 1
    months: int = 0
    fee_paid_gp: int = 0
    skill_level: Optional[str] = None
    dice_sides: Optional[int] = None
    skill_roll: Optional[int] = None


@dataclass
class RetainerRequest:
    race: str
    months: int
    knows_skill_level: bool
    known_skill_level: Optional[str] = None


@dataclass
class RetainerHireResult:
    state: RetainerState
    total_fee_gp: int
    skill_level: str
    skill_roll: Optional[int]
    dice_sides: int


@dataclass
class GemPlan:
    name: str
    color: str
    base_gp: float


@dataclass
class BatchRequest:
    batch_size: int
    category: str
    size_label: str
    size_modifier: float
    gem_plans: List[GemPlan]
    appraise: bool
    surcharge_rate: float = 0.10


@dataclass
class RetainerUsage:
    race: str
    months: int
    fee_paid_gp: int
    skill_level: Optional[str]
    skill_roll: Optional[int]
    dice_sides: Optional[int]
    type_bonus: int


@dataclass
class GemStartContext:
    index: int
    total: int
    plan: GemPlan
    size_label: str
    size_modifier: float
    base_value_sp: int


@dataclass
class GemAppraisal:
    base_value_sp: int
    adjusted_value_sp: int
    quality_label: str
    rolls: List[int] = field(default_factory=list)
    magical_property: str = "Not identified"
    color_properties: List[Tuple[str, str]] = field(default_factory=list)


@dataclass
class GemAppraisalContext:
    index: int
    total: int
    plan: GemPlan
    size_label: str
    size_modifier: float
    base_value_sp: int
    appraisal: GemAppraisal
    retainer_usage: Optional[RetainerUsage]


@dataclass
class SuperbRollStep:
    gem_index: int
    gem_name: str
    roll: int
    result_text: str
    current_value_sp: int
    cap_reached: bool
    dice_sides: int


@dataclass
class CutterOutcome:
    performed: bool
    result_text: str
    skill_level: Optional[str]
    skill_roll: Optional[int]
    die_roll: Optional[int]
    ruined_prev_rung_sp: int
    superb_steps: List[SuperbRollStep] = field(default_factory=list)
    final_value_sp: int = 0


@dataclass
class GemResult:
    index: int
    plan: GemPlan
    size_label: str
    size_modifier: float
    appraisal: GemAppraisal
    cutter_outcome: CutterOutcome
    surcharge_sp: int
    fees_this_gem_sp: int
    final_value_sp: int


@dataclass
class BatchResult:
    request: BatchRequest
    retainer_usage: Optional[RetainerUsage]
    gem_results: List[GemResult]
    total_surcharge_sp: int
    total_fees_sp: int
    total_final_value_sp: int
    ruined_count: int


# ------------------------
# HELPER FUNCTIONS
# ------------------------
def normalize_gem_key(name: str) -> str:
    s = name.strip().lower()
    if "agate" in s:
        if "cat" in s:
            return "Cats' eye agate"
        return "Agate"
    return NORMALIZATION_MAP.get(s, name)


def lookup_magical_property(gem_name: str) -> str:
    key = normalize_gem_key(gem_name)
    return MAGICAL_PROPERTIES.get(key, "No known magical properties")


def infer_color_notes_from_description(desc: str):
    s = desc.lower()
    found = {canon for sub, canon in COLOR_SUBSTRINGS.items() if sub in s}
    return [c for c in COLOR_ORDER if c in found]


def color_reputed_properties(desc: str):
    colors = infer_color_notes_from_description(desc)
    return [(c, COLOR_NOTES[c]) for c in colors]


def floor_rung(value_sp: int):
    last = None
    for r in RUNG_VALUES_SP:
        if value_sp >= r:
            last = r
        else:
            break
    return last


def rung_index_of(value_sp: int) -> int:
    idx = -1
    for i, r in enumerate(RUNG_VALUES_SP):
        if value_sp >= r:
            idx = i
        else:
            break
    return idx


def next_rung(value_sp: int) -> int:
    for r in RUNG_VALUES_SP:
        if r > value_sp:
            return r
    return RUNG_VALUES_SP[-1]


def prev_rung(value_sp: int) -> int:
    prev = None
    for r in RUNG_VALUES_SP:
        if r < value_sp:
            prev = r
        else:
            break
    return prev if prev is not None else RUNG_VALUES_SP[0]


def previous_ladder_rung(value_sp: int) -> int:
    fr = floor_rung(value_sp)
    if fr is None:
        return 0
    idx = RUNG_VALUES_SP.index(fr)
    return RUNG_VALUES_SP[idx - 1] if idx > 0 else 0


def clamp_to_band(value_sp: int, min_rung_sp: int, max_rung_sp: int) -> int:
    return max(min_rung_sp, min(value_sp, max_rung_sp))


# ------------------------
# PURE LOGIC ROUTINES
# ------------------------
def adjust_value(
    base_value_sp: int,
    min_rung_sp: Optional[int] = None,
    max_rung_sp: Optional[int] = None,
    *,
    rng: Optional[random.Random] = None,
) -> Tuple[int, str, List[int]]:
    rng = rng or random
    rolls: List[int] = []
    value = int(base_value_sp)
    quality_label = "Average"

    def apply_clamp(v: int) -> int:
        if min_rung_sp is not None and max_rung_sp is not None:
            return clamp_to_band(v, min_rung_sp, max_rung_sp)
        return v

    while True:
        roll = rng.randint(1, 10)
        rolls.append(roll)

        if roll == 1:
            value = next_rung(value)
            value = apply_clamp(value)
            quality_label = "Flawless (stepped up)"
            continue
        if roll == 2:
            quality_label = "Excellent"
            value *= 2
            value = apply_clamp(value)
            break
        if roll == 3:
            bonus = rng.randint(10, 60)
            quality_label = f"Good (+{bonus}%)"
            value = int(round(value * (1 + bonus / 100.0)))
            value = apply_clamp(value)
            break
        if 4 <= roll <= 8:
            quality_label = "Average"
            value = apply_clamp(value)
            break
        if roll == 9:
            penalty = rng.randint(10, 40)
            quality_label = f"Flawed (-{penalty}%)"
            value = int(round(value * (1 - penalty / 100.0)))
            value = apply_clamp(value)
            break
        if roll == 10:
            value = prev_rung(value)
            value = apply_clamp(value)
            quality_label = "Inferior (stepped down)"
            continue

    return int(value), quality_label, rolls


CUTTER_TYPES = {
    "Normal": {"skill_bonus": 0, "fee_mult": 1},
    "Dwarf": {"skill_bonus": 20, "fee_mult": 2},
    "Gnome": {"skill_bonus": 30, "fee_mult": 2},
}


def roll_for_category(categories: Sequence[str], *, rng: Optional[random.Random] = None) -> Tuple[str, int]:
    rng = rng or random
    r = rng.randint(1, 100)
    if r <= 25:
        idx = 0
    elif r <= 50:
        idx = 1
    elif r <= 70:
        idx = 2
    elif r <= 90:
        idx = 3
    elif r <= 99:
        idx = 4
    else:
        idx = 5
    return categories[idx], r


def roll_for_gem(gems_list: Sequence[Tuple[str, str, float]], *, rng: Optional[random.Random] = None) -> Tuple[int, int]:
    rng = rng or random
    n = len(gems_list)
    r = rng.randint(1, n)
    return r - 1, r


def select_batch_count(choice_index: int, custom_count: Optional[int] = None) -> int:
    if choice_index == 1:
        return 1
    if choice_index == 2:
        return 5
    if choice_index == 3:
        return 10
    if choice_index == 4:
        if custom_count is None:
            raise ValueError("custom_count must be provided when choice_index is 4")
        if custom_count < 1 or custom_count > 999:
            raise ValueError("custom_count must be between 1 and 999")
        return custom_count
    raise ValueError("choice_index must be between 1 and 4")


def choose_size(index: int) -> Tuple[str, float]:
    sizes = list(SIZE_MODIFIERS.keys())
    if index < 1 or index > len(sizes):
        raise ValueError("size index out of range")
    size_label = sizes[index - 1]
    return size_label, SIZE_MODIFIERS[size_label]


def determine_cutter_skill(
    skill_bonus: int,
    knows_skill_level: bool,
    known_skill_level: Optional[str],
    *,
    rng: Optional[random.Random] = None,
) -> Tuple[str, int, Optional[int]]:
    rng = rng or random
    if knows_skill_level:
        mapping = {
            "Shaky": 12,
            "Fair": 12,
            "Good": 12,
            "Superb": 20,
        }
        if known_skill_level not in mapping:
            raise ValueError("known_skill_level must be one of Shaky, Fair, Good, Superb")
        return known_skill_level, mapping[known_skill_level], None

    raw = rng.randint(1, 100)
    modded = min(raw + int(skill_bonus), 100)
    if modded <= 30:
        return "Shaky", 12, modded
    if modded <= 60:
        return "Fair", 12, modded
    if modded <= 90:
        return "Good", 12, modded
    return "Superb", 20, modded


def hire_retainer(
    state: RetainerState,
    request: RetainerRequest,
    *,
    rng: Optional[random.Random] = None,
) -> RetainerHireResult:
    if request.race not in CUTTER_TYPES:
        raise ValueError("Unknown cutter race")
    if request.months < 1:
        raise ValueError("months must be >= 1")

    cfg = CUTTER_TYPES[request.race]
    skill_level, dice_sides, skill_roll = determine_cutter_skill(
        cfg["skill_bonus"],
        request.knows_skill_level,
        request.known_skill_level,
        rng=rng,
    )

    fee_paid_gp = APPRAISAL_FEE_BASE * cfg["fee_mult"] * request.months
    new_state = RetainerState(
        active=True,
        race=request.race,
        type_bonus=cfg["skill_bonus"],
        fee_mult=cfg["fee_mult"],
        months=request.months,
        fee_paid_gp=fee_paid_gp,
        skill_level=skill_level,
        dice_sides=dice_sides,
        skill_roll=skill_roll,
    )
    return RetainerHireResult(
        state=new_state,
        total_fee_gp=fee_paid_gp,
        skill_level=skill_level,
        skill_roll=skill_roll,
        dice_sides=dice_sides,
    )


def cutter_adjustment(
    base_value_sp: int,
    *,
    cutter_type_name: str,
    skill_bonus: int,
    min_rung_sp: Optional[int] = None,
    max_rung_sp: Optional[int] = None,
    fixed_skill_level: Optional[str] = None,
    fixed_dice_sides: Optional[int] = None,
    fixed_skill_roll: Optional[int] = None,
    gem_index: int,
    gem_name: str,
    superb_decision_provider: Optional[Callable[[SuperbRollStep], bool]] = None,
    rng: Optional[random.Random] = None,
) -> CutterOutcome:
    rng = rng or random
    try:
        current = int(base_value_sp)
    except Exception:
        current = 0

    superb_steps: List[SuperbRollStep] = []
    if current >= CUTTING_CAP_SP:
        return CutterOutcome(
            performed=False,
            result_text=f"Cutting not permitted for gems valued at {gp(CUTTING_CAP_SP)} or more.",
            skill_level=fixed_skill_level,
            skill_roll=fixed_skill_roll,
            die_roll=None,
            ruined_prev_rung_sp=0,
            superb_steps=superb_steps,
            final_value_sp=current,
        )

    def apply_clamp(v: int) -> int:
        if min_rung_sp is not None and max_rung_sp is not None:
            return clamp_to_band(v, min_rung_sp, max_rung_sp)
        return v

    if fixed_skill_level is None or fixed_dice_sides is None:
        skill_level, dice_sides, skill_roll = determine_cutter_skill(
            skill_bonus,
            knows_skill_level=False,
            known_skill_level=None,
            rng=rng,
        )
    else:
        skill_level = fixed_skill_level
        dice_sides = fixed_dice_sides
        skill_roll = fixed_skill_roll

    last_die_roll: Optional[int] = None
    result_text = "No change."
    ruined_prev_rung = 0

    if skill_level != "Superb":
        roll = rng.randint(1, dice_sides)
        last_die_roll = roll
        if skill_level == "Shaky":
            if roll == 1:
                current = int(round(current * 2.0))
                current = apply_clamp(current)
                result_text = "Gem improved! (+100%)"
            elif 10 <= roll <= 12:
                ruined_prev_rung = previous_ladder_rung(current)
                current = 0
                result_text = "Gem ruined!"
            else:
                result_text = "No change."
        elif skill_level == "Fair":
            if roll in (1, 2):
                current = int(round(current * 2.0))
                current = apply_clamp(current)
                result_text = "Gem improved! (+100%)"
            elif roll == 12:
                ruined_prev_rung = previous_ladder_rung(current)
                current = 0
                result_text = "Gem ruined!"
            else:
                result_text = "No change."
        else:  # Good
            if roll in (1, 2, 3):
                current = int(round(current * 2.0))
                current = apply_clamp(current)
                result_text = "Gem improved! (+100%)"
            elif roll == 12:
                ruined_prev_rung = previous_ladder_rung(current)
                current = 0
                result_text = "Gem ruined!"
            else:
                result_text = "No change."

        return CutterOutcome(
            performed=True,
            result_text=result_text,
            skill_level=skill_level,
            skill_roll=skill_roll,
            die_roll=last_die_roll,
            ruined_prev_rung_sp=ruined_prev_rung,
            superb_steps=superb_steps,
            final_value_sp=current,
        )

    # Superb cutter flow
    while True:
        roll = rng.randint(1, dice_sides)
        last_die_roll = roll
        if roll in (1, 2, 3, 4, 5):
            current = int(round(current * 2.0))
            current = apply_clamp(current)
            result_text = "Gem improved! (+100%)"
        elif roll == 20:
            ruined_prev_rung = previous_ladder_rung(current)
            current = 0
            result_text = "Gem ruined!"
        else:
            result_text = "No change."

        cap_reached = current >= CUTTING_CAP_SP if current > 0 else False
        step = SuperbRollStep(
            gem_index=gem_index,
            gem_name=gem_name,
            roll=roll,
            result_text=result_text,
            current_value_sp=current,
            cap_reached=cap_reached,
            dice_sides=dice_sides,
        )
        superb_steps.append(step)

        if result_text == "Gem ruined!" or cap_reached:
            break

        continue_cut = False
        if superb_decision_provider is not None:
            continue_cut = bool(superb_decision_provider(step))
        if not continue_cut:
            break

    if current >= CUTTING_CAP_SP and current > 0:
        result_text = "Further cutting not permitted: gem has reached the cutting cap."
    elif current == 0 and result_text != "Gem ruined!":
        result_text = "No change."

    return CutterOutcome(
        performed=True,
        result_text=result_text,
        skill_level=skill_level,
        skill_roll=skill_roll,
        die_roll=last_die_roll,
        ruined_prev_rung_sp=ruined_prev_rung,
        superb_steps=superb_steps,
        final_value_sp=current,
    )


def process_batch(
    retainer: RetainerState,
    request: BatchRequest,
    *,
    rng: Optional[random.Random] = None,
    on_gem_start: Optional[Callable[[GemStartContext], None]] = None,
    on_appraisal: Optional[Callable[[GemAppraisalContext], None]] = None,
    cut_decision_provider: Optional[Callable[[GemAppraisalContext], bool]] = None,
    superb_decision_provider: Optional[Callable[[SuperbRollStep], bool]] = None,
) -> BatchResult:
    rng = rng or random
    if len(request.gem_plans) != request.batch_size:
        raise ValueError("gem_plans length must match batch_size")

    retainer_usage: Optional[RetainerUsage] = None
    if request.appraise:
        if not retainer.active:
            raise ValueError("Retainer must be active to appraise gems")
        retainer_usage = RetainerUsage(
            race=retainer.race or "Unknown",
            months=retainer.months,
            fee_paid_gp=retainer.fee_paid_gp,
            skill_level=retainer.skill_level,
            skill_roll=retainer.skill_roll,
            dice_sides=retainer.dice_sides,
            type_bonus=retainer.type_bonus,
        )

    gem_results: List[GemResult] = []
    total_surcharge_sp = 0
    total_final_value_sp = 0
    ruined_count = 0

    for idx, plan in enumerate(request.gem_plans, start=1):
        base_value_sp = to_sp(plan.base_gp * request.size_modifier)
        start_ctx = GemStartContext(
            index=idx,
            total=request.batch_size,
            plan=plan,
            size_label=request.size_label,
            size_modifier=request.size_modifier,
            base_value_sp=base_value_sp,
        )
        if on_gem_start:
            on_gem_start(start_ctx)

        min_rung_sp = max_rung_sp = None
        start_idx = rung_index_of(base_value_sp)
        if start_idx >= 0:
            min_idx = max(0, start_idx - 5)
            max_idx = min(len(RUNG_VALUES_SP) - 1, start_idx + 7)
            min_rung_sp = RUNG_VALUES_SP[min_idx]
            max_rung_sp = RUNG_VALUES_SP[max_idx]

        appraisal = GemAppraisal(
            base_value_sp=base_value_sp,
            adjusted_value_sp=base_value_sp,
            quality_label="Average (unappraised)" if not request.appraise else "Average",
        )

        if request.appraise:
            new_value_sp, quality_label, rolls = adjust_value(
                base_value_sp,
                min_rung_sp=min_rung_sp,
                max_rung_sp=max_rung_sp,
                rng=rng,
            )
            appraisal = GemAppraisal(
                base_value_sp=base_value_sp,
                adjusted_value_sp=new_value_sp,
                quality_label=quality_label,
                rolls=rolls,
                magical_property=lookup_magical_property(plan.name),
                color_properties=color_reputed_properties(plan.color),
            )

        appraisal_ctx = GemAppraisalContext(
            index=idx,
            total=request.batch_size,
            plan=plan,
            size_label=request.size_label,
            size_modifier=request.size_modifier,
            base_value_sp=base_value_sp,
            appraisal=appraisal,
            retainer_usage=retainer_usage,
        )
        if on_appraisal:
            on_appraisal(appraisal_ctx)

        perform_cut = False
        cutter_outcome = CutterOutcome(
            performed=False,
            result_text="Cutting not permitted (no appraisal)." if not request.appraise else "No gemcutting performed after appraisal.",
            skill_level=retainer.skill_level if request.appraise else None,
            skill_roll=retainer.skill_roll if request.appraise else None,
            die_roll=None,
            ruined_prev_rung_sp=0,
            superb_steps=[],
            final_value_sp=appraisal.adjusted_value_sp,
        )

        if request.appraise:
            if cut_decision_provider is not None:
                perform_cut = bool(cut_decision_provider(appraisal_ctx))
            if perform_cut:
                cutter_outcome = cutter_adjustment(
                    appraisal.adjusted_value_sp,
                    cutter_type_name=retainer.race or "Normal",
                    skill_bonus=retainer.type_bonus,
                    min_rung_sp=min_rung_sp,
                    max_rung_sp=max_rung_sp,
                    fixed_skill_level=retainer.skill_level,
                    fixed_dice_sides=retainer.dice_sides,
                    fixed_skill_roll=retainer.skill_roll,
                    gem_index=idx,
                    gem_name=plan.name,
                    superb_decision_provider=superb_decision_provider,
                    rng=rng,
                )

        final_value_sp = cutter_outcome.final_value_sp if request.appraise else appraisal.base_value_sp
        surcharge_sp = 0
        fees_this_gem_sp = 0
        if request.appraise:
            basis_sp = appraisal.adjusted_value_sp
            if cutter_outcome.performed:
                basis_sp = cutter_outcome.final_value_sp if cutter_outcome.final_value_sp > 0 else cutter_outcome.ruined_prev_rung_sp
            surcharge_sp = int(round(basis_sp * request.surcharge_rate))
            fees_this_gem_sp = surcharge_sp

        gem_result = GemResult(
            index=idx,
            plan=plan,
            size_label=request.size_label,
            size_modifier=request.size_modifier,
            appraisal=appraisal,
            cutter_outcome=cutter_outcome,
            surcharge_sp=surcharge_sp,
            fees_this_gem_sp=fees_this_gem_sp,
            final_value_sp=final_value_sp,
        )
        gem_results.append(gem_result)

        total_surcharge_sp += surcharge_sp
        total_final_value_sp += final_value_sp
        if final_value_sp == 0:
            ruined_count += 1

    total_fees_sp = total_surcharge_sp

    return BatchResult(
        request=request,
        retainer_usage=retainer_usage,
        gem_results=gem_results,
        total_surcharge_sp=total_surcharge_sp,
        total_fees_sp=total_fees_sp,
        total_final_value_sp=total_final_value_sp,
        ruined_count=ruined_count,
    )
