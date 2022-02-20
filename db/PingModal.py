from Database.pyMySQLPing import pyMySQLPing
def PingModal(modal:object | str, app=None):
    """Access the pyMySQLPing Wrapper

    Args:
        modal str | Object: Modal name
        app (str, optional): app name. Defaults to None. 
        Used in the Django modal to table name conversion

    Returns:
        pyMySQLPing: Instance of the pyMySQLPing Wrapper
    """
    modal = str(modal)
    if app is not None:
        modal = f"{app}_{modal}"
    
    db = pyMySQLPing()
    return db.modal(modal)