"""Tkinter-based GUI for the gem identification and cutting workflow."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

import tkinter as tk
from tkinter import messagebox, ttk

from core import (
    CUTTER_TYPES,
    GEMS,
    SIZE_MODIFIERS,
    BatchRequest,
    BatchResult,
    GemAppraisalContext,
    GemPlan,
    GemResult,
    GemStartContext,
    RetainerRequest,
    RetainerState,
    SuperbRollStep,
    gp,
    hire_retainer,
    process_batch,
    roll_for_category,
    roll_for_gem,
)


@dataclass
class GemRow:
    """Represents the desired gem plan for a single row in the GUI."""

    name: str
    color: str
    base_gp: float


class GemApp:
    """Main GUI application for gem identification."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Gem Identification & Cutting")
        self.root.geometry("1100x750")

        self.rng = random.Random()
        self.retainer_state = RetainerState()

        self.category_var = tk.StringVar(value=list(GEMS.keys())[0])
        self.batch_size_var = tk.IntVar(value=1)
        self.mixed_var = tk.BooleanVar(value=False)
        self.size_var = tk.StringVar(value=list(SIZE_MODIFIERS.keys())[2])
        self.appraise_var = tk.BooleanVar(value=False)
        self.auto_cut_var = tk.BooleanVar(value=False)

        self.selected_row_index: Optional[int] = None
        self.gem_rows: List[GemRow] = []
        self.latest_result: Optional[BatchResult] = None

        self._build_ui()
        self._initialize_rows()
        self._update_retainer_summary()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.retainer_frame = ttk.Frame(notebook, padding=12)
        self.batch_frame = ttk.Frame(notebook, padding=12)
        self.results_frame = ttk.Frame(notebook, padding=12)

        notebook.add(self.retainer_frame, text="Retainer")
        notebook.add(self.batch_frame, text="Batch Setup")
        notebook.add(self.results_frame, text="Processing & Results")

        self._build_retainer_tab()
        self._build_batch_tab()
        self._build_results_tab()

    def _build_retainer_tab(self) -> None:
        frame = self.retainer_frame

        header = ttk.Label(frame, text="Hire or review your gemcutter retainer", font=("TkDefaultFont", 12, "bold"))
        header.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        ttk.Label(frame, text="Cutter race:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.cutter_type = ttk.Combobox(frame, values=list(CUTTER_TYPES.keys()), state="readonly")
        self.cutter_type.current(0)
        self.cutter_type.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(frame, text="Retainer term (months):").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.months_spin = ttk.Spinbox(frame, from_=1, to=120, width=6)
        self.months_spin.set("1")
        self.months_spin.grid(row=1, column=3, sticky="w", pady=5)

        self.know_skill_var = tk.BooleanVar(value=False)
        know_skill_cb = ttk.Checkbutton(frame, text="I know the cutter's skill level", variable=self.know_skill_var, command=self._toggle_known_skill)
        know_skill_cb.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        ttk.Label(frame, text="Known skill level:").grid(row=2, column=2, sticky="e", padx=5, pady=5)
        self.skill_level_box = ttk.Combobox(frame, values=["Shaky", "Fair", "Good", "Superb"], state="disabled")
        self.skill_level_box.grid(row=2, column=3, sticky="w", pady=5)

        buttons = ttk.Frame(frame)
        buttons.grid(row=3, column=0, columnspan=4, sticky="w", pady=10)

        ttk.Button(buttons, text="Hire / Update Retainer", command=self._hire_retainer).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(buttons, text="Release Retainer", command=self._release_retainer).grid(row=0, column=1)

        summary_lab = ttk.Label(frame, text="Current retainer status:", font=("TkDefaultFont", 11, "bold"))
        summary_lab.grid(row=4, column=0, columnspan=4, sticky="w", pady=(15, 5))

        self.retainer_summary = tk.Text(frame, height=8, width=80, state="disabled", wrap="word")
        self.retainer_summary.grid(row=5, column=0, columnspan=4, sticky="nsew")

        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(3, weight=1)

    def _build_batch_tab(self) -> None:
        frame = self.batch_frame

        header = ttk.Label(frame, text="Configure batch parameters", font=("TkDefaultFont", 12, "bold"))
        header.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        ttk.Label(frame, text="Batch size:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.batch_size_spin = ttk.Spinbox(frame, from_=1, to=999, textvariable=self.batch_size_var, width=6, command=self._on_batch_size_change)
        self.batch_size_spin.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(frame, text="Gem category:").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.category_box = ttk.Combobox(frame, values=list(GEMS.keys()), textvariable=self.category_var, state="readonly")
        self.category_box.grid(row=1, column=3, sticky="w", pady=5)
        self.category_box.bind("<<ComboboxSelected>>", lambda _evt: self._on_category_change())

        ttk.Button(frame, text="Roll Category", command=self._roll_category).grid(row=1, column=4, sticky="w", padx=(8, 0))

        ttk.Label(frame, text="Gem size:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.size_frame = ttk.Frame(frame)
        self.size_frame.grid(row=2, column=1, columnspan=3, sticky="w")
        self.size_radios: Dict[str, ttk.Radiobutton] = {}
        for i, label in enumerate(SIZE_MODIFIERS.keys()):
            rb = ttk.Radiobutton(self.size_frame, text=f"{label} (x{SIZE_MODIFIERS[label]})", value=label, variable=self.size_var)
            rb.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            self.size_radios[label] = rb

        self.mixed_check = ttk.Checkbutton(frame, text="Allow different gems within this batch", variable=self.mixed_var, command=self._on_mixed_toggle)
        self.mixed_check.grid(row=3, column=0, columnspan=3, sticky="w", pady=10)

        ttk.Label(frame, text="Gem selection:").grid(row=4, column=0, sticky="ne", padx=5)
        gem_controls = ttk.Frame(frame)
        gem_controls.grid(row=4, column=1, columnspan=4, sticky="nsew")

        self.gem_choice_var = tk.StringVar()
        self.gem_choice_box = ttk.Combobox(gem_controls, state="readonly")
        self.gem_choice_box.grid(row=0, column=0, sticky="w", padx=(0, 8), pady=5)

        ttk.Button(gem_controls, text="Roll Gem", command=self._roll_gem_for_selection).grid(row=0, column=1, padx=5)
        ttk.Button(gem_controls, text="Set Selected Row", command=self._apply_gem_to_selected_row).grid(row=0, column=2, padx=5)
        ttk.Button(gem_controls, text="Fill Entire Batch", command=self._fill_entire_batch).grid(row=0, column=3, padx=5)
        ttk.Button(gem_controls, text="Roll Batch", command=self._roll_entire_batch).grid(row=0, column=4, padx=5)

        self.plans_tree = ttk.Treeview(frame, columns=("gem", "color", "base"), show="headings", selectmode="browse", height=12)
        self.plans_tree.heading("gem", text="Gem")
        self.plans_tree.heading("color", text="Color")
        self.plans_tree.heading("base", text="Base GP")
        self.plans_tree.column("gem", width=180)
        self.plans_tree.column("color", width=200)
        self.plans_tree.column("base", width=100, anchor="e")
        self.plans_tree.grid(row=5, column=0, columnspan=5, sticky="nsew", pady=(10, 0))
        self.plans_tree.bind("<<TreeviewSelect>>", self._on_plan_select)

        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(4, weight=1)

    def _build_results_tab(self) -> None:
        frame = self.results_frame

        options_frame = ttk.LabelFrame(frame, text="Batch Processing Options")
        options_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Checkbutton(options_frame, text="Appraise and cut this batch (requires active retainer)", variable=self.appraise_var, command=self._sync_appraise_controls).grid(row=0, column=0, sticky="w", padx=8, pady=5)
        ttk.Checkbutton(options_frame, text="Automatically cut all gems", variable=self.auto_cut_var).grid(row=0, column=1, sticky="w", padx=8, pady=5)

        ttk.Button(options_frame, text="Process Batch", command=self._process_batch).grid(row=0, column=2, padx=8, pady=5)

        splitter = ttk.Panedwindow(frame, orient=tk.VERTICAL)
        splitter.pack(fill=tk.BOTH, expand=True)

        top_panel = ttk.Frame(splitter)
        bottom_panel = ttk.Frame(splitter)
        splitter.add(top_panel, weight=3)
        splitter.add(bottom_panel, weight=2)

        self.results_tree = ttk.Treeview(top_panel, columns=("gem", "quality", "final", "fees"), show="headings", height=12)
        self.results_tree.heading("gem", text="Gem")
        self.results_tree.heading("quality", text="Quality")
        self.results_tree.heading("final", text="Final Value")
        self.results_tree.heading("fees", text="Fees")
        self.results_tree.column("gem", width=200)
        self.results_tree.column("quality", width=220)
        self.results_tree.column("final", width=140, anchor="e")
        self.results_tree.column("fees", width=120, anchor="e")
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        self.results_tree.bind("<<TreeviewSelect>>", self._on_result_select)

        info_frame = ttk.Frame(bottom_panel)
        info_frame.pack(fill=tk.BOTH, expand=True)

        self.summary_text = tk.Text(info_frame, height=6, state="disabled", wrap="word")
        self.summary_text.pack(fill=tk.X, pady=(0, 8))

        detail_label = ttk.Label(info_frame, text="Gem details:", font=("TkDefaultFont", 11, "bold"))
        detail_label.pack(anchor="w")

        self.detail_text = tk.Text(info_frame, height=12, state="disabled", wrap="word")
        self.detail_text.pack(fill=tk.BOTH, expand=True)

        log_label = ttk.Label(info_frame, text="Processing log:", font=("TkDefaultFont", 11, "bold"))
        log_label.pack(anchor="w", pady=(10, 0))

        self.log_text = tk.Text(info_frame, height=8, state="disabled", wrap="word")
        self.log_text.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------
    # Retainer interactions
    # ------------------------------------------------------------------
    def _toggle_known_skill(self) -> None:
        if self.know_skill_var.get():
            self.skill_level_box.configure(state="readonly")
            if not self.skill_level_box.get():
                self.skill_level_box.current(0)
        else:
            self.skill_level_box.set("")
            self.skill_level_box.configure(state="disabled")

    def _hire_retainer(self) -> None:
        try:
            months = int(self.months_spin.get())
        except ValueError:
            messagebox.showerror("Invalid months", "Enter a valid number of months between 1 and 120.")
            return

        if months < 1 or months > 120:
            messagebox.showerror("Invalid months", "Retainer term must be between 1 and 120 months.")
            return

        knows_skill = self.know_skill_var.get()
        known_skill = self.skill_level_box.get() if knows_skill else None

        try:
            result = hire_retainer(
                self.retainer_state,
                RetainerRequest(
                    race=self.cutter_type.get(),
                    months=months,
                    knows_skill_level=knows_skill,
                    known_skill_level=known_skill,
                ),
                rng=self.rng,
            )
        except ValueError as exc:
            messagebox.showerror("Retainer error", str(exc))
            return

        self.retainer_state = result.state
        self._update_retainer_summary()
        messagebox.showinfo("Retainer updated", "Retainer status has been updated.")

    def _release_retainer(self) -> None:
        self.retainer_state = RetainerState()
        self._update_retainer_summary()
        messagebox.showinfo("Retainer released", "No active retainer is currently hired.")

    def _update_retainer_summary(self) -> None:
        lines: List[str] = []
        if not self.retainer_state.active:
            lines.append("No active retainer. Appraisal and cutting are unavailable until a retainer is hired.")
        else:
            lines.append(f"Active retainer: {self.retainer_state.race}")
            lines.append(f"Term remaining: {self.retainer_state.months} month(s)")
            lines.append(f"Fee already paid: {self.retainer_state.fee_paid_gp:,} gp")
            shown_roll = "n/a" if self.retainer_state.skill_roll is None else str(self.retainer_state.skill_roll)
            lines.append(f"Skill level: {self.retainer_state.skill_level} (roll {shown_roll})")

        text = "\n".join(lines)
        self._set_text_widget(self.retainer_summary, text)
        self._sync_appraise_controls()

    # ------------------------------------------------------------------
    # Batch configuration helpers
    # ------------------------------------------------------------------
    def _initialize_rows(self) -> None:
        self._populate_gem_choices()
        self._refresh_plan_rows()

    def _populate_gem_choices(self) -> None:
        gems_list = list(GEMS[self.category_var.get()])
        names = [name for name, _color, _gp in gems_list]
        self.gem_choice_box.configure(values=names)
        if names:
            self.gem_choice_box.current(0)

    def _refresh_plan_rows(self) -> None:
        desired_size = self.batch_size_var.get()
        if desired_size < 1:
            desired_size = 1
            self.batch_size_var.set(1)

        gems_list = list(GEMS[self.category_var.get()])
        default_name, default_color, default_gp = gems_list[0]

        while len(self.gem_rows) < desired_size:
            self.gem_rows.append(GemRow(default_name, default_color, default_gp))

        if len(self.gem_rows) > desired_size:
            self.gem_rows = self.gem_rows[:desired_size]

        # rebuild tree
        for item in self.plans_tree.get_children():
            self.plans_tree.delete(item)

        for idx, row in enumerate(self.gem_rows, start=1):
            self.plans_tree.insert("", tk.END, iid=str(idx - 1), values=(row.name, row.color, f"{row.base_gp:,.0f}"))

    def _on_batch_size_change(self) -> None:
        try:
            val = int(self.batch_size_spin.get())
            self.batch_size_var.set(max(1, min(999, val)))
        except ValueError:
            self.batch_size_var.set(1)
        self._refresh_plan_rows()

    def _on_category_change(self) -> None:
        self._populate_gem_choices()
        gems_list = list(GEMS[self.category_var.get()])
        default_name, default_color, default_gp = gems_list[0]
        for row in self.gem_rows:
            row.name = default_name
            row.color = default_color
            row.base_gp = default_gp
        self._refresh_plan_rows()

    def _on_mixed_toggle(self) -> None:
        if not self.mixed_var.get():
            # keep all rows identical to first
            if self.gem_rows:
                first = self.gem_rows[0]
                for row in self.gem_rows:
                    row.name = first.name
                    row.color = first.color
                    row.base_gp = first.base_gp
            self._refresh_plan_rows()

    def _roll_category(self) -> None:
        categories = list(GEMS.keys())
        category, roll = roll_for_category(categories, rng=self.rng)
        shown = "00" if roll == 100 else f"{roll:02d}"
        messagebox.showinfo("Category roll", f"Rolled {shown} → {category}")
        self.category_var.set(category)
        self._on_category_change()

    def _roll_gem_for_selection(self) -> None:
        gems_list = list(GEMS[self.category_var.get()])
        idx, roll = roll_for_gem(gems_list, rng=self.rng)
        name, color, _ = gems_list[idx]
        messagebox.showinfo("Gem roll", f"Rolled d{len(gems_list)} = {roll} → {name} ({color})")
        self.gem_choice_box.set(name)

    def _apply_gem_to_selected_row(self) -> None:
        if self.selected_row_index is None:
            messagebox.showwarning("No selection", "Select a row in the plan list to update.")
            return
        self._apply_gem_to_index(self.selected_row_index)

    def _apply_gem_to_index(self, index: int) -> None:
        name = self.gem_choice_box.get()
        if not name:
            messagebox.showwarning("No gem chosen", "Select a gem from the dropdown first.")
            return
        gems_list = list(GEMS[self.category_var.get()])
        for gem_name, color, base in gems_list:
            if gem_name == name:
                self.gem_rows[index] = GemRow(gem_name, color, base)
                break
        self._refresh_plan_rows()

        if not self.mixed_var.get():
            first = self.gem_rows[index]
            for row in self.gem_rows:
                row.name = first.name
                row.color = first.color
                row.base_gp = first.base_gp
            self._refresh_plan_rows()

    def _fill_entire_batch(self) -> None:
        name = self.gem_choice_box.get()
        if not name:
            messagebox.showwarning("No gem chosen", "Select a gem to fill the batch.")
            return
        gems_list = list(GEMS[self.category_var.get()])
        for gem_name, color, base in gems_list:
            if gem_name == name:
                self.gem_rows = [GemRow(gem_name, color, base) for _ in self.gem_rows]
                break
        self._refresh_plan_rows()

    def _roll_entire_batch(self) -> None:
        gems_list = list(GEMS[self.category_var.get()])
        new_rows: List[GemRow] = []
        for _ in self.gem_rows:
            idx, roll = roll_for_gem(gems_list, rng=self.rng)
            name, color, base = gems_list[idx]
            new_rows.append(GemRow(name, color, base))
        self.gem_rows = new_rows
        self._refresh_plan_rows()

    def _on_plan_select(self, event: tk.Event) -> None:  # type: ignore[override]
        selection = self.plans_tree.selection()
        if not selection:
            self.selected_row_index = None
            return
        self.selected_row_index = int(selection[0])

    # ------------------------------------------------------------------
    # Processing helpers
    # ------------------------------------------------------------------
    def _sync_appraise_controls(self) -> None:
        if not self.retainer_state.active:
            self.appraise_var.set(False)
            self.auto_cut_var.set(False)

    def _process_batch(self) -> None:
        if self.appraise_var.get() and not self.retainer_state.active:
            messagebox.showerror("No retainer", "Hire a retainer before appraising and cutting gems.")
            return

        size_label = self.size_var.get()
        size_modifier = SIZE_MODIFIERS[size_label]

        gem_plans: List[GemPlan] = []
        for row in self.gem_rows:
            gem_plans.append(GemPlan(row.name, row.color, row.base_gp))

        batch_request = BatchRequest(
            batch_size=len(gem_plans),
            category=self.category_var.get(),
            size_label=size_label,
            size_modifier=size_modifier,
            gem_plans=gem_plans,
            appraise=self.appraise_var.get(),
        )

        self._set_text_widget(self.log_text, "")

        result = process_batch(
            self.retainer_state,
            batch_request,
            rng=self.rng,
            on_gem_start=self._handle_gem_start,
            on_appraisal=self._handle_appraisal,
            cut_decision_provider=self._make_cut_decision_provider(),
            superb_decision_provider=self._make_superb_decision_provider(),
        )

        self._populate_results(result)
        self._render_summary(result)

    def _handle_gem_start(self, ctx: GemStartContext) -> None:
        text = (
            f"Gem {ctx.index} of {ctx.total}: {ctx.plan.name} ({ctx.plan.color}) — "
            f"Size-adjusted base {gp(ctx.base_value_sp)}\n"
        )
        self._append_log(text)

    def _handle_appraisal(self, ctx: GemAppraisalContext) -> None:
        if not ctx.appraisal.rolls:
            return
        text = (
            f"Appraisal → {ctx.appraisal.quality_label}; value {gp(ctx.appraisal.adjusted_value_sp)}; "
            f"rolls {ctx.appraisal.rolls}\n"
        )
        self._append_log(text)

    def _make_cut_decision_provider(self) -> Optional[Callable[[GemAppraisalContext], bool]]:
        if not self.appraise_var.get():
            return None
        auto_cut = self.auto_cut_var.get()

        def provider(ctx: GemAppraisalContext) -> bool:
            if not ctx.appraisal.rolls:
                return False
            if auto_cut:
                return True
            prompt = (
                f"Proceed with cutting {ctx.plan.name}?\n"
                f"Quality: {ctx.appraisal.quality_label}\n"
                f"Current value: {gp(ctx.appraisal.adjusted_value_sp)}"
            )
            return messagebox.askyesno("Cut gem", prompt, parent=self.root)

        return provider

    def _make_superb_decision_provider(self) -> Optional[Callable[[SuperbRollStep], bool]]:
        if not self.appraise_var.get():
            return None

        def provider(step: SuperbRollStep) -> bool:
            base_message = (
                f"Superb cut result for {step.gem_name}: {step.result_text}\n"
                f"Current value: {gp(step.current_value_sp)}"
            )
            if step.cap_reached or step.result_text == "Gem ruined!":
                messagebox.showinfo("Superb cut", base_message, parent=self.root)
                return False
            return messagebox.askyesno("Superb cut", base_message + "\nRoll again?", parent=self.root)

        return provider

    # ------------------------------------------------------------------
    # Results rendering
    # ------------------------------------------------------------------
    def _populate_results(self, result: BatchResult) -> None:
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        for rec in result.gem_results:
            quality = rec.appraisal.quality_label if result.request.appraise else "n/a"
            final_value = gp(rec.final_value_sp)
            fees = gp(rec.fees_this_gem_sp) if result.request.appraise else "0 gp"
            self.results_tree.insert(
                "",
                tk.END,
                iid=str(rec.index - 1),
                values=(rec.plan.name, quality, final_value, fees),
            )

        if result.gem_results:
            self.results_tree.selection_set("0")
            self._show_gem_details(result.gem_results[0])
        else:
            self._set_text_widget(self.detail_text, "")

        self.latest_result = result

    def _render_summary(self, result: BatchResult) -> None:
        lines = [
            f"Batch size: {result.request.batch_size}",
            f"Category: {result.request.category}",
            f"Size: {result.request.size_label} (x{result.request.size_modifier})",
            f"Total final value: {gp(result.total_final_value_sp)}",
        ]
        if result.retainer_usage:
            shown_roll = (
                "n/a"
                if result.retainer_usage.skill_roll is None
                else str(result.retainer_usage.skill_roll)
            )
            lines.append(
                f"Retainer: {result.retainer_usage.race} — {result.retainer_usage.skill_level}"
                f" (roll {shown_roll})"
            )
            lines.append(
                f"Retainer term: {result.retainer_usage.months} month(s); fee paid:"
                f" {result.retainer_usage.fee_paid_gp:,} gp"
            )
        if result.request.appraise:
            lines.append(f"Total surcharges: {gp(result.total_surcharge_sp)}")
            lines.append(f"Total fees: {gp(result.total_fees_sp)}")
            lines.append(f"Ruined gems: {result.ruined_count}")
        self._set_text_widget(self.summary_text, "\n".join(lines))

    def _on_result_select(self, _event: tk.Event) -> None:  # type: ignore[override]
        selection = self.results_tree.selection()
        if not selection:
            return
        idx = int(selection[0])
        if not self.latest_result:
            return
        result: BatchResult = self.latest_result
        if 0 <= idx < len(result.gem_results):
            self._show_gem_details(result.gem_results[idx])

    def _show_gem_details(self, gem_result: GemResult) -> None:
        lines = [
            f"Gem: {gem_result.plan.name} ({gem_result.plan.color})",
            f"Size modifier: {gem_result.size_label} (x{gem_result.size_modifier})",
        ]
        if gem_result.appraisal.rolls:
            lines.append(f"Quality: {gem_result.appraisal.quality_label}")
            lines.append(f"Appraisal rolls: {gem_result.appraisal.rolls}")
            lines.append(f"Magical property: {gem_result.appraisal.magical_property or 'None'}")
            if gem_result.appraisal.color_properties:
                lines.append("Color properties:")
                for color, desc in gem_result.appraisal.color_properties:
                    lines.append(f" - {color}: {desc}")
        lines.append(f"Final value: {gp(gem_result.final_value_sp)}")
        if gem_result.cutter_outcome.performed:
            lines.append(f"Cutting outcome: {gem_result.cutter_outcome.result_text}")
            if gem_result.cutter_outcome.die_roll is not None:
                lines.append(f"Cutting die roll: {gem_result.cutter_outcome.die_roll}")
            if gem_result.cutter_outcome.superb_steps:
                rolls = [str(step.roll) for step in gem_result.cutter_outcome.superb_steps]
                lines.append(f"Superb roll sequence: {', '.join(rolls)}")
        if gem_result.fees_this_gem_sp:
            lines.append(f"Fees charged: {gp(gem_result.fees_this_gem_sp)}")

        self._set_text_widget(self.detail_text, "\n".join(lines))

    # ------------------------------------------------------------------
    # Logging utilities
    # ------------------------------------------------------------------
    def _append_log(self, message: str) -> None:
        current = self.log_text.get("1.0", tk.END)
        new_text = current.rstrip() + ("\n" if current.strip() else "") + message
        self._set_text_widget(self.log_text, new_text)

    def _set_text_widget(self, widget: tk.Text, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, value)
        widget.configure(state="disabled")

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        self.root.mainloop()


def run() -> None:
    """Launch the GUI application."""

    app = GemApp()
    app.run()


__all__ = ["run", "GemApp"]


if __name__ == "__main__":
    run()

