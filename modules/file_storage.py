# File Storage Module

import requests
import json
import os
import base64
from datetime import datetime

class FileStorage:
    """
    Handles file storage and retrieval using TinyCloud API.
    """
    
    def __init__(self, api_key):
        """
        Initialize the FileStorage with API key.
        
        Args:
            api_key (str): TinyCloud API key
        """
        self.api_key = api_key
        self.api_url = "https://api.tinycloud.com/v1"
        self.local_storage_path = "storage"
        
        # Create local storage directory if it doesn't exist
        if not os.path.exists(self.local_storage_path):
            os.makedirs(self.local_storage_path)
    
    def store_file(self, file_data, file_name, file_type):
        """
        Store a file using TinyCloud API or local fallback.
        
        Args:
            file_data (bytes): File data to store
            file_name (str): Name of the file
            file_type (str): Type of file (e.g., 'image', 'document')
            
        Returns:
            str: URL or path to the stored file
        """
        try:
            # Try to store using TinyCloud API
            return self._store_with_tinycloud(file_data, file_name, file_type)
        except Exception as e:
            print(f"Error storing file with TinyCloud: {e}")
            # Fall back to local storage
            return self._store_locally(file_data, file_name)
    
    def _store_with_tinycloud(self, file_data, file_name, file_type):
        """
        Store a file using TinyCloud API.
        
        Args:
            file_data (bytes): File data to store
            file_name (str): Name of the file
            file_type (str): Type of file
            
        Returns:
            str: URL to the stored file
        """
        # Encode file data as base64
        encoded_data = base64.b64encode(file_data).decode('utf-8')
        
        # Prepare request data
        data = {
            "file_name": file_name,
            "file_type": file_type,
            "file_data": encoded_data
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Make API request
        response = requests.post(f"{self.api_url}/files", headers=headers, json=data)
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            return result.get("file_url")
        else:
            raise Exception(f"TinyCloud API error: {response.status_code} - {response.text}")
    
    def _store_locally(self, file_data, file_name):
        """
        Store a file locally as fallback.
        
        Args:
            file_data (bytes): File data to store
            file_name (str): Name of the file
            
        Returns:
            str: Path to the stored file
        """
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{timestamp}_{file_name}"
        file_path = os.path.join(self.local_storage_path, unique_filename)
        
        # Write file to disk
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        return file_path
    
    def get_file(self, file_url):
        """
        Retrieve a file from TinyCloud or local storage.
        
        Args:
            file_url (str): URL or path to the file
            
        Returns:
            bytes: File data
        """
        # Check if it's a local file path
        if os.path.exists(file_url):
            with open(file_url, 'rb') as f:
                return f.read()
        
        # Otherwise, try to download from URL
        try:
            response = requests.get(file_url)
            if response.status_code == 200:
                return response.content
            else:
                raise Exception(f"Error downloading file: {response.status_code}")
        except Exception as e:
            print(f"Error retrieving file: {e}")
            return None
    
    def delete_file(self, file_url):
        """
        Delete a file from TinyCloud or local storage.
        
        Args:
            file_url (str): URL or path to the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if it's a local file path
        if os.path.exists(file_url):
            try:
                os.remove(file_url)
                return True
            except Exception as e:
                print(f"Error deleting local file: {e}")
                return False
        
        # Otherwise, try to delete from TinyCloud
        try:
            # Extract file ID from URL
            file_id = file_url.split('/')[-1]
            
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.delete(f"{self.api_url}/files/{file_id}", headers=headers)
            
            return response.status_code == 200 or response.status_code == 204
        except Exception as e:
            print(f"Error deleting file from TinyCloud: {e}")
            return False