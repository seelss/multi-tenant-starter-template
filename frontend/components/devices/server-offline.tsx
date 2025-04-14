import { Button } from "@/components/ui/button"
import { WifiOff, RefreshCw } from "lucide-react"

interface ServerOfflineProps {
  retry: () => void
  isRetrying?: boolean
}

export function ServerOffline({ retry, isRetrying = false }: ServerOfflineProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 rounded-lg border border-dashed border-muted-foreground/50 bg-muted/10 text-center h-[60vh]">
      <WifiOff className="h-12 w-12 text-muted-foreground mb-4" />
      <h2 className="text-2xl font-semibold mb-2">Server Connection Lost</h2>
      <p className="text-muted-foreground max-w-md mb-6">
        We can't connect to the device management server right now. Is the program running on this machine?
      </p>
      <Button 
        onClick={retry} 
        disabled={isRetrying}
        className="gap-2"
      >
        <RefreshCw className={`h-4 w-4 ${isRetrying ? 'animate-spin' : ''}`} />
        {isRetrying ? "Reconnecting..." : "Try Again"}
      </Button>
    </div>
  )
} 