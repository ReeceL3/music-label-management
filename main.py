"""
Music Label Management System
main.py  |  Reece
"""

from database import (
    create_connection,
    # artists
    get_all_artists, search_artists, add_artist,
    update_artist_bio, delete_artist,
    # albums
    get_albums_by_artist, add_album,
    # tracks
    get_tracks_by_album, search_tracks, add_track,
    # contracts
    get_contract_by_artist, update_contract_status,
    # producers / credits
    get_all_producers, get_credits_for_track,
    # transaction
    sign_new_artist,
    # reports
    report_active_contracts, report_tracks_by_genre, report_producer_credits,
)




def divider(char="─", width=55):
    print(char * width)

def header(title):
    print()
    divider("═")
    print(f"  {title}")
    divider("═")

def fmt_duration(seconds):
    """Convert integer seconds to m:ss string."""
    return f"{seconds // 60}:{seconds % 60:02d}"




def menu_artists(conn):
    while True:
        header("🎤  ARTISTS")
        print("  1. View all artists")
        print("  2. Search artist by name")
        print("  3. View artist albums")
        print("  4. Update artist bio")
        print("  5. Delete artist")
        print("  0. Back")
        divider()
        choice = input("  Choice: ").strip()

        if choice == "1":
            artists = get_all_artists(conn)
            if not artists:
                print("  No artists found.")
            else:
                print(f"\n  {'ID':<5} {'Name':<25} {'Country'}")
                divider()
                for a in artists:
                    print(f"  {a['artist_id']:<5} {a['name']:<25} {a['country']}")

        elif choice == "2":
            kw = input("  Search name: ").strip()
            if not kw:
                print("  ⚠  Please enter a search term.")
                continue
            results = search_artists(conn, kw)
            if not results:
                print("  No matches found.")
            else:
                for a in results:
                    print(f"\n  [{a['artist_id']}] {a['name']} — {a['country']}")
                    if a['bio']:
                        print(f"  {a['bio'][:100]}...")

        elif choice == "3":
            artist_id = _get_int("  Artist ID: ")
            if artist_id is None:
                continue
            albums = get_albums_by_artist(conn, artist_id)
            if not albums:
                print("  No albums found for that artist.")
            else:
                print(f"\n  {'ID':<5} {'Title':<30} {'Genre':<15} Released")
                divider()
                for al in albums:
                    print(f"  {al['album_id']:<5} {al['title']:<30} "
                          f"{al['genre']:<15} {al['release_date']}")

        elif choice == "4":
            artist_id = _get_int("  Artist ID to update: ")
            if artist_id is None:
                continue
            new_bio = input("  New bio: ").strip()
            if not new_bio:
                print("  ⚠  Bio cannot be empty.")
                continue
            if update_artist_bio(conn, artist_id, new_bio):
                print("  ✅ Bio updated.")
            else:
                print("  ❌ Artist not found.")

        elif choice == "5":
            artist_id = _get_int("  Artist ID to delete: ")
            if artist_id is None:
                continue
            confirm = input(
                "  ⚠  This deletes all their albums, tracks, "
                "credits and contract. Type YES to confirm: "
            ).strip()
            if confirm == "YES":
                if delete_artist(conn, artist_id):
                    print("  ✅ Artist deleted.")
                else:
                    print("  ❌ Artist not found.")
            else:
                print("  Cancelled.")

        elif choice == "0":
            break
        else:
            print("  ⚠  Invalid choice.")




def menu_albums_tracks(conn):
    while True:
        header("💿  ALBUMS & TRACKS")
        print("  1. View tracks on an album")
        print("  2. Search tracks by name")
        print("  3. Add a new album")
        print("  4. Add a track to an album")
        print("  5. View credits for a track")
        print("  0. Back")
        divider()
        choice = input("  Choice: ").strip()

        if choice == "1":
            album_id = _get_int("  Album ID: ")
            if album_id is None:
                continue
            tracks = get_tracks_by_album(conn, album_id)
            if not tracks:
                print("  No tracks found.")
            else:
                print(f"\n  {'ID':<5} {'Song':<35} {'Length':<8} Type")
                divider()
                for t in tracks:
                    print(f"  {t['track_id']:<5} {t['song_name']:<35} "
                          f"{fmt_duration(t['duration_seconds']):<8} {t['file_type']}")

        elif choice == "2":
            kw = input("  Search song name: ").strip()
            if not kw:
                print("  ⚠  Please enter a search term.")
                continue
            results = search_tracks(conn, kw)
            if not results:
                print("  No matches found.")
            else:
                print(f"\n  {'ID':<5} {'Song':<28} {'Length':<8} {'Album':<25} Artist")
                divider()
                for t in results:
                    print(f"  {t['track_id']:<5} {t['song_name']:<28} "
                          f"{fmt_duration(t['duration_seconds']):<8} "
                          f"{t['album']:<25} {t['artist']}")

        elif choice == "3":
            print("\n  -- New Album --")
            artist_id   = _get_int("  Artist ID: ")
            if artist_id is None:
                continue
            title        = input("  Album title: ").strip()
            release_date = input("  Release date (YYYY-MM-DD): ").strip()
            genre        = input("  Genre: ").strip()

            if not title or not release_date or not genre:
                print("  ⚠  All fields required.")
                continue

            new_id = add_album(conn, artist_id, title, release_date, genre)
            if new_id:
                print(f"  ✅ Album added (ID {new_id}).")

        elif choice == "4":
            print("\n  -- New Track --")
            album_id = _get_int("  Album ID: ")
            if album_id is None:
                continue
            song_name = input("  Song name: ").strip()
            duration  = _get_int("  Duration (seconds): ")
            if duration is None:
                continue
            print("  File type options: mp3 / wav / flac / aac")
            file_type = input("  File type: ").strip().lower()
            if file_type not in ("mp3", "wav", "flac", "aac"):
                print("  ⚠  Invalid file type.")
                continue

            new_id = add_track(conn, album_id, song_name, duration, file_type)
            if new_id:
                print(f"  ✅ Track added (ID {new_id}).")

        elif choice == "5":
            track_id = _get_int("  Track ID: ")
            if track_id is None:
                continue
            credits = get_credits_for_track(conn, track_id)
            if not credits:
                print("  No credits found for that track.")
            else:
                print(f"\n  {'Producer':<25} {'Role':<20} Specialty")
                divider()
                for c in credits:
                    print(f"  {c['producer']:<25} {c['role']:<20} {c['specialty']}")

        elif choice == "0":
            break
        else:
            print("  ⚠  Invalid choice.")




def menu_contracts(conn):
    while True:
        header("📄  CONTRACTS")
        print("  1. View contract for an artist")
        print("  2. Update contract status")
        print("  0. Back")
        divider()
        choice = input("  Choice: ").strip()

        if choice == "1":
            artist_id = _get_int("  Artist ID: ")
            if artist_id is None:
                continue
            c = get_contract_by_artist(conn, artist_id)
            if not c:
                print("  No contract found.")
            else:
                print(f"\n  Artist:       {c['artist']}")
                print(f"  Royalty rate: {c['royalty_rate']}%")
                print(f"  Start date:   {c['start_date']}")
                print(f"  End date:     {c['end_date'] or 'Open-ended'}")
                print(f"  Status:       {c['status']}")

        elif choice == "2":
            contract_id = _get_int("  Contract ID: ")
            if contract_id is None:
                continue
            print("  Statuses: active / expired / terminated")
            new_status = input("  New status: ").strip().lower()
            if new_status not in ("active", "expired", "terminated"):
                print("  ⚠  Invalid status.")
                continue
            if update_contract_status(conn, contract_id, new_status):
                print("  ✅ Contract updated.")
            else:
                print("  ❌ Contract not found.")

        elif choice == "0":
            break
        else:
            print("  ⚠  Invalid choice.")




def menu_producers(conn):
    header("🎛  PRODUCERS")
    producers = get_all_producers(conn)
    if not producers:
        print("  No producers found.")
    else:
        print(f"\n  {'ID':<5} {'Name':<25} Specialty")
        divider()
        for p in producers:
            print(f"  {p['producer_id']:<5} {p['name']:<25} {p['specialty']}")
    input("\n  Press Enter to continue...")



def menu_sign_artist(conn):
    header("✍  SIGN NEW ARTIST")
    print("  This creates an artist AND their contract in one transaction.\n")

    name        = input("  Artist name:               ").strip()
    country     = input("  Country:                   ").strip()
    bio         = input("  Bio:                       ").strip()
    royalty     = _get_float("  Royalty rate (0–100 %):   ")
    start_date  = input("  Contract start (YYYY-MM-DD): ").strip()

    if not all([name, country, start_date]) or royalty is None:
        print("  ⚠  All fields required.")
        return

    if not (0 <= royalty <= 100):
        print("  ⚠  Royalty must be between 0 and 100.")
        return

    new_id = sign_new_artist(conn, name, country, bio, royalty, start_date)
    if new_id:
        print(f"\n  ✅ Artist '{name}' signed! Artist ID: {new_id}")
        print(f"     Contract created with {royalty}% royalty rate.")
    input("\n  Press Enter to continue...")




def menu_reports(conn):
    while True:
        header("📊  REPORTS")
        print("  1. Active contracts & royalty rates")
        print("  2. Tracks by genre")
        print("  3. Producer credit counts")
        print("  0. Back")
        divider()
        choice = input("  Choice: ").strip()

        if choice == "1":
            rows = report_active_contracts(conn)
            print(f"\n  {'Artist':<22} {'Country':<14} {'Royalty%':<10} Start       End")
            divider()
            for r in rows:
                end = str(r['end_date']) if r['end_date'] else 'Open'
                print(f"  {r['artist']:<22} {r['country']:<14} "
                      f"{r['royalty_rate']:<10} {r['start_date']}  {end}")

        elif choice == "2":
            genre = input("  Genre keyword: ").strip()
            rows = report_tracks_by_genre(conn, genre)
            if not rows:
                print("  No tracks found.")
            else:
                print(f"\n  {'Artist':<20} {'Album':<25} {'Track':<28} Length")
                divider()
                for r in rows:
                    print(f"  {r['artist']:<20} {r['album']:<25} "
                          f"{r['track']:<28} {fmt_duration(r['duration_seconds'])}")

        elif choice == "3":
            rows = report_producer_credits(conn)
            print(f"\n  {'Producer':<25} {'Specialty':<20} Credits")
            divider()
            for r in rows:
                print(f"  {r['producer']:<25} {r['specialty']:<20} {r['total_credits']}")

        elif choice == "0":
            break
        else:
            print("  ⚠  Invalid choice.")




def _get_int(prompt):
    """Prompt for an integer; return None if invalid."""
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print("  ⚠  Please enter a valid number.")
        return None


def _get_float(prompt):
    """Prompt for a float; return None if invalid."""
    raw = input(prompt).strip()
    try:
        return float(raw)
    except ValueError:
        print("  ⚠  Please enter a valid number.")
        return None


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

def main():
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║        🎵  Music Label Management System             ║")
    print("╚══════════════════════════════════════════════════════╝")

    conn = create_connection()
    if not conn:
        print("  Could not connect to the database. Check your credentials.")
        return

    print("  ✅ Connected to music_label database.")

    while True:
        header("MAIN MENU")
        print("  1. Artists")
        print("  2. Albums & Tracks")
        print("  3. Contracts")
        print("  4. Producers")
        print("  5. Sign New Artist  (transaction)")
        print("  6. Reports")
        print("  0. Exit")
        divider()
        choice = input("  Choice: ").strip()

        if   choice == "1": menu_artists(conn)
        elif choice == "2": menu_albums_tracks(conn)
        elif choice == "3": menu_contracts(conn)
        elif choice == "4": menu_producers(conn)
        elif choice == "5": menu_sign_artist(conn)
        elif choice == "6": menu_reports(conn)
        elif choice == "0":
            print("\n  👋 Goodbye!\n")
            break
        else:
            print("  ⚠  Invalid choice.")

    conn.close()


if __name__ == "__main__":
    main()