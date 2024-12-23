from multiprocessing import Pool, cpu_count
from time import time


def factors(n):
    return [i for i in range(1, n + 1) if n % i == 0]


def factorize_sync(numbers):
    return [factors(number) for number in numbers]


def factorize_parallel(numbers):
    with Pool(cpu_count()) as pool:
        result = pool.map(factors, numbers)
    return result

if __name__ == "__main__":
    numbers = [128, 255, 99999, 10651060]


    start_sync = time()
    result_sync = factorize_sync(numbers)
    end_sync = time()

    print("Synchronous results:", result_sync)
    print(f"Synchronous execution time: {end_sync - start_sync:.2f} seconds")


    start_parallel = time()
    result_parallel = factorize_parallel(numbers)
    end_parallel = time()

    print("Parallel results:", result_parallel)
    print(f"Parallel execution time: {end_parallel - start_parallel:.2f} seconds")


    assert result_sync == result_parallel
    assert result_sync[0] == [1, 2, 4, 8, 16, 32, 64, 128]
    assert result_sync[1] == [1, 3, 5, 15, 17, 51, 85, 255]
    assert result_sync[2] == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert result_sync[3] == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
