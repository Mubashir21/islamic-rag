import ReactMarkdown from "react-markdown"
import { Card } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import SourceList from "./SourceList"
import CopyButton from "./CopyButton"

function UserBubble({ text }) {
  return (
    <div className="flex justify-end">
      <div className="bg-primary text-primary-foreground rounded-2xl rounded-br-sm px-4 py-2.5 max-w-[75%] text-sm">
        {text}
      </div>
    </div>
  )
}

function StatusIndicator({ status }) {
  return (
    <div className="flex justify-start">
      <Card className="w-[85%] px-4 py-3">
        <div className="flex items-center gap-2">
          <span className="flex gap-0.5">
            <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce [animation-delay:0ms]" />
            <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce [animation-delay:150ms]" />
            <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce [animation-delay:300ms]" />
          </span>
          <span className="text-sm text-muted-foreground">{status}</span>
        </div>
      </Card>
    </div>
  )
}

function AssistantBubble({ text, sources, loading, status }) {
  if (loading) {
    if (status) return <StatusIndicator status={status} />
    return (
      <div className="flex justify-start">
        <Card className="w-[85%] px-4 py-3 space-y-2">
          <Skeleton className="h-3 w-full" />
          <Skeleton className="h-3 w-[90%]" />
          <Skeleton className="h-3 w-[75%]" />
        </Card>
      </div>
    )
  }

  return (
    <div className="flex justify-start">
      <Card className="max-w-[85%] px-4 py-3">
        <div className="prose prose-sm prose-neutral dark:prose-invert max-w-none text-foreground
          [&_h3]:text-sm [&_h3]:font-semibold [&_h3]:mt-3 [&_h3]:mb-1
          [&_p]:text-sm [&_p]:leading-relaxed [&_p]:mb-2
          [&_ul]:text-sm [&_ul]:pl-4 [&_ul]:mb-2
          [&_li]:mb-0.5">
          <ReactMarkdown>{text}</ReactMarkdown>
        </div>
        <SourceList sources={sources} />
        <div className="mt-2 flex justify-end">
          <CopyButton text={text} />
        </div>
      </Card>
    </div>
  )
}

export default function MessageBubble({ message }) {
  if (message.role === "user") return <UserBubble text={message.text} />
  return (
    <AssistantBubble
      text={message.text}
      sources={message.sources}
      loading={message.loading}
      status={message.status}
    />
  )
}
