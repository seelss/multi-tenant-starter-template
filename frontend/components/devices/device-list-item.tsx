import { formatDistanceToNow } from "date-fns"
import { Badge } from "@/components/ui/badge"
import { getDeviceIcon } from "@/lib/devices/utils"
import type { Device } from "@/lib/devices/types"

type DeviceListItemProps = {
  device: Device
}

export function DeviceListItem({ device }: DeviceListItemProps) {
  const DeviceIcon = getDeviceIcon(device.type)

  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 border rounded-lg">
      <div className="flex items-center space-x-4 mb-3 sm:mb-0">
        <div className={`p-2 rounded-md ${device.status === "online" ? "bg-green-100" : "bg-gray-100"}`}>
          <DeviceIcon className={`h-5 w-5 ${device.status === "online" ? "text-green-600" : "text-gray-500"}`} />
        </div>
        <div>
          <div className="flex items-center">
            <h3 className="font-medium mr-2">{device.name}</h3>
            <Badge variant={device.status === "online" ? "default" : "outline"} className="ml-2">
              {device.status}
            </Badge>
          </div>
          <p className="text-sm text-muted-foreground">{device.type}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-x-8 gap-y-1 text-sm sm:flex sm:items-center sm:space-x-8">
        <div>
          <span className="text-muted-foreground mr-2 sm:mr-1">IP:</span>
          <span>{device.ipAddress}</span>
        </div>
        <div>
          <span className="text-muted-foreground mr-2 sm:mr-1">MAC:</span>
          <span>{device.macAddress}</span>
        </div>
        <div className="col-span-2 mt-1 sm:mt-0 text-xs text-muted-foreground">
          Last connected {formatDistanceToNow(new Date(device.lastConnected))} ago
        </div>
      </div>
    </div>
  )
}
