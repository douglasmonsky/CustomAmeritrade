import sqlite3
import pandas as pd

class Database:
    
    def __init__(self, db_name):
        '''Creates or connects to database and interaction cursor. 
        Checks for existing tables storing needed info for methods.'''
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        table_names = self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        self.tables = {} #stores table_name:columns key pairs of all tables in db
        tables = [table for table in table_names]
        for table in tables:
            cols = self.get_col_names(table[0])
            self.tables[table[0]] = cols
    
    def get_col_names(self, table_name):
        '''Returns a list of column names from a specified table.'''
        self.c.execute(f'SELECT * from {table_name}')
        return [member[0] for member in self.c.description]
    
    def create_table(self, table_name, columns):
        '''Adds new table to database. 
        columns = list of tuple pairs of (column_name, data_type)
        e.g. [('colname1', 'TEXT'), ('colname2', 'TEXT')]
        data_type options = NULL, INTEGER, REAL, TEXT, BLOB'''
        cols = [f'{column} {column_type}' for column, column_type in columns]
        column_string = ', '.join(cols)
        table_creation = f'CREATE TABLE IF NOT EXISTS {table_name}({column_string})'
        self.c.execute(table_creation)
        columns = [column[0] for column in columns] 
        self.tables[table_name] = columns
       
    def data_entry(self, table_name, values, columns=None, executemany=False, entry_type='REPLACE'):
        '''Enters new data into specified table.
        columns = list of column names e.g. ['colname1', 'colname2']
        values = list of tuples, where tuples are ordered by column
        e.g. ('colname1_value', 'colname2_value')
        '''
        if not columns:
            columns = self.tables[table_name]
        column_string = ', '.join(columns)
        placeholders = '?, ' * (len(columns)-1) + '?'
        entry = f'{entry_type} INTO {table_name} ({column_string}) VALUES({placeholders})'
          
        if executemany:
            self.c.executemany(entry, values)
        else:
            self.c.execute(entry, values)
        self.conn.commit()
    
    def read_from_table(self, table_name, columns=['*'], pandas=False, *args):
        '''Returns all values from specified table by default, can retrieve 
        values from specific columns and based on specific args.'''
        columns = ', '.join(columns)
        if args:
            args = ' AND '.join(args)
            read = f'SELECT {columns} FROM {table_name} WHERE {args}'
        else:
            read = f'SELECT {columns} FROM {table_name}'
        if pandas:
            data = pd.read_sql_query(read, self.conn)
        else:
            self.c.execute(read)
            data = self.c.fetchall()
        return data
        
    def unique_index(self, table_name, index_col, index=None):
        if not index:
            index = index_col
        final_index = f'CREATE UNIQUE INDEX IF NOT EXISTS {index} ON {table_name}({index_col})'
        self.c.execute(final_index)
    
    def close_database(self):
        '''Closes cursor and connection to database.'''
        self.c.close()
        self.conn.close()
        
if __name__ == "__main__":
    db = Database('revert_file.db')
    columns = [('original_file_path', 'TEXT'), ('new_file_path', 'TEXT')]
    #~ db.create_table('revert_table', columns)
    db.create_table('revert2', columns)
    values = ('8', '11')
    db.data_entry('revert_table', values, executemany=False)
    #~ db.unique_index('original_file_path', 'revert_table')
    #~ db.data_entry('revert_table', values, replace=True)
    #~ print(db.read_from_table('revert_table',['*'], 'original_file_path = 1'))
    #~ print(db.tables)
    #~ help(Database)
    #~ db.unique_index('revert_table', 'original_file_path')




