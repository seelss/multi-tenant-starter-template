"use client"

import { useEffect, useState } from "react"

export function useIsMobile() {
  // Default to false for server-side rendering
  const [isMobile, setIsMobile] = useState(false)
  // Track whether we're mounted to avoid hydration issues
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    // Mark as mounted
    setMounted(true)
    
    // Function to check if the viewport width is mobile
    const checkIsMobile = () => {
      if (typeof window !== 'undefined') {
        setIsMobile(window.innerWidth < 768)
      }
    }

    // Check on initial load
    checkIsMobile()

    // Set up event listener for window resize
    if (typeof window !== 'undefined') {
      window.addEventListener("resize", checkIsMobile)
      
      // Clean up event listener on component unmount
      return () => window.removeEventListener("resize", checkIsMobile)
    }
  }, [])

  // During SSR and initial hydration, return false
  // After mounting (client-side), return the actual value
  return mounted ? isMobile : false
} 