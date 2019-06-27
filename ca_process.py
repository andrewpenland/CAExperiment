import pandas as pd
import datetime
import os
import time

import CA

JOB_DIRECTORY = "jobs/"
RESULTS_DIRECTORY = "results/"
SLEEP_TIME = 180  # sleep time in seconds


class CAProcessor:

    def __init__(self):
        self.job_directory = JOB_DIRECTORY
        self.results_directory = RESULTS_DIRECTORY
        self.sleep_time = SLEEP_TIME

    def check_for_jobs(self):
        print(self.get_time() + "Checking for jobs...")
        job_count = len(next(os.walk(self.job_directory))[2])
        if job_count > 0:
            print(self.get_time() + "Found jobs...")
            self.process_jobs()

    @staticmethod
    def get_time():
        return str(datetime.datetime.now().time()) + " "

    def process_jobs(self):
        for file_name in os.listdir(self.job_directory):
            print(self.get_time() + "Processing job file " + str(file_name) +
                  "...")

            with open(self.job_directory + file_name, 'r') as file:
                file_base_name = os.path.splitext(file_name)[0]
                results = list()
                indexes = list()
                header = list()
                result_len = 0
                generation_len = 0

                """
                Calculate results for each line
                """
                for line in file:
                    args = [int(s) for s in line.split()]
                    r = CA.main(args[0], args[1], args[2], args[3], args[4])
                    r = [val for sublist in r for val in sublist]
                    results.append(r)
                    indexes.append(args[2])
                    if args[3] > result_len:
                        result_len = args[3]
                    if args[4] > generation_len:
                        # add one for zero based indexing
                        generation_len = args[4]+1

                """
                Construct header
                """
                for i in range(0, generation_len):
                    for j in range(0, result_len):
                        header.append("x" + str(j) + "t" + str(i))

                """
                Construct data frame
                """
                df = pd.DataFrame(results, columns=header, index=indexes)

                """
                Write data frame to CSV
                """
                self.write_job_csv(file_base_name, df)

    def sleep(self):
        time.sleep(self.sleep_time)

    def start(self):
        print(self.get_time() + "Starting CA Processor...")
        while True:
            self.check_for_jobs()
            self.sleep()

    def stop(self):
        print(self.get_time() + "Stopping CA Processor...")

    def write_job_csv(self, file_base_name, df_results):
        print(self.get_time() + "Writing results to csv file...\n")
        file_path = self.results_directory + file_base_name + ".csv"
        df_results.to_csv(file_path)


if __name__ == "__main__":
    p = CAProcessor()
    p.start()
