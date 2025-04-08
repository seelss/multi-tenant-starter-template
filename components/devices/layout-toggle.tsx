"use client"

import { LayoutGrid, List } from "lucide-react"
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"

type LayoutToggleProps = {
  layout: "grid" | "list"
  setLayout: (layout: "grid" | "list") => void
}

export function LayoutToggle({ layout, setLayout }: LayoutToggleProps) {
  return (
    <ToggleGroup type="single" value={layout} onValueChange={(value) => value && setLayout(value as "grid" | "list")}>
      <ToggleGroupItem value="grid" aria-label="Grid view">
        <LayoutGrid className="h-4 w-4" />
      </ToggleGroupItem>
      <ToggleGroupItem value="list" aria-label="List view">
        <List className="h-4 w-4" />
      </ToggleGroupItem>
    </ToggleGroup>
  )
}
