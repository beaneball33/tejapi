from .connection import Connection

def search_table(keyword):
    path = "search/table/%s" % (keyword)
    r = Connection.request('get', path).json()
    return r['result']['tables']