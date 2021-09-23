import datetime
import hashlib
import json
import os
from pathlib import Path

from sqlite_utils import Database

from .scrape import get_clients_without_service, get_outages

DATA_BASE_PATH = Path("./data")
DATASETTE_BASE_PATH = Path("./datasette")
CUSTOMERS_DATA_PATH = DATA_BASE_PATH / "customers"
OUTAGES_DATA_PATH = DATA_BASE_PATH / "outages"
RUNS_DATA_PATH = DATA_BASE_PATH / "runs"

# Date format used for data files
DATE_FORMAT_STR = "%Y%m%d%H"


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return super().default(o)


def calculate_checksum(results):
    data = json.dumps(results, cls=JSONEncoder, sort_keys=True)
    return hashlib.md5(data.encode("utf8")).hexdigest()


def recreate_database():
    db = Database(DATASETTE_BASE_PATH / "data.db", recreate=True)

    for entry in os.scandir(CUSTOMERS_DATA_PATH):
        if not entry.is_file():
            continue

        with open(entry.path) as file:
            data = json.load(file)
            created_at = datetime.datetime.strptime(
                entry.name.split(".json")[0], DATE_FORMAT_STR
            )
            db.table("customers").insert_all(
                [{**result, **{"created_at": created_at}} for result in data]
            )

    for entry in os.scandir(OUTAGES_DATA_PATH):
        if not entry.is_file():
            continue

        with open(entry.path) as file:
            data = json.load(file)
            created_at = datetime.datetime.strptime(
                entry.name.split(".json")[0], DATE_FORMAT_STR
            )
            db.table("outages").insert_all(
                [{**result, **{"created_at": created_at}} for result in data]
            )

    for entry in os.scandir(RUNS_DATA_PATH):
        if not entry.is_file():
            continue

        with open(entry.path) as file:
            data = json.load(file)
            created_at = datetime.datetime.strptime(
                entry.name.split(".json")[0], DATE_FORMAT_STR
            )
            db.table("runs").insert({**data, **{"created_at": created_at}})


def main():
    now = datetime.datetime.utcnow()
    filename = now.strftime(DATE_FORMAT_STR) + ".json"

    clients_without_service = get_clients_without_service()
    with open(CUSTOMERS_DATA_PATH / filename, "w") as f:
        json.dump(clients_without_service, f, cls=JSONEncoder)

    outages = get_outages()
    with open(OUTAGES_DATA_PATH / filename, "w") as f:
        json.dump(outages, f, cls=JSONEncoder)

    with open(RUNS_DATA_PATH / filename, "w") as f:
        json.dump(
            {
                "clients_without_service": calculate_checksum(clients_without_service),
                "outages": calculate_checksum(outages),
                "created_at": now,
            },
            f,
            cls=JSONEncoder,
        )

    recreate_database()


if __name__ == "__main__":
    main()
