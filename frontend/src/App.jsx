import { useState, useRef } from "react"
import Header from "./components/Header"
import ChatWindow from "./components/ChatWindow"
import QueryInput from "./components/QueryInput"
import { streamChat } from "./lib/api"

export default function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const sessionIdRef = useRef(null)

  function handleHome() {
    setMessages([])
    setLoading(false)
    sessionIdRef.current = null
  }

  function handleSubmit(question) {
    const userMsg = { id: Date.now(), role: "user", text: question }
    const placeholderId = Date.now() + 1
    const placeholder = {
      id: placeholderId,
      role: "assistant",
      text: "",
      sources: [],
      loading: true,
      status: null,
    }

    setMessages((prev) => [...prev, userMsg, placeholder])
    setLoading(true)

    streamChat(
      question,
      sessionIdRef.current,

      // onSessionId — store session ID for future messages
      (id) => {
        sessionIdRef.current = id
      },

      // onStatus — update the status line in the placeholder
      (msg) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === placeholderId ? { ...m, status: msg } : m
          )
        )
      },

      // onChunk — append token, clear status once answer starts flowing
      (chunk) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === placeholderId
              ? { ...m, text: m.text + chunk, loading: false, status: null }
              : m
          )
        )
      },

      // onDone — replace placeholder with final parsed answer + sources
      ({ answer, sources }) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === placeholderId
              ? { ...m, text: answer, sources, loading: false, status: null }
              : m
          )
        )
        setLoading(false)
      },

      // onError
      (err) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === placeholderId
              ? { ...m, text: `Something went wrong: ${err.message}`, sources: [], loading: false, status: null }
              : m
          )
        )
        setLoading(false)
      }
    )
  }

  return (
    <div className="flex flex-col h-[100dvh] bg-background">
      <Header onHome={handleHome} />
      <ChatWindow messages={messages} onExampleSelect={handleSubmit} />
      <QueryInput onSubmit={handleSubmit} disabled={loading} />
    </div>
  )
}
