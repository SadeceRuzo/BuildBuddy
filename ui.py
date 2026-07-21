import webbrowser
import tkinter.font as tkfont

import customtkinter as ctk

from database import cpus, gpus, motherboards, rams
from compatibility import check_build


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Kendi GitHub kullanıcı adını / linkini buraya yaz
GITHUB_URL = "https://github.com/KULLANICI_ADIN"

# iOS (koyu mod) esintili renk paleti
COLORS = {
    "bg": "#1C1C1E",            # pencere arka planı
    "surface": "#2C2C2E",       # kart / panel yüzeyi
    "surface_alt": "#3A3A3C",   # ikinci seviye yüzey (liste satırları, textbox)
    "accent": "#0A84FF",        # iOS sistem mavisi (koyu mod)
    "accent_hover": "#3C9CFF",
    "text_primary": "#FFFFFF",
    "text_secondary": "#8E8E93",
    "separator": "#38383A",
}


class BuildBuddyApp:

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("BuildBuddy")
        self.root.geometry("1200x720")
        self.root.resizable(False, False)
        self.root.configure(fg_color=COLORS["bg"])

        # Sistemde varsa SF Pro / Helvetica Neue gibi Apple fontlarını,
        # yoksa en yakın alternatifi seçiyoruz (Tk root oluşturulduktan
        # sonra çağrılmalı, aksi halde font listesi okunamıyor).
        self.font_family = self._pick_font(
            ["SF Pro Display", "SF Pro Text", "Helvetica Neue", "Segoe UI", "Arial"]
        )
        self.mono_font = self._pick_font(
            ["SF Mono", "Menlo", "Consolas", "Courier New"]
        )

        self.selected_cpu = None
        self.selected_gpu = None
        self.selected_motherboard = None
        self.selected_ram = None

        self.create_ui()

    def run(self):
        self.root.mainloop()

    @staticmethod
    def _pick_font(preferred):
        available = set(tkfont.families())
        for name in preferred:
            if name in available:
                return name
        return preferred[-1]

    # ---------------- UI KURULUMU ----------------

    def create_ui(self):
        header = ctk.CTkFrame(self.root, fg_color="transparent")
        header.pack(fill="x", padx=35, pady=(25, 0))

        self.title = ctk.CTkLabel(
            header,
            text="BuildBuddy",
            font=(self.font_family, 34, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w"
        )
        self.title.pack(anchor="w")

        self.subtitle = ctk.CTkLabel(
            header,
            text="Your Personal PC Part Picker!",
            font=(self.font_family, 15),
            text_color=COLORS["text_secondary"],
            anchor="w"
        )
        self.subtitle.pack(anchor="w", pady=(2, 0))

        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=20)

        self.left_frame = ctk.CTkFrame(
            self.main_frame, width=350, corner_radius=24, fg_color=COLORS["surface"]
        )
        self.left_frame.pack(side="left", fill="y", padx=(0, 15), pady=0)

        self.right_frame = ctk.CTkFrame(
            self.main_frame, corner_radius=24, fg_color=COLORS["surface"]
        )
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(15, 0), pady=0)

        self.create_left_panel()
        self.create_right_panel()

    def create_left_panel(self):
        self.components_title = ctk.CTkLabel(
            self.left_frame,
            text="Components",
            font=(self.font_family, 20, "bold"),
            text_color=COLORS["text_primary"]
        )
        self.components_title.pack(pady=(24, 16))

        self.cpu_button = ctk.CTkButton(
            self.left_frame,
            text="  Select CPU",
            width=290,
            height=48,
            corner_radius=14,
            anchor="w",
            font=(self.font_family, 14),
            fg_color=COLORS["surface_alt"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text_primary"],
            command=self.open_cpu_selector
        )
        self.cpu_button.pack(pady=6, padx=25)

        self.gpu_button = ctk.CTkButton(
            self.left_frame,
            text="  Select GPU",
            width=290,
            height=48,
            corner_radius=14,
            anchor="w",
            font=(self.font_family, 14),
            fg_color=COLORS["surface_alt"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text_primary"],
            command=self.open_gpu_selector
        )
        self.gpu_button.pack(pady=6, padx=25)

        self.mb_button = ctk.CTkButton(
            self.left_frame,
            text="  Select Motherboard",
            width=290,
            height=48,
            corner_radius=14,
            anchor="w",
            font=(self.font_family, 14),
            fg_color=COLORS["surface_alt"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text_primary"],
            command=self.open_mb_selector
        )
        self.mb_button.pack(pady=6, padx=25)

        self.ram_button = ctk.CTkButton(
            self.left_frame,
            text="  Select RAM",
            width=290,
            height=48,
            corner_radius=14,
            anchor="w",
            font=(self.font_family, 14),
            fg_color=COLORS["surface_alt"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text_primary"],
            command=self.open_ram_selector
        )
        self.ram_button.pack(pady=6, padx=25)

        self.check_button = ctk.CTkButton(
            self.left_frame,
            text="Check Compatibility",
            width=290,
            height=50,
            corner_radius=16,
            font=(self.font_family, 15, "bold"),
            state="disabled",
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color=COLORS["text_primary"],
            command=self.check
        )
        self.check_button.pack(pady=(28, 10), padx=25)

        self.version_label = ctk.CTkLabel(
            self.left_frame,
            text="v1.1.0",
            font=(self.font_family, 12),
            text_color=COLORS["text_secondary"],
            cursor="hand2"
        )
        self.version_label.pack(side="bottom", pady=14)
        self.version_label.bind("<Button-1>", self.open_github)

    def open_github(self, event=None):
        webbrowser.open(GITHUB_URL)

    def create_right_panel(self):
        self.result_title = ctk.CTkLabel(
            self.right_frame,
            text="Build Report",
            font=(self.font_family, 22, "bold"),
            text_color=COLORS["text_primary"]
        )
        self.result_title.pack(pady=(24, 12), padx=25, anchor="w")

        self.result_box = ctk.CTkTextbox(
            self.right_frame,
            corner_radius=18,
            fg_color=COLORS["surface_alt"],
            text_color=COLORS["text_primary"],
            font=(self.mono_font, 14),
            border_width=0
        )
        self.result_box.pack(padx=25, pady=(0, 25), fill="both", expand=True)

        self.result_box.insert("0.0", "Select all components to start.")
        self.result_box.configure(state="disabled")

    # ---------------- SEÇİM PENCERELERİ ----------------

    def open_selector(self, title, database, callback):
        window = ctk.CTkToplevel(self.root)
        window.title(title)
        window.geometry("450x550")
        window.configure(fg_color=COLORS["bg"])
        window.grab_set()

        search = ctk.CTkEntry(
            window,
            width=380,
            height=40,
            corner_radius=20,
            border_width=0,
            fg_color=COLORS["surface_alt"],
            text_color=COLORS["text_primary"],
            placeholder_text="Search...",
            placeholder_text_color=COLORS["text_secondary"],
            font=(self.font_family, 14)
        )
        search.pack(pady=18)

        frame = ctk.CTkScrollableFrame(
            window,
            width=390,
            height=430,
            fg_color="transparent"
        )
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        def refresh(event=None):
            for widget in frame.winfo_children():
                widget.destroy()

            text = search.get().lower()

            for item in database:
                if text in item["name"].lower():
                    ctk.CTkButton(
                        frame,
                        text=item["name"],
                        width=350,
                        height=42,
                        corner_radius=12,
                        anchor="w",
                        font=(self.font_family, 13),
                        fg_color=COLORS["surface"],
                        hover_color=COLORS["accent"],
                        text_color=COLORS["text_primary"],
                        command=lambda x=item: select(x)
                    ).pack(pady=3)

        def select(item):
            callback(item)
            window.destroy()
            self.update_check_button()
            self.show_overview()

        search.bind("<KeyRelease>", refresh)
        refresh()

    def open_cpu_selector(self):
        self.open_selector("Select CPU", cpus, self.select_cpu)

    def open_gpu_selector(self):
        self.open_selector("Select GPU", gpus, self.select_gpu)

    def open_mb_selector(self):
        self.open_selector("Select Motherboard", motherboards, self.select_motherboard)

    def open_ram_selector(self):
        self.open_selector("Select RAM", rams, self.select_ram)

    # ---------------- SEÇİM CALLBACK'LERİ ----------------

    def select_cpu(self, cpu):
        self.selected_cpu = cpu
        self.cpu_button.configure(text=f"🖥  {cpu['name']}")

    def select_gpu(self, gpu):
        self.selected_gpu = gpu
        self.gpu_button.configure(text=f"🎮  {gpu['name']}")

    def select_motherboard(self, motherboard):
        self.selected_motherboard = motherboard
        self.mb_button.configure(text=f"🧩  {motherboard['name']}")

    def select_ram(self, ram):
        self.selected_ram = ram
        self.ram_button.configure(text=f"💾  {ram['name']}")

    def update_check_button(self):
        if (
            self.selected_cpu
            and self.selected_gpu
            and self.selected_motherboard
            and self.selected_ram
        ):
            self.check_button.configure(state="normal")

    # ---------------- RAPORLAR ----------------

    def update_overview(self):
        return f"""
══════════════════════
     BUILD OVERVIEW
══════════════════════

CPU
{self.selected_cpu["name"] if self.selected_cpu else "Not Selected"}

GPU
{self.selected_gpu["name"] if self.selected_gpu else "Not Selected"}

Motherboard
{self.selected_motherboard["name"] if self.selected_motherboard else "Not Selected"}

RAM
{self.selected_ram["name"] if self.selected_ram else "Not Selected"}
══════════════════════
"""

    def show_overview(self):
        self._write_result(self.update_overview())

    def generate_build_report(self, compatibility_result):
        # compatibility.py zaten CPU/GPU/Anakart/RAM isimlerini ve gercek
        # uyum sonuclarini (✅/❌) rapor icine yaziyor, burada tekrar
        # etmiyoruz. BUILD STATUS artik check_build sonucuna gore
        # dinamik olarak hesaplaniyor; sabit "Ready To Build" yazmiyor.
        is_compatible = "❌" not in compatibility_result

        if is_compatible:
            status = "🟢 Ready To Build"
        else:
            status = "🔴 Not Compatible - Fix Issues Above"

        return f"""{compatibility_result}
        BUILD STATUS

{status}
════════════════════════════════
"""

    def _write_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", text)
        self.result_box.configure(state="disabled")

    def check(self):
        result = check_build(
            self.selected_cpu,
            self.selected_gpu,
            self.selected_motherboard,
            self.selected_ram
        )
        report = self.generate_build_report(result)
        self._write_result(report)

