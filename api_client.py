import os
import requests

class LucidApiClient:
    """
    Client for interacting with the Lucid API
    """
    
    def __init__(self, api_key):
        """
        Initialize the Lucid API client
        
        Args:
            api_key (str): The API key to use for authentication
        """
        if not api_key:
            raise ValueError("API key is required")
            
        self.api_key = api_key
        self.base_url = "https://api.lucid.co"
        
    def upload_document(self, lucid_file_path, title):
        """
        Upload a document to Lucid
        
        Args:
            lucid_file_path (str): Path to the .lucid file
            title (str): Title for the document
            
        Returns:
            dict: The API response
        """
        # Check if the file exists
        if not os.path.exists(lucid_file_path):
            raise FileNotFoundError(f"Lucid file not found: {lucid_file_path}")
        
        # Define the URL and headers for the direct upload
        url = f"{self.base_url}/documents"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Lucid-Api-Version": "1"
            # Content-Type is set automatically by requests when using files
        }
        
        print(f"\nUploading to Lucid API: {url}")
        print(f"Headers: Authorization: Bearer {self.api_key[:10]}... (truncated)")
        print(f"Lucid-Api-Version: 1")
        
        try:
            # Use multipart/form-data to upload the file directly to /documents endpoint
            with open(lucid_file_path, 'rb') as file:
                # Define the form data as specified in the documentation
                files = {
                    'file': (
                        os.path.basename(lucid_file_path), 
                        file, 
                        'x-application/vnd.lucid.standardImport'
                    )
                }
                data = {
                    'title': title,
                    'product': 'lucidchart'
                }
                
                print(f"File size: {os.path.getsize(lucid_file_path)} bytes")
                print(f"Sending form data: title={title}, product=lucidchart")
                
                # Send the POST request
                response = requests.post(url, headers=headers, files=files, data=data)
                
                # Print response details for debugging
                print(f"\nAPI Response Status Code: {response.status_code}")
                print(f"API Response Content: {response.text[:200]}...")  # Truncate long responses
                
                # Raise exception if response status is not successful (200-299)
                response.raise_for_status()
                
                # Extract the document ID or URL from the response
                response_json = response.json()
                document_id = response_json.get("id") or response_json.get("documentId")
                
                if not document_id:
                    print(f"Full API response: {response_json}")
                    document_url = response_json.get("editUrl") or response_json.get("viewUrl")
                    if document_url:
                        # Extract document ID from URL if present
                        import re
                        match = re.search(r'/([0-9a-f-]+)/(?:edit|view)$', document_url)
                        if match:
                            document_id = match.group(1)
                
                if document_id:
                    return {
                        "document_id": document_id,
                        "message": "Document uploaded successfully",
                        "document_url": f"https://lucid.app/documents/{document_id}"
                    }
                else:
                    # If we can't find an ID but the upload succeeded, return the response
                    edit_url = response_json.get("editUrl")
                    if edit_url:
                        return {
                            "message": "Document uploaded successfully",
                            "document_url": edit_url
                        }
                    else:
                        return {
                            "message": "Document uploaded successfully, but no URL was returned",
                            "api_response": response_json
                        }
                
        except requests.exceptions.RequestException as e:
            # Handle API errors
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('message', str(e))
                except:
                    pass
            
            raise Exception(f"API Error: {error_message}")
