import pandas as pd
from tejapi.errors.tej_error import ColumnNotFound


class DataMixin(object):
    # DataFrame will respect order of input list of list
    def to_pandas(self, keep_column_indexes=[], chinese_column_name=False):
        data = self.to_list()

        # ensure pandas gets a list of lists
        if data and isinstance(data, list) and not isinstance(data[0], list):
            data = [data]
        
        if chinese_column_name is True and 'cnames' in self.meta.keys():
            df = pd.DataFrame(data=data, columns=self.cnames)
            for index, type in enumerate(self.column_types):
                if type == 'Date' or type=='datetime':
                    df[self.cnames[index]] = df[self.cnames[index]].apply(lambda x: pd.to_datetime(x,errors='coerce'))            
        elif 'columns' in self.meta.keys():
            df = pd.DataFrame(data=data, columns=self.columns)
            for index, type in enumerate(self.column_types):
                if type == 'Date' or type=='datetime':
                    df[self.columns[index]] = df[self.columns[index]].apply(lambda x: pd.to_datetime(x,errors='coerce'))
        else:
            df = pd.DataFrame(data=data, columns=self.column_names)
            # ensure our first column of time series data is of pd.datetime
            df[self.column_names[0]] = df[self.column_names[0]].apply(pd.to_datetime)
            df.set_index(self.column_names[0], inplace=True)

        # unfortunately to_records() cannot handle unicode in 2.7
        df.index.name = str(df.index.name)

        # keep_column_indexes are 0 based, 0 is the first column
        if len(keep_column_indexes) > 0:
            self._validate_col_index(df, keep_column_indexes)
            # need to decrement all our indexes by 1 because
            # Date is considered a column by our API, but in pandas,
            # it is the index, so column 0 is the first column after Date index
            keep_column_indexes = list([x - 1 for x in keep_column_indexes])
            df = df.iloc[:, keep_column_indexes]
        return df

    def to_numpy(self):
        return self.to_pandas().to_records()

    def to_csv(self):
        return self.to_pandas().to_csv()

    def _validate_col_index(self, df, keep_column_indexes):
        num_columns = len(df.columns)
        for col_index in keep_column_indexes:
            if col_index > num_columns or col_index < 1:
                raise ColumnNotFound('Requested column index %s does not exist'
                                     % col_index)
