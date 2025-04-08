import { AppSidebar } from "@/components/app-sidebar"
import { DevicesPage } from "@/components/devices/devices-page"
import { getDevices } from "@/lib/devices/data"
import {
  SidebarInset,
  SidebarProvider,
} from "@/components/ui/sidebar"

export default function Page() {
  const devices = getDevices()
  
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <DevicesPage devices={devices} />
      </SidebarInset>
    </SidebarProvider>
  )
}
