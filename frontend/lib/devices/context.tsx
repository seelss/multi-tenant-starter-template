import React, { createContext, useContext, useEffect, useState } from 'react';
import type { Device } from './types';
import { deviceWebSocketService } from './websocket';

// Define context type
interface DeviceContextType {
  devices: Device[];
  isLoading: boolean;
  isConnected: boolean;
  refreshDevices: () => void;
}

// Create the context with default values
const DeviceContext = createContext<DeviceContextType>({
  devices: [],
  isLoading: true,
  isConnected: false,
  refreshDevices: () => {},
});

// Hook for using the device context
export const useDevices = () => useContext(DeviceContext);

interface DeviceProviderProps {
  children: React.ReactNode;
}

export const DeviceProvider: React.FC<DeviceProviderProps> = ({ children }) => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isConnected, setIsConnected] = useState(false);
  
  // Function to manually refresh devices
  const refreshDevices = () => {
    setIsLoading(true);
    deviceWebSocketService.requestDevices();
  };
  
  // Initialize WebSocket connection
  useEffect(() => {
    // Handle device list updates
    const unsubscribeDevices = deviceWebSocketService.onDevicesUpdate((deviceList, action) => {
      console.log('Received device update:', action, deviceList);
      
      if (action === 'device_info_updated') {
        // If this is a device_info_updated action, we want to ensure we have the latest data
        console.log('Device info updated, refreshing device list');
        refreshDevices();
      } else {
        // Regular device list update
        setDevices(deviceList);
        setIsLoading(false);
      }
    });
    
    // Handle individual device updates
    const unsubscribeDevice = deviceWebSocketService.onDeviceUpdate((updatedDevice) => {
      setDevices(currentDevices => {
        // Replace the updated device in the list
        const updatedDevices = currentDevices.map(device => 
          device.id === updatedDevice.id ? updatedDevice : device
        );
        
        // If the device wasn't in the list, add it
        if (!updatedDevices.some(device => device.id === updatedDevice.id)) {
          updatedDevices.push(updatedDevice);
        }
        
        return updatedDevices;
      });
    });
    
    // Handle connection status
    const unsubscribeConnect = deviceWebSocketService.onConnect(() => {
      setIsConnected(true);
      // Request initial device list on connection
      refreshDevices();
    });
    
    const unsubscribeDisconnect = deviceWebSocketService.onDisconnect(() => {
      setIsConnected(false);
    });
    
    // Connect to WebSocket
    deviceWebSocketService.connect();
    
    // Clean up on unmount
    return () => {
      unsubscribeDevices();
      unsubscribeDevice();
      unsubscribeConnect();
      unsubscribeDisconnect();
      deviceWebSocketService.disconnect();
    };
  }, []);
  
  return (
    <DeviceContext.Provider value={{ devices, isLoading, isConnected, refreshDevices }}>
      {children}
    </DeviceContext.Provider>
  );
}; 