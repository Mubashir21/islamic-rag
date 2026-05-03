const EXAMPLES = [
  "What is the ruling on praying with shoes on?",
  "Is it permissible to take out a mortgage to buy a house?",
  "What are the conditions for a valid Islamic marriage contract?",
]

export default function EmptyState({ onSelect }) {
  return (
    <div className="flex flex-col items-center justify-center h-full gap-6 px-4 text-center">
      <div>
        <div className="w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-3">
          <span className="text-primary text-2xl">ق</span>
        </div>
        <h2 className="text-base font-semibold text-foreground">Ask an Islamic question</h2>
        <p className="text-sm text-muted-foreground mt-1">
          Answers are retrieved from IslamQA and grounded in cited sources.
        </p>
      </div>
      <div className="flex flex-col gap-2 w-full max-w-sm">
        {EXAMPLES.map((q) => (
          <button
            key={q}
            onClick={() => onSelect(q)}
            className="text-left text-sm px-4 py-2.5 rounded-xl border border-border bg-card hover:bg-accent hover:border-primary/30 transition-colors text-muted-foreground hover:text-foreground"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  )
}
