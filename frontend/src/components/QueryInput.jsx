import { useState } from "react"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { ArrowUp } from "lucide-react"

export default function QueryInput({ onSubmit, disabled }) {
  const [value, setValue] = useState("")

  function handleSubmit() {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSubmit(trimmed)
    setValue("")
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="border-t border-border bg-card px-4 py-3 shrink-0">
      <div className="max-w-3xl mx-auto flex items-end gap-2">
        <Textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask an Islamic question…"
          disabled={disabled}
          rows={1}
          className="resize-none min-h-[40px] max-h-[120px] overflow-y-auto flex-1 text-base sm:text-sm"
        />
        <Button
          onClick={handleSubmit}
          disabled={!value.trim() || disabled}
          size="icon"
          className="shrink-0 h-10 w-10"
        >
          <ArrowUp className="w-4 h-4" />
        </Button>
      </div>
      <p className="text-center text-xs text-muted-foreground mt-2">
        Answers are AI-generated summaries of IslamQA Q&As. Always verify with a qualified scholar.
      </p>
    </div>
  )
}
