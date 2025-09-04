// src/content.js
(function sendOnLoad() {
  const url = window.location.href
  chrome.runtime.sendMessage({ type: 'PAGE_LOADED', url })
})()

// Optional: also re-send if SPA routes change
const origPush = history.pushState
history.pushState = function (...args) {
  origPush.apply(this, args)
  chrome.runtime.sendMessage({ type: 'PAGE_LOADED', url: window.location.href })
}
window.addEventListener('popstate', () => {
  chrome.runtime.sendMessage({ type: 'PAGE_LOADED', url: window.location.href })
})
