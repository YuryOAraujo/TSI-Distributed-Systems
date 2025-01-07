import time
# import matplotlib.pyplot as plt # type: ignore
from rpc import client
import os
import random

client = client.Client()

# print(client.check_primes([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
# print(client.check_primes([i for i in range (600)]))

print(client.validate_cpf('622.762.480-25'))
print(client.validate_cpf('622.762.480-26'))
print(client.validate_cpf(''))
client.validate_cpf('0asdasdasd')
for i in range(50):
    client.mul(random.randint(0, 1000), random.randint(0, 1000))
    client.sub(random.randint(0, 1000), random.randint(0, 1000))
# print(client.div(1, 5))
# print(client.div(1, 5))

# input_sizes = [100, 1_000, 5_000, 10_000, 20_000, 100_000, 500_000, 1_000_000, 2_000_000]
# sequential_times = []
# parallel_times = []

# for size in input_sizes:
#     numbers = list(range(size))

#     start_time = time.time()
#     client.check_primes(numbers)
#     sequential_times.append(time.time() - start_time)
    
#     start_time = time.time()
#     client.check_primes_parallel(numbers, os.cpu_count())
#     parallel_times.append(time.time() - start_time)

# plt.figure(figsize=(10, 5))
# bar_width = 0.35
# index = range(len(input_sizes))

# plt.bar(index, sequential_times, bar_width, label='Sequential')
# plt.bar([i + bar_width for i in index], parallel_times, bar_width, label='Parallel')

# plt.xlabel('Input Size')
# plt.ylabel('Execution Time (seconds)')
# plt.title('Execution Time Comparison: Sequential vs Parallel')
# plt.xticks([i + bar_width / 2 for i in index], input_sizes)
# plt.legend()

# plt.tight_layout()
# plt.show()