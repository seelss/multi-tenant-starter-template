import { io, Socket } from 'socket.io-client';
import type { Device } from './types';

// WebSocket event types
type DeviceListEvent = {
  type: 'device_list';
  devices: Device[];
};

type DeviceUpdateEvent = {
  type: 'device_update';
  device: Device;
};

type WebSocketEvent = DeviceListEvent | DeviceUpdateEvent;

// Callback types
type DevicesCallback = (devices: Device[]) => void;
type DeviceCallback = (device: Device) => void;

/**
 * DeviceWebSocketService manages WebSocket connection for real-time device updates
 */
export class DeviceWebSocketService {
  private socket: WebSocket | null = null;
  private isConnected = false;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectInterval = 3000; // 3 seconds
  
  // Callbacks
  private onDevicesUpdateCallbacks: DevicesCallback[] = [];
  private onDeviceUpdateCallbacks: DeviceCallback[] = [];
  private onConnectCallbacks: (() => void)[] = [];
  private onDisconnectCallbacks: (() => void)[] = [];
  
  constructor(private url: string = 'ws://localhost:8002/ws/devices/') {}
  
  /**
   * Connect to the WebSocket server
   */
  connect(): void {
    if (this.socket) {
      return;
    }
    
    try {
      this.socket = new WebSocket(this.url);
      
      this.socket.onopen = this.handleOpen.bind(this);
      this.socket.onclose = this.handleClose.bind(this);
      this.socket.onmessage = this.handleMessage.bind(this);
      this.socket.onerror = this.handleError.bind(this);
    } catch (error) {
      console.error('Failed to connect to WebSocket:', error);
      this.attemptReconnect();
    }
  }
  
  /**
   * Disconnect from the WebSocket server
   */
  disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
      this.isConnected = false;
    }
    
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
  }
  
  /**
   * Request updated list of devices
   */
  requestDevices(): void {
    if (this.isConnected && this.socket) {
      this.socket.send(JSON.stringify({ type: 'get_devices' }));
    }
  }
  
  /**
   * Register callback for device list updates
   */
  onDevicesUpdate(callback: DevicesCallback): () => void {
    this.onDevicesUpdateCallbacks.push(callback);
    return () => {
      this.onDevicesUpdateCallbacks = this.onDevicesUpdateCallbacks.filter(cb => cb !== callback);
    };
  }
  
  /**
   * Register callback for individual device updates
   */
  onDeviceUpdate(callback: DeviceCallback): () => void {
    this.onDeviceUpdateCallbacks.push(callback);
    return () => {
      this.onDeviceUpdateCallbacks = this.onDeviceUpdateCallbacks.filter(cb => cb !== callback);
    };
  }
  
  /**
   * Register callback for connection established
   */
  onConnect(callback: () => void): () => void {
    this.onConnectCallbacks.push(callback);
    return () => {
      this.onConnectCallbacks = this.onConnectCallbacks.filter(cb => cb !== callback);
    };
  }
  
  /**
   * Register callback for connection closed
   */
  onDisconnect(callback: () => void): () => void {
    this.onDisconnectCallbacks.push(callback);
    return () => {
      this.onDisconnectCallbacks = this.onDisconnectCallbacks.filter(cb => cb !== callback);
    };
  }
  
  // Private methods
  private handleOpen(): void {
    console.log('WebSocket connection established');
    this.isConnected = true;
    this.reconnectAttempts = 0;
    this.onConnectCallbacks.forEach(callback => callback());
  }
  
  private handleClose(): void {
    console.log('WebSocket connection closed');
    this.isConnected = false;
    this.socket = null;
    this.onDisconnectCallbacks.forEach(callback => callback());
    this.attemptReconnect();
  }
  
  private handleMessage(event: MessageEvent): void {
    try {
      const data = JSON.parse(event.data) as WebSocketEvent;
      
      switch (data.type) {
        case 'device_list':
          this.onDevicesUpdateCallbacks.forEach(callback => callback(data.devices));
          break;
        case 'device_update':
          this.onDeviceUpdateCallbacks.forEach(callback => callback(data.device));
          break;
        default:
          console.warn('Unknown WebSocket message type:', data);
      }
    } catch (error) {
      console.error('Error processing WebSocket message:', error);
    }
  }
  
  private handleError(error: Event): void {
    console.error('WebSocket error:', error);
  }
  
  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error(`Failed to reconnect after ${this.maxReconnectAttempts} attempts`);
      return;
    }
    
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }
    
    this.reconnectTimeout = setTimeout(() => {
      console.log(`Attempting to reconnect (${this.reconnectAttempts + 1}/${this.maxReconnectAttempts})...`);
      this.reconnectAttempts++;
      this.connect();
    }, this.reconnectInterval);
  }
}

// Create a singleton instance
export const deviceWebSocketService = new DeviceWebSocketService(); 