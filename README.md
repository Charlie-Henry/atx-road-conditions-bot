# atx-road-conditions-bot

A bluesky bot that live posts road conditions updates over at [@atx-road-condition.bsky.social](https://bsky.app/profile/atx-road-condition.bsky.social)

The `check_road_grip.py` script checks the [road conditions dataset](https://data.austintexas.gov/Transportation-and-Mobility/Real-Time-Road-Conditions/ypbq-i42h/about_data) 
for the latest data from the Austin Open Data Portal and decides if something is worth posting about.

Based on the [documentation](https://github.com/cityofaustin/atd-road-conditions/blob/production/5433-3X-manual.pdf) 
from the dataset, this data comes from "High Sierra Electronics Inc. Model 5433 RWIS IceSight remote sensor".

## Running locally

1. Clone this repo
2. Create a table in your own postgres instance using the SQL command in `db/table_creation.sql` 
3. `pip install -r requirements.txt`
4. Fill out the `env_template` with your own bluesky and db credentials
5. Run the script with `python check_road_grip.py`


## Forking this for other work

If you have your own data or something similar and would like to set something up using your own data:

### 1. Configure sensor API

Luckily this was already done for me, I was using the [socrata open data portal API](https://dev.socrata.com/docs/endpoints.html) for this.

You'll need to supply a `sensor_id` that is unique for each location along with data from the sensor itself:
- `grip_text`
- `condition_text_measured`

### 2. Configure postgres

I have supplied the sql command (`db/table_creation.sql`) I used to create a table to store some basic info about each sensor.

You will also need to populate the `sensor_id`s in the road_conditions table with the ids you are looking to monitor. 

### 3. Update check_road_grip.py

Update the `SENSOR_NAMES` dict with your own info. Along with `API_URL`, and the `tz` object to match the timezone of your API.

### 4. Run your script

Follow the above steps to install dependencies and fill out the `env_template` and your script!

