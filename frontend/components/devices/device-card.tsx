import { formatDistanceToNow } from "date-fns"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Battery, Globe, CheckCircle, MapPin, Settings, RefreshCw, Play } from "lucide-react"
import { getDeviceIcon } from "@/lib/devices/utils"
import type { Device } from "@/lib/devices/types"

type DeviceCardProps = {
  device: Device
}

export function DeviceCard({ device }: DeviceCardProps) {
  const DeviceIcon = getDeviceIcon(device.type)

  return (
    <Card className="w-full min-w-[340px] max-w-md mx-auto overflow-hidden border-2">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <div className="flex items-center space-x-2">
            <div className={`p-2 rounded-md ${device.status === "online" ? "bg-green-100 dark:bg-green-900" : "bg-gray-100 dark:bg-gray-900"}`}>
              <DeviceIcon className={`h-5 w-5 ${device.status === "online" ? "text-green-600 dark:text-green-400" : "text-gray-500 dark:text-gray-400"}`} />
            </div>
            <div>
              <h3 className="font-medium">{device.model}</h3>
              <p className="text-sm text-muted-foreground">
                {device.storage} - {device.color}
              </p>
            </div>
          </div>
          <Badge variant={device.status === "online" ? "default" : "outline"}>{device.status}</Badge>
        </div>
      </CardHeader>

      <CardContent className="p-6">
        <div className="flex flex-col gap-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1">
              <div className="text-xs text-muted-foreground">IMEI</div>
              <div className="font-medium">{device.imei}</div>
            </div>

            <div className="flex flex-col gap-1">
              <div className="text-xs text-muted-foreground">Serial Number</div>
              <div className="font-medium">{device.serialNumber}</div>
            </div>

            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-1">
                <Battery className="h-3.5 w-3.5 text-green-500" />
                <span className="text-xs text-muted-foreground">Battery Health</span>
              </div>
              <div className="font-medium">{device.batteryHealth}</div>
            </div>

            <div className="flex flex-col gap-1">
              <div className="text-xs text-muted-foreground">iOS Version</div>
              <div className="font-medium">{device.iosVersion}</div>
            </div>

            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-1">
                <CheckCircle className="h-3.5 w-3.5 text-green-500" />
                <span className="text-xs text-muted-foreground">Activation</span>
              </div>
              <div className="font-medium">
                {device.activationStatus === "Activated" ? (
                  <span className="text-green-500">Activated</span>
                ) : (
                  <span className="text-red-500">Not Activated</span>
                )}
              </div>
            </div>

            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-1">
                <MapPin className="h-3.5 w-3.5 text-blue-500" />
                <span className="text-xs text-muted-foreground">Find My</span>
              </div>
              <div className="font-medium">
                {device.findMyStatus === "on" ? (
                  <span className="text-green-500">On</span>
                ) : (
                  <span className="text-red-500">Off</span>
                )}
              </div>
            </div>

            <div className="flex flex-col gap-1 col-span-2">
              <div className="flex items-center gap-1">
                <Globe className="h-3.5 w-3.5 text-primary" />
                <span className="text-xs text-muted-foreground">Region</span>
              </div>
              <div className="font-medium">{device.region_info_human_readable}</div>
            </div>
          </div>
        </div>
      </CardContent>

      <CardFooter className="bg-slate-50 dark:bg-slate-900 p-4 flex flex-wrap gap-2 justify-center">
        <Button variant="outline" size="sm" className="flex items-center gap-1">
          <Settings className="h-4 w-4" />
          Actions
        </Button>
        <Button variant="outline" size="sm" className="flex items-center gap-1">
          <RefreshCw className="h-4 w-4" />
          Rescan
        </Button>
        <Button variant="outline" size="sm" className="flex items-center gap-1">
          <Play className="h-4 w-4" />
          Run Diag.
        </Button>
      </CardFooter>
    </Card>
  )
}
