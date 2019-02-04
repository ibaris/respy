# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# def test(*args):
#     print args
#     #for item in args.keys():
#     #    print item
#
# t = {'a':3, 'b':5}

import pandas as pd
import numpy as np
from respy.units import Quantity

class SubclassedSeries(pd.Series):

    @property
    def _constructor(self):
        return SubclassedSeries

    @property
    def _constructor_expanddim(self):
        return SubclassedDataFrame


class SubclassedDataFrame(pd.DataFrame):
    _attributes_ = ["header"]

    def __init_(self, data=None, index=None, columns=None, dtype=None, copy=False, units=None, description=None):
        super(SubclassedDataFrame, self).__init_(data=data, index=index, columns=columns, dtype=dtype, copy=copy)

        self.__set_table(units, description)

        self._attributes_[0]._copy_attrs(self)

    def _copy_attrs(self, df):
        for attr in self._attributes_.split(","):
            df.__dict__[attr] = getattr(self, attr, None)

    def __set_table(self, units, description):
        index_name = '*' + self.index.name if self.index.name != None else '*Index'
        index_dtype = self.index.dtype
        index_value = self.index.values

        columns = self.columns
        values = self.values


        # values = [self[item].values for item in columns]

        dtypes_str = [str(self[item].dtypes) for item in columns]
        dtypes = [self[item].dtypes for item in columns]

        total_values = np.zeros((values.shape[0], values.shape[1] + 1))
        total_dtypes = list()
        total_columns = list()

        total_columns.append(index_name)
        total_dtypes.append(str(index_dtype))

        total_values[:, 0] = index_value

        self.columns = list()
        self.dtype = list()
        self.__dtype_str = list()

        for i, _ in enumerate(columns):
            self.columns.append(columns[i])
            self.dtype.append(dtypes[i])
            self.__dtype_str.append(dtypes_str[i])

        unit_list = list()
        if units is None:
            unit_list = ['[-]' for i in self.columns]

        elif len(units) != len(self.columns):
            raise ValueError
        else:
            pass

        self.all_values = total_values
        self.__values_str = total_values.astype(np.str)

        len_str_array = np.zeros(self.all_values.shape[1], dtype=np.int)

        for i in range(self.all_values.shape[1]):
            sliced = self.__values_str[:, i]
            len_list = list()

            for j in range(sliced.shape[0]):
                len_list.append(len(sliced[j]))

            len_str_array[i] = max(len_list)

        len_columns = [len(item) for item in total_columns]
        len_dtypes = [len(item) for item in total_dtypes]

        zipped_lens = zip(len_columns, len_dtypes, len_str_array)

        self.__max_lens = [max(item) for item in zipped_lens]
        self.__stripes = [self.make_stripe(max(item)) for item in zipped_lens]

        body = list()
        columns_line = ''
        dtype_line = ''
        stripes_line = ''

        # total_values_T = [item.transpose() for item in total_values]

        self.__header = ''
        for i in range(len(total_columns)):
            columns_line += total_columns[i].rjust(self.__max_lens[i]) + '  '
            dtype_line += total_dtypes[i].rjust(self.__max_lens[i]) + '  '
            stripes_line += self.__stripes[i].rjust(self.__max_lens[i]) + '  '

            self.__header = columns_line + '\n' + dtype_line + '\n' + stripes_line + '\n'




    @property
    def _constructor(self):
        def f(*args, **kw):
            df = SubclassedDataFrame(*args, **kw)
            self._copy_attrs(df)
            return df
        return f

    @property
    def _constructor_sliced(self):
        return SubclassedSeries

    def space(self, n):
        space = ''
        for i in range(n):
            space += ' '
        return space

    def __repr__(self):

        for i in range(self.all_values.shape[0]):
            value_row = self.__values_str[i]

            row = ''

            for j in range(value_row.shape[0]):
                row += value_row[j].rjust(self.__max_lens[j]) + '  '

            self.__header += row + '\n'

        return self.__header

    def make_stripe(self, n):
        stripe = ''

        for i in range(n):
            stripe += '-'

        return stripe


df = SubclassedDataFrame({'DDD': [1, 2, 3], 'CCCCCCC': [10, 200, 3], 'BBB': [40000, 50, 656565645], 'AAA': [70, 0.8585858, 900]})
self = df

# print df
# df2 = df.set_index('Index')
# self = df2

# df = pd.DataFrame({'Index': [1, 2, 3], 'CCC': [1, 2, 3], 'BBB': [4, 5, 6], 'AAA': [7, 8, 9]})
# df2 = df.set_index('Index')
