-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."road_conditions" (
    "sensor_id" text NOT NULL,
    "last_message_grip" text,
    "last_message_date" timestamp
);
