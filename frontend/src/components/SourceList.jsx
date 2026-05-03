import { Badge } from "@/components/ui/badge"
import { ExternalLink } from "lucide-react"

export default function SourceList({ sources }) {
  if (!sources || sources.length === 0) return null

  return (
    <div className="mt-3 pt-3 border-t border-border">
      <p className="text-xs text-muted-foreground mb-2 font-medium">Sources</p>
      <div className="flex flex-col gap-1.5">
        {sources.map((s) => (
          <a
            key={s.number}
            href={s.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 group w-fit max-w-full"
          >
            <Badge variant="secondary" className="shrink-0 text-primary">
              {s.number}
            </Badge>
            <span className="text-xs text-muted-foreground group-hover:text-primary truncate transition-colors">
              {s.url.replace(/^https?:\/\//, "")}
            </span>
            <ExternalLink className="w-3 h-3 text-muted-foreground group-hover:text-primary shrink-0 transition-colors" />
          </a>
        ))}
      </div>
    </div>
  )
}
