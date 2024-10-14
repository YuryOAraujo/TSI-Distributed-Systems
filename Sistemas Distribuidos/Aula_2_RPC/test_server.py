from rpc import server

server = server.Server('127.0.0.1', 65432)

server.start()