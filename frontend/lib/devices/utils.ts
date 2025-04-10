import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
import { Smartphone, Laptop, Tablet, Monitor, Watch, Tv, HardDrive, type LucideIcon } from "lucide-react"
import type { DeviceType } from "./types"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getDeviceIcon(type: DeviceType): LucideIcon {
  switch (type) {
    case "smartphone":
      return Smartphone
    case "laptop":
      return Laptop
    case "tablet":
      return Tablet
    case "desktop":
      return Monitor
    case "smartwatch":
      return Watch
    case "tv":
      return Tv
    default:
      return HardDrive
  }
}
