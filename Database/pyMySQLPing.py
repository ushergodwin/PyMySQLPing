from Connection.pyMySQLConnect import pyMySQLConnect
from Query.pyMySQLQueryBuilder import pyMySQLQueryBuilder


class pyMySQLPing(pyMySQLQueryBuilder, pyMySQLConnect):

    def get(self, columns:str="*"):
        """Return a dict or a list of dicts

        Args:
            columns (str, optional): Column Names. Defaults to "*".

        Returns:
            dict | list: A dict collection of items
        """
        self._connect()
        query = self._build_query(columns=columns)

        if self._find_one:
            return self._fetch_one(query, self._db.cursor())
        
        return self._fetch_all(query=query, cursor=self._db.cursor())
        
    
    def _fetch_all(self, query, cursor):
        if len(self._query_data) > 0:
            cursor.execute(query, tuple(self._query_data))
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        self._close()
        return self._extract_result(result)
    
    def _fetch_one(self, query, cursor):
        if not self._is_aggregate and len(self._query_data) < 1:
            raise ValueError("Missing resource identifier")

        cursor.execute(query, tuple(self._query_data))
        result = cursor.fetchone()
        if result is None:
            return None
        self._close()
        return self._extract_result(result)


    def value(self, column:str):
        """Single value from a column collection

        Args:
            column (str): Column Name

        Returns:
            Any: Value of a given column
        """
        result = self.get(columns=column)
        
        if result is None:
            return None
        
        return self._extract_result(result=result.get(column))
    
    
    def count(self, column:str="*"):
        """Number of items in a collection

        Args:
            column (str, optional): Column names. Defaults to "*".

        Returns:
            int | None: Number of Items or None if empty
        """
        if len(self._query_data) > 0:
            column = f" COUNT({column}) as num"
            return self._aggregative_result(column, 'num')
        return len(self.get(columns=column))
      
    
    def max(self, column:str):
        """Maximum value in a collection

        Args:
            column (str): Column Name

        Returns:
            int | None: Maximum value or None if the collection is empty
        """
        return self._extract_aggregate_column(' MAX(', column, ') as max', 'max')


    def sum(self, column:str):
        """The total sum of values in column collection

        Args:
            column (str): Column Name

        Returns:
            int | None: Total Sum or None
        """
        return self._extract_aggregate_column(' SUM(', column, ') as sum', 'sum')


    def avg(self, column:str):
        """The Average value in a collection of a given column

        Args:
            column (str): Column Name

        Returns:
            float | None: Float agregate value or None if empty
        """
        return self._extract_aggregate_column(' AVG(', column, ') as avg', 'avg')
    
    
    def min(self, column:str):
        """The minimum value of in a collection of a given column

        Args:
            column (str): table column name

        Returns:
            int | None: The min value if the collection is not empty, None otherwise
        """
        return self._extract_aggregate_column(' MIN(', column, ') as min', 'min')
    
    
    def _extract_aggregate_column(self, aggregate, column, alias, alias_name):
        column = f'{aggregate}{column}{alias}'
        return self._aggregative_result(column, alias_name)
    
    
    def _is_filtered(self):
        if len(self._query_data) < 1:
            raise Exception("Expected at least one condition to be parsed in the filter method")
        

    def _aggregative_result(self, column, alias):
        self._find_one = True
        self._is_aggregate = True
        result = self.get(columns=column)
        if result is None:
            return result
        return result.get(alias)
    
     
    def _extract_result(self, result):
        self._reset()
        return result


    def _close(self):
        self._db.close()

    