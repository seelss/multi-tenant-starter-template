"use client"

import { useState } from "react"
import { DeviceGrid } from "./device-grid"
import { DeviceList } from "./device-list"
import { LayoutToggle } from "./layout-toggle"
import { useDevices } from "@/lib/devices/context"
import { Button } from "@/components/ui/button"
import { RefreshCw } from "lucide-react"

export function DevicesPage() {
  const { devices, isLoading, isConnected, refreshDevices } = useDevices();
  const [layout, setLayout] = useState<"grid" | "list">("grid")

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Devices</h1>
          <p className="text-muted-foreground mt-1">
            {isConnected 
              ? `${devices.length} connected devices` 
              : "Connecting to device service..."}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button 
            variant="outline" 
            size="icon"
            onClick={refreshDevices}
            disabled={isLoading}
          >
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
          <LayoutToggle layout={layout} setLayout={setLayout} />
        </div>
      </div>

      {layout === "grid" ? <DeviceGrid devices={devices} /> : <DeviceList devices={devices} />}
    </div>
  )
}
