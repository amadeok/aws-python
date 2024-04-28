from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging


# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load the service account's credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(
    'social-media-helper-417814-22917349ca42.json',
    scopes=['https://www.googleapis.com/auth/drive']
)

# Create a Google Drive API client
drive_service = build('drive', 'v3', credentials=credentials)

def create_file( file_to_upload, file_name):
    try:
    # File metadata
        file_metadata = {
        'name': file_name,  # Name of the file in Google Drive
         #'parents': ['1NzbyWS6HAFLGhTI_BmzI3BVjiufdfs3g']      # Optional: ID of the folder where you want to upload the file
    }
        media = MediaFileUpload(file_to_upload, mimetype='text/plain')
        uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
        ).execute()

        logging.info(f'File uploaded with ID: {uploaded_file.get("id")}')

    except Exception as e:
        logging.error(f'An error occurred: {e}')
    return uploaded_file.get("id")



if __name__ == "__main__":
    create_file(drive_service)
    
def delete_file( id):
    try:
        drive_service.files().delete(fileId=id).execute()
        logging.info(f'Item with ID {id} deleted successfully.')
    except Exception as e:
        logging.error(f'An error occurred: {e}')
