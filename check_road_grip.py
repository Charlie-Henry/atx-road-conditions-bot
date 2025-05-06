from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
import requests
from zoneinfo import ZoneInfo
import os

import psycopg2

from config import SENSOR_NAMES, CONDITION_CODES
from bsky_utils import login_bsky, upload_image

# postgres DB info
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_DATABASE")
HOST = os.getenv("DB_HOST")

# Austin is in central timezone
tz = ZoneInfo("America/Chicago")

# json endpoint to open data portal
API_URL = "https://data.austintexas.gov/resource/ypbq-i42h.json?$order=timestamp%20DESC&$limit=1"


def get_latest_data_from_sensor(sensor):
    response = requests.get(API_URL + f"&$where=sensor_id={sensor['id']}")
    return response.json()[0]


def check_stored_data(conn, sensor):
    cur = conn.cursor()
    query = f"SELECT last_message_date, last_message_grip from road_conditions WHERE sensor_id='{sensor['id']}';"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    if not data:
        return None, None
    return data[0]


def update_stored_data(conn, sensor, tweet_time, grip):
    cur = conn.cursor()
    query = f"UPDATE road_conditions SET last_message_date = '{tweet_time}', last_message_grip = '{grip}' WHERE sensor_id = '{sensor['id']}';"
    cur.execute(query)
    conn.commit()
    cur.close()


def get_cam_image(url):
    res = requests.get(url)
    print(f"image retrieved with status: {res.status_code}")
    if res.status_code == 200:
        image_data = res.content
        image = Image.open(BytesIO(image_data))
        # Check if it's exactly 1920x1080, the placeholder "unavailable" image is smaller.
        if image.size != (1920, 1080):
            print("Image is not 1920x1080. Skipping uploading image.")
            return None
        return image_data
    return None


def main():
    # connecting to postgres DB
    conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

    # Get the current time
    now = datetime.now(tz)
    # Calculate the time 10 minutes ago
    ten_minutes_ago = now - timedelta(minutes=10)
    bsky_client = None
    for sensor in SENSOR_NAMES:
        tweet_text = None
        latest_data_from_sensor = get_latest_data_from_sensor(sensor)
        if latest_data_from_sensor["condition_text_displayed"] in CONDITION_CODES:
            condition = CONDITION_CODES[
                latest_data_from_sensor["condition_text_displayed"]
            ]
        else:
            condition = latest_data_from_sensor["condition_text_displayed"]

        timestamp = latest_data_from_sensor["timestamp"]
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
        timestamp = timestamp.replace(tzinfo=tz)

        # Check if the data is somewhat recent
        if timestamp >= ten_minutes_ago:
            # Retrieving when we last tweeted about this sensor data
            last_message_date, last_message_grip = check_stored_data(conn, sensor)
            # handling the case of a new sensor, we just tweet some boilerplate text
            if last_message_date is None or last_message_grip is None:
                tweet_text = f"{latest_data_from_sensor['grip_text']} roadway grip reported at {sensor['name']}. \nCurrent roadway condition is {condition}."
            # We will not tweet more often than every 30 minutes for every sensor
            elif now - last_message_date.replace(tzinfo=tz) > timedelta(minutes=30):
                # Checking for a change in the road grip status
                if last_message_grip != latest_data_from_sensor["grip_text"]:
                    tweet_text = f"{latest_data_from_sensor['grip_text']} roadway grip reported at {sensor['name']}, was previously {last_message_grip}. \nCurrent roadway condition is {condition}."
        # checking if we have something to tweet
        if tweet_text:
            if not bsky_client:
                # Log into bluesky
                bsky_client = login_bsky(conn)
            print(tweet_text)
            image_data = get_cam_image(sensor["cctv_url"])
            if image_data:
                embed = upload_image(bsky_client, image_data)
            else:
                embed = None
            post = bsky_client.send_post(tweet_text, embed=embed)
            update_stored_data(conn, sensor, now, latest_data_from_sensor["grip_text"])
        else:
            print("Nothing new to tweet, did nothing.")


if __name__ == "__main__":
    main()
