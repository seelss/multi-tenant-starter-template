import { AppSidebar } from "@/components/app-sidebar"
import { DevicesPage } from "@/components/devices/devices-page"
import {
  SidebarInset,
  SidebarProvider,
} from "@/components/ui/sidebar"

export default function Page() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <DevicesPage />
      </SidebarInset>
    </SidebarProvider>
  )
}
