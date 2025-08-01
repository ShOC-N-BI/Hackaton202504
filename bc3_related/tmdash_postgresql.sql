-- Table: bc3lookup.platform_types

-- DROP TABLE IF EXISTS bc3lookup.platform_types;

CREATE TABLE IF NOT EXISTS bc3lookup.platform_types
(
    platform_id bigint,
    platform_descr text COLLATE pg_catalog."default"
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS bc3lookup.platform_types
    OWNER to shooca;
	
-- Table: bc3lookup.specific_types

-- DROP TABLE IF EXISTS bc3lookup.specific_types;

CREATE TABLE IF NOT EXISTS bc3lookup.specific_types
(
    track_category text COLLATE pg_catalog."default",
    type_id bigint,
    type_descr text COLLATE pg_catalog."default"
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS bc3lookup.specific_types
    OWNER to shooca;
	
-- Table: bc3lookup.tmdash_ato

-- DROP TABLE IF EXISTS bc3lookup.tmdash_ato;

CREATE TABLE IF NOT EXISTS bc3lookup.tmdash_ato
(
    callsign text COLLATE pg_catalog."default" NOT NULL,
    aircraft_type text COLLATE pg_catalog."default",
    num_aircraft double precision,
    mode3 text COLLATE pg_catalog."default",
    nation text COLLATE pg_catalog."default",
    comm_deliverables text COLLATE pg_catalog."default",
    sensing_deliverables text COLLATE pg_catalog."default",
    default_munitions text COLLATE pg_catalog."default",
    ea_deliverables text COLLATE pg_catalog."default",
    other_deliverables text COLLATE pg_catalog."default",
    CONSTRAINT tmdash_ato_pkey PRIMARY KEY (callsign)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS bc3lookup.tmdash_ato
    OWNER to shooca;
	
-- Table: public.bc3_client

-- DROP TABLE IF EXISTS public.bc3_client;

CREATE TABLE IF NOT EXISTS public.bc3_client
(
    tracknumber integer NOT NULL,
    latitude double precision,
    longitude double precision,
    altitude double precision,
    groundspeed double precision,
    heading double precision,
    trackquality integer,
    trackcategory text COLLATE pg_catalog."default",
    trackid text COLLATE pg_catalog."default",
    jtn text COLLATE pg_catalog."default",
    last_updated timestamp without time zone,
    specifictype integer,
    platform integer,
    callsign text COLLATE pg_catalog."default",
    source text COLLATE pg_catalog."default",
    squawkid text COLLATE pg_catalog."default",
    CONSTRAINT bc3_client_pkey PRIMARY KEY (tracknumber),
    CONSTRAINT uix_tracknumber UNIQUE (tracknumber)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bc3_client
    OWNER to shooca;

COMMENT ON COLUMN public.bc3_client.squawkid
    IS 'bc3 e7.mode3';

-- Table: public.bc3_fuel

-- DROP TABLE IF EXISTS public.bc3_fuel;

CREATE TABLE IF NOT EXISTS public.bc3_fuel
(
    jtn text COLLATE pg_catalog."default" NOT NULL,
    fuel text COLLATE pg_catalog."default",
    fuel_factor text COLLATE pg_catalog."default",
    fuel_time_marker text COLLATE pg_catalog."default",
    last_updated timestamp without time zone,
    CONSTRAINT bc3_fuel_pkey PRIMARY KEY (jtn)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bc3_fuel
    OWNER to shooca;

-- Table: public.bc3_sensors

-- DROP TABLE IF EXISTS public.bc3_sensors;

CREATE TABLE IF NOT EXISTS public.bc3_sensors
(
    jtn text COLLATE pg_catalog."default" NOT NULL,
    aircraft_type text COLLATE pg_catalog."default",
    radar text COLLATE pg_catalog."default",
    radar_warning text COLLATE pg_catalog."default",
    laser text COLLATE pg_catalog."default",
    air_to_ground text COLLATE pg_catalog."default",
    air_to_air text COLLATE pg_catalog."default",
    last_updated timestamp without time zone,
    CONSTRAINT bc3_sensors_pkey PRIMARY KEY (jtn)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bc3_sensors
    OWNER to shooca;

-- Table: public.bc3_vcs

-- DROP TABLE IF EXISTS public.bc3_vcs;

CREATE TABLE IF NOT EXISTS public.bc3_vcs
(
    jtn text COLLATE pg_catalog."default" NOT NULL,
    vcs text COLLATE pg_catalog."default",
    last_updated timestamp without time zone,
    CONSTRAINT link16_vcs_pkey PRIMARY KEY (jtn)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bc3_vcs
    OWNER to shooca;

-- Table: public.bc3_weapons

-- DROP TABLE IF EXISTS public.bc3_weapons;

CREATE TABLE IF NOT EXISTS public.bc3_weapons
(
    jtn text COLLATE pg_catalog."default" NOT NULL,
    slot integer NOT NULL,
    weapon text COLLATE pg_catalog."default",
    quantity integer,
    last_updated timestamp without time zone,
    CONSTRAINT pk_jtn_slot PRIMARY KEY (jtn, slot),
    CONSTRAINT uq_jtn_slot UNIQUE (jtn, slot)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bc3_weapons
    OWNER to shooca;

-- View: public.bc3_friends_vw

-- DROP VIEW public.bc3_friends_vw;

CREATE OR REPLACE VIEW public.bc3_friends_vw
 AS
 SELECT DISTINCT ON (mt.latitude, mt.longitude) mt.latitude,
    mt.longitude,
    mt.trackcategory,
    mt.callsign,
    mt.vcs,
    mt.mode3,
    mt.aircraft_type,
    mt.bc3_jtn,
    mt.merged_tracknumber,
    COALESCE(mt.weapon, ato.default_munitions) AS munition_deliverables,
    ato.comm_deliverables,
    ato.sensing_deliverables,
    ato.ea_deliverables,
    ato.other_deliverables
   FROM bc3_merged_track_vw mt
     LEFT JOIN bc3lookup.tmdash_ato ato ON "left"(mt.callsign, COALESCE(NULLIF(POSITION((' '::text) IN (mt.callsign)) - 1, '-1'::integer), 8)) ~~ "left"(ato.callsign, COALESCE(NULLIF(POSITION((' '::text) IN (ato.callsign)) - 1, '-1'::integer), 8));

ALTER TABLE public.bc3_friends_vw
    OWNER TO shooca;

-- View: public.bc3_merged_track_vw

-- DROP VIEW public.bc3_merged_track_vw;

CREATE OR REPLACE VIEW public.bc3_merged_track_vw
 AS
 WITH bc3 AS (
         SELECT DISTINCT bc3_with_all_vw.tracknumber,
            bc3_with_all_vw.latitude,
            bc3_with_all_vw.longitude,
            bc3_with_all_vw.altitude,
            bc3_with_all_vw.groundspeed,
            bc3_with_all_vw.heading,
            bc3_with_all_vw.trackquality,
            bc3_with_all_vw.trackcategory,
            bc3_with_all_vw.trackid,
            bc3_with_all_vw.specifictype,
            bc3_with_all_vw.specifictype_descr,
            bc3_with_all_vw.platform,
            bc3_with_all_vw.platform_descr,
            bc3_with_all_vw.callsign,
            bc3_with_all_vw.bc3_vcs,
            bc3_with_all_vw.source,
            bc3_with_all_vw.squawkid,
            bc3_with_all_vw.bc3_jtn,
            bc3_with_all_vw.aircraft_type,
            bc3_with_all_vw.bc3_updated,
            bc3_with_all_vw.fuel,
            bc3_with_all_vw.fuel_factor,
            bc3_with_all_vw.fuel_time_marker,
            bc3_with_all_vw.weapon
           FROM bc3_with_all_vw
          WHERE bc3_with_all_vw.trackid = 'Friend'::text AND bc3_with_all_vw.source = 'PPLI'::text AND bc3_with_all_vw.bc3_updated >= (now() - '03:00:00'::interval) AND bc3_with_all_vw.bc3_updated <= now()
        ), dis AS (
         SELECT DISTINCT bc3_with_all_vw.latitude,
            bc3_with_all_vw.longitude,
            bc3_with_all_vw.trackcategory,
            TRIM(BOTH FROM bc3_with_all_vw.callsign) AS callsign,
            ("left"(bc3_with_all_vw.callsign, 1) || (( SELECT "right"(regexp_replace(bc3_with_all_vw.callsign, '[\s\d]+$'::text, ''::text), 1) AS "right"))) || (( SELECT regexp_matches(bc3_with_all_vw.callsign, '\d+$'::text) AS regexp_matches
                 LIMIT 1))[1] AS callsign_abbr,
            bc3_with_all_vw.bc3_vcs,
            bc3_with_all_vw.squawkid,
            bc3_with_all_vw.aircraft_type,
            bc3_with_all_vw.source,
            bc3_with_all_vw.weapon,
            bc3_with_all_vw.bc3_jtn,
            bc3_with_all_vw.tracknumber,
            bc3_with_all_vw.bc3_updated,
            row_number() OVER (PARTITION BY bc3_with_all_vw.latitude, bc3_with_all_vw.longitude ORDER BY bc3_with_all_vw.bc3_updated DESC) AS rn
           FROM bc3_with_all_vw
          WHERE bc3_with_all_vw.trackid = 'Friend'::text AND bc3_with_all_vw.source <> 'PPLI'::text AND bc3_with_all_vw.bc3_updated >= (now() - '03:00:00'::interval) AND bc3_with_all_vw.bc3_updated <= now()
        )
 SELECT DISTINCT COALESCE(bc3.latitude, dis.latitude) AS latitude,
    COALESCE(bc3.longitude, dis.longitude) AS longitude,
    COALESCE(bc3.trackcategory, dis.trackcategory) AS trackcategory,
    TRIM(BOTH FROM COALESCE(bc3.callsign, dis.callsign)) AS callsign,
    COALESCE(bc3.bc3_vcs, dis.bc3_vcs) AS vcs,
    COALESCE(bc3.squawkid, dis.squawkid) AS mode3,
    COALESCE(bc3.aircraft_type, dis.aircraft_type) AS aircraft_type,
    COALESCE(bc3.weapon, dis.weapon) AS weapon,
    COALESCE(bc3.bc3_jtn, dis.bc3_jtn) AS bc3_jtn,
    COALESCE(bc3.tracknumber, dis.tracknumber) AS merged_tracknumber
   FROM bc3
     LEFT JOIN dis ON bc3.bc3_vcs = dis.callsign_abbr AND dis.rn = 1;

ALTER TABLE public.bc3_merged_track_vw
    OWNER TO shooca;

-- View: public.bc3_others_vw

-- DROP VIEW public.bc3_others_vw;

CREATE OR REPLACE VIEW public.bc3_others_vw
 AS
 WITH bc3 AS (
         SELECT DISTINCT bc3_with_all_vw.tracknumber,
            bc3_with_all_vw.latitude,
            bc3_with_all_vw.longitude,
            bc3_with_all_vw.altitude,
            bc3_with_all_vw.groundspeed,
            bc3_with_all_vw.heading,
            bc3_with_all_vw.trackquality,
            bc3_with_all_vw.trackcategory,
            bc3_with_all_vw.trackid,
            bc3_with_all_vw.specifictype,
            bc3_with_all_vw.specifictype_descr,
            bc3_with_all_vw.platform,
            bc3_with_all_vw.platform_descr,
            bc3_with_all_vw.callsign,
            bc3_with_all_vw.bc3_vcs,
            bc3_with_all_vw.source,
            bc3_with_all_vw.squawkid,
            bc3_with_all_vw.bc3_jtn,
            bc3_with_all_vw.aircraft_type,
            bc3_with_all_vw.bc3_updated,
            bc3_with_all_vw.fuel,
            bc3_with_all_vw.fuel_factor,
            bc3_with_all_vw.fuel_time_marker,
            bc3_with_all_vw.weapon
           FROM bc3_with_all_vw
          WHERE bc3_with_all_vw.trackid <> 'Friend'::text AND bc3_with_all_vw.source = 'PPLI'::text AND bc3_with_all_vw.bc3_updated >= (now() - '03:00:00'::interval) AND bc3_with_all_vw.bc3_updated <= now()
        ), dis AS (
         SELECT DISTINCT bc3_with_all_vw.latitude,
            bc3_with_all_vw.longitude,
            bc3_with_all_vw.trackcategory,
            bc3_with_all_vw.trackid,
            TRIM(BOTH FROM bc3_with_all_vw.callsign) AS callsign,
            ("left"(bc3_with_all_vw.callsign, 1) || (( SELECT "right"(regexp_replace(bc3_with_all_vw.callsign, '[\s\d]+$'::text, ''::text), 1) AS "right"))) || (( SELECT regexp_matches(bc3_with_all_vw.callsign, '\d+$'::text) AS regexp_matches
                 LIMIT 1))[1] AS callsign_abbr,
            bc3_with_all_vw.bc3_vcs,
            bc3_with_all_vw.squawkid,
            bc3_with_all_vw.aircraft_type,
            bc3_with_all_vw.source,
            bc3_with_all_vw.weapon,
            bc3_with_all_vw.bc3_jtn,
            bc3_with_all_vw.tracknumber,
            bc3_with_all_vw.bc3_updated,
            row_number() OVER (PARTITION BY bc3_with_all_vw.latitude, bc3_with_all_vw.longitude ORDER BY bc3_with_all_vw.bc3_updated DESC) AS rn
           FROM bc3_with_all_vw
          WHERE bc3_with_all_vw.trackid <> 'Friend'::text AND bc3_with_all_vw.source <> 'PPLI'::text AND bc3_with_all_vw.bc3_updated >= (now() - '03:00:00'::interval) AND bc3_with_all_vw.bc3_updated <= now()
        )
 SELECT DISTINCT COALESCE(bc3.latitude, dis.latitude) AS latitude,
    COALESCE(bc3.longitude, dis.longitude) AS longitude,
    COALESCE(bc3.trackid, dis.trackid) AS trackid,
    COALESCE(bc3.trackcategory, dis.trackcategory) AS trackcategory,
    TRIM(BOTH FROM COALESCE(bc3.callsign, dis.callsign)) AS callsign,
    COALESCE(bc3.bc3_vcs, dis.bc3_vcs) AS vcs,
    COALESCE(bc3.squawkid, dis.squawkid) AS mode3,
    COALESCE(bc3.aircraft_type, dis.aircraft_type) AS aircraft_type,
    COALESCE(bc3.weapon, dis.weapon) AS weapon,
    COALESCE(bc3.bc3_jtn, dis.bc3_jtn) AS bc3_jtn,
    COALESCE(bc3.tracknumber, dis.tracknumber) AS merged_tracknumber
   FROM dis
     LEFT JOIN bc3 ON bc3.bc3_vcs = dis.callsign_abbr AND dis.rn = 1;

ALTER TABLE public.bc3_others_vw
    OWNER TO shooca;

-- View: public.bc3_weapons_flat_vw

-- DROP VIEW public.bc3_weapons_flat_vw;

CREATE OR REPLACE VIEW public.bc3_weapons_flat_vw
 AS
 SELECT jtn,
    string_agg((quantity::text || 'X'::text) || weapon, ', '::text ORDER BY slot) AS packed_weapons
   FROM bc3_weapons
  WHERE weapon <> 'NS'::text
  GROUP BY jtn
  ORDER BY jtn;

ALTER TABLE public.bc3_weapons_flat_vw
    OWNER TO shooca;

-- View: public.bc3_with_all_vw

-- DROP VIEW public.bc3_with_all_vw;

CREATE OR REPLACE VIEW public.bc3_with_all_vw
 AS
 WITH ranked_bc3 AS (
         SELECT bc3_1.tracknumber,
            bc3_1.latitude,
            bc3_1.longitude,
            bc3_1.altitude,
            bc3_1.groundspeed,
            bc3_1.heading,
            bc3_1.trackquality,
            bc3_1.trackcategory,
            bc3_1.trackid,
            bc3_1.jtn,
            bc3_1.last_updated,
            bc3_1.specifictype,
            bc3_1.platform,
            bc3_1.callsign,
            bc3_1.source,
            bc3_1.squawkid,
            row_number() OVER (PARTITION BY (regexp_replace(bc3_1.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer) ORDER BY bc3_1.last_updated DESC) AS rn
           FROM bc3_client bc3_1
          WHERE bc3_1.jtn IS NOT NULL
        ), null_jtn AS (
         SELECT bc3_1.tracknumber,
            bc3_1.latitude,
            bc3_1.longitude,
            bc3_1.altitude,
            bc3_1.groundspeed,
            bc3_1.heading,
            bc3_1.trackquality,
            bc3_1.trackcategory,
            bc3_1.trackid,
            bc3_1.jtn,
            bc3_1.last_updated,
            bc3_1.specifictype,
            bc3_1.platform,
            bc3_1.callsign,
            bc3_1.source,
            bc3_1.squawkid,
            row_number() OVER (PARTITION BY bc3_1.callsign ORDER BY bc3_1.last_updated DESC) AS rn
           FROM bc3_client bc3_1
          WHERE bc3_1.jtn IS NULL
        ), null_bc3 AS (
         SELECT bc3_1.tracknumber,
            bc3_1.latitude,
            bc3_1.longitude,
            bc3_1.altitude,
            bc3_1.groundspeed,
            bc3_1.heading,
            bc3_1.trackquality,
            bc3_1.trackcategory,
            bc3_1.trackid,
            bc3_1.jtn,
            bc3_1.last_updated,
            bc3_1.specifictype,
            bc3_1.platform,
            bc3_1.callsign,
            bc3_1.source,
            bc3_1.squawkid,
            row_number() OVER (PARTITION BY bc3_1.latitude, bc3_1.longitude ORDER BY bc3_1.last_updated DESC) AS rn
           FROM bc3_client bc3_1
          WHERE bc3_1.jtn IS NULL AND TRIM(BOTH FROM bc3_1.callsign) = ''::text
          ORDER BY bc3_1.latitude, bc3_1.longitude, (row_number() OVER (PARTITION BY bc3_1.latitude, bc3_1.longitude ORDER BY bc3_1.last_updated DESC))
        ), latest_bc3 AS (
         SELECT ranked_bc3.tracknumber,
            ranked_bc3.latitude,
            ranked_bc3.longitude,
            ranked_bc3.altitude,
            ranked_bc3.groundspeed,
            ranked_bc3.heading,
            ranked_bc3.trackquality,
            ranked_bc3.trackcategory,
            ranked_bc3.trackid,
            ranked_bc3.jtn,
            ranked_bc3.last_updated,
            ranked_bc3.specifictype,
            ranked_bc3.platform,
            ranked_bc3.callsign,
            ranked_bc3.source,
            ranked_bc3.squawkid,
            ranked_bc3.rn
           FROM ranked_bc3
          WHERE ranked_bc3.rn = 1
        UNION ALL
         SELECT null_jtn.tracknumber,
            null_jtn.latitude,
            null_jtn.longitude,
            null_jtn.altitude,
            null_jtn.groundspeed,
            null_jtn.heading,
            null_jtn.trackquality,
            null_jtn.trackcategory,
            null_jtn.trackid,
            null_jtn.jtn,
            null_jtn.last_updated,
            null_jtn.specifictype,
            null_jtn.platform,
            null_jtn.callsign,
            null_jtn.source,
            null_jtn.squawkid,
            null_jtn.rn
           FROM null_jtn
          WHERE null_jtn.rn = 1
        UNION ALL
         SELECT null_bc3.tracknumber,
            null_bc3.latitude,
            null_bc3.longitude,
            null_bc3.altitude,
            null_bc3.groundspeed,
            null_bc3.heading,
            null_bc3.trackquality,
            null_bc3.trackcategory,
            null_bc3.trackid,
            null_bc3.jtn,
            null_bc3.last_updated,
            null_bc3.specifictype,
            null_bc3.platform,
            null_bc3.callsign,
            null_bc3.source,
            null_bc3.squawkid,
            null_bc3.rn
           FROM null_bc3
          WHERE null_bc3.rn = 1
        )
 SELECT bc3.tracknumber,
    bc3.latitude,
    bc3.longitude,
    bc3.altitude,
    bc3.groundspeed,
    bc3.heading,
    bc3.trackquality,
    bc3.trackcategory,
    bc3.trackid,
    bc3.specifictype,
    st.type_descr AS specifictype_descr,
    bc3.platform,
    pt.platform_descr,
    COALESCE(ato.callsign, NULLIF(bc3.callsign, ''::text)) AS callsign,
    vcs.vcs AS bc3_vcs,
    bc3.source,
    bc3.squawkid,
    bc3.jtn AS bc3_jtn,
    COALESCE(bsen.aircraft_type, ato.aircraft_type) AS aircraft_type,
    bc3.last_updated AS bc3_updated,
    bf.fuel,
    bf.fuel_factor,
    bf.fuel_time_marker,
    COALESCE(wpn.packed_weapons, ato.default_munitions) AS weapon
   FROM latest_bc3 bc3
     LEFT JOIN bc3_weapons_flat_vw wpn ON regexp_replace(wpn.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer = regexp_replace(bc3.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer
     LEFT JOIN bc3lookup.specific_types st ON st.track_category = bc3.trackcategory AND st.type_id = bc3.specifictype
     LEFT JOIN bc3lookup.platform_types pt ON pt.platform_id = bc3.platform
     LEFT JOIN bc3_fuel bf ON regexp_replace(bf.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer = regexp_replace(bc3.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer
     LEFT JOIN bc3_sensors bsen ON regexp_replace(bsen.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer = regexp_replace(bc3.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer
     LEFT JOIN bc3_vcs vcs ON regexp_replace(vcs.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer = regexp_replace(bc3.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer
     LEFT JOIN bc3lookup.tmdash_ato ato ON ato.mode3 = bc3.squawkid
  WHERE bc3.last_updated >= (now() - '03:00:00'::interval) AND bc3.last_updated <= now()
  ORDER BY bc3.last_updated DESC;

ALTER TABLE public.bc3_with_all_vw
    OWNER TO shooca;

-- View: public.bc3_with_weapons_vw

-- DROP VIEW public.bc3_with_weapons_vw;

CREATE OR REPLACE VIEW public.bc3_with_weapons_vw
 AS
 WITH ranked_bc3 AS (
         SELECT bc3_1.tracknumber,
            bc3_1.latitude,
            bc3_1.longitude,
            bc3_1.altitude,
            bc3_1.groundspeed,
            bc3_1.heading,
            bc3_1.trackquality,
            bc3_1.trackcategory,
            bc3_1.trackid,
            bc3_1.jtn,
            bc3_1.last_updated,
            bc3_1.specifictype,
            bc3_1.platform,
            bc3_1.callsign,
            bc3_1.source,
            bc3_1.squawkid,
            row_number() OVER (PARTITION BY (regexp_replace(bc3_1.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer) ORDER BY bc3_1.last_updated DESC) AS rn
           FROM bc3_client bc3_1
          WHERE bc3_1.jtn IS NOT NULL
        ), null_jtn AS (
         SELECT bc3_1.tracknumber,
            bc3_1.latitude,
            bc3_1.longitude,
            bc3_1.altitude,
            bc3_1.groundspeed,
            bc3_1.heading,
            bc3_1.trackquality,
            bc3_1.trackcategory,
            bc3_1.trackid,
            bc3_1.jtn,
            bc3_1.last_updated,
            bc3_1.specifictype,
            bc3_1.platform,
            bc3_1.callsign,
            bc3_1.source,
            bc3_1.squawkid,
            row_number() OVER (PARTITION BY bc3_1.callsign ORDER BY bc3_1.last_updated DESC) AS rn
           FROM bc3_client bc3_1
          WHERE bc3_1.jtn IS NULL
        ), null_bc3 AS (
         SELECT bc3_1.tracknumber,
            bc3_1.latitude,
            bc3_1.longitude,
            bc3_1.altitude,
            bc3_1.groundspeed,
            bc3_1.heading,
            bc3_1.trackquality,
            bc3_1.trackcategory,
            bc3_1.trackid,
            bc3_1.jtn,
            bc3_1.last_updated,
            bc3_1.specifictype,
            bc3_1.platform,
            bc3_1.callsign,
            bc3_1.source,
            bc3_1.squawkid,
            row_number() OVER (PARTITION BY bc3_1.latitude, bc3_1.longitude ORDER BY bc3_1.last_updated DESC) AS rn
           FROM bc3_client bc3_1
          WHERE bc3_1.jtn IS NULL AND TRIM(BOTH FROM bc3_1.callsign) = ''::text
          ORDER BY bc3_1.latitude, bc3_1.longitude, (row_number() OVER (PARTITION BY bc3_1.latitude, bc3_1.longitude ORDER BY bc3_1.last_updated DESC))
        ), latest_bc3 AS (
         SELECT ranked_bc3.tracknumber,
            ranked_bc3.latitude,
            ranked_bc3.longitude,
            ranked_bc3.altitude,
            ranked_bc3.groundspeed,
            ranked_bc3.heading,
            ranked_bc3.trackquality,
            ranked_bc3.trackcategory,
            ranked_bc3.trackid,
            ranked_bc3.jtn,
            ranked_bc3.last_updated,
            ranked_bc3.specifictype,
            ranked_bc3.platform,
            ranked_bc3.callsign,
            ranked_bc3.source,
            ranked_bc3.squawkid,
            ranked_bc3.rn
           FROM ranked_bc3
          WHERE ranked_bc3.rn = 1
        UNION ALL
         SELECT null_jtn.tracknumber,
            null_jtn.latitude,
            null_jtn.longitude,
            null_jtn.altitude,
            null_jtn.groundspeed,
            null_jtn.heading,
            null_jtn.trackquality,
            null_jtn.trackcategory,
            null_jtn.trackid,
            null_jtn.jtn,
            null_jtn.last_updated,
            null_jtn.specifictype,
            null_jtn.platform,
            null_jtn.callsign,
            null_jtn.source,
            null_jtn.squawkid,
            null_jtn.rn
           FROM null_jtn
          WHERE null_jtn.rn = 1
        UNION ALL
         SELECT null_bc3.tracknumber,
            null_bc3.latitude,
            null_bc3.longitude,
            null_bc3.altitude,
            null_bc3.groundspeed,
            null_bc3.heading,
            null_bc3.trackquality,
            null_bc3.trackcategory,
            null_bc3.trackid,
            null_bc3.jtn,
            null_bc3.last_updated,
            null_bc3.specifictype,
            null_bc3.platform,
            null_bc3.callsign,
            null_bc3.source,
            null_bc3.squawkid,
            null_bc3.rn
           FROM null_bc3
          WHERE null_bc3.rn = 1
        )
 SELECT bc3.tracknumber,
    bc3.latitude,
    bc3.longitude,
    bc3.altitude,
    bc3.groundspeed,
    bc3.heading,
    bc3.trackquality,
    bc3.trackcategory,
    bc3.trackid,
    bc3.specifictype,
    st.type_descr AS specifictype_descr,
    bc3.platform,
    pt.platform_descr,
    bc3.callsign,
    vcs.vcs,
    bc3.source,
    bc3.squawkid,
    bc3.jtn AS bc3_jtn,
    bsen.aircraft_type,
    bc3.last_updated AS bc3_updated,
    bf.fuel,
    bf.fuel_factor,
    bf.fuel_time_marker,
    wpn.jtn AS wpn_jtn,
    wpn.slot,
    wpn.weapon,
    wpn.quantity,
    wpn.last_updated AS wpn_updated
   FROM latest_bc3 bc3
     LEFT JOIN bc3_weapons wpn ON (regexp_replace(wpn.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer = regexp_replace(bc3.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer OR wpn.jtn IS NULL AND bc3.jtn IS NULL) AND wpn.weapon <> 'NS'::text
     LEFT JOIN bc3lookup.specific_types st ON st.track_category = bc3.trackcategory AND st.type_id = bc3.specifictype
     LEFT JOIN bc3lookup.platform_types pt ON pt.platform_id = bc3.platform
     LEFT JOIN bc3_fuel bf ON regexp_replace(bf.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer = regexp_replace(bc3.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer
     LEFT JOIN bc3_sensors bsen ON regexp_replace(bsen.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer = regexp_replace(bc3.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer
     LEFT JOIN bc3_vcs vcs ON regexp_replace(vcs.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer = regexp_replace(bc3.jtn, '[^0-9]'::text, ''::text, 'g'::text)::integer
     LEFT JOIN bc3lookup.tmdash_ato ato ON ato.mode3 = bc3.squawkid
  ORDER BY bc3.last_updated DESC;

ALTER TABLE public.bc3_with_weapons_vw
    OWNER TO shooca;

