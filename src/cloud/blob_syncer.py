import os

class BlobSync:
    def sync_folder_to_blob(self, folder, blob_url):
        command = f'azcopy copy "{folder}" "{blob_url}" --recursive=true'
        os.system(command)

    def sync_folder_from_blob(self, folder, blob_url):
        command = f'azcopy copy "{blob_url}" "{folder}" --recursive=true'
        os.system(command)

