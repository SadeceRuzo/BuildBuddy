def find_part(database, name):
    """
    Finds a component by its name in the given database.
    Returns the component if found, otherwise returns None.
    """

    for part in database:
        if part["name"] == name:
            return part

    return None


def get_ram_capacity(capacity):
    """
    Converts '32GB' -> 32
    """

    return int(capacity.replace("GB", ""))


def get_ram_speed(speed):
    """
    Converts RAM speed to integer if needed.
    Example:
    6000 -> 6000
    """

    return int(speed)


def is_cpu_motherboard_compatible(cpu, motherboard):
    """
    Checks CPU socket compatibility.
    """

    return cpu["socket"] == motherboard["socket"]


def is_ram_type_compatible(ram, motherboard):
    """
    Checks RAM type compatibility.
    """

    return ram["type"] == motherboard["ram_type"]


def is_ram_capacity_compatible(ram, motherboard):
    """
    Checks maximum RAM capacity.
    """

    return get_ram_capacity(ram["capacity"]) <= get_ram_capacity(motherboard["max_ram"])


def is_ram_speed_compatible(ram, motherboard):
    """
    Checks RAM speed compatibility.
    """

    motherboard_speed = int(
        motherboard["ram_speed"]
        .replace("DDR4-", "")
        .replace("DDR5-", "")
    )

    return get_ram_speed(ram["speed"]) <= motherboard_speed


def calculate_bottleneck(cpu, gpu):
    """
    Calculates CPU/GPU balance.
    """

    difference = gpu["performance"] - cpu["performance"]

    if difference >= 20:
        return "CPU Bottleneck"

    elif difference <= -20:
        return "GPU Bottleneck"

    else:
        return "Balanced"
