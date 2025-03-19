#!/usr/bin/env python3

import os
import pandas as pd
from datetime import datetime

def create_sample_excel():
    """
    Creates a sample Excel file for the Lucid Firewall Diagram Generator
    from the Enterprise_Firewall_Template.csv file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "Enterprise_Firewall_Template.csv")
    
    # Define the output directory (source data) and ensure it exists
    source_data_dir = os.path.join(os.path.dirname(script_dir), "source data")
    os.makedirs(source_data_dir, exist_ok=True)
    
    excel_path = os.path.join(source_data_dir, "Firewall Template.xlsx")
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return False
    
    try:
        # Read the CSV file
        print(f"Reading CSV data from {csv_path}...")
        df = pd.read_csv(csv_path)
        
        # Create a writer to work with multiple sheets
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Add instruction rows at the top (as empty rows that will be ignored by the tool)
            instruction_df = pd.DataFrame({
                "Instructions": [
                    "Firewall Rules Template for Lucid Diagram Generator",
                    f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "The tool will skip these instruction rows when processing"
                ]
            })
            
            # Write the instructions to the Excel file
            instruction_df.to_excel(writer, sheet_name="External Ports", index=False)
            
            # Write the actual data starting at row 4 (after instructions)
            df.to_excel(writer, sheet_name="External Ports", startrow=3, index=False)
        
        print(f"\nSuccessfully created Excel template: {excel_path}")
        print("This file can be used directly with the Lucid Firewall Diagram Generator.")
        print("\nThe Excel file includes the following realistic network zones:")
        print("- Internet Services: External services and users")
        print("- DMZ: Demilitarized zone with load balancers and web servers")
        print("- Application Zone: Internal application servers")
        print("- Database Zone: Database servers")
        print("- Authentication Zone: Authentication services")
        print("- Management Zone: Administrative and monitoring systems")
        print("- Client Network: Internal user access")
        
        return True
    
    except Exception as e:
        print(f"Error creating Excel file: {str(e)}")
        return False

if __name__ == "__main__":
    print("Lucid Firewall Diagram Generator - Sample Excel Creator")
    print("------------------------------------------------------")
    create_sample_excel()
