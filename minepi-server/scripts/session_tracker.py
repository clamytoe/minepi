import argparse
import gzip
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta
from glob import glob

from tabulate import tabulate

base_dir = "/home/clamytoe/minecraft-server"
data_dir = f"{base_dir}/data"
log_dir = f"{data_dir}/logs"
output_path = f"{base_dir}/logs/player_sessions.json"
parsed_log_path = f"{base_dir}/logs/parsed_logs.json"

logins = {}
current_sessions = {}

DEBUG = False


def dryrun(log_files, new_session_ids):
    print(f"\n[DRY-RUN] Parsed {len(log_files)} log files")
    print(f"[DRY-RUN] Would add {len(new_session_ids)} sessions:")
    for sid in new_session_ids:
        print(f"  - {sid}")
    print("[DRY-RUN] No files were written.")
    return


def generate_summary(logins):
    summary = defaultdict(
        lambda: {"count": 0, "total_time": timedelta(), "last_date": None}
    )

    for name, data in logins.items():
        for session in data.get("sessions", []):
            summary[name]["count"] += 1  # type: ignore
            duration = session.get("session_duration")
            if duration:
                try:
                    h, m, s = map(int, duration.split(":"))
                    summary[name]["total_time"] += timedelta(
                        hours=h, minutes=m, seconds=s
                    )  # type: ignore
                except Exception:
                    pass
            date_str = session.get("session_id", "").split("_")[1][:8]
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str, "%Y%m%d")
                    if (
                        not summary[name]["last_date"]
                        or date_obj > summary[name]["last_date"]  # type: ignore
                    ):
                        summary[name]["last_date"] = date_obj  # type: ignore
                except Exception:
                    pass

    return summary


def parse_time(t):
    try:
        return datetime.strptime(t, "%H:%M:%S")
    except Exception as e:
        if DEBUG:
            print(f"[ERROR] Failed to parse time '{t}': {e}")
        return None


def parse_achievement(line, timestamp):
    name = (
        line.split("[Server thread/INFO]: ")[1]
        .split(" has made the advancement")[0]
        .strip()
    )
    advancement = line[line.rfind("[") + 1 : line.rfind("]")].strip()
    if name in current_sessions:
        current_sessions[name]["achievements"].append(
            {"name": advancement, "time": timestamp}
        )
        if DEBUG:
            print(f"[DEBUG] Achievement logged for {name}: {advancement}")


def parse_login(line, timestamp):
    if "] logged in with entity id" in line:
        name = line.split("[Server thread/INFO]: ")[1].split("[")[0].strip()
        spawn = line.split("at (")[1].split(")")[0].strip()
        current_sessions[name] = {
            "login_time": timestamp,
            "spawn": spawn,
            "achievements": [],
        }
        if DEBUG:
            print(f"[INFO] Login detected for {name} at {timestamp}")


def parse_logout(line, timestamp, log_date):
    name = line.split("[Server thread/INFO]: ")[1].split(" left the game")[0].strip()
    if name in current_sessions and "login_time" in current_sessions[name]:
        current_sessions[name]["logout_time"] = timestamp
        login = parse_time(current_sessions[name]["login_time"])
        logout = parse_time(timestamp)
        if login and logout:
            current_sessions[name]["session_duration"] = str(logout - login)
            session_id = f"{name}_{log_date.replace('-', '')}_{current_sessions[name]['login_time'].replace(':', '')}"
            current_sessions[name]["session_id"] = session_id

            if name not in logins:
                logins[name] = {"uuid": None, "sessions": []}

            existing_ids = {s["session_id"] for s in logins[name]["sessions"]}
            if session_id not in existing_ids:
                logins[name]["sessions"].append(current_sessions[name])
                if DEBUG:
                    print(f"[INFO] Session saved for {name}: {session_id}")
        else:
            if DEBUG:
                print(
                    f"[WARN] Skipping session for {name} due to timestamp parse failure"
                )
        current_sessions[name] = {}


def parse_uuid(line):
    parts = line.split("UUID of player ")
    if len(parts) > 1:
        name_uuid = parts[1].split(" is ")
        if len(name_uuid) == 2:
            return name_uuid[0].strip(), name_uuid[1].strip()
    return None, None


def parse_lines(lines, log_date):
    for line in lines:
        timestamp = (
            line[1 : line.index("]")] if line.startswith("[") and "]" in line else None
        )
        if not timestamp:
            if DEBUG:
                print(f"[WARN] Skipping line due to missing timestamp: {line.strip()}")
            continue

        match line:
            case _ if "UUID of player" in line:
                name, uuid = parse_uuid(line)
                if name and uuid:
                    if name not in logins:
                        logins[name] = {"uuid": uuid, "sessions": []}
                    else:
                        logins[name]["uuid"] = uuid
                    if DEBUG:
                        print(f"[DEBUG] UUID registered for {name}: {uuid}")

            case _ if "logged in with entity id" in line:
                parse_login(line, timestamp)

            case _ if "left the game" in line:
                parse_logout(line, timestamp, log_date)

            case _ if "has made the advancement" in line:
                parse_achievement(line, timestamp)


def read_log_file(path, is_gz=False):
    open_fn = gzip.open if is_gz else open
    with open_fn(path, "rt", encoding="utf-8") as f:
        return f.readlines()


def load_parsed_logs():
    if os.path.exists(parsed_log_path):
        with open(parsed_log_path) as f:
            return set(json.load(f))
    return set()


def save_parsed_logs(parsed_logs):
    with open(parsed_log_path, "w") as f:
        json.dump(sorted(parsed_logs), f, indent=2)


def print_summary_table(logins):
    summary = generate_summary(logins)
    table = []
    for name, stats in summary.items():
        table.append(
            [
                name,
                stats["count"],
                (
                    stats["last_date"].strftime("%Y-%m-%d")  # type: ignore
                    if stats["last_date"]
                    else "N/A"
                ),
                str(stats["total_time"]),
            ]
        )

    print("\n📊 Session Summary:")
    print(
        tabulate(
            table,
            headers=["Player", "Sessions", "Last Session", "Total Playtime"],
            tablefmt="github",
        )
    )


def main(force=False, dry_run=False):
    if os.path.exists(output_path):
        with open(output_path) as f:
            logins.update(json.load(f))

    parsed_logs = set() if force else load_parsed_logs()
    new_logs = [
        f for f in glob(f"{log_dir}/*.log.gz") if os.path.basename(f) not in parsed_logs
    ]
    log_files = sorted(new_logs) + [f"{log_dir}/latest.log"]

    new_session_ids = []

    for log_file in log_files:
        mod_time = os.path.getmtime(log_file)
        log_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
        if DEBUG:
            print(f"[INFO] Parsing {log_file} with log date: {log_date}")
        lines = read_log_file(log_file, is_gz=log_file.endswith(".gz"))
        parse_lines(lines, log_date)

    # Collect new session IDs for preview
    for name, data in logins.items():
        for session in data.get("sessions", []):
            sid = session.get("session_id")
            if sid:
                new_session_ids.append(sid)

    if dry_run:
        dryrun(log_files, new_session_ids)

    with open(output_path, "w") as f:
        json.dump(logins, f, indent=2)

    # Also write player_logins.json for charting
    login_events = []
    for name, data in logins.items():
        for session in data.get("sessions", []):
            login_time = session.get("login_time")
            if login_time:
                login_events.append({"player": name, "login_time": login_time})

    login_output_path = f"{base_dir}/logs/player_logins.json"
    with open(login_output_path, "w") as f:
        json.dump(login_events, f, indent=2)

    if DEBUG:
        print(f"[SUCCESS] Session data written to {output_path}")

    if not force:
        parsed_logs.update(os.path.basename(f) for f in new_logs)
        save_parsed_logs(parsed_logs)

    print_summary_table(logins)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minecraft session tracker")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-parse all logs including previously parsed archives",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview sessions without writing output"
    )
    args = parser.parse_args()
    main(force=args.force, dry_run=args.dry_run)
