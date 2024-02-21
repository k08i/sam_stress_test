from domain_list import POPULAR_DOMAIN_LIST
import requests
import random
import time
import sys
import csv
from statistics import mean
import numpy as np

class Test_tools():
    def __init__(self,concurrent_requests,number_of_domains,test_timeout,collect_more_stats) -> None:
        self.total_requests= 0
        self.failed_requests = 0
        self.test_timeout =test_timeout 
        self.response_times = []
        self.concurrent_requests = concurrent_requests
        self.number_of_domains = number_of_domains
        self.collect_more_stats = collect_more_stats
        if self.collect_more_stats:
            self.response_stat = {}
        pass
    
    def make_request(self,domain):
        start = time.time()
        try:
            url = f"https://microcks.gin.dev.securingsam.io/rest/Reputation+API/1.0.0/domain/ranking/{domain}"
            response = requests.get(url, headers={"Authorization": "Token I_am_under_stress_when_I_test"})
            if response.status_code == 200:
                end = time.time()
                self.response_times.append(end - start)
                if self.collect_more_stats == True:
                    result = response.json()
                    if result['categories'][0] not in self.response_stat:
                        self.response_stat[result['categories'][0]] =[result['reputation']]
                    else:
                        self.response_stat[result['categories'][0]].append(result['reputation'])
  
            else:
                self.failed_requests += 1
        except Exception:
            self.failed_requests += 1
        finally:
            self.total_requests += 1

    
    def get_user_input():
        concurrent_requests = int(input("Enter the number of concurrent requests: "))
        if concurrent_requests > 9999:
            print("Number of concurrent requests is high, this might affect test time")
        number_of_domains = int(input("Enter the number of domains to run: "))
        if number_of_domains > 5000:
            print("Number of domains cannot exceed 5000.")
            exit(1)
        if concurrent_requests < number_of_domains:
            print("The number of domains is larger than the number of concurrent requests; therefore, the number of domains will be adjusted.")
        test_timeout = int(input("Enter the timeout value in seconds for the test: "))
        collect_more_stats = input("Would you like more statistics about the test? (y/n): ").lower()
        while collect_more_stats not in ['y', 'n']:
            print("Invalid input. Please enter 'y' or 'n'.")
            collect_more_stats = input("Would you like more statistics about the test? (y/n): ").lower()
        collect_more_stats = True if collect_more_stats == 'y' else False
        return concurrent_requests, number_of_domains, test_timeout, collect_more_stats


    # Function to print results and optionally exit
    def print_results_and_exit(self,reason="Completed", exit_program=True):
        self.total_time = time.time() - self.start_time
        error_rate = (self.failed_requests / self.total_requests) * 100 if self.total_requests > 0 else 0
        avg_time = mean(self.response_times) if self.response_times else 0
        max_time = max(self.response_times) if self.response_times else 0
        p90_time = np.percentile(self.response_times, 90) if self.response_times else 0
        print(f"\nTest is over!\nReason: {reason}\nTime in total: {self.total_time:.2f} seconds\nRequests in total: {self.total_requests}\nError rate: {error_rate:.2f}% ({self.failed_requests} / {self.total_requests})\nAverage time for one request: {(avg_time * 1000):.4f} ms\nMax time for one request: {max_time:.4f} seconds\n90th percentile time:{p90_time:.4f}  seconds")
        if self.collect_more_stats == True:
            for category in self.response_stat:
                print(f"Average reputation for category: {category}, is: {mean(self.response_stat[category]):.2f}")
        # Save  test stats to CSV file
        with open('stress_test_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Reason', 'Total Time (s)', 'Total Requests', 'Failed Requests', 'Error Rate (%)', 'Average Time (ms)', 'Max Time (s)', '90th Percentile Time (s)'])
            writer.writerow([reason, f"{self.total_time:.2f}", self.total_requests, self.failed_requests, f"{error_rate:.2f}", f"{avg_time * 1000:.4f}", f"{max_time:.4f}",f"{p90_time:.4f}" ])
            print("test statistics saved as 'stress_test_results.csv', thank you.")
        if exit_program:
            sys.exit()

    def create_domain_list(self,number_of_domains):
        #Create domain list. if the requested number < POPULAR_DOMAIN_LIST, randomlly take domain fro the list,else create list with repeted domains.
        if number_of_domains > len(POPULAR_DOMAIN_LIST):
            repeat_times = (number_of_domains // len(POPULAR_DOMAIN_LIST))  
            domains = (POPULAR_DOMAIN_LIST * repeat_times) + POPULAR_DOMAIN_LIST[:number_of_domains % len(POPULAR_DOMAIN_LIST)]
        else:
            domains = random.sample(POPULAR_DOMAIN_LIST ,k= number_of_domains)
        return domains
        
