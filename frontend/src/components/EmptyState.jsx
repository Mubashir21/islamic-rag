import { useState, useEffect } from "react"
import DaleelIcon from "./DaleelIcon"

const ALL_QUESTIONS = [
  "What is the ruling on praying with shoes on?",
  "Is it permissible to take out a mortgage to buy a house?",
  "What are the conditions for a valid Islamic marriage contract?",
  "What is the Islamic ruling on working in a bank?",
  "Is music permissible in Islam?",
  "What breaks the fast during Ramadan?",
  "What is the ruling on combining prayers while travelling?",
  "Is it permissible to have a dog as a pet?",
  "What is the ruling on celebrating birthdays?",
]

const SETS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
const STAGGER = ["delay-0", "delay-100", "delay-200"]

export default function EmptyState({ onSelect }) {
  const [setIndex, setSetIndex] = useState(0)
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const id = setInterval(() => {
      setVisible(false)
      setTimeout(() => {
        setSetIndex((prev) => (prev + 1) % SETS.length)
        setVisible(true)
      }, 400)
    }, 4000)
    return () => clearInterval(id)
  }, [])

  const questions = SETS[setIndex].map((i) => ALL_QUESTIONS[i])

  return (
    <div className="flex flex-col items-center justify-center h-full gap-6 px-4 text-center">
      <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 fill-mode-both">
        <div className="flex items-center justify-center mx-auto mb-3">
          <DaleelIcon size={52} className="text-primary" />
        </div>
        <h2 className="text-base font-semibold text-foreground">What's your question?</h2>
        <p className="text-sm text-muted-foreground mt-1">
          This tool searches thousands of IslamQA Q&As and generates a grounded answer with sources.
        </p>
      </div>

      <div className="flex flex-col gap-2 w-full max-w-sm h-[200px] overflow-hidden">
        {questions.map((q, i) => (
          <button
            key={q}
            onClick={() => onSelect(q)}
            className={[
              "text-left text-sm px-4 py-2.5 rounded-xl border border-border bg-card",
              "hover:bg-accent hover:border-primary/30 transition-colors text-muted-foreground hover:text-foreground",
              visible
                ? `animate-in fade-in slide-in-from-bottom-2 duration-500 fill-mode-both ${STAGGER[i]}`
                : `animate-out fade-out slide-out-to-top-2 duration-300 fill-mode-forwards ${STAGGER[i]}`,
            ].join(" ")}
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  )
}
