#Arrumar outras operações e ver erro de números 10000+

from rpc import client
import random

client = client.Client('127.0.0.1', 65432)

# for i in range(100):
#     v1 = client.sum(random.randint(1,1000), random.randint(1,1000))
#     v2 = client.mul(random.randint(1,1000), random.randint(1,1000))
#     print(v1 + v2)

print(client.sum(1, 2))
print(client.mul(1, 2))
print(client.mul(1, 2))
print(client.div(1, 2))
print(client.sub(1, 2))
print(client.sum_n(list(range(100000))))