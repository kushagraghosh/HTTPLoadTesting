# HTTP Load Tester

HTTP Load Tester is a Python library for load testing and benchmarking HTTP endpoints. 

## Features

- **Load Testing:** Send a specified number of HTTP requests to a given URL and measure response times and error rates.
- **Stress Testing:** Determine the maximum capacity of requests before system failure by gradually increasing the load.
- **Rate Limiting:** Control the rate of queries per second (QPS) to simulate real-world scenarios. You can use a --qps flag to generate requests at a given fixed QPS.


The code in `load_tester.py` utilizes the `requests`, `argparse`, and `time` libraries. It defines a decorator named `measure_time` to measure and print the execution time of a function. The `RateLimitedSession` class extends `requests.Session` to introduce a delay between requests to maintain a desired rate of queries per second (QPS). It overrides the `send()` method to implement this functionality. The reason I create a `requests.Session` object to manage and persist settings across multiple requests is because if there are "several requests to the same host, the underlying TCP connection will be reused, which can result in a significant performance increase" (from https://requests.readthedocs.io/en/latest/user/advanced/#session-objects). The `LoadTester` class initializes with a URL and QPS, and it includes methods to send HTTP requests and run load or stress tests. The `main()` function parses command-line arguments using `argparse` and creates a `LoadTester` object based on the provided arguments, running either a load or stress test based on the specified test type.

There is also code in `test_load_tester.py` to create a LoadTester instance to run a load test in `test_run_load_test()` (for instance having the URL be Google and defining a mock user behavior function to search "Fireworks AI" in Google). This test file also includes code to run a stress test in `test_run_stress_test()` that creates a LoadTester instance to do stress testing to determine the maximum capacity of requests before system failure.

## Setup and Usage

To set up the project, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/kushagraghosh/HTTPLoadTesting.git   
```

2. Go to the project directory:
```bash
cd HTTPLoadTesting
```

3. Build the Docker image:
```bash
docker build -t http_load_tester .
```

Once the Docker image is built, you can run the load testing tool by executing the Docker container with appropriate arguments. 

## Usage

### Command-line Arguments

- **URL**: The URL of the endpoint to test.

Optional Arguments:

- `--num-requests NUM_REQUESTS`: Number of requests to send. Default is 10.
- `--qps QPS`: Queries per second (QPS). Default is 1.0.
- `--test-type {load,stress}`: Type of test to run. Default is 'load'.

### Running Load Test

To run a load test, execute the following two commands:

```bash 
docker run -it <image_name> /bin/bash
```

```bash
python load_tester.py <URL> [--num-requests NUM_REQUESTS] [--qps QPS] [--test-type {load,stress}]
```

Example:

```bash 
docker run -it http_load_tester /bin/bash
```

```bash
python load_tester.py https://www.google.com/ --num-requests 4 --qps 2.0
```

This command will send 4 requests to https://www.google.com/ with a rate of 2 queries per second.

### Running Stress Test

To run a stress test, specify the `--test-type stress` argument:

```bash 
docker run -it <image_name> /bin/bash
```

```bash
python load_tester.py <URL> --test-type stress [--num-requests NUM_REQUESTS] [--qps QPS]
```

Example:

```bash 
docker run -it http_load_tester /bin/bash
```

```bash
python load_tester.py https://fireworks.ai/ --test-type stress --num-requests 20 --qps 2.0
```

This command will continuously increase the number of requests sent to https://fireworks.ai/ until system failure or 20, aiming for a QPS of 2.0.
