from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging, io


# Set up logging
#logging.basicConfig(level=logging.INFO)

_service = None

def get_service():
    global _service
    if _service is None:
        credentials = service_account.Credentials.from_service_account_file(
            'social-media-helper-417814-22917349ca42.json',
            scopes=['https://www.googleapis.com/auth/drive']
        )
        _service = build('drive', 'v3', credentials=credentials)
    return _service

def create_file( file_to_upload, file_name):
    drive_service = get_service()

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
    drive_service = get_service()

    create_file(drive_service)
    
def delete_file( id):
    drive_service = get_service()

    try:
        drive_service.files().delete(fileId=id).execute()
        logging.info(f'Item with ID {id} deleted successfully.')
    except Exception as e:
        logging.error(f'An error occurred: {e}')


def download_file( file_id, file_name):
    drive_service = get_service()

    try:
        # Request the file content
        request = drive_service.files().get_media(fileId=file_id)
        
        # Create a local file to save the downloaded content
        with open(file_name, 'wb') as f:
            # Write the file content to the local file
            downloader = io.BytesIO()
            downloader.write(request.execute())
            f.write(downloader.getvalue())

        logging.info(f'File downloaded successfully: {file_name}')
        return True

    except Exception as e:
        logging.error(f'An error occurred: {e}')
        return False