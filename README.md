# HTTP Load Tester

HTTP Load Tester is a Python library for load testing and benchmarking HTTP endpoints. 

## Features

- **Load Testing:** Send a specified number of HTTP requests to a given URL and measure response times and error rates.
- **Stress Testing:** Determine the maximum capacity of requests before system failure by gradually increasing the load.
- **Rate Limiting:** Control the rate of queries per second (QPS) to simulate real-world scenarios. You can use a --qps flag to generate requests at a given fixed QPS.

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
