def isolation_level(db, level):
    """ Decorator to set isolation level per request.
        This will perform "dirty reads" which means it will read uncommited changes directly from the database.
        :param db: database object.
        :param level: isolation_level
        :return decorator
    """
    def decorator(view):
        def view_wrapper(*args, **kwargs):
            db.session.connection(execution_options={'isolation_level': level})
            return view(*args, **kwargs)

        return view_wrapper

    return decorator
