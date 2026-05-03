import { useState } from "react"
import Header from "./components/Header"
import ChatWindow from "./components/ChatWindow"
import QueryInput from "./components/QueryInput"
import { streamQuery } from "./lib/api"

export default function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  function handleSubmit(question) {
    const userMsg = { id: Date.now(), role: "user", text: question }
    const placeholderId = Date.now() + 1
    const placeholder = { id: placeholderId, role: "assistant", text: "", sources: [], loading: true }

    setMessages((prev) => [...prev, userMsg, placeholder])
    setLoading(true)

    streamQuery(
      question,
      (chunk) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === placeholderId
              ? { ...m, text: m.text + chunk, loading: false }
              : m
          )
        )
      },
      ({ answer, sources }) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === placeholderId
              ? { ...m, text: answer, sources, loading: false }
              : m
          )
        )
        setLoading(false)
      },
      (err) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === placeholderId
              ? { ...m, text: `Something went wrong: ${err.message}`, sources: [], loading: false }
              : m
          )
        )
        setLoading(false)
      }
    )
  }

  return (
    <div className="flex flex-col h-screen bg-background">
      <Header />
      <ChatWindow messages={messages} onExampleSelect={handleSubmit} />
      <QueryInput onSubmit={handleSubmit} disabled={loading} />
    </div>
  )
}
