import type { Device } from "@/lib/devices/types"
import { DeviceListItem } from "./device-list-item"

type DeviceListProps = {
  devices: Device[]
}

export function DeviceList({ devices }: DeviceListProps) {
  return (
    <div className="space-y-3">
      {devices.map((device) => (
        <DeviceListItem key={device.id} device={device} />
      ))}
    </div>
  )
}
