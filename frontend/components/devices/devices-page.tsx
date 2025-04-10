"use client"

import { useState } from "react"
import { DeviceGrid } from "./device-grid"
import { DeviceList } from "./device-list"
import { LayoutToggle } from "./layout-toggle"
import type { Device } from "@/lib/devices/types"

type DevicesPageProps = {
  devices: Device[]
}

export function DevicesPage({ devices }: DevicesPageProps) {
  const [layout, setLayout] = useState<"grid" | "list">("grid")

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Devices</h1>
          <p className="text-muted-foreground mt-1">Manage your connected devices</p>
        </div>
        <LayoutToggle layout={layout} setLayout={setLayout} />
      </div>

      {layout === "grid" ? <DeviceGrid devices={devices} /> : <DeviceList devices={devices} />}
    </div>
  )
}
