from app import cache

def get_cache(name):
    """get memcache data
    
    Arguments:
        name {string} -- name
    
    Returns:
        dict -- cache data
    """
    return cache.get(name)


def set_cache(name, data, timeout=5*60):
    """set memcache data
    
    Arguments:
        name {string} -- name
        data {dict} -- data
    
    Keyword Arguments:
        timeout {int} -- timeout of cache (default: {5*60})
    
    Returns:
        bool -- status
    """
    return cache.set(name, data, timeout)


def delete_cache(name):
    """delete memcache data
    
    Arguments:
        name {string} -- name
    
    Returns:
        bool -- status
    """
    return cache.delete(name)
