#!/usr/bin/env python3

import os
import sys
import pandas as pd
from excel_reader import read_excel_data, get_software_types, filter_by_software_type
from lucid_generator import create_lucid_file
from api_client import LucidApiClient

def display_menu(software_types):
    """
    Display a menu of software types for the user to select from
    
    Args:
        software_types (list): List of software types
        
    Returns:
        int: The index of the selected software type
    """
    print("\nAvailable Software Types:")
    for i, software_type in enumerate(software_types, 1):
        print(f"{i}. {software_type}")
    
    while True:
        try:
            choice = input("\nEnter the number of the Software Type to generate a diagram for: ")
            selection = int(choice) - 1
            
            if 0 <= selection < len(software_types):
                return selection
            else:
                print(f"Please enter a number between 1 and {len(software_types)}")
        except ValueError:
            print("Please enter a valid number")

def main():
    """
    Main function to run the Lucid Firewall Diagram Generator
    """
    # Define the path to the Excel file
    excel_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                 "source data", "Firewall Template.xlsx")
    
    # Check if the Excel file exists
    if not os.path.exists(excel_file_path):
        print(f"Error: Excel file not found at {excel_file_path}")
        sys.exit(1)
    
    try:
        # Read the Excel data
        print(f"Reading Excel data from {excel_file_path}...")
        df = read_excel_data(excel_file_path)
        
        # Get the list of software types
        software_types = get_software_types(df)
        
        if not software_types:
            print("Error: No software types found in the Excel file")
            sys.exit(1)
        
        # Display menu and get user selection
        selection = display_menu(software_types)
        selected_software_type = software_types[selection]
        
        # Filter the data by the selected software type
        print(f"\nGenerating diagram for: {selected_software_type}")
        filtered_data = filter_by_software_type(df, selected_software_type)
        
        if filtered_data.empty:
            print(f"Error: No data found for software type '{selected_software_type}'")
            sys.exit(1)
        
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Define the output path
        output_filename = f"{selected_software_type.replace(' ', '_')}.lucid"
        output_path = os.path.join(output_dir, output_filename)
        
        # Create the Lucid file
        print(f"Creating Lucid diagram...")
        create_lucid_file(filtered_data, selected_software_type, output_path)
        
        print(f"\nSuccessfully created Lucid diagram: {output_path}")
        print("You can import this file into Lucid to view the diagram.")
        
        # Ask if the user wants to upload to Lucid
        upload_choice = input("\nWould you like to upload this diagram to Lucid? (y/n): ").strip().lower()
        
        if upload_choice in ('y', 'yes'):
            try:
                # Ask for API key
                print("\nAn API key is required to upload to Lucid.")
                api_key = input("Enter your Lucid API key: ").strip()
                
                if not api_key:
                    print("API key cannot be empty. Skipping upload.")
                    return
                
                # Create API client
                client = LucidApiClient(api_key)
                
                # Upload the document
                print("Uploading to Lucid...")
                response = client.upload_document(output_path, f"Firewall Rules - {selected_software_type}")
                
                print(f"\nSuccess! Document uploaded to Lucid.")
                print(f"Document URL: {response['document_url']}")
                
            except Exception as e:
                print(f"Error uploading to Lucid: {str(e)}")
                print("The .lucid file is still available locally.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("Lucid Firewall Diagram Generator")
    print("--------------------------------")
    main()
