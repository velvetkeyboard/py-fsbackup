import os
# 3rd
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
# 1st
from fsbackup.backends.lib import Backend


SCOPES = [
    'https://www.googleapis.com/auth/drive',
    ]


class GoogleDriveBackend(Backend):
    name = 'google_drive'

    def upload(self, file_path, name=None):
        cfg = self.get_config()
        folder_name = os.path.expanduser(cfg['folder'])
        client = self.get_client()
        folder_id = self.get_folder_id(client, folder_name)
        if not folder_id:
            folder_id = self.create_backup_folder(client, folder_name)
        print(f'Copying {file_path} to {folder_name} ({folder_id})')
        self.create_file(client, file_path, folder_id)

    def get_credential_json_path(self):
        cfg = self.get_config()
        ret = cfg['credential']
        ret = os.path.expanduser(ret)
        return ret

    def get_folder_id(self, client, folder_name):
        q = ' and '.join([
            'trashed = false',
            "mimeType = 'application/vnd.google-apps.folder'",
            f"name = '{folder_name}'",
            ])
        fields = 'files(id)'
        resp = client.files().list(
            q=q,
            fields=fields,
            )\
            .execute()\
            .get('files', [])
        if resp:
            return resp[0].get('id')

    def create_backup_folder(self, client, name):
        if not self.get_folder_id(client, name):
            body = {
                'name': f'{name}',
                'mimeType': 'application/vnd.google-apps.folder',
                }
            resp = client.files().create(
                    body=body,
                    fields='id',
                    ).execute()
            return resp

    def create_file(self, client, local_file_path, folder_id):
        local_file_path = os.path.basename(local_file_path)
        file_name, file_extension = os.path.splitext(local_file_path)
        body = {
                'name': f'{file_name}',
                'parents': [folder_id],
                'mimeType': 'fsbackup/{file_extension}'
                }
        media_body = MediaFileUpload(
                local_file_path,
                )
        resp = client.files().create(
            body=body,
            media_body=media_body,
            fields='id, parents'
            ).execute()
        return resp

    def get_client(self):
        creds = self.get_creds()
        return build('drive', 'v3', credentials=creds)

    def get_creds(self):
        # The file token.pickle stores the user's access and refresh tokens,
        # and is created automatically when the authorization flow completes
        # for the first time.
        creds = None
        token_path = os.path.expanduser('~/.fsbackup_google_api_token.pickle')
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.get_credential_json_path(),
                    SCOPES,
                    )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        return creds
