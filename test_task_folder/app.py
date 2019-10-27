from typing import Dict, List, Tuple


def clean_mongo_field_names(dict_object: Dict) -> List[Tuple[str, str]]:
    """
    Patch a field names (keys) in dict for MongoDB, replace dot (.) symbol to uFF0E unicode symbol
    and dollar ($) symbol to FF04 unicode symbol if they first symbol of field name
    Args:
        dict_object: dict object that will be patched
    See Also:
        https://docs.mongodb.com/manual/reference/limits/#Restrictions-on-Field-Names
        http://www.fileformat.info/info/unicode/char/ff04/index.htm
        http://www.fileformat.info/info/unicode/char/ff0e/index.htm
    Returns:
         List of tuples where 0 is an old key and 1 is patched new key
    """
    patched_keys = []
    for key, value in dict_object.items():
        old_key = key
        if isinstance(value, dict):
            patched_keys += clean_mongo_field_names(value)
        if not isinstance(key, str):
            continue
        if key.startswith('$'):
            key = '\uFF04' + key[1:]
        key = key.replace('.', '\uFF0E')
        if key == old_key:
            continue
        dict_object[key] = dict_object.pop(old_key)
        patched_keys.append((old_key, key))
    return patched_keys


