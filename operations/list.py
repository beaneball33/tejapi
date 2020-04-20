from .operation import Operation
from tejapi.connection import Connection
from tejapi.util import Util
from tejapi.model.paginated_list import PaginatedList


class ListOperation(Operation):

    @classmethod
    def all(cls, **options):
        if 'params' not in options:
            options['params'] = {}
        path = Util.constructed_path(cls.list_path(), options['params'])
        
        http_verb='get'
        if len(str(options)) > 1024:
            options['data']=options['params']
            del options['params']
            http_verb='post'
            
        r = Connection.request(http_verb, path, **options)
        response_data = r.json()
        Util.convert_to_dates(response_data)
        resource = cls.create_list_from_response(response_data)
        return resource

    @classmethod
    def page(cls, datatable, **options):
        params = {'id': str(datatable.code)}
        path = Util.constructed_path(datatable.default_path(), params)

        http_verb='get'
        if len(str(options)) > 1024:
            options['data']=options['params']
            del options['params']
            http_verb='post'

        r = Connection.request(http_verb, path, **options)
        response_data = r.json()
        Util.convert_to_dates(response_data)
        resource = cls.create_datatable_list_from_response(response_data)
        return resource

    @classmethod
    def create_list_from_response(cls, data):
        return PaginatedList(cls, data[cls.lookup_key()], data['meta'])

    @classmethod
    def list_path(cls):
        return cls.lookup_key()
