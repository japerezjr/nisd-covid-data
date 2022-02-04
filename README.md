# nisd-covid-data

requires bs4 and requests to run

This code will scrape https://www.nisd.net/schools/health to pull the current covid numbers.  The result is displayed as a list of tuples for the overall district and then as a json dictionary for the individual schools.  The program is run in a crontab nightly and saves the results to a log file.  The current accumulated set of logs can be found in the data folder.
