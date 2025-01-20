SENSOR_NAMES = [
    {
        "id": "2",
        "name": "FM 2222 RD / LAKEWOOD DR",
    },
    {
        "id": "3",
        "name": "LAKELINE BLVD / 183 HWY SVRD",
    },
    {
        "id": "4",
        "name": "BEN WHITE BLVD SVRD / BANISTER LN",
    },
]

# from documentation here:
# https://github.com/cityofaustin/atd-road-conditions/blob/production/5433-3X-manual.pdf
CONDITION_CODES = {
    "UNK": "Unknown",
    "DRY": "Dry",
    "WT1": "Damp",
    "WT2": "Wet",
    "SN1": "Snow",
    "IC1": "Ice",
    "WT3": "Standing water",
    "SN2": "Deep snow",
    "IC2": "Black ice",
    "MAX": "Error",
    "ERR": "Error",
}
