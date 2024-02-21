import concurrent.futures
import time
from itertools import islice, cycle
from test_tools import Test_tools

class Test_stress(Test_tools):
    def stress_test(self):
        #Create domain list  
        self.domains = self.create_domain_list(self.number_of_domains)
        # Start the stress test
        print(f"Starting test!\nconcurrent requests:{self.concurrent_requests}\ndomains number: {self.number_of_domains}\ntest timeout: {self.test_timeout}")
        try:
            self.start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrent_requests) as executor:
                futures = [executor.submit(self.make_request,domain) for domain in islice(cycle(self.domains), self.concurrent_requests)]
                concurrent.futures.wait(futures,timeout =self.test_timeout)
                elapsed_time = time.time() - self.start_time
                if elapsed_time >= self.test_timeout:
                    self.print_results_and_exit( "Timeout",exit_program = False)#exit = False in order to raise TimeoutError
                    raise TimeoutError("test timeout occured! stopping stress test")
            self.print_results_and_exit( "Completed",exit_program = False)
            
        except KeyboardInterrupt:
            self.print_results_and_exit(reason="Keyboard interrupt",exit_program= True)
            print("Keyboard interrupt occurred")


if __name__ == "__main__":
    concurrent_requests, number_of_domains,test_timeout,collect_more_stats = Test_tools.get_user_input()
    stress = Test_stress(concurrent_requests,number_of_domains,test_timeout,collect_more_stats)
    stress.stress_test()

