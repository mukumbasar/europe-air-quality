-- ==========================================
-- CORE DATA TABLES
-- ==========================================

-- processed_air_quality: One row for every distinct city and month combination.
CREATE TABLE processed_air_quality (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    date DATE NOT NULL, -- the first day of the month that the readings were taken
    pm2_5 FLOAT, -- monthly average of PM2.5 readings
    pm10 FLOAT, -- monthly average of PM10 readings
    ozone FLOAT, -- monthly average of Ozone readings
    nitrogen_dioxide FLOAT, -- monthly average of Nitrogen Dioxide readings
    sulphur_dioxide FLOAT, -- monthly average of Sulfur Dioxide readings
    carbon_monoxide FLOAT, -- monthly average of Carbon Monoxide readings
    hours_available INT NOT NULL, -- how many hourly readings went into this month's average
    processed_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (city, country, date)
);

-- forecast_air_quality: One row for every distinct city and month combination.
CREATE TABLE forecast_air_quality (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    date DATE NOT NULL, -- the first day of the month for forecasted readings
    pm2_5 FLOAT, -- monthly average of PM2.5 readings
    pm10 FLOAT, -- monthly average of PM10 readings
    ozone FLOAT, -- monthly average of Ozone readings
    nitrogen_dioxide FLOAT, -- monthly average of Nitrogen Dioxide readings
    sulphur_dioxide FLOAT, -- monthly average of Sulfur Dioxide readings
    carbon_monoxide FLOAT, -- monthly average of Carbon Monoxide readings
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (city, country, date)
);


-- ==========================================
-- REFERENCE & LOOKUP TABLES
-- ==========================================

-- pollutant_details: Reference lookup table for UI color coding.
-- Note: Not using foreign keys was a deliberate choice to avoid unnecessary normalization.
CREATE TABLE pollutant_details (
    id SERIAL PRIMARY KEY,
    pollutant_name VARCHAR(50) NOT NULL UNIQUE,
    middle_limit FLOAT NOT NULL,
    high_limit FLOAT NOT NULL,
    unit VARCHAR(20) DEFAULT 'µg/m³',
    is_active BOOLEAN DEFAULT TRUE
);

-- cities: One row for every distinct city in the scope of the project.
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);


-- ==========================================
-- DATA SEEDS
-- ==========================================

-- Insert default pollutant thresholds for UI color coding.
INSERT INTO pollutant_details (pollutant_name, middle_limit, high_limit) VALUES
('pm2_5', 12.0, 35.4),
('pm10', 54.0, 154.0),
('ozone', 54.0, 70.0),
('nitrogen_dioxide', 53.0, 100.0),
('sulphur_dioxide', 35.0, 75.0),
('carbon_monoxide', 4.4, 9.4)
ON CONFLICT (pollutant_name) DO NOTHING;

-- Insert default cities according to the project scope: European capitals.
INSERT INTO cities (city, country, latitude, longitude) VALUES
('Amsterdam', 'Netherlands', 52.3676, 4.9041),
('Andorra la Vella', 'Andorra', 42.5063, 1.5218),
('Ankara', 'Türkiye', 39.9334, 32.8597),
('Athens', 'Greece', 37.9838, 23.7275),
('Belgrade', 'Serbia', 44.7866, 20.4489),
('Berlin', 'Germany', 52.5200, 13.4050),
('Bern', 'Switzerland', 46.9480, 7.4474),
('Bratislava', 'Slovakia', 48.1486, 17.1077),
('Brussels', 'Belgium', 50.8503, 4.3517),
('Bucharest', 'Romania', 44.4323, 26.1063),
('Budapest', 'Hungary', 47.4979, 19.0402),
('Chisinau', 'Moldova', 47.0105, 28.8638),
('Copenhagen', 'Denmark', 55.6761, 12.5683),
('Dublin', 'Ireland', 53.3498, -6.2603),
('Helsinki', 'Finland', 60.1699, 24.9384),
('Kyiv', 'Ukraine', 50.4501, 30.5234),
('Lisbon', 'Portugal', 38.7223, -9.1393),
('Ljubljana', 'Slovenia', 46.0569, 14.5058),
('London', 'United Kingdom', 51.5074, -0.1278),
('Luxembourg', 'Luxembourg', 49.6116, 6.1319),
('Madrid', 'Spain', 40.4168, -3.7038),
('Minsk', 'Belarus', 53.9006, 27.5590),
('Monaco', 'Monaco', 43.7384, 7.4246),
('Moscow', 'Russia', 55.7558, 37.6173),
('Nicosia', 'Cyprus', 35.1856, 33.3823),
('Oslo', 'Norway', 59.9139, 10.7522),
('Paris', 'France', 48.8566, 2.3522),
('Podgorica', 'Montenegro', 42.4304, 19.2594),
('Prague', 'Czech Republic', 50.0755, 14.4378),
('Pristina', 'Kosovo', 42.6629, 21.1655),
('Reykjavik', 'Iceland', 64.1466, -21.9426),
('Riga', 'Latvia', 56.9496, 24.1052),
('Rome', 'Italy', 41.9028, 12.4964),
('San Marino', 'San Marino', 43.9424, 12.4578),
('Sarajevo', 'Bosnia and Herzegovina', 43.8563, 18.4131),
('Skopje', 'North Macedonia', 41.9981, 21.4254),
('Sofia', 'Bulgaria', 42.6977, 23.3219),
('Stockholm', 'Sweden', 59.3293, 18.0686),
('Tallinn', 'Estonia', 59.4370, 24.7536),
('Tirana', 'Albania', 41.3275, 19.8187),
('Vaduz', 'Liechtenstein', 47.1410, 9.5209),
('Valletta', 'Malta', 35.8997, 14.5148),
('Vatican City', 'Vatican City', 41.9029, 12.4534),
('Vienna', 'Austria', 48.2082, 16.3738),
('Vilnius', 'Lithuania', 54.6872, 25.2797),
('Warsaw', 'Poland', 52.2297, 21.0122),
('Zagreb', 'Croatia', 45.8150, 15.9819)
ON CONFLICT (city) DO NOTHING;