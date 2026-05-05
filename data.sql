-- ============================================================
--  Music Label Management System
--  data.sql  |  Sample Data (10+ rows per table)
-- ============================================================

USE music_label;

-- ------------------------------------------------------------
-- ARTISTS (12 rows)
-- ------------------------------------------------------------
INSERT INTO artists (name, country, bio) VALUES
('Drake',          'Canada',        'Multi-platinum rapper and singer known for blending hip-hop and R&B.'),
('Taylor Swift',   'USA',           'Country-turned-pop superstar with record-breaking album sales.'),
('Bad Bunny',      'Puerto Rico',   'Latin trap and reggaeton pioneer dominating global charts.'),
('Kendrick Lamar', 'USA',           'Pulitzer Prize-winning rapper considered one of the best of his generation.'),
('Billie Eilish',  'USA',           'Dark-pop singer who rose to fame as a teenager.'),
('J. Cole',        'USA',           'Rapper and producer known for introspective lyricism.'),
('SZA',            'USA',           'Neo-soul and R&B artist with critically acclaimed storytelling.'),
('Tyler the Creator','USA',         'Producer and rapper with an eclectic genre-blending style.'),
('Doja Cat',       'USA',           'Genre-fluid artist merging rap, pop, and R&B.'),
('Frank Ocean',    'USA',           'Cult R&B singer known for channel ORANGE and Blonde.'),
('The Weeknd',     'Canada',        'R&B and synth-pop artist known for dark, cinematic records.'),
('Olivia Rodrigo', 'USA',           'Pop and pop-punk singer who debuted with the SOUR album.');

-- ------------------------------------------------------------
-- CONTRACTS (12 rows — one per artist)
-- ------------------------------------------------------------
INSERT INTO contracts (artist_id, royalty_rate, start_date, end_date, status) VALUES
(1,  22.50, '2020-01-01', '2025-12-31', 'active'),
(2,  30.00, '2019-06-15', '2024-06-14', 'expired'),
(3,  18.75, '2021-03-01', '2026-02-28', 'active'),
(4,  25.00, '2018-09-10', '2023-09-09', 'expired'),
(5,  27.00, '2022-01-01', '2027-01-01', 'active'),
(6,  20.00, '2017-07-04', '2022-07-03', 'expired'),
(7,  24.50, '2021-11-01', '2026-10-31', 'active'),
(8,  19.00, '2020-05-20', '2025-05-19', 'active'),
(9,  23.00, '2022-08-01', '2027-07-31', 'active'),
(10, 35.00, '2016-04-01', NULL,          'active'),
(11, 21.00, '2019-09-01', '2024-08-31', 'expired'),
(12, 26.50, '2021-05-21', '2026-05-20', 'active');

-- ------------------------------------------------------------
-- ALBUMS (14 rows)
-- ------------------------------------------------------------
INSERT INTO albums (artist_id, title, release_date, genre) VALUES
(1,  'Certified Lover Boy',    '2021-09-03', 'Hip-Hop'),
(1,  'Scorpion',               '2018-06-29', 'Hip-Hop'),
(2,  'Midnights',              '2022-10-21', 'Pop'),
(2,  '1989',                   '2014-10-27', 'Pop'),
(3,  'Un Verano Sin Ti',       '2022-05-06', 'Reggaeton'),
(4,  'Mr. Morale & The Big Steppers','2022-05-13','Hip-Hop'),
(5,  'Happier Than Ever',      '2021-07-30', 'Pop'),
(6,  'KOD',                    '2018-04-20', 'Hip-Hop'),
(7,  'SOS',                    '2022-12-09', 'R&B'),
(8,  'Call Me If You Get Lost','2021-06-25', 'Hip-Hop'),
(9,  'Planet Her',             '2021-06-25', 'Pop'),
(11, 'After Hours',            '2020-03-20', 'R&B'),
(11, 'Dawn FM',                '2022-01-07', 'Synth-Pop'),
(12, 'SOUR',                   '2021-05-21', 'Pop-Punk');

-- ------------------------------------------------------------
-- TRACKS (14 rows)
-- ------------------------------------------------------------
INSERT INTO tracks (album_id, song_name, duration_seconds, file_type) VALUES
(1,  'Way 2 Sexy',          213, 'mp3'),
(1,  'Champagne Poetry',    330, 'mp3'),
(2,  'In My Feelings',      234, 'mp3'),
(3,  'Anti-Hero',           200, 'flac'),
(3,  'Lavender Haze',       202, 'flac'),
(5,  'Titi Me Pregunto',    178, 'mp3'),
(6,  'The Heart Part 5',    312, 'wav'),
(7,  'Happier Than Ever',   295, 'flac'),
(8,  'KOD',                 220, 'mp3'),
(9,  'Kill Bill',           154, 'flac'),
(10, 'Lumberjack',          185, 'mp3'),
(11, 'Need to Know',        215, 'mp3'),
(12, 'Blinding Lights',     200, 'mp3'),
(14, 'drivers license',     242, 'flac');

-- ------------------------------------------------------------
-- PRODUCERS (11 rows)
-- ------------------------------------------------------------
INSERT INTO producers (name, specialty) VALUES
('Noah "40" Shebib',    'Mixing'),
('Metro Boomin',        'Beat Making'),
('Jack Antonoff',       'Songwriting'),
('Mike Dean',           'Mixing'),
('Oscar Holter',        'Songwriting'),
('Mustard',             'Beat Making'),
('Sounwave',            'Beat Making'),
('Finneas',             'Recording'),
('DJ Dahi',             'Beat Making'),
('Harv',                'Mixing'),
('Danger Mouse',        'Beat Making');

-- ------------------------------------------------------------
-- CREDITS (12 rows)
-- ------------------------------------------------------------
INSERT INTO credits (track_id, producer_id, role) VALUES
(1,  1,  'Mixing'),
(1,  2,  'Beat Maker'),
(2,  1,  'Producer'),
(3,  1,  'Mixing'),
(4,  3,  'Songwriter'),
(4,  5,  'Mixing'),
(5,  3,  'Producer'),
(7,  7,  'Beat Maker'),
(8,  8,  'Songwriter'),
(8,  8,  'Recording Engineer'),
(9,  4,  'Mixing'),
(14, 8,  'Producer');
