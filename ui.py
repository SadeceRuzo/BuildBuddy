import webbrowser

import customtkinter as ctk

from database import cpus, gpus, motherboards, rams
from compatibility import check_build


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Kendi GitHub kullanıcı adını / linkini buraya yaz
GITHUB_URL = "https://github.com/SadeceRuzo"


class BuildBuddyApp:

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("BuildBuddy")
        self.root.geometry("1200x720")
        self.root.resizable(False, False)

        self.selected_cpu = None
        self.selected_gpu = None
        self.selected_motherboard = None
        self.selected_ram = None

        self.create_ui()

    def run(self):
        self.root.mainloop()

    # ---------------- UI KURULUMU ----------------

    def create_ui(self):
        self.title = ctk.CTkLabel(
            self.root, text="BuildBuddy", font=("Arial", 40, "bold")
        )
        self.title.pack(pady=(20, 5))

        self.subtitle = ctk.CTkLabel(
            self.root, text="PC Compatibility Checker", font=("Arial", 18)
        )
        self.subtitle.pack()

        self.main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=20)

        self.left_frame = ctk.CTkFrame(self.main_frame, width=350)
        self.left_frame.pack(side="left", fill="y", padx=20, pady=20)

        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.create_left_panel()
        self.create_right_panel()

    def create_left_panel(self):
        self.components_title = ctk.CTkLabel(
            self.left_frame, text="Components", font=("Arial", 24, "bold")
        )
        self.components_title.pack(pady=20)

        self.cpu_button = ctk.CTkButton(
            self.left_frame, text="Select CPU", width=280, height=42,
            command=self.open_cpu_selector
        )
        self.cpu_button.pack(pady=8)

        self.gpu_button = ctk.CTkButton(
            self.left_frame, text="Select GPU", width=280, height=42,
            command=self.open_gpu_selector
        )
        self.gpu_button.pack(pady=8)

        self.mb_button = ctk.CTkButton(
            self.left_frame, text="Select Motherboard", width=280, height=42,
            command=self.open_mb_selector
        )
        self.mb_button.pack(pady=8)

        self.ram_button = ctk.CTkButton(
            self.left_frame, text="Select RAM", width=280, height=42,
            command=self.open_ram_selector
        )
        self.ram_button.pack(pady=8)

        self.check_button = ctk.CTkButton(
            self.left_frame, text="Check Compatibility", width=280, height=45,
            state="disabled", command=self.check
        )
        self.check_button.pack(pady=30)

        self.version_label = ctk.CTkLabel(
            self.left_frame,
            text="v1.0.1",
            font=("Arial", 12),
            text_color="gray60",
            cursor="hand2"
        )
        self.version_label.pack(side="bottom", pady=10)
        self.version_label.bind("<Button-1>", self.open_github)

    def open_github(self, event=None):
        webbrowser.open(GITHUB_URL)

    def create_right_panel(self):
        self.result_title = ctk.CTkLabel(
            self.right_frame, text="Build Report", font=("Arial", 28, "bold")
        )
        self.result_title.pack(pady=20)

        self.result_box = ctk.CTkTextbox(
            self.right_frame, width=650, height=500, font=("Consolas", 15)
        )
        self.result_box.pack(padx=20, pady=20, fill="both", expand=True)

        self.result_box.insert("0.0", "Select all components to start.")
        self.result_box.configure(state="disabled")

    # ---------------- SEÇİM PENCERELERİ ----------------

    def open_selector(self, title, database, callback):
        window = ctk.CTkToplevel(self.root)
        window.title(title)
        window.geometry("450x550")
        window.grab_set()

        search = ctk.CTkEntry(window, width=350, placeholder_text="Search...")
        search.pack(pady=15)

        frame = ctk.CTkScrollableFrame(window, width=380, height=420)
        frame.pack(fill="both", expand=True, padx=15, pady=10)

        def refresh(event=None):
            for widget in frame.winfo_children():
                widget.destroy()

            text = search.get().lower()

            for item in database:
                if text in item["name"].lower():
                    ctk.CTkButton(
                        frame, text=item["name"], width=330,
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
        self.cpu_button.configure(text=cpu["name"])

    def select_gpu(self, gpu):
        self.selected_gpu = gpu
        self.gpu_button.configure(text=gpu["name"])

    def select_motherboard(self, motherboard):
        self.selected_motherboard = motherboard
        self.mb_button.configure(text=motherboard["name"])

    def select_ram(self, ram):
        self.selected_ram = ram
        self.ram_button.configure(text=ram["name"])

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

🖥 CPU
{self.selected_cpu["name"] if self.selected_cpu else "Not Selected"}

🎮 GPU
{self.selected_gpu["name"] if self.selected_gpu else "Not Selected"}

🧩 Motherboard
{self.selected_motherboard["name"] if self.selected_motherboard else "Not Selected"}

💾 RAM
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
