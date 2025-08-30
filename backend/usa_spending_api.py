import requests
import datetime as dt

BASE = "https://api.usaspending.gov/api/v2/search/spending_by_category/recipient"
DOD_TOPTIER_CODE = "097"  # Department of Defense


def current_fy(today=None):
    today = today or dt.date.today()
    return today.year + 1 if today.month >= 10 else today.year


def fy_date_range(fy):
    """Return (start_date, end_date) in YYYY-MM-DD for a fiscal year."""
    start = dt.date(fy - 1, 10, 1)
    end = dt.date(fy, 9, 30)
    return {"start_date": start.isoformat(), "end_date": end.isoformat()}


def last_n_fy_ranges(n=5, today=None):
    """Return list of time_period dicts for last n FYs (incl. current)."""
    today = today or dt.date.today()
    cur = current_fy(today)
    return [fy_date_range(fy) for fy in range(cur - n + 1, cur + 1)]


def get_dod_spending_by_recipient(fy_count=5, limit=100):
    """
    Query USAspending API for total DoD obligations grouped by recipient.

    :param fy_count: number of fiscal years back (default 5)
    :param limit: number of recipients per page (default 100, max 100)
    :return: dict {recipient_name: aggregated_amount}
    """
    filters = {
        "time_period": last_n_fy_ranges(fy_count),
        "agencies": [
            {"type": "awarding", "tier": "toptier", "name": "Department of Defense"}
        ],
        "award_type_codes": ["A", "B", "C", "D"]  # contracts & IDVs
    }

    page = 1
    results = {}

    while True:
        payload = {
            "type": "award",
            "filters": filters,
            "limit": limit,
            "page": page,
            "subawards": False
        }
        r = requests.post(BASE, json=payload, timeout=60)
        if r.status_code != 200:
            print("Status:", r.status_code)
            print("Response:", r.text)
            break
        data = r.json()

        for row in data.get("results", []):
            name = row.get("recipient_name")
            amt = row.get("aggregated_amount", 0.0)
            if name:
                results[name] = results.get(name, 0.0) + amt

        meta = data.get("page_metadata") or {}
        if meta.get("hasNext"):
            page += 1
        else:
            break

    return results


if __name__ == "__main__":
    # spending = get_dod_spending_by_recipient(fy_count=5)
    # # print top 10 recipients by DoD obligations
    # for name, amt in sorted(spending.items(), key=lambda kv: kv[1], reverse=True)[:10]:
    #     print(f"{name:40} ${amt:,.2f}")
    url = "https://api.usaspending.gov/api/v2/search/spending_by_category/recipient"

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
            "limit": 100
        }
        r = requests.post(url, json=payload, timeout=60)
        if r.status_code != 200:
            print("Status:", r.status_code)
            print("Response:", r.text)
            break
        data = r.json()

        for row in data.get('results'):
            name = row['name']
            amount = int(row['amount'])
            if name in results:
                results[name] += amount
            else:
                results[name] = amount


        meta = data.get("page_metadata") or {}
        if meta.get("hasNext"):
            page += 1
        else:
            break
            
        