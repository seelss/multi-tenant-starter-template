import { AppSidebar } from "@/components/app-sidebar"
import { DevicesContent } from "@/components/devices/DevicesContent"
import {
  SidebarInset,
  SidebarProvider,
} from "@/components/ui/sidebar"

export default function Page() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <DevicesContent />
      </SidebarInset>
    </SidebarProvider>
  )
}
