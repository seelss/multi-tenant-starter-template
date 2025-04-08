export type DeviceType = "smartphone" | "laptop" | "tablet" | "desktop" | "smartwatch" | "tv" | "other"

export type DeviceStatus = "online" | "offline" | "sleep" | "error"

export interface Device {
  id: string
  name: string
  type: DeviceType
  status: DeviceStatus
  ipAddress: string
  macAddress: string
  lastConnected: string // ISO date string
}
