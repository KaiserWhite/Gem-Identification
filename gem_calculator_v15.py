"""Command-line and GUI entry points for the gem identification workflow."""
from __future__ import annotations

import argparse
import random
from typing import Callable, List, Optional

from core import (
    CUTTING_CAP_SP,
    CUTTER_TYPES,
    GEMS,
    SIZE_MODIFIERS,
    BatchRequest,
    GemPlan,
    GemAppraisalContext,
    GemStartContext,
    RetainerRequest,
    RetainerState,
    SuperbRollStep,
    gp,
    to_sp,
    hire_retainer,
    process_batch,
    roll_for_category,
    roll_for_gem,
    select_batch_count,
    choose_size,
)


# ------------------------
# CLI UTILITIES
# ------------------------
def safe_int_choice(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            val = int(input(prompt))
            if val < min_val or val > max_val:
                print(f"Enter a number between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("Enter a valid number.")


def yes_no(prompt: str) -> bool:
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("Enter Y or N.")


def choose_cutter_type_cli() -> str:
    print("\nSelect gemcutter race:")
    print(" 1. Normal (no bonus, standard fees)")
    print(" 2. Dwarf (+20 to skill roll, fees x2)")
    print(" 3. Gnome (+30 to skill roll, fees x2)")
    idx = safe_int_choice("Choice: ", 1, 3)
    return ["Normal", "Dwarf", "Gnome"][idx - 1]


def choose_retainer_months_cli() -> int:
    return safe_int_choice("How many months will you retain the gemcutter? ", 1, 120)


def choose_skill_level_cli() -> str:
    print("Select cutter skill level:")
    print(" 1. Shaky (01-30)")
    print(" 2. Fair  (31-60)")
    print(" 3. Good  (61-90)")
    print(" 4. Superb (91-100)")
    idx = safe_int_choice("Choice: ", 1, 4)
    return ["Shaky", "Fair", "Good", "Superb"][idx - 1]


def prompt_batch_count() -> int:
    print("\nHow many gems do you want to process at once?")
    print(" 1. 1")
    print(" 2. 5")
    print(" 3. 10")
    print(" 4. X (custom)")
    idx = safe_int_choice("Choice: ", 1, 4)
    custom = None
    if idx == 4:
        custom = safe_int_choice("Enter a positive number (1–999): ", 1, 999)
    return select_batch_count(idx, custom)


def prompt_size_choice() -> tuple[str, float]:
    print("\nSelect gem size (applies to the whole batch):")
    size_labels = list(SIZE_MODIFIERS.keys())
    for i, label in enumerate(size_labels, start=1):
        modifier = SIZE_MODIFIERS[label]
        print(f" {i}. {label} (x{modifier})")
    idx = safe_int_choice("Choice: ", 1, len(size_labels))
    return choose_size(idx)


def prompt_category(rng: random.Random) -> str:
    categories = list(GEMS.keys())
    print("\nSelect gem category (applies to the whole batch):")
    if yes_no("Roll randomly for gem category using d%? (Y/N) "):
        category, roll = roll_for_category(categories, rng=rng)
        shown = "00" if roll == 100 else f"{roll:02d}"
        print(f"[Category Roll] d% = {shown} → {category}")
        return category

    for i, cat in enumerate(categories, start=1):
        print(f" {i}. {cat}")
    idx = safe_int_choice("Choice: ", 1, len(categories))
    return categories[idx - 1]


def prompt_gem_selection(
    gems_list: List[tuple[str, str, float]],
    rng: random.Random,
) -> tuple[int, bool]:
    if yes_no("Roll randomly for a specific gem in this category? (Y/N) "):
        index, roll = roll_for_gem(gems_list, rng=rng)
        name, color, _ = gems_list[index]
        print(f"[Gem Roll] d{len(gems_list)} = {roll} → {name} ({color})")
        return index, True

    for i, (name, color, _) in enumerate(gems_list, start=1):
        print(f" {i}. {name} ({color})")
    idx = safe_int_choice("Choice: ", 1, len(gems_list)) - 1
    name, color, _ = gems_list[idx]
    print(f"[Chosen] {name} ({color})")
    return idx, False


def collect_gem_plans(
    batch_size: int,
    gems_list: List[tuple[str, str, float]],
    rng: random.Random,
    mixed: bool,
) -> List[GemPlan]:
    plans: List[GemPlan] = []
    if not mixed:
        index, _ = prompt_gem_selection(gems_list, rng)
        name, color, base_gp = gems_list[index]
        plans = [GemPlan(name, color, base_gp) for _ in range(batch_size)]
        return plans

    auto_roll_each = yes_no("Roll randomly for EACH gem in this batch? (Y/N) ")
    if not auto_roll_each:
        print(f"\nGems available in this category:")
        for i, (name, color, _) in enumerate(gems_list, start=1):
            print(f" {i}. {name} ({color})")

    for gi in range(batch_size):
        print(f"\nSelecting gem {gi + 1} of {batch_size}")
        if auto_roll_each:
            idx, roll = roll_for_gem(gems_list, rng=rng)
            name, color, _ = gems_list[idx]
            print(f"[Gem Roll] d{len(gems_list)} = {roll} → {name} ({color})")
        else:
            if yes_no("Roll randomly for THIS gem? (Y/N) "):
                idx, roll = roll_for_gem(gems_list, rng=rng)
                name, color, _ = gems_list[idx]
                print(f"[Gem Roll] d{len(gems_list)} = {roll} → {name} ({color})")
            else:
                idx = safe_int_choice(f"Choose gem index (1-{len(gems_list)}): ", 1, len(gems_list)) - 1
                name, color, _ = gems_list[idx]
                print(f"[Chosen] {name} ({color})")
        _, _, base_gp = gems_list[idx]
        plans.append(GemPlan(name, color, base_gp))
    return plans


def handle_gem_start(ctx: GemStartContext) -> None:
    print(f"\n===== Gem {ctx.index} of {ctx.total} =====")
    print("\n--- Appraisal & Cutting ---")
    print(f"Gem: {ctx.plan.name} ({ctx.plan.color})")
    print(f"Size-adjusted base for this gem: {gp(ctx.base_value_sp)}")


def handle_appraisal(ctx: GemAppraisalContext) -> None:
    if not ctx.appraisal.rolls:
        return
    print(
        f"[Appraisal] Quality: {ctx.appraisal.quality_label}; value now {gp(ctx.appraisal.adjusted_value_sp)}; "
        f"rolls: {ctx.appraisal.rolls}"
    )
    print(f"[Appraisal] Reputed magical properties: {ctx.appraisal.magical_property}")
    if ctx.appraisal.color_properties:
        print("[Appraisal] Color-based reputed properties:")
        for color, note in ctx.appraisal.color_properties:
            print(f" - {color}: {note}")


def make_cut_decision_provider(auto_cut_all: bool) -> Callable[[GemAppraisalContext], bool]:
    def provider(ctx: GemAppraisalContext) -> bool:
        if not ctx.appraisal.rolls:
            return False
        if auto_cut_all:
            return True
        return yes_no("\nProceed with CUTTING on this gem? (Y/N) ")

    return provider


def make_superb_decision_provider() -> Callable[[SuperbRollStep], bool]:
    def provider(step: SuperbRollStep) -> bool:
        print(
            f"[Superb cut] d{step.dice_sides}={step.roll}: {step.result_text} — "
            f"current value: {gp(step.current_value_sp)}"
        )
        if step.cap_reached:
            print(f"Further cutting not permitted: gem has reached {gp(CUTTING_CAP_SP)} or more.")
            return False
        if step.result_text == "Gem ruined!":
            return False
        return yes_no("Superb cutter may try again. Roll again? (Y/N) ")

    return provider


def display_gem_results(batch_request: BatchRequest, result, retainer_usage) -> None:
    print("\n--- GEM RESULTS ---")
    print(f"Category: {batch_request.category}")
    print(f"Size: {result.size_label} (x{result.size_modifier})")
    print(f"Base value after size: {gp(result.appraisal.base_value_sp)}")
    print(f"Rolls on adjustment table (DMG 26): {result.appraisal.rolls}")
    print(f"Quality: {result.appraisal.quality_label}")
    if retainer_usage:
        shown_roll = "n/a" if retainer_usage.skill_roll is None else str(retainer_usage.skill_roll)
        print(f"Gemcutter race: {retainer_usage.race}")
        print(
            f"Hire term: Monthly ({retainer_usage.months} month(s)) — retainer already paid: "
            f"{retainer_usage.fee_paid_gp:,} gp"
        )
        print(f"Gemcutter skill (retainer): {retainer_usage.skill_level} (roll {shown_roll})")
    print(f"Gemcutter: {result.cutter_outcome.result_text}")
    if result.cutter_outcome.performed and result.cutter_outcome.skill_level:
        shown = "n/a" if result.cutter_outcome.skill_roll is None else str(result.cutter_outcome.skill_roll)
        print(f"Gemcutter skill (this cut): {result.cutter_outcome.skill_level} (roll {shown})")
        if result.cutter_outcome.die_roll is not None:
            print(f"Gemcutter die roll: {result.cutter_outcome.die_roll}")
        if result.cutter_outcome.superb_steps:
            rolls = [step.roll for step in result.cutter_outcome.superb_steps]
            print(f"Superb sequence: {rolls}")
    print(f"Final value: {gp(result.final_value_sp)}")
    print(f"Magical properties: {result.appraisal.magical_property}")
    if result.appraisal.color_properties:
        print("Color-based reputed properties:")
        for color, note in result.appraisal.color_properties:
            print(f" - {color}: {note}")
    if retainer_usage:
        print("\n--- FEES BREAKDOWN ---")
        label = "identification + cutting" if result.cutter_outcome.performed else "identification only"
        print(f"Surcharge for this gem ({label}): {gp(result.surcharge_sp)}")
        print(
            f"(Monthly retainer already paid for session: {retainer_usage.fee_paid_gp:,} gp for "
            f"{retainer_usage.months} month(s))"
        )
        print(f"Total fees charged for THIS gem: {gp(result.fees_this_gem_sp)}")
    print("\n--- END OF RESULTS ---")


def display_batch_summary(batch_result) -> None:
    print("\n=== BATCH SUMMARY ===")
    print(f"Gems processed: {batch_result.request.batch_size}")
    print(f"Ruined: {batch_result.ruined_count}")
    print(f"Sum of final values: {gp(batch_result.total_final_value_sp)}")
    if batch_result.request.appraise:
        print(f"Total surcharges (all gems this batch): {gp(batch_result.total_surcharge_sp)}")
    print(f"Total fees paid THIS batch (excluding prior retainer): {gp(batch_result.total_fees_sp)}")

    print("\nEnding value per gem:")
    for rec in batch_result.gem_results:
        if rec.final_value_sp > 0:
            print(f"  Gem {rec.index:>2} — {rec.plan.name}: {gp(rec.final_value_sp)}")
        else:
            prev = rec.cutter_outcome.ruined_prev_rung_sp
            note = f" (previous rung {gp(prev)})" if prev else ""
            print(f"  Gem {rec.index:>2} — {rec.plan.name}: Ruined{note}")


def run_cli() -> None:
    rng = random.Random()
    retainer = RetainerState()

    while True:
        batch_n = prompt_batch_count()
        category = prompt_category(rng)
        gems_list = list(GEMS[category])

        print("\nGems for this batch can be identical or vary per item.")
        mixed_gems = yes_no("Allow different gems within this batch (same category)? (Y/N) ")

        size_label, size_mod = prompt_size_choice()

        plans = collect_gem_plans(batch_n, gems_list, rng, mixed_gems)

        if not mixed_gems:
            base_sp = to_sp(plans[0].base_gp * size_mod)
            print(f"\n== Starting batch of {batch_n} gem(s) ==")
            print(f"Category: {category}")
            print(f"Gem (same for all): {plans[0].name} ({plans[0].color})")
            print(f"Size: {size_label} (x{size_mod}) | Size-adjusted base: {gp(base_sp)}")
            print("Each gem will be appraised/cut individually from this same base.\n")
        else:
            print(f"\n== Starting batch of {batch_n} gem(s) ==")
            print(f"Category: {category}")
            print(f"Size (same for all): {size_label} (x{size_mod})")
            print("Each gem will be selected per item; base value depends on the chosen gem's base for this category.\n")

        did_appraisal_batch = False

        if retainer.active:
            print(
                f"[Retainer] Using existing {retainer.race} (fee already paid: "
                f"{retainer.fee_paid_gp:,} gp for {retainer.months} month(s))."
            )
            shown = "n/a" if retainer.skill_roll is None else str(retainer.skill_roll)
            print(f"[Retainer Skill Persisting] {retainer.skill_level} (roll {shown})")
            did_appraisal_batch = yes_no("Appraise the entire batch with your retainer? (Y/N) ")
        else:
            print("\nNo retainer is active. You must hire a monthly retainer to appraise/cut.")
            if yes_no("Hire a gemcutter retainer now to appraise this batch? (Y/N) "):
                race = choose_cutter_type_cli()
                months = choose_retainer_months_cli()
                knows_skill = yes_no("Do you already know the gemcutter's skill level for this retainer? (Y/N) ")
                known_skill = choose_skill_level_cli() if knows_skill else None
                hire_result = hire_retainer(
                    retainer,
                    RetainerRequest(
                        race=race,
                        months=months,
                        knows_skill_level=knows_skill,
                        known_skill_level=known_skill,
                    ),
                    rng=rng,
                )
                retainer = hire_result.state
                print(
                    f"[Retainer Hired] {retainer.race} for {retainer.months} month(s). "
                    f"One-time fee paid: {retainer.fee_paid_gp:,} gp."
                )
                shown = "n/a" if retainer.skill_roll is None else str(retainer.skill_roll)
                print(f"[Retainer Skill Persisting] {retainer.skill_level} (roll {shown})")
                did_appraisal_batch = True
            else:
                did_appraisal_batch = False

        auto_cut_all = False
        cut_provider = None
        superb_provider = None
        if did_appraisal_batch:
            auto_cut_all = yes_no("Auto-cut ALL gems in this batch? (Y/N) ")
            cut_provider = make_cut_decision_provider(auto_cut_all)
            superb_provider = make_superb_decision_provider()

        batch_request = BatchRequest(
            batch_size=batch_n,
            category=category,
            size_label=size_label,
            size_modifier=size_mod,
            gem_plans=plans,
            appraise=did_appraisal_batch,
        )

        result = process_batch(
            retainer,
            batch_request,
            rng=rng,
            on_gem_start=handle_gem_start,
            on_appraisal=handle_appraisal,
            cut_decision_provider=cut_provider,
            superb_decision_provider=superb_provider,
        )

        for gem_result in result.gem_results:
            display_gem_results(result.request, gem_result, result.retainer_usage)

        display_batch_summary(result)

        cont = input("\nBatch complete. Press Enter to process another batch, or type Q to quit: ").strip().lower()
        if cont == "q":
            print("Goodbye!")
            break


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gem identification workflow")
    parser.add_argument("--gui", action="store_true", help="Launch the Tkinter GUI instead of the CLI")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    if args.gui:
        from gui import run as run_gui

        run_gui()
    else:
        run_cli()


if __name__ == "__main__":
    main()
