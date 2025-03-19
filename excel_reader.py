import pandas as pd
import os
import warnings

# Suppress specific openpyxl warnings about data validation
warnings.filterwarnings("ignore", 
                       message="Data Validation extension is not supported and will be removed",
                       module="openpyxl")

def read_excel_data(file_path):
    """
    Read the Excel file and return the data as a pandas DataFrame
    
    Args:
        file_path (str): Path to the Excel file
        
    Returns:
        pd.DataFrame: DataFrame containing the Excel data
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    
    try:
        # First try to read the sheet with default settings
        try:
            df = pd.read_excel(file_path, sheet_name="External Ports")
            
            # Check if we have the required columns
            required_columns = ["Software Type", "Source", "Destination", 
                               "Source AZ (Used for Diagram Generation)", 
                               "Destination AZ (Used for Diagram Generation)"]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"Warning: Missing required columns: {', '.join(missing_columns)}")
                print("Trying to read the file with different settings...")
                raise ValueError("Missing required columns")
                
        except (ValueError, KeyError):
            # If that fails, try skipping the first few rows which might contain instructions
            print("Attempting to skip header rows...")
            for skip_rows in range(1, 6):  # Try skipping 1-5 rows
                try:
                    df = pd.read_excel(file_path, sheet_name="External Ports", skiprows=skip_rows)
                    
                    # Check if we have the required columns now
                    required_columns = ["Software Type", "Source", "Destination", 
                                       "Source AZ (Used for Diagram Generation)", 
                                       "Destination AZ (Used for Diagram Generation)"]
                    
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    if not missing_columns:
                        print(f"Successfully read Excel file by skipping {skip_rows} rows")
                        break
                except:
                    continue
            else:
                raise Exception("Could not find required columns in the Excel file")
        
        # Clean up any potential NaN values in key columns
        df = df.dropna(subset=["Software Type", "Source", "Destination"])
        
        return df
    except Exception as e:
        raise Exception(f"Error reading Excel file: {str(e)}")

def get_software_types(df):
    """
    Extract unique software types from the DataFrame
    
    Args:
        df (pd.DataFrame): DataFrame containing the Excel data
        
    Returns:
        list: List of unique software types
    """
    return sorted(df["Software Type"].dropna().unique().tolist())

def filter_by_software_type(df, software_type):
    """
    Filter the DataFrame by the selected software type
    
    Args:
        df (pd.DataFrame): DataFrame containing the Excel data
        software_type (str): Software type to filter by
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    return df[df["Software Type"] == software_type].copy()

def get_unique_az_values(df):
    """
    Get unique AZ values from the DataFrame
    
    Args:
        df (pd.DataFrame): DataFrame containing the Excel data
        
    Returns:
        list: List of unique AZ values
    """
    source_az = df["Source AZ (Used for Diagram Generation)"].dropna().unique().tolist()
    dest_az = df["Destination AZ (Used for Diagram Generation)"].dropna().unique().tolist()
    
    # Combine and get unique values
    all_az = sorted(list(set(source_az + dest_az)))
    
    return all_az

def get_unique_entities(df):
    """
    Get unique source and destination entities from the DataFrame
    
    Args:
        df (pd.DataFrame): DataFrame containing the Excel data
        
    Returns:
        dict: Dictionary containing unique sources and destinations grouped by AZ
    """
    entities_by_az = {}
    
    # Process sources
    for _, row in df.iterrows():
        source = row["Source"]
        source_az = row["Source AZ (Used for Diagram Generation)"]
        
        if pd.notna(source) and pd.notna(source_az):
            if source_az not in entities_by_az:
                entities_by_az[source_az] = {"sources": set(), "destinations": set()}
            
            entities_by_az[source_az]["sources"].add(source)
    
    # Process destinations
    for _, row in df.iterrows():
        destination = row["Destination"]
        dest_az = row["Destination AZ (Used for Diagram Generation)"]
        
        if pd.notna(destination) and pd.notna(dest_az):
            if dest_az not in entities_by_az:
                entities_by_az[dest_az] = {"sources": set(), "destinations": set()}
            
            entities_by_az[dest_az]["destinations"].add(destination)
    
    # Convert sets to lists for easier processing
    for az in entities_by_az:
        entities_by_az[az]["sources"] = sorted(list(entities_by_az[az]["sources"]))
        entities_by_az[az]["destinations"] = sorted(list(entities_by_az[az]["destinations"]))
    
    return entities_by_az
