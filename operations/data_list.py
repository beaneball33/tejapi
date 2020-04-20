from tejapi.model.data_list import DataList
from .list import ListOperation
from tejapi.errors.tej_error import (InvalidDataError, ColumnNotFound)
from tejapi.message import Message


class DataListOperation(ListOperation):
    @classmethod
    def create_datatable_list_from_response(cls, data):
        #print(cls)
        #print(data)
        if len(data['datatable']['data']) > 0 \
                and len(data['datatable']['columns']) != len(
                    data['datatable']['data'][0]):
            raise InvalidDataError(
                Message.ERROR_COLUMNS_DATA_NOT_MATCHED,
                response_data=data)
        values = data['datatable'].pop('data')
        metadata = {'columns': data['datatable']['columns'],
                    'next_cursor_id': data['meta']['next_cursor_id']}
        return DataList(cls, values, metadata)
