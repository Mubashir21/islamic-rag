const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

export function parseSources(text) {
  const parts = text.split(/###\s*Sources/i)
  const answer = parts[0].trim()
  const sources = []

  if (parts[1]) {
    const lines = parts[1].trim().split("\n")
    for (const line of lines) {
      const match = line.match(/\[Source\s*(\d+)\]\s*(https?:\/\/\S+)/i)
      if (match) {
        sources.push({ number: parseInt(match[1]), url: match[2].trim() })
      }
    }
  }

  return { answer, sources }
}

export async function streamQuery(question, onChunk, onDone, onError) {
  let res

  try {
    res = await fetch(`${API_BASE}/query/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: question }),
    })
  } catch (err) {
    onError(err)
    return
  }

  if (!res.ok) {
    onError(new Error(`Server error: ${res.status}`))
    return
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let accumulated = ""
  let buffer = ""

  try {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split("\n")
      buffer = lines.pop()

      for (const line of lines) {
        if (line.startsWith("event: done")) continue
        if (line.startsWith("data: ")) {
          const raw = line.slice(6)
          if (raw === "[DONE]") {
            onDone(parseSources(accumulated))
            return
          }
          const text = JSON.parse(raw)
          accumulated += text
          onChunk(text)
        }
      }
    }
  } catch (err) {
    onError(err)
    return
  }

  onDone(parseSources(accumulated))
}
