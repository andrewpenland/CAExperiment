import CA
import sys
import socket
from threading import Thread
import traceback

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 12345


def process_ca_job(input_string):
    print("Received job: " + input_string)
    job = str(parse_ca_job_string(input_string))
    return job


def parse_ca_job_string(arguments):
    arguments = arguments.split(' ')
    the_rule_num = int(arguments[0])
    rule_radius = int(arguments[1])
    conf_num = arguments[2].split(",")
    conf_length = int(arguments[3])
    this_ngens = int(arguments[4])
    result = submit_job(the_rule_num, rule_radius, conf_num, conf_length,
                        this_ngens)
    return result


def submit_job(the_rule_num, rule_radius, conf_num, conf_length, this_ngens):
    result = CA.main(the_rule_num, rule_radius, conf_num, conf_length,
                     this_ngens)
    return result


def client_thread(conn, ip, port, max_buffer_size=4096):

    # the input is in bytes, so decode it
    input_from_client_bytes = conn.recv(max_buffer_size)

    # max_buffer_size is how big the message can be
    siz = sys.getsizeof(input_from_client_bytes)
    if siz >= max_buffer_size:
        print("The length of input is probably too long: {}".format(siz))

    # decode input and strip the end of line
    input_from_client = input_from_client_bytes.decode("utf8").rstrip()

    res = process_ca_job(input_from_client)
    print("Result of processing {} is: {}".format(input_from_client, res))

    vysl = res.encode("utf8")  # encode the result string
    conn.sendall(vysl)  # send it to client
    conn.close()  # close connection
    print('Connection ' + ip + ':' + port + " ended")


def start_server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind((SERVER_ADDRESS, SERVER_PORT))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    # Start listening on socket
    soc.listen(10)
    print('Socket now listening')

    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            traceback.print_exc()


start_server()
