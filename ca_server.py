import datetime
import os
import socket
import sys
import traceback
from threading import Thread

import CA
from ca_process import CAProcessor

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 12345
JOB_DIRECTORY = "jobs/"
RESULTS_DIRECTORY = "results/"


class CAServer:

    def __init__(self, address, port, job_directory, results_directory):
        self.address = address
        self.port = port
        self.job_directory = job_directory
        self.results_directory = results_directory
        self.ca_processor = CAProcessor()

    def check_job_directory(self):
        print(self.get_time() + "Checking for job directory...")
        if not os.path.exists(self.job_directory):
            print(self.get_time() + "Job directory not found!")
            print(self.get_time() + "Creating job directory...")
            os.makedirs(self.job_directory)
        else:
            print(self.get_time() + "Job directory found...")

    def check_results_directory(self):
        print(self.get_time() + "Checking for results directory...")
        if not os.path.exists(self.results_directory):
            print(self.get_time() + "Results directory not found!")
            print(self.get_time() + "Creating results directory...")
            os.makedirs(self.results_directory)
        else:
            print(self.get_time() + "Results directory found...")

    def client_thread(self, conn, ip, port, max_buffer_size=4096):

        # the input is in bytes, so decode it
        input_from_client_bytes = conn.recv(max_buffer_size)

        # max_buffer_size is how big the message can be
        siz = sys.getsizeof(input_from_client_bytes)
        if siz >= max_buffer_size:
            print("The length of input is probably too long: {}".format(siz))

        # decode input and strip the end of line
        input_from_client = input_from_client_bytes.decode("utf8").rstrip()

        res = self.parse_ca_job_string(input_from_client)
        # print("Result of processing {} is: {}".format(input_from_client, res))

        vysl = res.encode("utf8")  # encode the result string
        conn.sendall(vysl)  # send it to client
        conn.close()  # close connection
        print(self.get_time() + "Connection " + ip + ":" + port + " ended...")

    @staticmethod
    def get_time():
        return str(datetime.datetime.now().time()) + " "

    def parse_ca_job_string(self, arguments):
        print(self.get_time() + "Received job request " + str(arguments) +
              "...")
        print(self.get_time() + "Parsing job request " + str(arguments) + "...")
        arguments = arguments.split(' ')
        the_rule_num = int(arguments[0])
        rule_radius = int(arguments[1])
        conf_num = arguments[2].split(",")
        conf_length = int(arguments[3])
        this_ngens = int(arguments[4])
        self.queue_job(the_rule_num, rule_radius, conf_num, conf_length,
                       this_ngens)
        return self.get_time() + "Job successfully queued..."

    def queue_job(self, the_rule_num, rule_radius, conf_num, conf_length,
                  this_ngens):
        print(self.get_time() + "Queueing job...")
        new_job = CaJob(the_rule_num, rule_radius, conf_num, conf_length,
                        this_ngens)
        file_name = new_job.get_file_name()
        conf_num = "".join(str(x) for x in conf_num)
        conf_num.strip(",")
        job_string = str(the_rule_num) + " " + str(rule_radius) + " " + str(
            conf_num) + " " + str(conf_length) + " " + str(this_ngens)
        with open(self.job_directory + file_name, "w") as text_file:
            print(f"{job_string}", file=text_file)

    def start_server(self):
        print(self.get_time() + "Starting CA server...")

        # check for directories exist and create them it if not
        self.check_job_directory()
        self.check_results_directory()

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this is for easy starting/killing the app
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(self.get_time() + "Socket created...")

        try:
            soc.bind((self.address, self.port))
            print(self.get_time() + "Socket bind complete...")
        except socket.error as msg:
            print(self.get_time() + "Bind failed. Error : " + str(
                sys.exc_info()))
            sys.exit()

        # Start listening on socket
        soc.listen(10)
        print(self.get_time() + "Socket now listening...")

        while True:
            conn, addr = soc.accept()
            ip, port = str(addr[0]), str(addr[1])
            print(self.get_time() + "Accepting connection from " + ip + ":" +
                  port)
            try:
                Thread(target=self.client_thread, args=(conn, ip, port)).start()
            except:
                traceback.print_exc()

    def stop_server(self):
        print(self.get_time() + "Stopping Server...")
        sys.exit(1)


class CaJob:

    def __init__(self, the_rule_num, rule_radius, conf_num, conf_length,
                 this_ngens):
        self.the_rule_num = the_rule_num
        self.rule_radius = rule_radius
        if type(conf_num) is not list:
            self.conf_num = list(conf_num)
        else:
            self.conf_num = conf_num
        self.conf_length = conf_length
        self.this_ngens = this_ngens
        self.file_name = self.config_file_name()
        self.result = self.run_job()

    def config_file_name(self):
        date = datetime.datetime.now()
        date = date.strftime("%m%d%y_%H%M%S")
        file_name = str(self.the_rule_num) + "_" + \
            str(self.rule_radius) + "_" + \
            str(self.conf_length) + "_" + \
            str(self.this_ngens) + "_" + date + ".txt"
        return file_name

    def get_file_name(self):
        return self.file_name

    def run_job(self):
        result = list()
        for i in range(0, len(self.conf_num)):
            conf_result = CA.main(self.the_rule_num, self.rule_radius,
                                  self.conf_num, self.conf_length,
                                  self.this_ngens)
            result.append(conf_result)
        return result


if __name__ == "__main__":
    s = CAServer(SERVER_ADDRESS, SERVER_PORT, JOB_DIRECTORY, RESULTS_DIRECTORY)
    s.start_server()
