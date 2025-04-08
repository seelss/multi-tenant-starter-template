import { formatDistanceToNow } from "date-fns"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { getDeviceIcon } from "@/lib/devices/utils"
import type { Device } from "@/lib/devices/types"

type DeviceCardProps = {
  device: Device
}

export function DeviceCard({ device }: DeviceCardProps) {
  const DeviceIcon = getDeviceIcon(device.type)

  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <div className="flex items-center space-x-2">
            <div className={`p-2 rounded-md ${device.status === "online" ? "bg-green-100" : "bg-gray-100"}`}>
              <DeviceIcon className={`h-5 w-5 ${device.status === "online" ? "text-green-600" : "text-gray-500"}`} />
            </div>
            <div>
              <h3 className="font-medium">{device.name}</h3>
              <p className="text-sm text-muted-foreground">{device.type}</p>
            </div>
          </div>
          <Badge variant={device.status === "online" ? "default" : "outline"}>{device.status}</Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-sm">
          <div className="grid grid-cols-2 gap-2">
            <div className="text-muted-foreground">IP Address</div>
            <div className="text-right">{device.ipAddress}</div>
            <div className="text-muted-foreground">MAC Address</div>
            <div className="text-right">{device.macAddress}</div>
          </div>
        </div>
      </CardContent>
      <CardFooter className="text-xs text-muted-foreground border-t pt-3">
        Last connected {formatDistanceToNow(new Date(device.lastConnected))} ago
      </CardFooter>
    </Card>
  )
}
