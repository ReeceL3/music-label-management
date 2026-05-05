-- ============================================================
--  Music Label Management System
--  queries.sql  |  8 Example Queries
-- ============================================================

USE music_label;

-- ============================================================
-- Query 1: All artists and their active contract royalty rates
-- (JOIN + WHERE filter)
-- ============================================================
SELECT
    a.name          AS artist,
    a.country,
    c.royalty_rate  AS royalty_pct,
    c.start_date,
    c.status
FROM artists a
JOIN contracts c ON a.artist_id = c.artist_id
WHERE c.status = 'active'
ORDER BY c.royalty_rate DESC;

-- ============================================================
-- Query 2: Full track listing — artist, album, track, duration
-- (3-table JOIN)
-- ============================================================
SELECT
    a.name                                      AS artist,
    al.title                                    AS album,
    t.song_name                                 AS track,
    CONCAT(
        FLOOR(t.duration_seconds / 60), ':',
        LPAD(MOD(t.duration_seconds, 60), 2, '0')
    )                                           AS duration,
    t.file_type
FROM tracks t
JOIN albums al  ON t.album_id   = al.album_id
JOIN artists a  ON al.artist_id = a.artist_id
ORDER BY a.name, al.title, t.track_id;

-- ============================================================
-- Query 3: All producers on a specific track
-- (M:N join through credits)
-- ============================================================
SELECT
    t.song_name     AS track,
    p.name          AS producer,
    cr.role
FROM credits cr
JOIN tracks    t ON cr.track_id    = t.track_id
JOIN producers p ON cr.producer_id = p.producer_id
WHERE t.song_name = 'Anti-Hero';

-- ============================================================
-- Query 4: Album count and average track duration per artist
-- (GROUP BY + aggregate)
-- ============================================================
SELECT
    a.name                                  AS artist,
    COUNT(DISTINCT al.album_id)             AS total_albums,
    COUNT(t.track_id)                       AS total_tracks,
    ROUND(AVG(t.duration_seconds) / 60, 2) AS avg_track_min
FROM artists a
LEFT JOIN albums al ON a.artist_id = al.artist_id
LEFT JOIN tracks t  ON al.album_id  = t.album_id
GROUP BY a.artist_id, a.name
ORDER BY total_albums DESC;

-- ============================================================
-- Query 5: Artists with expired contracts still in the system
-- (subquery / filter)
-- ============================================================
SELECT
    a.name,
    c.end_date,
    c.royalty_rate
FROM artists a
JOIN contracts c ON a.artist_id = c.artist_id
WHERE c.status = 'expired'
ORDER BY c.end_date DESC;

-- ============================================================
-- Query 6: Most prolific producers (number of credits)
-- (GROUP BY + HAVING)
-- ============================================================
SELECT
    p.name          AS producer,
    p.specialty,
    COUNT(*)        AS total_credits
FROM producers p
JOIN credits cr ON p.producer_id = cr.producer_id
GROUP BY p.producer_id, p.name, p.specialty
HAVING total_credits >= 1
ORDER BY total_credits DESC;

-- ============================================================
-- Query 7: Albums released after 2021 with their genre
-- (date filter)
-- ============================================================
SELECT
    a.name          AS artist,
    al.title        AS album,
    al.genre,
    al.release_date
FROM albums al
JOIN artists a ON al.artist_id = a.artist_id
WHERE al.release_date >= '2022-01-01'
ORDER BY al.release_date DESC;

-- ============================================================
-- Query 8: Full credits report — which producer touched
--          which track on which album for which artist
-- (5-table JOIN)
-- ============================================================
SELECT
    a.name          AS artist,
    al.title        AS album,
    t.song_name     AS track,
    p.name          AS producer,
    cr.role,
    p.specialty
FROM credits cr
JOIN tracks    t  ON cr.track_id    = t.track_id
JOIN albums    al ON t.album_id     = al.album_id
JOIN artists   a  ON al.artist_id   = a.artist_id
JOIN producers p  ON cr.producer_id = p.producer_id
ORDER BY a.name, al.title, t.song_name;
