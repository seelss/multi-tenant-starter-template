"use client"

import { AppSidebar } from "@/components/app-sidebar"
import { DevicesPage } from "@/components/devices/devices-page"
import { DeviceProvider } from "@/lib/devices/context"
import {
  SidebarInset,
  SidebarProvider,
} from "@/components/ui/sidebar"

export default function Page() {
  return (
    <DeviceProvider>
      <SidebarProvider>
        <AppSidebar />
        <SidebarInset>
          <DevicesPage />
        </SidebarInset>
      </SidebarProvider>
    </DeviceProvider>
  )
}
