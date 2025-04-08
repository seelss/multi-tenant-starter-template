import type { Device } from "./types"

export function getDevices(): Device[] {
  return [
    {
      id: "1",
      name: "iPhone 13 Pro",
      type: "smartphone",
      status: "online",
      ipAddress: "192.168.1.101",
      macAddress: "00:1B:44:11:3A:B7",
      lastConnected: new Date(Date.now() - 5 * 60 * 1000).toISOString(), // 5 minutes ago
    },
    {
      id: "2",
      name: "MacBook Pro",
      type: "laptop",
      status: "online",
      ipAddress: "192.168.1.102",
      macAddress: "00:1B:44:11:3A:B8",
      lastConnected: new Date(Date.now() - 15 * 60 * 1000).toISOString(), // 15 minutes ago
    },
    {
      id: "3",
      name: "iPad Air",
      type: "tablet",
      status: "sleep",
      ipAddress: "192.168.1.103",
      macAddress: "00:1B:44:11:3A:B9",
      lastConnected: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(), // 3 hours ago
    },
    {
      id: "4",
      name: "Desktop PC",
      type: "desktop",
      status: "offline",
      ipAddress: "192.168.1.104",
      macAddress: "00:1B:44:11:3A:C0",
      lastConnected: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
    },
    {
      id: "5",
      name: "Apple Watch",
      type: "smartwatch",
      status: "online",
      ipAddress: "192.168.1.105",
      macAddress: "00:1B:44:11:3A:C1",
      lastConnected: new Date(Date.now() - 30 * 60 * 1000).toISOString(), // 30 minutes ago
    },
    {
      id: "6",
      name: "Samsung Smart TV",
      type: "tv",
      status: "offline",
      ipAddress: "192.168.1.106",
      macAddress: "00:1B:44:11:3A:C2",
      lastConnected: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), // 5 days ago
    },
    {
      id: "7",
      name: "Android Tablet",
      type: "tablet",
      status: "error",
      ipAddress: "192.168.1.107",
      macAddress: "00:1B:44:11:3A:C3",
      lastConnected: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(), // 12 hours ago
    },
    {
      id: "8",
      name: "Work Laptop",
      type: "laptop",
      status: "online",
      ipAddress: "192.168.1.108",
      macAddress: "00:1B:44:11:3A:C4",
      lastConnected: new Date(Date.now() - 45 * 60 * 1000).toISOString(), // 45 minutes ago
    },
  ]
}
