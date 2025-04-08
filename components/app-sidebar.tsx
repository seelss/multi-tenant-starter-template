"use client"

import * as React from "react"
import Link from "next/link"
import { useParams, useRouter, usePathname } from "next/navigation"
import {
  ArrowUpCircleIcon,
  BarChartIcon,
  CameraIcon,
  ClipboardListIcon,
  DatabaseIcon,
  FileCodeIcon,
  FileIcon,
  FileTextIcon,
  FolderIcon,
  HelpCircleIcon,
  LayoutDashboardIcon,
  ListIcon,
  SearchIcon,
  SettingsIcon,
  UsersIcon,
} from "lucide-react"

import { NavDocuments } from "@/components/nav-documents"
import { NavMain } from "@/components/nav-main"
import { NavSecondary } from "@/components/nav-secondary"
import { NavUser } from "@/components/nav-user"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const params = useParams();
  const router = useRouter();
  const pathname = usePathname();
  
  // Extract teamId if present in route params
  const teamId = params?.teamId as string;
  const basePath = teamId ? `/dashboard/${teamId}` : '';
  
  // Build navigation data with dynamic paths
  const navMainItems = [
    {
      title: "Dashboard",
      url: teamId ? `/dashboard/${teamId}` : "/",
      icon: LayoutDashboardIcon,
    },
    {
      title: "Lifecycle",
      url: `${basePath}/lifecycle`,
      icon: ListIcon,
    },
    {
      title: "Analytics",
      url: `${basePath}/analytics`,
      icon: BarChartIcon,
    },
    {
      title: "Projects",
      url: `${basePath}/projects`,
      icon: FolderIcon,
    },
    {
      title: "Team",
      url: `${basePath}/team`,
      icon: UsersIcon,
    },
  ];
  
  const navSecondaryItems = [
    {
      title: "Settings",
      url: `${basePath}/settings`,
      icon: SettingsIcon,
    },
    {
      title: "Get Help",
      url: `${basePath}/help`,
      icon: HelpCircleIcon,
    },
    {
      title: "Search",
      url: `${basePath}/search`,
      icon: SearchIcon,
    },
  ];
  
  const documentItems = [
    {
      name: "Data Library",
      url: `${basePath}/data`,
      icon: DatabaseIcon,
    },
    {
      name: "Reports",
      url: `${basePath}/reports`,
      icon: ClipboardListIcon,
    },
    {
      name: "Word Assistant",
      url: `${basePath}/assistant`,
      icon: FileIcon,
    },
  ];

  const userData = {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  };

  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <Link href={teamId ? `/dashboard/${teamId}` : "/"}>
                <ArrowUpCircleIcon className="h-5 w-5" />
                <span className="text-base font-semibold">Acme Inc.</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={navMainItems} />
        <NavDocuments items={documentItems} />
        <NavSecondary items={navSecondaryItems} className="mt-auto" />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={userData} />
      </SidebarFooter>
    </Sidebar>
  )
}
