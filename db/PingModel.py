from Database.pyMySQLPing import pyMySQLPing

class PingModel:
    
    def __init__(self, object: object | str, app=None):
        
        self.objects = self.__pingModel(model=object, app=app)
    
    def __pingModel(self, model, app=None):
        """Access the pyMySQLPing Package

        Args:
            model str | Object: model name
            app (str, optional): app name. Defaults to None. 
            Used in the Django model to table name conversion

        Returns:
            pyMySQLPing: Instance of the pyMySQLPing Package
        """
        model = str(model)
        if "." in model:
            split_model = model.split('.')
            model = split_model[-1][:-2]

        if app is not None:
            model = f"{app}_{model}"
        
        db = pyMySQLPing()
        return db.model(model.lower())