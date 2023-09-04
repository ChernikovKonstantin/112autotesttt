def on_index_error_return_none(no_args_predicate):
    try:
        return no_args_predicate()
    except IndexError:
        return None
