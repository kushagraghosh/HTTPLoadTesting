import requests
import argparse
import time

# Decorator to measure and print the time taken for a load tester function to execute
def measure_time(func):
    def wrapper_func(*args, **kwargs):
        '''
        Measure the time taken for the function to execute and print the result.'''
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f}s")
        return result
    return wrapper_func

class RateLimitedSession(requests.Session):
    '''
    RateLimitedSession is a subclass of requests.Session that adds a delay between requests to keep a desired rate of queries per second (QPS).'''
    #create a requests.Session object to manage and persist settings across multiple requests
    #I use Session objects because if there are "several requests to the same host, the underlying TCP connection will be reused, which can result in a significant performance increase" 
    #above quote is from https://requests.readthedocs.io/en/latest/user/advanced/#session-objects
    def __init__(self, qps):
        super().__init__()
        self.qps = qps
        self.last_request_time = time.time()

    def send(self, *args, **kwargs):
        '''
        Override the send() method of requests.Session to introduce a delay between requests. The delay ensures that the rate of requests matches the desired QPS (queries per second).
        '''
        #Calculate time since last request
        elapsed_time = time.time() - self.last_request_time

        interval = 1 / self.qps #calculate the time interval between each request based on the QPS (queries per second)
        if elapsed_time < interval:
            time.sleep(interval - elapsed_time) #If elapsed time is less than the desired interval, sleep to maintain QPS

        #Make the request and update last_request_time
        response = super().send(*args, **kwargs)
        self.last_request_time = time.time()
        return response
    
class LoadTester:
    def __init__(self, url: str, qps: float):
        '''
        Initialize LoadTester with URL and QPS (queries per second)'''
        self.url: str = url  # URL to test
        self.qps: float = qps  # QPS (queries per second)
        self.latencies: list = [] #list that stores the latencies (or response times) of the HTTP requests made during the load testing process
        self.error_count: int = 0  #counter that keeps track of the number of failed requests
        self.session = RateLimitedSession(qps) #create a RateLimitedSession object to manage the requests and maintain the desired QPS

    def send_request(self):
        '''
        Send a GET request to the URL and return the status code.'''
        try:
            start_time = time.time()
            response = self.session.get(self.url)
            end_time = time.time()
            latency = end_time - start_time #calculate the latency (or response time) of the request
            self.latencies.append(latency)
            return response.status_code
        except requests.RequestException as e: #catch any requests exceptions (https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions)
            print(f"Request failed: {e}")
            self.error_count += 1 #increment the error_count counter if the request fails
            return None

    @measure_time
    def run_load_test(self, num_requests: int, user_behaviors: list=None):
        '''
        Run the load test with the given number of requests and custom defined user behaviors (this parameter is optional and is defined as a list of functions).'''
        print("\nRunning load test...")
        successful_requests = 0
        self.start_time = time.time()

        for _ in range(num_requests):
            if user_behaviors:
                for behavior in user_behaviors:
                    behavior()

            status_code = self.send_request()
            if status_code:
                successful_requests += 1

        total_time = time.time() - self.start_time
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        error_rate = self.error_count / num_requests if num_requests > 0 else 0

        print(f"Total time taken: {total_time:.2f}s")
        print(f"Average latency: {avg_latency:.2f}s")
        print(f"Error rate: {error_rate:.2%}")
        print(f"{successful_requests} successful requests out of {num_requests}")
    
    #Added functionality for stress testing (determining the maximum capacity of requests before system breaks down)
    #Inspiration from https://medium.com/@rico098098/load-testing-with-python-fea13369af43 
    @measure_time
    def run_stress_test(self, max_requests: int, user_behaviors: list = None):
        """
        Run the stress test to determine the maximum capacity of requests before system failure.
        """
        print("\nRunning stress test...")
        successful_requests = 0
        self.start_time = time.time()

        for num_requests in range(1, max_requests + 1):
            if user_behaviors:
                for behavior in user_behaviors:
                    behavior()

            status_code = self.send_request()
            if status_code:
                successful_requests += 1
            else:
                print(f"Failed at {num_requests} requests")
                break

        total_time = time.time() - self.start_time
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        error_rate = (max_requests - successful_requests) / max_requests if max_requests > 0 else 0

        print(f"Total time taken: {total_time:.2f}s")
        print(f"Average latency: {avg_latency:.2f}s")
        print(f"Error rate: {error_rate:.2%}")
        print(f"{successful_requests} successful requests out of {max_requests}")

def main():
    parser = argparse.ArgumentParser(description="HTTP Load Tester")
    parser.add_argument("url", type=str, help="URL to test")
    parser.add_argument("--num-requests", type=int, default=10, help="Number of requests to send (default: 10)")
    parser.add_argument("--qps", type=float, default=1.0, help="Queries per second (default: 1.0)")
    parser.add_argument("--test-type", choices=["load", "stress"], default="load", help="Type of test to run: 'load' for normal load test, 'stress' for stress test (default: 'load')")
    args = parser.parse_args()

    tester = LoadTester(args.url, args.qps)
    
    # Define user behaviors here with your own custom functions (look at the example in the test_load_tester.py file)
    user_behaviors = []

    if args.test_type == "load":
        tester.run_load_test(args.num_requests, user_behaviors)
    elif args.test_type == "stress":
        tester.run_stress_test(args.num_requests, user_behaviors)

if __name__ == "__main__":
    main()
