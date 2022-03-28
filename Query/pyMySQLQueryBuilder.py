class pyMySQLQueryBuilder:
    
    _query = ""
    _where_query = " WHERE "
    _order_by = ""
    _limit = ""
    _query_data = []
    _find_one = False
    _is_aggregate = False
    
    def model(self, name:str):
        """Entry Point to the database modal

        Args:
            name (str): Modal Name or Table Name

        Returns:
            pyMySQLPing: self
        """
        self._query = f"SELECT * FROM {name}"
        return self
    
    def filter(self, column:str, value, operator:str="="):
        """Filter Items in a collection (An equivalent of SQL WHERE clause)

        Args:
            column (str): column name to use when filtering
            value (str | int): value to use when filtering
            operator (str, optional): Opereator. Defaults to "=".

        Returns:
            pyMySQLPing: self
        """
        self._where_query += f"{column} {operator} %s AND "
        self._query_data.append(value)
        return self
    
    def sort(self, column:str, order="ASC"):
        """Sort Items in a collection (An equivalent of SQL ORDER BY)

        Args:
            column (str): Column Name to use in sorting the items
            order (str, optional): Sorting Order. Defaults to "ASC".

        Returns:
            pyMySQLPing: A sorted collection of items after calling get()
        """
        self._order_by = f"ORDER BY {column} {order}"
        return self
    
    def limit(self, number:int):
        """Specify the number of items to return from a collection (An equivalent of SQL LIMIT)

        Args:
            number (int): number of items to return eg, 10

        Returns:
            pyMySQLPing: self
        """
        self._limit = f" LIMIT {number}"
        return self

    
    def _build_query(self, columns):
        self._where_query = self._where_query[:-4]
        new_query = f"{self._query} {self._where_query}"
        if len(self._order_by) > 1:
            new_query += self._order_by
        
        if len(self._limit) > 1:
            new_query += self._limit
        
        new_query = new_query.replace('*', columns)
        return new_query
    
    
    def find(self, identifier, column:str='id'):
        """Find a single resource (An equivalent of SQL WHERE cluase)

        Args:
            identifier (str | int): Unique identifier of the resource
            column (str, optional): column name to use in a condition. Defaults to 'id'.

        Returns:
            pyMySQLPing: A Single dict Resource after calling get()
        """
        self._find_one = True
        return self.filter(column=column, value=identifier)
    
    
    def filter_exact(self, column:str, value):
        """A Collection of items exaclty match a given value

            An Equivalent to SQL LIKE %/value%/ statement 
        Args:
            column (str): column name
            value (str | int): value

        Returns:
            pyMySQLPing: A list of dicts with items that saticify the condition afte calling get()
        """
        self._where_query += f" {column} LIKE %s AND "
        self._query_data.append(f"%{value}%")
        return self
    
    
    def filter_ending_with(self, column:str, value):
        """A Collection of items ending with a given value

            An Equivalent to SQL LIKE value%/ statement 
        Args:
            column (str): column name
            value (str | int): value

        Returns:
            pyMySQLPing: A list of dicts with items that saticify the condition after calling get()
        """
        self._where_query += f" {column} LIKE %s AND "
        self._query_data.append(f"%{value}")
        return self
    
    def filter_begining_with(self, column:str, value):
        """A Collection of items begining with a given value

            An Equivalent to SQL LIKE value%/ statement 
        Args:
            column (str): column name
            value (str | int): value

        Returns:
            pyMySQLPing: A list of dicts with items that saticify the condition after calling get()
        """
        self._where_query += f" {column} LIKE %s AND "
        self._query_data.append(f"{value}%")
        return self
    
    def _reset(self):
        self._query = ""
        self._where_query = " WHERE "
        self._order_by = ""
        self._limit = ""
        self._query_data = []
        self._find_one = False
        self._is_aggregate = False