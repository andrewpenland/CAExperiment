import socket

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 12345

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
soc.connect((SERVER_ADDRESS, SERVER_PORT))

print("CA Experimenter: Generates and evolves a CA rule number over a given "
      "radius and number of generations. ")
clients_input = input("Enter the CA job (the_rule_num, rule_radius, conf_num, "
                      "conf_length, this_ngens) :\n")
soc.send(clients_input.encode("utf8"))
result_bytes = soc.recv(4096)
result_string = result_bytes.decode("utf8")

print("Result from server is {}".format(result_string)) 