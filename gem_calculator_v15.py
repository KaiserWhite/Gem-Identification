import random

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
    "Huge": 2.0
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

# ------------------------
# COLOR NOTES (reputed properties by color)
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
    "black": "Black", "blue": "Blue", "green": "Green", "red": "Red",
    "white": "White", "clear": "Clear", "yellow": "Yellow",
    "bluish": "Blue", "blueish": "Blue", "greenish": "Green",
    "reddish": "Red", "whitish": "White", "blackish": "Black",
    "yellowish": "Yellow", "pinkish": "Red", "purplish": "Blue", "violet": "Blue",
    "azure": "Blue", "cerulean": "Blue", "cobalt": "Blue", "indigo": "Blue", "navy": "Blue", "sapphire": "Blue",
    "turquoise": "Blue",
    "emerald": "Green", "olive": "Green", "teal": "Green", "verdant": "Green",
    "crimson": "Red", "scarlet": "Red", "ruby": "Red", "magenta": "Red", "rose": "Red", "rosy": "Red", "pink": "Red",
    "milky": "White", "ivory": "White", "snow": "White", "snowy": "White", "colorless": "Clear",
    "gold": "Yellow", "golden": "Yellow", "lemon": "Yellow", "saffron": "Yellow", "amber": "Yellow", "honey": "Yellow",
}
COLOR_ORDER = ["Black", "Blue", "Clear", "Green", "Red", "White", "Yellow"]

def infer_color_notes_from_description(desc: str):
    s = desc.lower()
    found = set()
    for sub, canon in COLOR_SUBSTRINGS.items():
        if sub in s:
            found.add(canon)
    return [c for c in COLOR_ORDER if c in found]

def color_reputed_properties(desc: str):
    colors = infer_color_notes_from_description(desc)
    return [(c, COLOR_NOTES[c]) for c in colors]

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
        else:
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
    1,            # 1 sp
    5,            # 5 sp
    10,           # 10 sp
    20,           # 1 gp
    100,          # 5 gp
    200,          # 10 gp
    1_000,        # 50 gp
    2_000,        # 100 gp
    10_000,       # 500 gp
    20_000,       # 1,000 gp
    100_000,      # 5,000 gp
    200_000,      # 10,000 gp
    500_000,      # 25,000 gp
    1_000_000,    # 50,000 gp
    2_000_000,    # 100,000 gp
    5_000_000,    # 250,000 gp
    10_000_000,   # 500,000 gp
    20_000_000    # 1,000,000 gp
]

def floor_rung(value_sp: int):
    """Greatest rung (SP) <= value_sp; None if below smallest rung."""
    last = None
    for r in RUNG_VALUES_SP:
        if value_sp >= r:
            last = r
        else:
            break
    return last

def rung_index_of(value_sp: int) -> int:
    """Index of floor rung; -1 if below smallest."""
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
    """Previous rung strictly below the floor rung of value_sp; 0 if none."""
    fr = floor_rung(value_sp)
    if fr is None:
        return 0
    idx = RUNG_VALUES_SP.index(fr)
    return RUNG_VALUES_SP[idx-1] if idx > 0 else 0

def clamp_to_band(value_sp: int, min_rung_sp: int, max_rung_sp: int) -> int:
    return max(min_rung_sp, min(value_sp, max_rung_sp))

# ------------------------
# ADJUST VALUE (DMG p.26) — SP with rung band limits
# ------------------------
def adjust_value(base_value_sp: int, min_rung_sp=None, max_rung_sp=None):
    """
    1 -> step up to next rung; reroll
    2 -> double; stop
    3 -> +10%..+60%; stop
    4-8 -> unchanged; stop
    9 -> -10%..-40%; stop
    10 -> step down to previous rung; reroll
    """
    rolls = []
    value = int(base_value_sp)
    quality_label = "Average"

    def apply_clamp(v):
        if min_rung_sp is not None and max_rung_sp is not None:
            return clamp_to_band(v, min_rung_sp, max_rung_sp)
        return v

    while True:
        roll = random.randint(1, 10)
        rolls.append(roll)

        if roll == 1:
            value = next_rung(value)
            value = apply_clamp(value)
            quality_label = "Flawless (stepped up)"
            continue
        elif roll == 2:
            quality_label = "Excellent"
            value *= 2
            value = apply_clamp(value)
            break
        elif roll == 3:
            bonus = random.randint(10, 60)
            quality_label = f"Good (+{bonus}%)"
            value = int(round(value * (1 + bonus / 100.0)))
            value = apply_clamp(value)
            break
        elif 4 <= roll <= 8:
            quality_label = "Average"
            value = apply_clamp(value)
            break
        elif roll == 9:
            penalty = random.randint(10, 40)
            quality_label = f"Flawed (-{penalty}%)"
            value = int(round(value * (1 - penalty / 100.0)))
            value = apply_clamp(value)
            break
        elif roll == 10:
            value = prev_rung(value)
            value = apply_clamp(value)
            quality_label = "Inferior (stepped down)"
            continue

    return int(value), quality_label, rolls

# ------------------------
# CUTTER TYPES (race) & MONTHLY RETAINER ONLY
# ------------------------
CUTTER_TYPES = {
    "Normal": {"skill_bonus": 0, "fee_mult": 1},
    "Dwarf":  {"skill_bonus": 20, "fee_mult": 2},
    "Gnome":  {"skill_bonus": 30, "fee_mult": 2},
}

def choose_cutter_type():
    print("\nSelect gemcutter race:")
    print(" 1. Normal (no bonus, standard fees)")
    print(" 2. Dwarf (+20 to skill roll, fees x2)")
    print(" 3. Gnome (+30 to skill roll, fees x2)")
    idx = safe_int_choice("Choice: ", 1, 3)
    name = ["Normal", "Dwarf", "Gnome"][idx - 1]
    return name, CUTTER_TYPES[name]["skill_bonus"], CUTTER_TYPES[name]["fee_mult"]

def choose_retainer_months():
    """Ask how many months to retain the gemcutter (>=1)."""
    return safe_int_choice("How many months will you retain the gemcutter? ", 1, 120)

# ------------------------
# Batch-wide skill determination (used when hiring/ replacing retainer)
# ------------------------
def determine_cutter_skill(skill_bonus):
    """Return (skill_level, dice_sides, skill_roll_or_None) and persist for retainer."""
    if yes_no("Do you already know the gemcutter's skill level for this retainer? (Y/N) "):
        print("Select cutter skill level:")
        print(" 1. Shaky (01-30)")
        print(" 2. Fair  (31-60)")
        print(" 3. Good  (61-90)")
        print(" 4. Superb (91-100)")
        choice = safe_int_choice("Choice: ", 1, 4)
        if choice == 1:
            return "Shaky", 12, None
        elif choice == 2:
            return "Fair", 12, None
        elif choice == 3:
            return "Good", 12, None
        else:
            return "Superb", 20, None
    else:
        raw = random.randint(1, 100)
        modded = min(raw + int(skill_bonus), 100)
        if modded <= 30:
            return "Shaky", 12, modded
        elif modded <= 60:
            return "Fair", 12, modded
        elif modded <= 90:
            return "Good", 12, modded
        else:
            return "Superb", 20, modded

# ------------------------
# GEM CUTTER (skill & outcome) — SP units, +100% improvement, band-limited
# ------------------------
def cutter_adjustment(
    base_value_sp,
    cutter_type_name="Normal",
    skill_bonus=0,
    min_rung_sp=None,
    max_rung_sp=None,
    # fixed retainer/batch skill (no extra prompts)
    fixed_skill_level=None,
    fixed_dice_sides=None,
    fixed_skill_roll=None
):
    """
    Returns: (new_value_sp, result_text, skill_level, skill_roll, last_die, ruined_prev_rung_sp, superb_rolls)
    """
    try:
        current = int(base_value_sp)
    except Exception:
        current = 0
    superb_rolls = []
    if current >= CUTTING_CAP_SP:
        return current, f"Cutting not permitted for gems valued at {gp(CUTTING_CAP_SP)} or more.", None, None, None, 0, superb_rolls

    def apply_clamp(v):
        if min_rung_sp is not None and max_rung_sp is not None:
            return clamp_to_band(v, min_rung_sp, max_rung_sp)
        return v

    # ----- Skill (fixed by retainer/batch) -----
    if fixed_skill_level is not None and fixed_dice_sides is not None:
        skill_level = fixed_skill_level
        dice_sides  = fixed_dice_sides
        skill_roll  = fixed_skill_roll  # may be None if 'known'
    else:
        # Fallback (shouldn't happen when persisting retainer skill)
        if yes_no("Do you already know the gemcutter's skill level? (Y/N) "):
            print("Select cutter skill level:")
            print(" 1. Shaky (01-30)")
            print(" 2. Fair  (31-60)")
            print(" 3. Good  (61-90)")
            print(" 4. Superb (91-100)")
            choice = safe_int_choice("Choice: ", 1, 4)
            if choice == 1:
                skill_level, dice_sides = "Shaky", 12
            elif choice == 2:
                skill_level, dice_sides = "Fair", 12
            elif choice == 3:
                skill_level, dice_sides = "Good", 12
            else:
                skill_level, dice_sides = "Superb", 20
            skill_roll = None
        else:
            raw = random.randint(1, 100)
            modded = min(raw + int(skill_bonus), 100)
            skill_roll = modded
            if modded <= 30:
                skill_level, dice_sides = "Shaky", 12
            elif modded <= 60:
                skill_level, dice_sides = "Fair", 12
            elif modded <= 90:
                skill_level, dice_sides = "Good", 12
            else:
                skill_level, dice_sides = "Superb", 20

    last_die_roll = None
    last_result = "No change."
    ruined_prev_rung = 0

    # ----- Non-superb (single attempt) -----
    if skill_level != "Superb":
        roll = random.randint(1, dice_sides)
        last_die_roll = roll
        if skill_level == "Shaky":
            if roll == 1:
                current = int(round(current * 2.0)); last_result = "Gem improved! (+100%)"
                current = apply_clamp(current)
            elif 10 <= roll <= 12:
                ruined_prev_rung = previous_ladder_rung(current)
                current = 0; last_result = "Gem ruined!"
        elif skill_level == "Fair":
            if roll in (1, 2):
                current = int(round(current * 2.0)); last_result = "Gem improved! (+100%)"
                current = apply_clamp(current)
            elif roll == 12:
                ruined_prev_rung = previous_ladder_rung(current)
                current = 0; last_result = "Gem ruined!"
        else:  # Good
            if roll in (1, 2, 3):
                current = int(round(current * 2.0)); last_result = "Gem improved! (+100%)"
                current = apply_clamp(current)
            elif roll == 12:
                ruined_prev_rung = previous_ladder_rung(current)
                current = 0; last_result = "Gem ruined!"

        return current, last_result, skill_level, skill_roll, last_die_roll, ruined_prev_rung, superb_rolls

    # ----- Superb: iterative (manual continue; no auto-continue) -----
    while True:
        roll = random.randint(1, dice_sides)
        superb_rolls.append(roll)
        last_die_roll = roll

        if roll in (1, 2, 3, 4, 5):
            current = int(round(current * 2.0))
            current = apply_clamp(current)
            last_result = "Gem improved! (+100%)"
        elif roll == 20:
            ruined_prev_rung = previous_ladder_rung(current)
            current = 0
            last_result = "Gem ruined!"
        else:
            last_result = "No change."

        print(f"[Superb cut] d20={roll}: {last_result} — current value: {gp(current)}")

        if last_result == "Gem ruined!" or current >= CUTTING_CAP_SP:
            if current >= CUTTING_CAP_SP:
                print(f"Further cutting not permitted: gem has reached {gp(CUTTING_CAP_SP)} or more.")
            break

        if yes_no("Superb cutter may try again. Roll again? (Y/N) "):
            continue
        else:
            break

    return current, last_result, skill_level, skill_roll, last_die_roll, ruined_prev_rung, superb_rolls

# ------------------------
# SAFE INPUT
# ------------------------
def safe_int_choice(prompt, min_val, max_val):
    while True:
        try:
            val = int(input(prompt))
            if val < min_val or val > max_val:
                print(f"Enter a number between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("Enter a valid number.")

def yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        else:
            print("Enter Y or N.")

# ------------------------
# CATEGORY ROLL (DMG d% bands)
# ------------------------
def roll_for_category(categories):
    """
    Roll d% to pick category using DMG bands:
    01–25, 26–50, 51–70, 71–90, 91–99, 00(=100)
    Assumes categories are in DMG order as defined in GEMS.
    """
    r = random.randint(1, 100)  # 100 represents '00'
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
    chosen = categories[idx]
    shown = "00" if r == 100 else f"{r:02d}"
    print(f"[Category Roll] d% = {shown} → {chosen}")
    return chosen

# ------------------------
# GEM ROLL (dN within a category)
# ------------------------
def roll_for_gem(gems_list):
    """
    Roll a die equal to the number of gems in the category (dN)
    and pick that gem. Echo the roll and selection.
    """
    n = len(gems_list)
    r = random.randint(1, n)
    name, color, _ = gems_list[r - 1]
    print(f"[Gem Roll] d{n} = {r} → {name} ({color})")
    return r - 1  # return index

# ------------------------
# BATCH SELECTOR
# ------------------------
def select_batch_count():
    print("\nHow many gems do you want to process at once?")
    print(" 1. 1")
    print(" 2. 5")
    print(" 3. 10")
    print(" 4. X (custom)")
    idx = safe_int_choice("Choice: ", 1, 4)
    if idx == 1:
        return 1
    elif idx == 2:
        return 5
    elif idx == 3:
        return 10
    else:
        return safe_int_choice("Enter a positive number (1–999): ", 1, 999)

# ------------------------
# MAIN MENU / WORKFLOW  (MONTHLY ONLY, RETAINER + SKILL PERSIST ACROSS BATCHES)
# ------------------------
def main():
    # --- Session-persistent retainer and skill (persists until program ends) ---
    retainer_active = False
    retainer = {
        "race": None,
        "type_bonus": 0,
        "fee_mult": 1,
        "months": 0,
        "fee_paid_gp": 0,   # charged once when hired (kept in gp)
        "skill_level": None,
        "dice_sides": None,
        "skill_roll": None, # may be None if skill was "known"
    }

    while True:
        print("\n--- AD&D 1e Gem Generator ---")
        print("Process a batch of stones from a single category.")
        print("Employment: Monthly retainer ONLY (retainer & skill persist across batches this session).")
        if retainer_active:
            sr = f"{retainer['race']} | Months: {retainer['months']} | One-time fee paid: {retainer['fee_paid_gp']:,} gp"
            sk = f"{retainer['skill_level']} (roll {'n/a' if retainer['skill_roll'] is None else retainer['skill_roll']})"
            print(f"Retainer: {sr} | Skill: {sk}")
        else:
            print("No retainer hired yet.")
        print(" - Retainer fee (one-time): 100 gp × race multiplier × months (covers APPRAISAL for all batches this session).")
        print(" - Cutting is optional and per-gem (no extra job fee).")
        print(" - 10% surcharge per gem:")
        print("     • ID-only: 10% of that gem's identified value.")
        print("     • ID+Cut: 10% of that gem's ending value (or previous rung if ruined).")
        print(" ")
        print("1. Generate gem(s)")
        print("2. Hire / Replace retainer")
        print("3. Quit")
        print(" ")
        choice = safe_int_choice("Choice: ", 1, 3)
        if choice == 3:
            print("Goodbye!")
            break

        # Option 2: (Re)hire/replace retainer up front (skill set once, persists)
        if choice == 2:
            cutter_type_name, type_bonus, fee_mult = choose_cutter_type()
            months = choose_retainer_months()
            fee_paid = APPRAISAL_FEE_BASE * fee_mult * months
            skill_level, dice_sides, skill_roll = determine_cutter_skill(type_bonus)
            retainer_active = True
            retainer.update({
                "race": cutter_type_name,
                "type_bonus": type_bonus,
                "fee_mult": fee_mult,
                "months": months,
                "fee_paid_gp": fee_paid,
                "skill_level": skill_level,
                "dice_sides": dice_sides,
                "skill_roll": skill_roll,
            })
            print(f"\n[Retainer Hired] {cutter_type_name} for {months} month(s). One-time fee paid: {fee_paid:,} gp.")
            shown = "n/a" if skill_roll is None else str(skill_roll)
            print(f"[Retainer Skill Persisting] {skill_level} (roll {shown})")
            continue

        # --- Option 1: Generate gems (batch processing) ---
        batch_n = select_batch_count()

        # --- Choose the batch's base gem CATEGORY (manual or roll) ---
        categories = list(GEMS.keys())
        print("\nSelect gem category (applies to the whole batch):")
        if yes_no("Roll randomly for gem category using d%? (Y/N) "):
            category = roll_for_category(categories)
        else:
            for i, cat in enumerate(categories, start=1):
                print(f" {i}. {cat}")
            cat_idx = safe_int_choice("Choice: ", 1, len(categories)) - 1
            category = categories[cat_idx]

        gems_list = GEMS[category]

        # --- Mixed gems toggle ---
        print("\nGems for this batch can be identical or vary per item.")
        mixed_gems = yes_no("Allow different gems within this batch (same category)? (Y/N) ")

        if not mixed_gems:
            # Choose a single gem (manual or roll) for the whole batch
            print(f"\nSelect a gem from {category} (applies to the whole batch):")
            if yes_no("Roll randomly for a specific gem in this category? (Y/N) "):
                gem_idx = roll_for_gem(gems_list)
            else:
                for i, (name, color, base_gp) in enumerate(gems_list, start=1):
                    print(f" {i}. {name} ({color})")
                gem_idx = safe_int_choice("Choice: ", 1, len(gems_list)) - 1
            gem_name, gem_color, base_gp = gems_list[gem_idx]
            size_label, size_mod = choose_size_once()
            adjusted_base_sp = to_sp(base_gp * size_mod)

            # Establish rung band from this shared base (+7 / -5 rungs)
            start_idx = rung_index_of(adjusted_base_sp)
            min_idx = max(0, start_idx - 5)
            max_idx = min(len(RUNG_VALUES_SP) - 1, start_idx + 7)
            min_rung_sp = RUNG_VALUES_SP[min_idx]
            max_rung_sp = RUNG_VALUES_SP[max_idx]

            color_prop_pairs_batch = color_reputed_properties(gem_color)

            print(f"\n== Starting batch of {batch_n} gem(s) ==")
            print(f"Category: {category}")
            print(f"Gem (same for all): {gem_name} ({gem_color})")
            print(f"Size: {size_label} (x{size_mod}) | Size-adjusted base: {gp(adjusted_base_sp)}")
            print("Each gem will be appraised/cut individually from this same base.\n")

        else:
            # Mixed: choose size once; choose gem per item (auto-roll or per-item choice)
            size_label, size_mod = choose_size_once()

            print(f"\n== Starting batch of {batch_n} gem(s) ==")
            print(f"Category: {category}")
            print(f"Size (same for all): {size_label} (x{size_mod})")
            print("Each gem will be selected per item; base value depends on the chosen gem's base for this category.\n")

            auto_roll_each_gem = yes_no("Roll randomly for EACH gem in this batch? (Y/N) ")
            # Show the list once up front (helps manual selection)
            if not auto_roll_each_gem:
                print(f"\nGems available in {category}:")
                for i, (name, color, base_gp) in enumerate(gems_list, start=1):
                    print(f" {i}. {name} ({color})")

        # ---------------- Batch-level appraisal/cutting prompts ----------------
        did_appraisal_batch = False

        # If retainer active, use it automatically; else offer to hire now
        if retainer_active:
            print(f"[Retainer] Using existing {retainer['race']} (fee already paid: {retainer['fee_paid_gp']:,} gp for {retainer['months']} month(s)).")
            print(f"[Retainer Skill Persisting] {retainer['skill_level']} (roll {'n/a' if retainer['skill_roll'] is None else retainer['skill_roll']})")
            did_appraisal_batch = yes_no("Appraise the entire batch with your retainer? (Y/N) ")
        else:
            print("\nNo retainer is active. You must hire a monthly retainer to appraise/cut.")
            if yes_no("Hire a gemcutter retainer now to appraise this batch? (Y/N) "):
                cutter_type_name, type_bonus, fee_mult = choose_cutter_type()
                months = choose_retainer_months()
                fee_paid = APPRAISAL_FEE_BASE * fee_mult * months
                skill_level, dice_sides, skill_roll = determine_cutter_skill(type_bonus)
                retainer_active = True
                retainer.update({
                    "race": cutter_type_name,
                    "type_bonus": type_bonus,
                    "fee_mult": fee_mult,
                    "months": months,
                    "fee_paid_gp": fee_paid,
                    "skill_level": skill_level,
                    "dice_sides": dice_sides,
                    "skill_roll": skill_roll,
                })
                print(f"[Retainer Hired] {cutter_type_name} for {months} month(s). One-time fee paid: {fee_paid:,} gp.")
                shown = "n/a" if skill_roll is None else str(skill_roll)
                print(f"[Retainer Skill Persisting] {skill_level} (roll {shown})")
                did_appraisal_batch = True
            else:
                did_appraisal_batch = False

        # Decide auto-cut for this batch (only meaningful if appraising)
        auto_cut_all = False
        if did_appraisal_batch:
            auto_cut_all = yes_no("Auto-cut ALL gems in this batch? (Y/N) ")

        # Batch skill is the retainer's persisted skill
        batch_skill_level = retainer["skill_level"] if did_appraisal_batch else None
        batch_dice_sides = retainer["dice_sides"] if did_appraisal_batch else None
        batch_skill_roll = retainer["skill_roll"] if did_appraisal_batch else None

        # ---------------- Batch aggregations ----------------
        # Note: retainer fee is session-persistent; DO NOT add again.
        batch_total_fees_sp = 0           # per-gem surcharges in sp
        batch_total_surcharges_sp = 0     # sum of surcharges in sp
        batch_total_final_value_sp = 0
        batch_ruined_count = 0

        # Keep ending values for each gem
        per_gem_records = []  # list of {"index": int, "name": str, "final_value_sp": int, "ruined_prev_rung_sp": int}

        # ---------------- Process each gem ----------------
        for gi in range(batch_n):
            print(f"\n===== Gem {gi+1} of {batch_n} =====")

            # ----- Choose gem for this item (depends on mixed_gems) -----
            if not mixed_gems:
                # Use the single batch gem selected earlier
                this_gem_name, this_gem_color, this_base_gp = gem_name, gem_color, base_gp
            else:
                if 'auto_roll_each_gem' in locals() and auto_roll_each_gem:
                    idx = roll_for_gem(gems_list)
                else:
                    # Per-item choice or roll
                    if yes_no("Roll randomly for THIS gem? (Y/N) "):
                        idx = roll_for_gem(gems_list)
                    else:
                        idx = safe_int_choice(f"Choose gem index (1-{len(gems_list)}): ", 1, len(gems_list)) - 1
                        chosen = gems_list[idx]
                        print(f"[Chosen] {chosen[0]} ({chosen[1]})")
                this_gem_name, this_gem_color, this_base_gp = gems_list[idx]

            # ----- Compute per-gem base & band (size is shared) -----
            adjusted_base_sp = to_sp(this_base_gp * size_mod)

            start_idx = rung_index_of(adjusted_base_sp)
            min_idx = max(0, start_idx - 5)
            max_idx = min(len(RUNG_VALUES_SP) - 1, start_idx + 7)
            min_rung_sp = RUNG_VALUES_SP[min_idx]
            max_rung_sp = RUNG_VALUES_SP[max_idx]

            # ----- Per-gem state -----
            fees_this_gem_sp = 0  # ONLY per-gem surcharge (retainer already paid)
            skill_level = skill_roll = die_roll = None
            cutter_result = "No gemcutter hired."
            magical_prop = "Not identified"
            quality_label = "Average (unappraised)"
            rolls = []
            final_value_sp = adjusted_base_sp  # start from per-gem base
            ruined_prev_rung_sp = 0
            superb_rolls = []
            did_cutting = False

            print("\n--- Appraisal & Cutting ---")
            print(f"Gem: {this_gem_name} ({this_gem_color})")
            print(f"Size-adjusted base for this gem: {gp(adjusted_base_sp)}")

            # ---- Appraise (individual roll per gem) ----
            if did_appraisal_batch:
                final_value_sp, quality_label, rolls = adjust_value(
                    adjusted_base_sp, min_rung_sp=min_rung_sp, max_rung_sp=max_rung_sp
                )
                magical_prop = lookup_magical_property(this_gem_name)

                print(f"[Appraisal] Quality: {quality_label}; value now {gp(final_value_sp)}; rolls: {rolls}")
                print(f"[Appraisal] Reputed magical properties: {magical_prop}")
                color_prop_pairs = color_reputed_properties(this_gem_color)
                if color_prop_pairs:
                    print("[Appraisal] Color-based reputed properties:")
                    for c, note in color_prop_pairs:
                        print(f" - {c}: {note}")

                # ---- Cutting (optional per gem) ----
                if final_value_sp >= CUTTING_CAP_SP or adjusted_base_sp >= CUTTING_CAP_SP:
                    cutter_result = f"Cutting not permitted: base or appraised value is {gp(CUTTING_CAP_SP)} or more."
                else:
                    # Auto-cut whole batch? Otherwise ask per gem.
                    if auto_cut_all or yes_no("\nProceed with CUTTING on this gem? (Y/N) "):
                        did_cutting = True
                        final_value_sp, cutter_result, skill_level, skill_roll, die_roll, ruined_prev_rung_sp, superb_rolls = cutter_adjustment(
                            final_value_sp,
                            cutter_type_name=retainer["race"],
                            skill_bonus=retainer["type_bonus"],
                            min_rung_sp=min_rung_sp,
                            max_rung_sp=max_rung_sp,
                            fixed_skill_level=batch_skill_level,
                            fixed_dice_sides=batch_dice_sides,
                            fixed_skill_roll=batch_skill_roll
                        )
                    else:
                        cutter_result = "No gemcutting performed after appraisal."
            else:
                cutter_result = "Cutting not permitted (no appraisal)."

            # ---- 10% surcharge (always in monthly model) ----
            surcharge_sp = 0
            if did_appraisal_batch:
                if did_cutting:
                    basis_sp = final_value_sp if final_value_sp > 0 else ruined_prev_rung_sp
                else:
                    basis_sp = final_value_sp  # ID-only
                surcharge_sp = int(round(basis_sp * 0.10))
                fees_this_gem_sp += surcharge_sp
                batch_total_surcharges_sp += surcharge_sp

            # --- RESULTS (per gem) ---
            print("\n--- GEM RESULTS ---")
            print(f"Category: {category}")
            print(f"Size: {size_label} (x{size_mod})")
            print(f"Base value after size: {gp(adjusted_base_sp)}")
            print(f"Rolls on adjustment table (DMG 26): {rolls}")
            print(f"Quality: {quality_label}")
            if did_appraisal_batch:
                shown_batch = "n/a" if batch_skill_roll is None else str(batch_skill_roll)
                print(f"Gemcutter race: {retainer['race']}")
                print(f"Hire term: Monthly ({retainer['months']} month(s)) — retainer already paid: {retainer['fee_paid_gp']:,} gp")
                print(f"Gemcutter skill (retainer): {batch_skill_level} (roll {shown_batch})")
            print(f"Gemcutter: {cutter_result}")
            if skill_level:
                shown_skill_roll = "n/a" if skill_roll is None else str(skill_roll)
                print(f"Gemcutter skill (this cut): {skill_level} (roll {shown_skill_roll})")
                print(f"Gemcutter die roll: {die_roll}")
                if skill_level == "Superb" and superb_rolls:
                    print(f"Superb sequence: {superb_rolls}")
            print(f"Final value: {gp(final_value_sp)}")
            print(f"Magical properties: {magical_prop}")

            # Color-based reputed properties in Results (already printed under appraisal)

            # --- FEES BREAKDOWN (per gem) ---
            if did_appraisal_batch:
                print("\n--- FEES BREAKDOWN ---")
                label = "identification + cutting" if did_cutting else "identification only"
                print(f"Surcharge for this gem ({label}): {gp(surcharge_sp)}")
                print(f"(Monthly retainer already paid for session: {retainer['fee_paid_gp']:,} gp for {retainer['months']} month(s))")
                print(f"Total fees charged for THIS gem: {gp(fees_this_gem_sp)}")

            print("\n--- END OF RESULTS ---")

            # Record this gem's ending value (and previous rung if ruined)
            per_gem_records.append({
                "index": gi + 1,
                "name": this_gem_name,
                "final_value_sp": final_value_sp,
                "ruined_prev_rung_sp": ruined_prev_rung_sp
            })

            # Batch totals
            batch_total_fees_sp += fees_this_gem_sp
            batch_total_final_value_sp += final_value_sp
            if final_value_sp == 0:
                batch_ruined_count += 1

        # --- BATCH SUMMARY (retainer fee is session-persistent; not added here) ---
        print("\n=== BATCH SUMMARY ===")
        print(f"Gems processed: {batch_n}")
        print(f"Ruined: {batch_ruined_count}")
        print(f"Sum of final values: {gp(batch_total_final_value_sp)}")
        if did_appraisal_batch:
            print(f"Total surcharges (all gems this batch): {gp(batch_total_surcharges_sp)}")
        print(f"Total fees paid THIS batch (excluding prior retainer): {gp(batch_total_fees_sp)}")

        # Per-gem ending values
        print("\nEnding value per gem:")
        for rec in per_gem_records:
            i = rec["index"]
            nm = rec["name"]
            fv = rec["final_value_sp"]
            if fv > 0:
                print(f"  Gem {i:>2} — {nm}: {gp(fv)}")
            else:
                prev_rung_sp = rec["ruined_prev_rung_sp"]
                note = f" (previous rung {gp(prev_rung_sp)})" if prev_rung_sp else ""
                print(f"  Gem {i:>2} — {nm}: Ruined{note}")

        cont = input("\nBatch complete. Press Enter to process another batch, or type Q to quit: ").strip().lower()
        if cont == 'q':
            print("Goodbye!")
            break

# ------------------------
# SIZE PICKER (shared across the batch)
# ------------------------
def choose_size_once():
    sizes = list(SIZE_MODIFIERS.keys())
    print("\nSelect gem size (applies to the whole batch):")
    for i, s2 in enumerate(sizes, start=1):
        print(f" {i}. {s2} (x{SIZE_MODIFIERS[s2]})")
    size_idx = safe_int_choice("Choice: ", 1, len(sizes)) - 1
    size_label = sizes[size_idx]
    size_mod = SIZE_MODIFIERS[size_label]
    return size_label, size_mod

# ------------------------
# RUN PROGRAM
# ------------------------
if __name__ == "__main__":
    main()
