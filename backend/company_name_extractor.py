import tldextract


def extract_company_name(url: str):
    ext = tldextract.extract(url)



def extract_from_url(url: str):
    if "workday" in url:
        url_components = tldextract.extract(url)
        return url_components.subdomain.split('.')[0]
    url_components = tldextract.extract(url)
    return url_components.domain



if __name__ == "__main__":
    # test cases
    test_urls = [
        "https://careers.lockheedmartin.com/en-us",
        "https://jobs.northropgrumman.com",
        "https://boeing.com/careers",
        "https://raytheon.jobs",
        "https://adobe.wd5.myworkdayjobs.com/external_experienced/login/ok",
        "https://cvshealth.wd1.myworkdayjobs.com/en-US/cvs_health_careers/job/CT---Hartford/Associate-Software-Development-Engineer_R0699201-1?utm_source=Simplify&ref=Simplify",
        "https://careers-gdms.icims.com/jobs/67867/entry-level-software-engineer/job?utm_source=Simplify&ref=Simplify",
    ]

    for url in test_urls:
        company = extract_from_url(url)
        print(f"URL: {url} → Company: {company}")