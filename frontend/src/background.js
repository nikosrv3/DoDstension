function normalizeUrl(u) {
  try {
    const obj = new URL(u)
    obj.search = ""   // strip query params
    obj.hash = ""     // strip fragment
    return obj.toString()
  } catch {
    return u
  }
}



chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed')
})

const API_BASE = 'http://localhost:8000'
const GRADE_ENDPOINT = '/grades'

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg?.type !== 'PAGE_COMPANY_JSONLD' || !msg.url) return

  const payload = {
    url: msg.url,
    companyName: msg.companyName || null
  }

  console.log("Forwarding payload to backend", payload)

  fetch(`${API_BASE}${GRADE_ENDPOINT}`, {
    method: 'POST',
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(async (r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`)
      const data = await r.json()


      const normUrl = normalizeUrl(msg.url)
      const key = `resp:${normUrl}`

      const cached = { [key]: data, last: { url: normUrl, ts: Date.now() } }
      chrome.storage.local.set(cached, () => {
        chrome.runtime.sendMessage({
          type: 'PAGE_DATA_CACHED',
          url: normUrl,
          data
        })
      })
      // const key = `resp:${msg.url}`

      // const cached = { [key]: data, last: { url: msg.url, ts: Date.now() } }
      console.log("BG storing under key:", key, "with data:", data)

      chrome.storage.local.set(cached, () => {
        // notify any open UIs (popup/options) that new data is available
        chrome.runtime.sendMessage({  type: 'PAGE_DATA_CACHED', url: msg.url, data })
      })
    })
    .catch((err) => {
      console.error('Fetch failed:', err)
      chrome.runtime.sendMessage({ type: 'PAGE_DATA_ERROR', url: msg.url, error: String(err) })
    })

  return true
})
