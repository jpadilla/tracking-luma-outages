import random

import requests
import structlog

from src.constants import TOWNS, USER_AGENTS

logger = structlog.get_logger()

s = requests.Session()
s.headers.update({"User-Agent": random.choice(USER_AGENTS)})


def get_clients_without_service():
    # Loading this page first sets Incapsula cookies into session
    # which seems to allow bypassing checks on further requests to AI.
    r = s.get("https://miluma.lumapr.com", allow_redirects=True)

    r = s.get(
        "https://api.miluma.lumapr.com/miluma-outage-api/outage/regionsWithoutService",
        allow_redirects=True,
    )

    try:
        response = r.json()
    except requests.exceptions.JSONDecodeError as exc:
        logger.error("error fetching clients without service", text=r.text)
        raise exc

    results = []

    for row in response.get("regions") or []:
        region = row.get("name")
        total_customers = row.get("totalClients")
        no_service_customers = row.get("totalClientsWithoutService")

        if region:
            results.append(
                {
                    "region": region.upper(),
                    "total_customers": total_customers,
                    "affected_customers": no_service_customers,
                }
            )

    return results


def get_outages():
    s = requests.Session()
    r = s.post(
        "https://api.miluma.lumapr.com/miluma-outage-api/outage/municipality/towns",
        json=TOWNS,
    )

    try:
        response = r.json()
    except requests.exceptions.JSONDecodeError as exc:
        logger.error("error fetching outages", text=r.text)
        raise exc

    results = []

    for region, outages in response.items():
        for outage in outages:
            area = outage.get("area")
            zone = outage.get("zone", "n/a")

            if not area:
                raise Exception(
                    f"invalid area({area}) or zone({zone}) for region({region})"
                )

            results.append({"region": region, "area": area, "zone": zone})

    return results
