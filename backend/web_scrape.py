import re
import requests
from bs4 import BeautifulSoup


def extract_company_from_html(url: str) -> str:
    """Return best guess company name from a webpage (title, meta, or footer ©)."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    footer = soup.find("footer")
    footer = soup.find("footer")
    if footer:
        footer_text = footer.get_text(strip=True)

        match = re.search(r"©\s*\d{4}\s*[^a-zA-Z0-9]*([a-zA-Z0-9].+)", footer_text, re.IGNORECASE)
        if not match:
            match = re.search(r"Copyright\s*\d{4}\s*[^a-zA-Z0-9]*([a-zA-Z0-9].+)", footer_text, re.IGNORECASE)

        if match:
            pre_regex_match = re.split(r"[^a-zA-Z0-9 ]", match.group(1).strip(), maxsplit=1)[0]
            cleaned_match = re.sub(r"[^a-zA-Z0-9 ]", "", pre_regex_match)
            return cleaned_match
    meta = soup.find("meta", property="og:site_name")
    if meta and meta.get("content"):
        return meta["content"].strip()

    if soup.title and soup.title.string:
        return soup.title.string.strip()

    return None


if __name__ == "__main__":
    test_urls = [
        "https://www.lockheedmartin.com",
        "https://www.northropgrumman.com/who-we-are/the-facts/solid-rocket-motors-propulsion/boosting-production?utm_source=googlesem&utm_medium=search&utm_campaign=space-crm&utm_audience=customer&utm_content=keywords&utm_format=cpc&code=OTH-13321&source=OTH-13321&gad_source=1&gad_campaignid=22847333944&gbraid=0AAAAADmzLUhAXOuBxE7HvZD0kiH2QOoi9&gclid=Cj0KCQjwwsrFBhD6ARIsAPnUFD3mXqZwbgbvU9X7K5u0rNf58daxtsXs4qr6tkFth31Ll7oZ6dSuD5IaAjkwEALw_wcB",
        "https://www.boeing.com",
        "https://www.northropgrumman.com",
        "https://nominal.io/",
        "https://careers-gdms.icims.com/jobs/67867/entry-level-software-engineer/job?utm_source=Simplify&ref=Simplify",
    ]

    for url in test_urls:
        print(f"{url}: {extract_company_from_html(url)}")
