export type DeviceType = "smartphone" | "laptop" | "tablet" | "desktop" | "smartwatch" | "tv" | "other"

export type DeviceStatus = "online" | "offline" | "sleep" | "error"

export interface Device {
  id: string
  type: DeviceType
  status: DeviceStatus
  lastConnected: string // ISO date string
  model: string
  storage: string
  color: string
  imei: string
  serialNumber: string
  batteryHealth: string
  iosVersion: string
  activationStatus: "Activated" | "Not Activated"
  findMyStatus: "On" | "Off"
  region: string
}
