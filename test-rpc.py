from jsonrpc.proxy import ServiceProxy
s = ServiceProxy('http://localhost:8000/api/rpc/')
print s.authenticate()
