from utils import *


def check_build(cpu, gpu, motherboard, ram):

    report = []

    report.append("========== BUILD REPORT ==========\n")


    report.append(f"🖥 CPU : {cpu['name']}")
    report.append(f"🎮 GPU : {gpu['name']}")
    report.append(f"🧩 Motherboard : {motherboard['name']}")
    report.append(f"💾 RAM : {ram['name']}\n")



    # CPU SOCKET

    if cpu["socket"] == motherboard["socket"]:

        report.append("✅ CPU and Motherboard Compatible")

    else:

        report.append("❌ CPU and Motherboard Incompatible")



    # RAM TYPE

    if ram["type"] == motherboard["ram_type"]:

        report.append("✅ RAM Type Compatible")

    else:

        report.append("❌ RAM Type Incompatible")



    # RAM CAPACITY

    ram_capacity = int(
        ram["capacity"].replace("GB","")
    )

    motherboard_capacity = int(
        motherboard["max_ram"].replace("GB","")
    )


    if ram_capacity <= motherboard_capacity:

        report.append("✅ RAM Capacity Supported")

    else:

        report.append("❌ RAM Capacity Too High")



    # BOTTLENECK SYSTEM

    cpu_perf = cpu["performance"]

    gpu_perf = gpu["performance"]


    difference = abs(
        gpu_perf - cpu_perf
    )


    report.append("")

    report.append("⚖ Bottleneck Analysis")

    report.append(
        f"CPU Performance : {cpu_perf}"
    )

    report.append(
        f"GPU Performance : {gpu_perf}"
    )

    report.append(
        f"Difference : {difference}%"
    )



    if difference <= 5:

        report.append(
            "🟢 Balanced Build"
        )


    elif difference <= 15:

        report.append(
            "🟡 Slight Bottleneck"
        )


    else:

        if gpu_perf > cpu_perf:

            report.append(
                "🟠 CPU Bottleneck"
            )

        else:

            report.append(
                "🟠 GPU Bottleneck"
            )



    # OVERALL RATING

    report.append("")
    report.append("⭐ Overall Rating")


    if difference <= 5:

        report.append(
            "★★★★★ Excellent Build"
        )


    elif difference <= 15:

        report.append(
            "★★★★☆ Very Good Build"
        )


    elif difference <= 25:

        report.append(
            "★★★☆☆ Good Build"
        )


    else:

        report.append(
            "★★☆☆☆ Needs Improvement"
        )



    report.append("")
    report.append("================================")


    return "\n".join(report)
