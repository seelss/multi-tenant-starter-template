"use client"

import * as React from "react"
import {
  AudioWaveform,
  BookOpen,
  Bot,
  Command,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,
  Settings2,
  SquareTerminal,
  Home,
  Smartphone,
  type LucideIcon,
} from "lucide-react"
import { useParams, useRouter } from "next/navigation"

import { NavMain } from "@/components/nav-main"
import { NavProjects } from "@/components/nav-projects"
import { NavUser } from "@/components/nav-user"
import { TeamSwitcher } from "@/components/team-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"

type NavItemBase = {
  title: string;
  type: string;
}

type NavItemFull = NavItemBase & {
  type: "item";
  url: string;
  icon?: LucideIcon;
  isActive?: boolean;
}

type NavItemLabel = NavItemBase & {
  type: "label";
}

type NavItem = NavItemFull | NavItemLabel;

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const params = useParams()
  const router = useRouter()
  const teamId = params?.teamId as string

  // Navigation items following the layout.tsxold structure
  const navigationItems: NavItem[] = [
    {
      title: "Overview",
      url: "/",
      icon: Home,
      type: "item",
    },
    {
      type: 'label',
      title: 'Platform',
    },
    {
      title: "Playground",
      url: "/playground",
      icon: SquareTerminal,
      type: "item",
      isActive: true,
    },
    {
      title: "Models",
      url: "/models",
      icon: Bot,
      type: "item",
    },
    {
      title: "Devices",
      url: "/devices",
      icon: Smartphone,
      type: "item",
    },
    {
      type: 'label',
      title: 'Resources',
    },
    {
      title: "Documentation",
      url: "/documentation",
      icon: BookOpen,
      type: "item",
    },
    {
      type: 'label',
      title: 'Settings',
    },
    {
      title: "Settings",
      url: "/settings",
      icon: Settings2,
      type: "item",
    },
  ]

  // Sample data for other sidebar elements
  const data = {
    user: {
      name: "shadcn",
      email: "m@example.com",
      avatar: "/avatars/shadcn.jpg",
    },
    teams: [
      {
        name: "Acme Inc",
        logo: GalleryVerticalEnd,
        plan: "Enterprise",
      },
      {
        name: "Acme Corp.",
        logo: AudioWaveform,
        plan: "Startup",
      },
      {
        name: "Evil Corp.",
        logo: Command,
        plan: "Free",
      },
    ],
    projects: [
      {
        name: "Design Engineering",
        url: "/projects/design",
        icon: Frame,
      },
      {
        name: "Sales & Marketing",
        url: "/projects/sales",
        icon: PieChart,
      },
      {
        name: "Travel",
        url: "/projects/travel",
        icon: Map,
      },
    ],
  }

  const handleNavigation = (url: string) => {
    if (teamId) {
      router.push(`/dashboard/${teamId}${url}`)
    } else {
      router.push(url)
    }
  }

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain 
          items={navigationItems} 
          basePath={teamId ? `/dashboard/${teamId}` : ""} 
          onNavigate={handleNavigation}
        />
        <NavProjects projects={data.projects} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
