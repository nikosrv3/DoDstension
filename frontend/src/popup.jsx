// src/popup.jsx
import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

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

function Popup() {
  const [tabUrl, setTabUrl] = useState('')
  const [data, setData] = useState(null)
  const [grade, setGrade] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const blurbs = {
    0: "No DoD funding!",
    1: "Very little DoD funding.",
    2: "Some DoD funding.",
    3: "A lot of DoD funding.",
    4: "An obscene amount of DoD funding."
  }

  useEffect(() => {
    async function init() {
      try {
        const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true })
        const url = activeTab?.url || ''
        console.log("Popup init: activeTab.url =", url)

        setTabUrl(url)

        if (url) {
          const normUrl = normalizeUrl(url)
          const key = `resp:${normUrl}`
          const cached = await chrome.storage.local.get([key])
          console.log("Popup init: checking storage with key =", key, "cached =", cached)
          console.log("Popup init: cached object =", JSON.stringify(cached, null, 2))
          
          if (cached[key]) {
            console.log("Popup init: setting data from cache =", cached[key])
            console.log("Popup init: cached object =", JSON.stringify(cached, null, 2))

            setData(cached[key])
          }
        }
      } catch (e) {
        setError(String(e))
      } finally {
        setLoading(false)
      }
    }
    init()

    // listen for updates from background
    const onMsg = (msg) => {
      console.log("Popup got message:", msg, "current tabUrl =", tabUrl)      
      if (msg?.type === 'PAGE_DATA_CACHED' && msg.url === tabUrl) {
        console.log("Popup got message:", msg, "current tabUrl =", tabUrl)      

        setData(msg.data)
        setError('')
      }
      if (msg?.type === 'PAGE_DATA_ERROR' && msg.url === tabUrl) {
        console.log("Popup got message:", msg, "current tabUrl =", tabUrl)      
        setError(msg.error || 'Unknown error')
      }
    }
    chrome.runtime.onMessage.addListener(onMsg)
    return () => chrome.runtime.onMessage.removeListener(onMsg)
  }, [tabUrl])

  return (
    <div style={{ padding: 16, width: 340 }}>
        <h3>{data?.company}</h3>
        {loading && <p>Loading…</p>}
        {!loading && error && <p style={{ color: 'crimson' }}>{error}</p>}
        {!loading && !error && (
            <>
            {/* Display n icons in a row, where n = data.grade */}
            {typeof data?.grade === 'number' && data.grade > 0 && (
                <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', margin: '8px 0' }}>
                {Array.from({ length: data.grade }).map((_, i) => (
                    <img
                    key={i}
                    src={chrome.runtime.getURL('icons/icon.svg')}
                    alt="icon"
                    style={{ width: 24, height: 24, marginRight: 4 }}
                    />
                ))}
                <p style={{color: "red"}}><b>${data?.total_awards.toLocaleString()}</b></p>
                </div>
            )}

            {typeof blurbs[data?.grade] === "string" && (
                <p><b>Grade {data?.grade}/4</b>: {blurbs[data?.grade]}</p>
            )}

            {data === null && (
                <p>No data available.</p>
            )}

            </>
        )}
        </div>
  )
}

createRoot(document.getElementById('root')).render(<Popup />)