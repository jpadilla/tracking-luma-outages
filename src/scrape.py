import requests

from src.constants import TOWNS


def get_clients_without_service():
    s = requests.Session()
    r = s.get(
        "https://api.miluma.lumapr.com/miluma-outage-api/outage/regionsWithoutService"
    )

    response = r.json()
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
    response = r.json()
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
