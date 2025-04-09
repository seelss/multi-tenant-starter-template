"use client"

import { type LucideIcon } from "lucide-react"
import { useRouter } from "next/navigation"

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar"
import { ChevronRightIcon } from "@radix-ui/react-icons"

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

export function NavMain({
  items,
  basePath = "",
  onNavigate,
}: {
  items: NavItem[];
  basePath?: string;
  onNavigate?: (url: string) => void;
}) {
  const router = useRouter()

  const handleNavigation = (url: string) => {
    if (onNavigate) {
      onNavigate(url)
    } else {
      router.push(basePath + url)
    }
  }

  return (
    <SidebarGroup>
      <SidebarMenu>
        {items.map((item, index) => {
          if (item.type === "label") {
            return (
              <SidebarGroupLabel key={`label-${index}`}>
                {item.title}
              </SidebarGroupLabel>
            )
          }

          if (item.type === "item") {
            return (
              <SidebarMenuItem key={`item-${item.title}`}>
                <SidebarMenuButton 
                  tooltip={item.title} 
                  onClick={() => handleNavigation(item.url)}
                >
                  {item.icon && <item.icon />}
                  <span>{item.title}</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            )
          }

          return null
        })}
      </SidebarMenu>
    </SidebarGroup>
  )
}
