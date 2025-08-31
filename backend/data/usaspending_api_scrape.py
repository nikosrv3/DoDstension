import requests
import datetime as dt
import json

URL = "https://api.usaspending.gov/api/v2/search/spending_by_category/recipient"
DOD_TOPTIER_CODE = "097"  # Department of Defense


def get_dod_spending_by_recipient(limit=100):
    """
    Query USAspending API for total DoD obligations grouped by recipient.

    :param fy_count: number of fiscal years back (default 5)
    :param limit: number of recipients per page (default 100, max 100)
    :return: dict {recipient_name: aggregated_amount}
    """

    page = 1

    results = {}

    while True:
        payload = {
            "type": "award",
            "filters": {
                "time_period": [{"start_date": "2007-10-01", "end_date": "2025-09-30"}],
                "agencies": [
                    {"type": "awarding", "tier": "toptier", "name": "Department of Defense"}
                ],
                
                "award_type_codes": ["A","B","C","D"],
            },
            "page": page,
            "limit": limit
        }
        print(f"Loading page {page}...")
        r = requests.post(URL, json=payload, timeout=60)
        if r.status_code != 200:
            print("Status:", r.status_code)
            print("Response:", r.text)
            break
        data = r.json()

        for row in data.get('results'):
            name = row['name']
            amount = int(row['amount'])

            #Check common aliases

            if "LOCKHEED MARTIN" in name:
                name = "LOCKHEED MARTIN CORPORATION"
            elif "NORTHROP GRUMMAN" in name:
                name = "NORTHROP GRUMMAN"

            #Add to total awards

            if name in results:
                results[name]['total_awards'] += amount
            else:
                results[name] = {}
                results[name]['total_awards'] = amount


        meta = data.get("page_metadata") or {}
        if meta.get("hasNext"):
            page += 1
            if page > 200:
                break
        else:
            break

    return results


if __name__ == "__main__":

    result_dictionary = get_dod_spending_by_recipient()
    
    with open("company_data.json", "w") as f:
        json.dump(result_dictionary, f, indent=4)