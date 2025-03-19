# Excel Template Format Guide

This document explains how to structure your Excel file for use with the Lucid Firewall Diagram Generator.

## Required File Location

The Excel file must be placed in the **"source data"** directory inside the lucid-generator project:

```
lucid-generator/
└── source data/
    └── your_excel_file.xlsx
```

When you run the tool, you'll be able to select which Excel file to use from this directory.

## Required Sheet

The Excel file must contain a sheet named **"External Ports"** where your firewall rules will be defined.

## Column Structure

The following columns are required in the "External Ports" sheet:

| Column | Description |
|--------|-------------|
| Software Type | The type of software or infrastructure component for which this firewall rule applies |
| Source | The source entity of the network traffic |
| Ports | The port numbers (comma-separated or range using hyphens) |
| Transfer Protocol | The protocol used (TCP, UDP, TCP/UDP, ICMP) |
| Destination | The destination entity of the network traffic |
| Service Flow | Description of the traffic flow (auto-generated) |
| Additional Notes | Optional field for extra information about the rule |
| Source AZ (Used for Diagram Generation) | Availability Zone name for the source entity |
| Destination AZ (Used for Diagram Generation) | Availability Zone name for the destination entity |

## Availability Zones (AZ)

Availability Zones (AZ) are used to organize entities in the diagram. Common AZ names include:

- Local AZ
- AZ1, AZ2, AZ3
- Client Network
- Internet Services
- External Services

The diagram will visually group entities by their AZ, making it easier to understand network segmentation.

## Example Data Structure

Here's an example of how to structure your data:

| Software Type | Source | Ports | Transfer Protocol | Destination | Service Flow | Additional Notes | Source AZ | Destination AZ |
|---------------|--------|-------|-----------------|-------------|--------------|-----------------|----------|---------------|
| Web Platform | Web Server | 443 | TCP | Application Server | Web Server to Application Server HTTPS (443 TCP) | Frontend to middle tier | DMZ | Application Zone |
| Database Access | Application Server | 1433 | TCP | Database Server | Application Server to Database Server SQL (1433 TCP) | Read/write access | Application Zone | Database Zone |
| Monitoring | Monitoring Server | 161 | UDP | Web Server | Monitoring Server to Web Server SNMP (161 UDP) | Health checks | Management | DMZ |

## Tips for Creating Your Excel File

1. **Start with a few rows**: Begin with essential firewall rules and add more as needed.
2. **Consistent naming**: Use consistent names for sources and destinations throughout the file.
3. **Group by Software Type**: This allows you to generate diagrams for specific components.
4. **Use meaningful AZ names**: Choose names that represent your actual network zones or regions.
5. **Add Notes**: Use the Additional Notes field to clarify the purpose of each rule.

## Common Availability Zone Layout

For infrastructure projects, a typical AZ layout might include:

- **Client Network**: User/client access layer
- **DMZ**: Demilitarized zone for public-facing services
- **Application Zone**: Middle-tier applications
- **Database Zone**: Database and storage systems
- **Management**: Administrative and monitoring systems
- **Internet Services**: External cloud or internet services

This logical grouping helps create clear, organized diagrams that are easy to understand.
