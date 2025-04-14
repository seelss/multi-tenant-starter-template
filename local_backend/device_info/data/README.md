# Device Info Mapping Data Files

This directory contains CSV files that map device identifiers to human-readable information:

## model_mapping.csv

Maps device model numbers to detailed device information:

```
model_number,identifier,variant,emc,model_name,storage_capacity,housing_color,network,cellular_network,camera,controller,ports,power_cord,power_brick,dimensions,avg_weight,release_date,msrp
MT752CH/A,"iPhone11,6",A2104,3261,iPhone Xs Max,256GB,Silver,WiFi + Cellular,GSM/CDMA/LTE,12.0 Megapixels,3D Touch,Lightning,Lightning,5w,6.20 x 3.05 x 0.30 inches,7.34 oz,September 12th 2018,1249
```

The iOS device collector primarily uses these columns:
- `model_number`: The model number of the device (e.g., "MT752CH/A")
- `model_name`: Human-readable model name (e.g., "iPhone Xs Max")
- `storage_capacity`: Storage capacity (e.g., "256GB")
- `housing_color`: Device color (e.g., "Silver")

## region.csv

Maps region codes to human-readable region names:

```
code,region
A,Canada
```

Where:
- `code`: The region code from the device model number (e.g., "A")
- `region`: Human-readable region name (e.g., "Canada") 