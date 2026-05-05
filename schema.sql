-- ============================================================
--  Music Label Management System
--  schema.sql  |  Reece
-- ============================================================

DROP DATABASE IF EXISTS music_label;
CREATE DATABASE music_label;
USE music_label;

-- ------------------------------------------------------------
-- ARTISTS
-- ------------------------------------------------------------
CREATE TABLE artists (
    artist_id   INT           AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    country     VARCHAR(80)   NOT NULL DEFAULT 'Unknown',
    bio         TEXT,
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (name)
);

-- ------------------------------------------------------------
-- CONTRACTS  (1:1 with artists)
-- ------------------------------------------------------------
CREATE TABLE contracts (
    contract_id  INT            AUTO_INCREMENT PRIMARY KEY,
    artist_id    INT            NOT NULL UNIQUE,
    royalty_rate DECIMAL(5, 2)  NOT NULL,
    start_date   DATE           NOT NULL,
    end_date     DATE,
    status       VARCHAR(20)    NOT NULL DEFAULT 'active',
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (royalty_rate >= 0 AND royalty_rate <= 100),
    CHECK (status IN ('active', 'expired', 'terminated'))
);

-- ------------------------------------------------------------
-- ALBUMS  (M:1 with artists)
-- ------------------------------------------------------------
CREATE TABLE albums (
    album_id      INT          AUTO_INCREMENT PRIMARY KEY,
    artist_id     INT          NOT NULL,
    title         VARCHAR(150) NOT NULL,
    release_date  DATE,
    genre         VARCHAR(60)  NOT NULL DEFAULT 'Uncategorized',
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- TRACKS  (M:1 with albums)
-- ------------------------------------------------------------
CREATE TABLE tracks (
    track_id          INT          AUTO_INCREMENT PRIMARY KEY,
    album_id          INT          NOT NULL,
    song_name         VARCHAR(150) NOT NULL,
    duration_seconds  INT          NOT NULL DEFAULT 0,
    file_type         VARCHAR(10)  NOT NULL DEFAULT 'mp3',
    FOREIGN KEY (album_id) REFERENCES albums(album_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (duration_seconds >= 0),
    CHECK (file_type IN ('mp3', 'wav', 'flac', 'aac'))
);

-- ------------------------------------------------------------
-- PRODUCERS
-- ------------------------------------------------------------
CREATE TABLE producers (
    producer_id  INT          AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    specialty    VARCHAR(80)  NOT NULL DEFAULT 'General',
    UNIQUE (name)
);

-- ------------------------------------------------------------
-- CREDITS  — junction table for TRACKS M:N PRODUCERS
-- ------------------------------------------------------------
CREATE TABLE credits (
    credit_id    INT         AUTO_INCREMENT PRIMARY KEY,
    track_id     INT         NOT NULL,
    producer_id  INT         NOT NULL,
    role         VARCHAR(60) NOT NULL DEFAULT 'Producer',
    FOREIGN KEY (track_id)    REFERENCES tracks(track_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (producer_id) REFERENCES producers(producer_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (track_id, producer_id, role)
);
