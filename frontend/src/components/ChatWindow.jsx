import { useEffect, useRef } from "react"
import { ScrollArea } from "@/components/ui/scroll-area"
import MessageBubble from "./MessageBubble"
import EmptyState from "./EmptyState"

export default function ChatWindow({ messages, onExampleSelect }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center min-h-0">
        <EmptyState onSelect={onExampleSelect} />
      </div>
    )
  }

  return (
    <ScrollArea className="flex-1 min-h-0">
      <div className="max-w-3xl mx-auto px-4 py-6">
        <div className="flex flex-col gap-4">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          <div ref={bottomRef} />
        </div>
      </div>
    </ScrollArea>
  )
}
