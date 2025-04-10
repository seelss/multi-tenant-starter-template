import type { Device } from "./types"

export function getDevices(): Device[] {
  return [
    {
      id: "1",
      type: "smartphone",
      status: "online",
      lastConnected: new Date(Date.now() - 5 * 60 * 1000).toISOString(), // 5 minutes ago
      model: "iPhone 13 Pro",
      storage: "256GB",
      color: "Sierra Blue",
      imei: "123456789012345",
      serialNumber: "C02X12345678",
      batteryHealth: "98%",
      iosVersion: "16.4.1",
      activationStatus: "Activated",
      findMyStatus: "On",
      region: "US"
    },
    {
      id: "2",
      type: "smartphone",
      status: "online",
      lastConnected: new Date(Date.now() - 15 * 60 * 1000).toISOString(), // 15 minutes ago
      model: "iPhone 14 Pro Max",
      storage: "512GB",
      color: "Deep Purple",
      imei: "987654321098765",
      serialNumber: "C02X98765432",
      batteryHealth: "95%",
      iosVersion: "16.5",
      activationStatus: "Activated",
      findMyStatus: "On",
      region: "US"
    },
    {
      id: "3",
      type: "smartphone",
      status: "sleep",
      lastConnected: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(), // 3 hours ago
      model: "iPhone 12",
      storage: "128GB",
      color: "Black",
      imei: "456789123456789",
      serialNumber: "C02X45678912",
      batteryHealth: "87%",
      iosVersion: "16.3.1",
      activationStatus: "Activated",
      findMyStatus: "Off",
      region: "EU"
    },
    {
      id: "4",
      type: "smartphone",
      status: "offline",
      lastConnected: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
      model: "iPhone 13",
      storage: "128GB",
      color: "Pink",
      imei: "789123456789123",
      serialNumber: "C02X78912345",
      batteryHealth: "92%",
      iosVersion: "16.4",
      activationStatus: "Not Activated",
      findMyStatus: "Off",
      region: "AS"
    }
  ]
}
