from google.cloud import storage

import logging
import os

_bucket = None


class Storage:

    def __init__(self, bucket_name): 
        self.bucket_name = bucket_name 

    def get_storage_client(self):
        global _bucket 
        try:
            if not _bucket:
                storage_client = storage.Client.from_service_account_json(
                    'app/scammersuppression-f90e353e5381.json')
                _bucket = storage_client.get_bucket(self.bucket_name) 
        except Exception as ex:
            logging.exception(ex)
            raise ex
        else:
            return _bucket
 
    def upload_to_bucket(self,blob_name,folder):
        path_to_file = blob_name 
        try: 
            storage_client = storage.Client.from_service_account_json(
                    'app/scammersuppression-f90e353e5381.json')
            _bucket = storage_client.get_bucket(self.bucket_name) 
            blob = _bucket.blob(folder+'/'+blob_name)  
            blob.upload_from_filename(path_to_file)
        except Exception as ex:
            raise ex
        else:
            return {
                'file_name': blob_name,
                'url': blob.public_url,
                'size': blob.size
            }
        finally:
            os.remove(path_to_file)

    @staticmethod
    def remove_from_bucket(file_name):
        try:
            _bucket.delete_blob(blob_name=file_name)
        except Exception as ex:
            logging.exception(ex)
            raise ex
        else:
            return {'message': 'sucess in delete {} file.'.format(file_name)}