'''
Functions for determining company name from url or html for various url / job posting types

job posting types:
- workday: not all are of same type
- oraclecloud
- on simplify directly
- jobvite
- icims
- handshake jobs
- other / company local
- linkedin - don't use
- handshake don't use
'''
import json
import tldextract
import re
import requests
from bs4 import BeautifulSoup

job_app_provider = {
    "workday": r"\.myworkdayjobs\.com",
    "oracle": r"\.oraclecloud\.com",
    "jobvite": r"\.jobs\.jobvite\.com",
    "icims": r"\.icims\.com",
    "handshake": r"\.joinhandshake\.com",
    "linkedin": r"\.linkedin\.com"
}

def identify_url_type(url):
    """Return url type if matches known pattern, else None"""
    for name, pattern in job_app_provider.items():
        if re.search(pattern, url):
            return name
    return None


def extract_company_from_known_url(url, url_type):
    ext = tldextract.extract(url)

    if url_type == "workday":
        return ext.subdomain.split('.')[0]
    elif url_type == "oracle":
        # need to route to extracting from html
        return extract_company_from_html(url, url_type)
    elif url_type == "linkedin" or url_type == "handshake":
        return "unsupported"
    elif url_type == "jobvite":
        return extract_company_from_html(url, url_type)
    elif url_type == "icims":
        return extract_company_from_html(url, url_type)
    return None







def extract_html_basic(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    try:
        with open("test2.txt", 'x') as file:
            file.write(soup.prettify())
    except FileExistsError:
        # If file exists, overwrite it
        with open("test2.txt", 'w', encoding="utf-8") as file:
            file.write(soup.prettify())
    # print(soup)


def extract_company_from_html(url: str, url_type) -> str:
    """Return best guess company name from a webpage (title, meta, or footer ©)."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")


    # icims
    if url_type == "icims":
        print("here")
        # use hiringOrganization tag
        # return parse_hiring_org(soup)

    footer = soup.find("footer")


    # checks footer for copyright marker
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

    # checks meta_content for name
    if meta and meta.get("content"):
        return meta["content"].strip()

    # checks html title
    if soup.title and soup.title.string:
        return soup.title.string.strip()

    return None


if __name__ == "__main__":
    test_urls = [
        "https://www.lockheedmartin.com",
        "https://www.boeing.com",
        "https://www.northropgrumman.com",
        "https://nominal.io/",
        "https://careers-gdms.icims.com/jobs/67867/entry-level-software-engineer/job?utm_source=Simplify&ref=Simplify",
    ]

    # for url in test_urls:
    #     print(f"{url}: {extract_company_from_html(url)}")

    print(f"url=https://careers-gdms.icims.com/jobs/67867/entry-level-software-engineer/job?utm_source=Simplify&ref=Simplify, company_name = {extract_company_from_html("https://careers-gdms.icims.com/jobs/67867/entry-level-software-engineer/job?utm_source=Simplify&ref=Simplify", identify_url_type("https://careers-gdms.icims.com/jobs/67867/entry-level-software-engineer/job?utm_source=Simplify&ref=Simplify"))}")