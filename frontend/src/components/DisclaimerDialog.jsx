import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { TriangleAlert } from "lucide-react"

export default function DisclaimerDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground text-xs gap-1.5">
          <TriangleAlert className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Disclaimer</span>
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Disclaimer</DialogTitle>
        </DialogHeader>
        <div className="space-y-3 text-sm text-muted-foreground leading-relaxed">
          <p>
            This tool is a personal project built to apply and learn about
            Retrieval-Augmented Generation (RAG). It is not a substitute for qualified Islamic scholarship.
          </p>
          <p>
            All answers are AI-generated summaries based on Q&amp;A content from{" "}
            <a
              href="https://islamqa.info"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary underline underline-offset-2"
            >
              IslamQA.info
            </a>
            . The tool may misrepresent, omit, or incorrectly attribute rulings.
          </p>
          <p>
            <span className="font-medium text-foreground">
              Always verify with a qualified Islamic scholar
            </span>{" "}
            before acting on any information provided here.
          </p>
          <p>
            I do not bear any responsibility for decisions made based on the
            output of this tool.
          </p>
        </div>
      </DialogContent>
    </Dialog>
  )
}
