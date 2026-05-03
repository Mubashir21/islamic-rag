export default function Header() {
  return (
    <header className="border-b border-border bg-card px-6 py-4 shrink-0">
      <div className="max-w-3xl mx-auto flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0">
          <span className="text-primary-foreground text-sm font-semibold">ق</span>
        </div>
        <div>
          <h1 className="text-base font-semibold text-foreground leading-tight">Islamic Q&A</h1>
          <p className="text-xs text-muted-foreground">Answers sourced from IslamQA</p>
        </div>
      </div>
    </header>
  )
}
