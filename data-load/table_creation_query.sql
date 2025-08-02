CREATE TABLE IF NOT EXISTS "user" (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    review_count INTEGER,
    yelping_since TIMESTAMP,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    elite INTEGER,
    friends TEXT,
    fans INTEGER,
    average_stars FLOAT,
    compliment_hot INTEGER,
    compliment_more INTEGER,
    compliment_profile INTEGER,
    compliment_cute INTEGER,
    compliment_list INTEGER,
    compliment_note INTEGER,
    compliment_plain INTEGER,
    compliment_cool INTEGER,
    compliment_funny INTEGER,
    compliment_writer INTEGER,
    compliment_photos INTEGER
);



CREATE TABLE IF NOT EXISTS "tip" (
    user_id TEXT,
    business_id TEXT,
    text TEXT,
    date TIMESTAMP,
    compliment_count INTEGER
);


CREATE TABLE IF NOT EXISTS review (
    review_id TEXT PRIMARY KEY,
    user_id TEXT,
    business_id TEXT,
    stars INTEGER,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    text TEXT,
    date TIMESTAMP
);


CREATE TABLE IF NOT EXISTS checkin (
    business_id TEXT,
    date TEXT
);



CREATE TABLE IF NOT EXISTS business (
    business_id TEXT PRIMARY KEY,
    name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    postal_code INTEGER,
    latitude FLOAT,
    longitude FLOAT,
    stars FLOAT,
    review_count INTEGER,
    is_open INTEGER,
    attributes TEXT,
    categories TEXT,
    hours TEXT
);
