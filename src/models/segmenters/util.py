def trim(tokens):
    '''Trim spaces in the list'''
    return [token.strip() for token in tokens]


def remove_empty(tokens):
    '''Remove an empty string in the list'''
    return list(filter(None, [token.strip() for token in tokens]))


def clean(tokens):
    '''Trim spaces and remove an empty element (empty string) in the list'''
    return remove_empty(trim(tokens))
