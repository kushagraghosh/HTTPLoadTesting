import unittest
from load_tester import LoadTester

class TestLoadTester(unittest.TestCase):
    def test_run_load_test(self):
        #Create a LoadTester instance to run a load test
        url = "https://www.google.com"  #I am using Google for testing
        tester = LoadTester(url, 2) #1 query per second

        #Define a mock user behavior function (in this case, this user behavior is to search "Fireworks AI" in Google)
        def mock_user_behavior():
            response = tester.session.get(f"{url}/search?q=Fireworks+AI")
            #print("Response status code:", response.status_code)

        #Now, run the load test with the mock user behavior
        tester.run_load_test(4, [mock_user_behavior])

        #Assert that latencies list is not empty (there were some valid response times recorded)
        self.assertTrue(tester.latencies)

    def test_run_stress_test(self):
        #Create a LoadTester instance to do stress testing to determine the maximum capacity of requests before system failure
        url = "https://fireworks.ai/"
        tester = LoadTester(url, 2)

        #Mock user behavior function (in this case, this user behavior is to do nothing on the website)
        def mock_user_behavior():
            pass

        #Run stress test with 20 requests initially (feel free to increase this number to determine the maximum capacity of requests before system failure)
        max_requests = 20
        try:
            tester.run_stress_test(max_requests, [mock_user_behavior])
            print(f"Successfully completed {max_requests} requests without failure.")
        except Exception as e:
            print(f"System failed at {max_requests} requests.")
            print(f"Error message: {e}")
            

if __name__ == '__main__':
    unittest.main()
