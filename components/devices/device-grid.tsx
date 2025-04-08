import { DeviceCard } from "./device-card"
import type { Device } from "@/lib/devices/types"

type DeviceGridProps = {
  devices: Device[]
}

export function DeviceGrid({ devices }: DeviceGridProps) {
  if (!devices || devices.length === 0) {
    return <div className="text-center py-6">No devices found</div>
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {devices.map((device) => (
        <DeviceCard key={device.id} device={device} />
      ))}
    </div>
  )
}
