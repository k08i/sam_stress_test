Stress Test Tool Overview
This tool is designed to simulate stress on a web service by making concurrent HTTP requests to various domains.
It allows the user to specify the number of concurrent requests, the total number of domains to test, an overall timeout for the test execution, and get average reputation for category.

Working Process
Setup: Ensure Python 3 and necessary packages are installed using the requirements.txt file provided.
Configuration: Upon execution, the tool prompts the user for three inputs: the number of concurrent requests, the number of domains, and the test timeout in seconds. it also allows you to chose additional statistics.
Execution: The tool performs the stress test based on the provided inputs. It distributes the requests among the specified domains, handling each request in parallel up to the limit of concurrent requests.
Timeout Handling: The test adheres to the specified timeout, ensuring the entire process does not exceed the user-defined time limit.
Results: At the end, the tool prints out the test results, including the total number of requests, error rate, average response time, the 90th percentile response time, and average reputation for category if asked.
Interruption: The tool is designed to handle keyboard interrupts, ensuring that partial results can be printed if the test is manually stopped.
Notes for Users
The tool requires internet access to perform requests to the specified domains.
Ensure the machine has sufficient resources to handle the number of concurrent requests specified.
The tool is best used in a controlled environment to avoid unintentional stress on external web services.

How to run tool:
at tool directory-> "python .\stress_test.py"