chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed')
})

const API_BASE = 'http://localhost:8000'
const GET_GRADE_ENDPOINT = '/get_grade'

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg?.type !== 'PAGE_LOADED' || !msg.url) return

  const url = msg.url
  const query = `${API_BASE}${GET_GRADE_ENDPOINT}?url=${encodeURIComponent(url)}`

  fetch(query, { method: 'GET' })
    .then(async (r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`)
      const data = await r.json()
      const key = `resp:${url}`
      const payload = { [key]: data, last: { url, ts: Date.now() } }
      chrome.storage.local.set(payload, () => {
        // notify any open UIs (popup/options) that new data is available
        chrome.runtime.sendMessage({ type: 'PAGE_DATA_CACHED', url, data })
      })
    })
    .catch((err) => {
      console.error('Fetch failed:', err)
      chrome.runtime.sendMessage({ type: 'PAGE_DATA_ERROR', url, error: String(err) })
    })

  // MV3 listeners must return true if they respond async — we’re not using sendResponse here.
})
