import customtkinter as ctk
import json


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# DATABASE

with open("database/gpus.json", "r") as file:
    gpu_database = json.load(file)

with open("database/cpus.json", "r") as file:
    cpu_database = json.load(file)

with open("database/motherboards.json", "r") as file:
    motherboard_database = json.load(file)

with open("database/ram.json", "r") as file:
    ram_database = json.load(file)



app = ctk.CTk()

app.title("BuildBuddy")

app.geometry("950x750")

app.resizable(False, False)



title = ctk.CTkLabel(
    app,
    text="BuildBuddy",
    font=("Arial",40,"bold")
)

title.pack(pady=20)



selected_gpu = ctk.StringVar(value="Select GPU")
selected_cpu = ctk.StringVar(value="Select CPU")
selected_motherboard = ctk.StringVar(value="Select Motherboard")
selected_ram = ctk.StringVar(value="Select RAM")



# GENEL ARAMALI SEÇİCİ

def create_selector(title_text, database, variable):


    def open_selector():

        window = ctk.CTkToplevel(app)

        window.title(title_text)

        window.geometry("420x550")


        search = ctk.CTkEntry(
            window,
            width=320,
            placeholder_text="Search..."
        )

        search.pack(pady=15)



        frame = ctk.CTkScrollableFrame(
            window,
            width=350,
            height=380
        )

        frame.pack()



        def refresh(event=None):

            for widget in frame.winfo_children():
                widget.destroy()


            text = search.get().lower()


            for item in database:


                if text in item["name"].lower():

                    button = ctk.CTkButton(
                        frame,
                        text=item["name"],
                        width=300,
                        command=lambda x=item: select(x)
                    )

                    button.pack(pady=3)



        def select(item):

            variable.set(item["name"])

            window.destroy()



        search.bind(
            "<KeyRelease>",
            refresh
        )


        refresh()



    return open_selector





gpu_button = ctk.CTkButton(
    app,
    textvariable=selected_gpu,
    width=350,
    command=create_selector(
        "Select GPU",
        gpu_database,
        selected_gpu
    )
)

gpu_button.pack(pady=6)




cpu_button = ctk.CTkButton(
    app,
    textvariable=selected_cpu,
    width=350,
    command=create_selector(
        "Select CPU",
        cpu_database,
        selected_cpu
    )
)

cpu_button.pack(pady=6)




motherboard_button = ctk.CTkButton(
    app,
    textvariable=selected_motherboard,
    width=350,
    command=create_selector(
        "Select Motherboard",
        motherboard_database,
        selected_motherboard
    )
)

motherboard_button.pack(pady=6)




ram_button = ctk.CTkButton(
    app,
    textvariable=selected_ram,
    width=350,
    command=create_selector(
        "Select RAM",
        ram_database,
        selected_ram
    )
)

ram_button.pack(pady=6)





# SONUÇ

result = ctk.CTkTextbox(
    app,
    width=700,
    height=300
)

result.pack(pady=25)





def check_build():


    result.configure(
        state="normal"
    )

    result.delete(
        "0.0",
        "end"
    )


    cpu_name = selected_cpu.get()
    gpu_name = selected_gpu.get()
    mb_name = selected_motherboard.get()
    ram_name = selected_ram.get()



    if "Select" in [
        cpu_name,
        gpu_name,
        mb_name,
        ram_name
    ]:

        result.insert(
            "end",
            "Please select all components."
        )


    else:


        cpu = next(
            x for x in cpu_database
            if x["name"] == cpu_name
        )


        gpu = next(
            x for x in gpu_database
            if x["name"] == gpu_name
        )


        mb = next(
            x for x in motherboard_database
            if x["name"] == mb_name
        )


        ram = next(
            x for x in ram_database
            if x["name"] == ram_name
        )



        result.insert(
            "end",
            "BuildBuddy Report\n\n"
        )


        result.insert(
            "end",
            f"CPU: {cpu_name}\n"
        )

        result.insert(
            "end",
            f"GPU: {gpu_name}\n"
        )

        result.insert(
            "end",
            f"Motherboard: {mb_name}\n"
        )

        result.insert(
            "end",
            f"RAM: {ram_name}\n\n"
        )



        # CPU - MOTHERBOARD


        if cpu["socket"] == mb["socket"]:

            result.insert(
                "end",
                "CPU + Motherboard: ✅ Compatible\n"
            )

        else:

            result.insert(
                "end",
                "CPU + Motherboard: ❌ Incompatible\n"
            )



        # RAM TYPE


        if ram["type"] in mb["ram_type"]:

            result.insert(
                "end",
                "RAM Type: ✅ Compatible\n"
            )

        else:

            result.insert(
                "end",
                "RAM Type: ❌ Incompatible\n"
            )



        # RAM CAPACITY


        ram_capacity = int(
            ram["capacity"].replace("GB","")
        )


        max_ram = int(
            mb["max_ram"].replace("GB","")
        )


        if ram_capacity <= max_ram:

            result.insert(
                "end",
                "RAM Capacity: ✅ OK\n"
            )

        else:

            result.insert(
                "end",
                "RAM Capacity: ❌ Too Much\n"
            )



        # BOTTLENECK


        difference = (
            gpu["performance"]
            -
            cpu["performance"]
        )


        if difference >= 20:

            result.insert(
                "end",
                "\n⚠ CPU Bottleneck Warning"
            )


        elif difference <= -20:

            result.insert(
                "end",
                "\n⚠ GPU Limitation Warning"
            )


        else:

            result.insert(
                "end",
                "\n✅ CPU + GPU Balanced"
            )



    result.configure(
        state="disabled"
    )





check_button = ctk.CTkButton(
    app,
    text="Check Compatibility",
    width=350,
    height=40,
    command=check_build
)

check_button.pack(pady=10)



app.mainloop()