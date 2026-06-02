import time

def evaluate_generation(generator_func, *args):

    start_time = time.time()

    output = generator_func(*args)

    latency = time.time() - start_time

    metrics = {
        "generation_latency": round(latency, 3),
        "output_length": len(str(output))
    }

    return output, metrics