try:
    from urllib.parse import urlparse
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode

import os

from tejapi.connection import Connection
from tejapi.util import Util
from tejapi.errors.tej_error import TejError
from tejapi.operations.get import GetOperation
from tejapi.operations.list import ListOperation
from .model_base import ModelBase
from tejapi.message import Message


class Database(GetOperation, ListOperation, ModelBase):
    BULK_CHUNK_SIZE = 512

    @classmethod
    def get_code_from_meta(cls, metadata):
        return metadata['database_code']

    def bulk_download_url(self, **options):
        url = self._bulk_download_path()
        url = ApiConfig.api_base + '/' + url

        if 'params' not in options:
            options['params'] = {}
        if ApiConfig.api_key:
            options['params']['api_key'] = ApiConfig.api_key
        if ApiConfig.api_version:
            options['params']['api_version'] = ApiConfig.api_version

        if list(options.keys()):
            url += '?' + urlencode(options['params'])

        return url

    def bulk_download_to_file(self, file_or_folder_path, **options):
        if not isinstance(file_or_folder_path, str):
            raise TejError(Message.ERROR_FOLDER_ISSUE)

        path_url = self._bulk_download_path()

        options['stream'] = True
        r = Connection.request('get', path_url, **options)
        file_path = file_or_folder_path
        if os.path.isdir(file_or_folder_path):
            file_path = file_or_folder_path + '/' + os.path.basename(urlparse(r.url).path)
        with open(file_path, 'wb') as fd:
            for chunk in r.iter_content(self.BULK_CHUNK_SIZE):
                fd.write(chunk)

        return file_path

    def _bulk_download_path(self):
        url = self.default_path() + '/data'
        url = Util.constructed_path(url, {'id': self.code})
        return url
