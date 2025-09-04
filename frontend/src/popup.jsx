// src/popup.jsx
import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

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
        setTabUrl(url)

        if (url) {
          const key = `resp:${url}`
          const cached = await chrome.storage.local.get([key])
          if (cached[key]) setData(cached[key])
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
      if (msg?.type === 'PAGE_DATA_CACHED' && msg.url === tabUrl) {
        setData(msg.data)
        setError('')
      }
      if (msg?.type === 'PAGE_DATA_ERROR' && msg.url === tabUrl) {
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