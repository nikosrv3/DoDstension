// src/content.js
// recursive json search for company name
function findHiringOrg(obj) {
  if (!obj || typeof obj !== "object") return null;

  if (obj.hiringOrganization?.name) {
    return obj.hiringOrganization.name;
  }

  if (Array.isArray(obj)) {
    for (const entry of obj) {
      const found = findHiringOrg(entry);
      if (found) return found;
    }
  }

  for (const key in obj) {
    const val = obj[key];
    if (typeof val === "object") {
      const found = findHiringOrg(val);
      if (found) return found;
    }
  }

  return null;
}

(function sendOnLoad() {
  const scripts = document.querySelectorAll('script[type="application/ld+json"]');
  let companyName = null;

  scripts.forEach(script => {
    try {
      const data = JSON.parse(script.textContent.trim());
      const org = findHiringOrg(data);
      if (org) {
        companyName = org;
      }
    } catch (e) {
      // ignore bad JSON
    }
  });

  if (companyName) {
    console.log("Found JSON-LD hiringOrganization:", companyName);
    chrome.runtime.sendMessage({
      type: "PAGE_COMPANY_JSONLD",
      url: window.location.href,
      companyName
    });
    chrome.runtime.sendMessage({
      type: "PAGE_COMPANY_JSONLD",
      url: window.location.href,
      companyName
    });
  }
})();



