import os

from atproto import Client, models
import atproto_client

# bluesky login
BSKY_HANDLE = os.getenv("BSKY_HANDLE")
BSKY_PASSWORD = os.getenv("BSKY_PASSWORD")


def get_session_string(conn):
    cur = conn.cursor()
    query = f"SELECT session_string from bluesky_sessions WHERE bsky_handle='{BSKY_HANDLE}';"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    if not data:
        return None
    return data[0][0]


def store_session_string(conn, session_string):
    cur = conn.cursor()
    query = f"UPDATE bluesky_sessions SET session_string = '{session_string}' WHERE bsky_handle='{BSKY_HANDLE}';"
    cur.execute(query)
    conn.commit()
    cur.close()


def upload_image(client, image_data):
    upload = client.upload_blob(image_data)
    images = [
        models.AppBskyEmbedImages.Image(
            alt="screenshot from a traffic camera nearby",
            image=upload.blob,
            aspectRatio={"width": 1920, "height": 1080},
        )
    ]
    embed = models.AppBskyEmbedImages.Main(images=images)
    return embed


def login_bsky(conn):
    # Get stored session string
    session_string = get_session_string(conn)

    # Logging into bsky
    client = Client()
    try:
        # First try with the stored session string in the DB.
        client.login(session_string=session_string)
        print("Logged in using previous bluesky session string.")
    except atproto_client.exceptions.BadRequestError:
        print("Issuing new bluesky session string.")
        # Our previous session string has expired, so we need a new one.
        client = Client()
        # Note that this .login method is quite rate limited, so this is why we need to handle these session strings
        client.login(login=BSKY_HANDLE, password=BSKY_PASSWORD)
        session_string = client.export_session_string()
        store_session_string(conn, session_string)

    return client
