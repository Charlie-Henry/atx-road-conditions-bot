SENSOR_NAMES = [
    {
        "id": "2",
        "name": "FM 2222 RD / LAKEWOOD DR",
        "cctv_url": "https://cctv.austinmobility.io/image/1136.jpg",
    },
    {
        "id": "3",
        "name": "LAKELINE BLVD / 183 HWY SVRD",
        "cctv_url": "https://cctv.austinmobility.io/image/1018.jpg",
    },
    {
        "id": "4",
        "name": "BEN WHITE BLVD SVRD / BANISTER LN",
        "cctv_url": "https://cctv.austinmobility.io/image/962.jpg",
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
