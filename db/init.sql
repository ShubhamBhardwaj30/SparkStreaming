CREATE TABLE IF NOT EXISTS stream_data (
    user_id INTEGER,
    event_type TEXT,
    value DOUBLE PRECISION,
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS public.aggregated_stream_data
(
    window_start timestamp without time zone,
    window_end timestamp without time zone,
    event_type text COLLATE pg_catalog."default",
    total_value double precision,
    average_value double precision,
    event_count integer
)