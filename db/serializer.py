import sqlite3

class Serializable():

    def __init__(self, serialize_table):
        self.serialize_table = serialize_table

    def deserialize(self):
        pass

    def insert_into(self, sqlite_table):
        ''' Serialize object into a sqlite INSERT call.
        Example:
        >>> class SerializeMe(Serializable):
        >>>   def __init__(self, name):
        >>>     self.name = name
        >>>     self.seiralize_table = {'name': 'name'}
        >>>
        >>> test = SerializeMe('jack')
        >>> query = test.insert_into('names')
        >>> self.assertEquals(query, ('INSERT INTO names (name) VALUES (?)', 'jack')) '''
        keys = list(self.serialize_table)
        values = [getattr(self, prop) for prop in self.serialize_table.values()]
        placeholders = ', '.join('?' for value in values)
        sqlite_query_format = f'INSERT INTO {sqlite_table} ({keys}) VALUES ({placeholders})'
        return sqlite_query_format, values
