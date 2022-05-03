import locale

import requests
from parsel import Selector

from src.constants import TOWNS

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


def get_clients_without_service():
    s = requests.Session()
    r = s.get("https://webapps.prepa.com/pls/web/f?p=141:1:0")

    selector = Selector(text=r.text)
    rows = selector.css("table.uReport").css("tbody > tr")

    results = []

    for i, row in enumerate(rows):
        if i + 1 == len(rows):
            # Skipping last row since it's just aggregation
            continue

        # Skipping last column since it's just aggregation
        region = row.css('td[headers="REGION"]::text').get()
        total_customers = row.css('td[headers="TCUSTOMERS"]::text').get()
        no_service_customers = row.css('td[headers="NOSERVICE"]::text').get()

        if region:
            results.append(
                {
                    "region": region,
                    "total_customers": locale.atoi(total_customers),
                    "affected_customers": locale.atoi(no_service_customers),
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
            zone = outage.get("zone")
            
            if not area or not zone:
                raise Exception(f"invalid area({area}) or zone({zone}) for region({region})")
            
            results.append(
                {"region": region, "area": area, "zone": zone}
            )

    return results
