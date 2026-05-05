import mysql.connector
from mysql.connector import Error


# ── connection ────────────────────────────────────────────────
def create_connection():
    """Create and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            database="music_label",
            user="root",
            password="password"        # 👈 empty string — no password
)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"  ❌ Connection error: {e}")
        return None


# ════════════════════════════════════════════════════════════════
# ARTISTS
# ════════════════════════════════════════════════════════════════

def get_all_artists(conn):
    """Return every artist row."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT artist_id, name, country FROM artists ORDER BY name")
        return cur.fetchall()
    except Error as e:
        print(f"  ❌ {e}")
        return []


def search_artists(conn, keyword):
    """Search artists by name (partial match)."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT artist_id, name, country, bio FROM artists "
            "WHERE name LIKE %s ORDER BY name",
            (f"%{keyword}%",)
        )
        return cur.fetchall()
    except Error as e:
        print(f"  ❌ {e}")
        return []


def add_artist(conn, name, country, bio):
    """Insert a new artist. Returns new artist_id or None."""
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO artists (name, country, bio) VALUES (%s, %s, %s)",
            (name, country, bio)
        )
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"  ❌ {e}")
        return None


def update_artist_bio(conn, artist_id, new_bio):
    """Update an artist's bio."""
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE artists SET bio = %s WHERE artist_id = %s",
            (new_bio, artist_id)
        )
        conn.commit()
        return cur.rowcount > 0
    except Error as e:
        print(f"  ❌ {e}")
        return False


def delete_artist(conn, artist_id):
    """Delete an artist (cascades to albums, tracks, credits, contract)."""
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM artists WHERE artist_id = %s", (artist_id,))
        conn.commit()
        return cur.rowcount > 0
    except Error as e:
        print(f"  ❌ {e}")
        return False


# ════════════════════════════════════════════════════════════════
# ALBUMS
# ════════════════════════════════════════════════════════════════

def get_albums_by_artist(conn, artist_id):
    """Return all albums for a given artist."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT album_id, title, release_date, genre "
            "FROM albums WHERE artist_id = %s ORDER BY release_date DESC",
            (artist_id,)
        )
        return cur.fetchall()
    except Error as e:
        print(f"  ❌ {e}")
        return []


def add_album(conn, artist_id, title, release_date, genre):
    """Insert a new album. Returns new album_id or None."""
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO albums (artist_id, title, release_date, genre) "
            "VALUES (%s, %s, %s, %s)",
            (artist_id, title, release_date, genre)
        )
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"  ❌ {e}")
        return None


# ════════════════════════════════════════════════════════════════
# TRACKS
# ════════════════════════════════════════════════════════════════

def get_tracks_by_album(conn, album_id):
    """Return all tracks for a given album."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT track_id, song_name, duration_seconds, file_type "
            "FROM tracks WHERE album_id = %s ORDER BY track_id",
            (album_id,)
        )
        return cur.fetchall()
    except Error as e:
        print(f"  ❌ {e}")
        return []


def search_tracks(conn, keyword):
    """Search tracks by song name (partial match), joining artist/album."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT t.track_id, t.song_name, t.duration_seconds, t.file_type, "
            "       al.title AS album, a.name AS artist "
            "FROM tracks t "
            "JOIN albums al ON t.album_id = al.album_id "
            "JOIN artists a ON al.artist_id = a.artist_id "
            "WHERE t.song_name LIKE %s "
            "ORDER BY a.name, al.title",
            (f"%{keyword}%",)
        )
        return cur.fetchall()
    except Error as e:
        print(f"  ❌ {e}")
        return []


def add_track(conn, album_id, song_name, duration_seconds, file_type):
    """Insert a new track. Returns new track_id or None."""
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tracks (album_id, song_name, duration_seconds, file_type) "
            "VALUES (%s, %s, %s, %s)",
            (album_id, song_name, duration_seconds, file_type)
        )
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"  ❌ {e}")
        return None


# ════════════════════════════════════════════════════════════════
# CONTRACTS
# ════════════════════════════════════════════════════════════════

def get_contract_by_artist(conn, artist_id):
    """Return the contract for a given artist."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT c.contract_id, a.name AS artist, c.royalty_rate, "
            "       c.start_date, c.end_date, c.status "
            "FROM contracts c "
            "JOIN artists a ON c.artist_id = a.artist_id "
            "WHERE c.artist_id = %s",
            (artist_id,)
        )
        return cur.fetchone()
    except Error as e:
        print(f"  ❌ {e}")
        return None


def update_contract_status(conn, contract_id, new_status):
    """Update contract status (active / expired / terminated)."""
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE contracts SET status = %s WHERE contract_id = %s",
            (new_status, contract_id)
        )
        conn.commit()
        return cur.rowcount > 0
    except Error as e:
        print(f"  ❌ {e}")
        return False


# ════════════════════════════════════════════════════════════════
# PRODUCERS & CREDITS
# ════════════════════════════════════════════════════════════════

def get_all_producers(conn):
    """Return all producers."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT producer_id, name, specialty FROM producers ORDER BY name"
        )
        return cur.fetchall()
    except Error as e:
        print(f"  ❌ {e}")
        return []


def get_credits_for_track(conn, track_id):
    """Return all producers credited on a track."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT p.name AS producer, cr.role, p.specialty "
            "FROM credits cr "
            "JOIN producers p ON cr.producer_id = p.producer_id "
            "WHERE cr.track_id = %s",
            (track_id,)
        )
        return cur.fetchall()
    except Error as e:
        print(f"  ❌ {e}")
        return []


# ════════════════════════════════════════════════════════════════
# TRANSACTION — sign a new artist
#   Creates: artist row + contract row atomically
# ════════════════════════════════════════════════════════════════

def sign_new_artist(conn, name, country, bio, royalty_rate, start_date):
    """
    Atomically insert a new artist AND their contract.
    Rolls back both if either insert fails.
    """
    try:
        conn.start_transaction()
        cur = conn.cursor()

        # Step 1 — insert artist
        cur.execute(
            "INSERT INTO artists (name, country, bio) VALUES (%s, %s, %s)",
            (name, country, bio)
        )
        new_artist_id = cur.lastrowid

        # Step 2 — insert contract
        cur.execute(
            "INSERT INTO contracts (artist_id, royalty_rate, start_date, status) "
            "VALUES (%s, %s, %s, 'active')",
            (new_artist_id, royalty_rate, start_date)
        )

        conn.commit()
        return new_artist_id

    except Error as e:
        conn.rollback()
        print(f"  ❌ Transaction rolled back: {e}")
        return None


# ════════════════════════════════════════════════════════════════
# REPORTS  (read-only, used in reporting menu)
# ════════════════════════════════════════════════════════════════

def report_active_contracts(conn):
    """Artists with active contracts and their royalty rates."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT a.name AS artist, a.country, c.royalty_rate, "
            "       c.start_date, c.end_date "
            "FROM contracts c "
            "JOIN artists a ON c.artist_id = a.artist_id "
            "WHERE c.status = 'active' "
            "ORDER BY c.royalty_rate DESC"
        )
        return cur.fetchall()
    except Error as e:
        print(f"  ❌ {e}")
        return []


def report_tracks_by_genre(conn, genre):
    """All tracks in albums of a given genre."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT a.name AS artist, al.title AS album, "
            "       t.song_name AS track, t.duration_seconds "
            "FROM tracks t "
            "JOIN albums al ON t.album_id = al.album_id "
            "JOIN artists a ON al.artist_id = a.artist_id "
            "WHERE al.genre LIKE %s "
            "ORDER BY a.name, al.title",
            (f"%{genre}%",)
        )
        return cur.fetchall()
    except Error as e:
        print(f"  ❌ {e}")
        return []


def report_producer_credits(conn):
    """How many tracks each producer has credits on."""
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT p.name AS producer, p.specialty, COUNT(*) AS total_credits "
            "FROM credits cr "
            "JOIN producers p ON cr.producer_id = p.producer_id "
            "GROUP BY p.producer_id, p.name, p.specialty "
            "ORDER BY total_credits DESC"
        )
        return cur.fetchall()
    except Error as e:
        print(f"  ❌ {e}")
        return []