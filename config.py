SENSOR_NAMES = [
    {
        "id": "2",
        "name": "FM 2222 at Lakewood Drive",
        "cctv_url": "https://cctv.austinmobility.io/image/1136.jpg",
    },
    {
        "id": "3",
        "name": "Lakeline Boulevard at US-183",
        "cctv_url": "https://cctv.austinmobility.io/image/1018.jpg",
    },
    {
        "id": "4",
        "name": "Ben White Boulevard at Banister Lane",
        "cctv_url": "https://cctv.austinmobility.io/image/962.jpg",
    },
]

# from documentation here:
# https://github.com/cityofaustin/atd-road-conditions/blob/production/5433-3X-manual.pdf
CONDITION_CODES = {
    "UNK": "unknown",
    "DRY": "dry",
    "WT1": "damp",
    "WT2": "wet",
    "SN1": "snow",
    "IC1": "ice",
    "WT3": "standing water",
    "SN2": "deep snow",
    "IC2": "black ice",
    "MAX": "error",
    "ERR": "error",
}
