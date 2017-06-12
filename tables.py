from __future__ import division
import csv

def merge_tables(left, right, on):

    setupp.assert_class(left, Table)
    setupp.assert_class(right, Table)

    merged_table = {
        column: [] for column in left.column_names + right.column_names
    }

    left_hash = left._generate_hash(on)
    right_hash = right._generate_hash(on)

    for hash_key in left_hash._hash_table:
        try:
            data_to_add = right_hash._hash_table[hash_key]
        except KeyError:
            data_to_add = [{column: 'NA' for column in right_hash._source_table.column_names}]

        for left_row in left_hash._hash_table[hash_key]:
            for right_row in data_to_add:
                row_to_add = left_row.copy()
                row_to_add.update(right_row)

                for column in merged_table:
                    merged_table[column].append(row_to_add[column])

    left.update_table(merged_table)

    return left


class HashTable(object):

    def __init__(self, table, on):
        self._source_table = table
        self._on = on
        self._hash_table = self._generate_hash_table()

    def _generate_hash_table(self):
        hash_table = {}

        for n, row in enumerate(self._source_table._table[self._source_table.column_names[0]]):
            hash_key = ''

            for key_column in self._on:
                key_value = self._source_table[key_column][n]
                hash_key += '_{}'.format(key_value)

            hash_entry = {column: self._source_table._table[column][n] for column in self._source_table._table}

            try:
                hash_table[hash_key].append(hash_entry)
            except KeyError:
                hash_table[hash_key] = [hash_entry]

        return hash_table


class Table(object):
    """
    A light dataframe. Doesn't do much.
    """

    def __init__(self):
        self.filename = None
        self.delimiter= None
        self._table = None
        self.column_order = {}
        self.column_names = []
        self.shape = (0, 0)

    def _generate_table(self, filename, delimiter):

        table = {}

        with open(filename, 'rU') as f:

            c = csv.reader(f, delimiter=delimiter)
            column_order = {}

            for n, row in enumerate(c):

                if n > 0:

                    for column_n, item in enumerate(row):

                        table[column_order[column_n]].append(item)

                else:

                    column_order = {position: column for position, column in enumerate(row) if len(column) > 0}
                    #print column_order
                    table = {column_order[column]: [] for column in column_order}

        return (column_order, table)

    def _generate_hash(self, on):

       return HashTable(self, on)

    def from_tsv(self, filename, delimiter='\t'):

        self.delimiter = delimiter
        self.filename = filename

        table_tuple = self._generate_table(filename, delimiter)
        self._table = table_tuple[1]
        self.column_order = table_tuple[0]

        self.column_names = [self.column_order[column_number] for column_number in sorted(list(self.column_order))]
        #print self.column_names
        self.shape = (len(self._table[self.column_names[0]]), len(self._table))

        return self

    def update_table(self, dictionary):
        self._table = dictionary
        self.column_names = [self.column_order[column_number] for column_number in sorted(list(self.column_order))]
        self.shape = (len(self._table[self.column_names[0]]), len(self._table))
        return self

    def rows(self):

        for row_number in range(self.shape[0]):

            yield {column: self._table[column][row_number] for column in self._table}

    def to_csv(self, filename):
        with open(filename, 'w') as f:
            c = csv.writer(f)
            c.writerow(self.column_names)
            for n, row in enumerate(self._table[self.column_names[0]]):
                row_to_write = [self._table[column][n] for column in self.column_names]
                c.writerow(row_to_write)
        return filename


    def __str__(self):
        string = 'Table from {} with {} rows and {} columns: {}'.format(
            self.filename,
            self.shape[0],
            self.shape[1],
            ', '.join(self.column_names)
        )
        return string

    def __getitem__(self, key):
        return self._table[key]

    def __setitem__(self, key, value):
        self._table[key] = value
        self.column_names = sorted(list(self._table))
        self.shape = (len(self._table[self.column_names[0]]), len(self._table))
        return self._table[key]