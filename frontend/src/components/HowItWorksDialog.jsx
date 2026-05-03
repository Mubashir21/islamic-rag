import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Info } from "lucide-react"

const steps = [
  {
    title: "Retrieval",
    body: "Your question is converted into a vector embedding and matched against ~39,000 chunks derived from ~15,000 IslamQA questions and answers, stored in a Pinecone vector database using a combination of semantic and keyword search.",
  },
  {
    title: "Reranking",
    body: "The top 40 candidate chunks are reranked by Cohere's reranking model to surface the 5 most relevant passages.",
  },
  {
    title: "Generation",
    body: "The retrieved passages are passed to a language model along with strict instructions to only use the provided sources — no outside knowledge. The answer is streamed back in real time with inline citations.",
  },
]

export default function HowItWorksDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground text-xs gap-1.5">
          <Info className="w-3.5 h-3.5" />
          How it works
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>How it works</DialogTitle>
        </DialogHeader>
        <div className="space-y-4 text-sm text-muted-foreground leading-relaxed">
          <div className="space-y-3">
            {steps.map((step, i) => (
              <div key={step.title} className="flex gap-3">
                <div className="w-5 h-5 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs font-semibold shrink-0 mt-0.5">
                  {i + 1}
                </div>
                <div>
                  <p className="font-medium text-foreground">{step.title}</p>
                  <p className="mt-0.5">{step.body}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="border-t border-border pt-3 space-y-1.5">
            <p className="font-medium text-foreground">Things to know</p>
            <ul className="space-y-1 list-disc list-inside">
              <li>Messages are not connected — each question is answered independently, there is no conversation memory.</li>
              <li>Cohere's free tier is used for reranking, which has a rate limit of 10 requests per minute.</li>
              <li>Source content is from IslamQA. All credit for the underlying knowledge goes to them.</li>
            </ul>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
