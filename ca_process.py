import os
import time
import datetime
import CA
SLEEP_TIME = 60  # sleep time in seconds
JOB_DIRECTORY = "jobs/"
RESULTS_DIRECTORY = "results/"


class CAProcessor:

    def __init__(self):
        self.job_directory = JOB_DIRECTORY
        self.results_directory = RESULTS_DIRECTORY
        self.sleep_time = SLEEP_TIME

    @staticmethod
    def get_time():
        return str(datetime.datetime.now().time()) + " "

    def check_for_jobs(self):
        print(self.get_time() + "Checking for jobs...")
        job_count = len(next(os.walk(self.job_directory))[2])
        if job_count > 0:
            print(self.get_time() + "Found jobs...")
            self.process_jobs()

    def process_jobs(self):
        for file_name in os.listdir(self.job_directory):
            print(self.get_time() + "Processing job file " + str(file_name) +
                  "...")
            with open(self.job_directory + file_name, 'r') as file:
                data = file.read()
                data = list(data.split())
                print(data)
                # self.write_job_csv(file_name, data)
            result = CA.main(int(data[0]), int(data[1]), data[2], int(data[3]),
                             int(data[4]))
            print(result)

    def write_job_csv(self, file_name, data):
        col_length = len(data[2])  # get length of columns
        col_names = list()
        col_index = list()
        for i in range(0, col_length):
            col_index.append(i)
            for j in range(0, len(job)):
                col_names.append("x" + str(i) + "t" + str(j))
        df = pd.DataFrame(job, columns=col_names, index=col_index)
        print(self.get_time() + "Results\n===================")
        print(df)
        print(self.get_time() + "Writing results to csv file...\n")
        df.to_csv(self.job_directory + file_name + '.csv')

    def start(self):
        print(self.get_time() + "Starting CA Processor...")
        while True:
            self.check_for_jobs()
            self.sleep()

    def stop(self):
        print(self.get_time() + "Stopping CA Processor...")

    def sleep(self):
        time.sleep(self.sleep_time)


if __name__ == "__main__":
    p = CAProcessor()
    p.start()
