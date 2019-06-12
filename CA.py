import math
import sys
import random

'''
bin_to_dec

convert a number from binary to decimal
'''

def bin_to_dec(bin_string):
    # tot = 0
    # n = len(bin_string)
    # #add the appropriate power of 2 at each step
    # for i in range(n):
    #     tot += bin_string[(n-1)-i]*2**i
    # return tot
    return int(bin_string, 2)

'''
dec_to_bin

convert a number from decimal to binary (as a list)

'''

def dec_to_bin(num, nbits = 8):
    new_num = num
    bin = []
    for j in range(nbits):
        #create the appropriate power of 2 for the current step
        current_bin_mark = 2**(nbits-1-j)
        #check to see if you can subtract this power of 2; if so, then subtract it and append 1
        if (new_num >= current_bin_mark):
            bin.append(1)
            new_num = new_num - current_bin_mark
        #if you can't subtract, append 0
        else:
            bin.append(0)
    return bin

'''
rule_table

take a number and a radius as input, return a CA rule table.
this only works with symmetric rules
'''

def make_rule_table(num,radius):
    #convert the number to the appropriate binary number
    binary_form = dec_to_bin(num, 2**(2*radius+1))
    #make the binary number readable as a lookup table (reverse it)
    the_table = binary_form[::-1]
    return the_table

'''
make_config

take a number and a length and return a configuration
'''

def make_config(num,config_length):
    #convert the number to the appropriate binary number
    binary_form = dec_to_bin(num, config_length)
    #make the binary number readable as a configuration (reverse it)
    the_config = binary_form[::-1]
    return the_config

'''
config_density

it seemed like an interesting thing to test -- this is the total number of 1's in the configuration
divided by the length of the configuration (a.k.a. the average)
'''

def config_density(config):
    return float(sum(config))/float((len(config)))


'''
evolve_one_step

this is a helper function for evolve. 

apply a given rule to a given configuration (both expressed as lists).
for this one, we want to use the table so that we don't have to call 
the "convert to table" function every time evolve calls this function. 
'''

def evolve_one_step(rule_table,config_to_update):
    old_config = config_to_update
    new_config = []
    config_length = len(config_to_update)
    #the expression below recovers the radius r,
    #using the fact that in a symmetric rule table
    #the length is equal to 2**(2*r-1)
    radius = int(math.floor((math.log(len(rule_table),2) - 1)/2))
    for i in range(config_length):
        local_config = []
        for j in range(i - radius, i + radius + 1):
            local_config.append(old_config[j%config_length])
        cell_update = rule_table[bin_to_dec(local_config)]
        new_config.append(cell_update)
    return new_config

'''
evolve

apply a given rule to a given configuration (both expressed as integers) 
'''

def evolve(rule_num, radius, config_num, config_length, ngens):
    #check to see if we got the ``rule number version'' as an integer
    #or as a list
    if type(rule_num) is int:
        rule_table_to_use = make_rule_table(rule_num, radius)
    else:
        rule_table_to_use = rule_num
    orbit = []
    if type(config_num) is int:
        init_config = make_config(config_num,config_length)
        old_config = make_config(config_num, config_length)
    else:
        init_config = config_num
        old_config = config_num
    orbit.append(init_config)
    updated_config = []
    for gen in range(ngens):
        updated_config = evolve_one_step(rule_table_to_use, old_config)
        orbit.append(updated_config)
        old_config = updated_config
    return orbit

'''random_initial_config

make a random initial configuration of a given length
'''

def random_initial_config(config_length):
    config = [random.choice([0,1]) for i in range(config_length)]
    return config

'''
random_initial_ensemble

make an initial ensemble of randomly chosen configurations
'''

def random_initial_ensemble(config_length,size):
    i = 0
    initial_ensemble = []
    while i < size:
        config_to_consider = random_initial_config(config_length)
        if not(config_to_consider in initial_ensemble):
            initial_ensemble.append(config_to_consider)
            i = i+1
    return initial_ensemble



'''random_rule_table

make a random rule table of a given length
'''

def random_rule_table(radius):
    config = [random.choice([0,1]) for i in range(2**(2*radius+1))]
    return config

'''
take_sequence

takes a sequence from an orbit by taking the values at a specified cell
'''

def take_sequence(orbit_to_use, cell_to_strip):
    #use a list comprehension
    return [value[cell_to_strip] for value in orbit_to_use]

'''
generate_ca_sequence

takes an initial configuration, a CA rule, and returns the binary sequence given by
stripping out the values at a particular cell. 
'''

def generate_ca_sequence(rule_num, radius, config_num, config_length, ngens, cell_to_strip = 0):
    orbit = evolve(rule_num, radius, config_num, config_length,ngens)
    sequence = take_sequence(orbit, cell_to_strip)
    return sequence



'''
test_rule_for_time
'''

def main():
    #we need to parse the individual arguments in the string we were given
    #then convert those to integers
    #then run the program with those arguments
    #then return the output

    #in practice, this will probably never pop up, since we will probably always be calling this
    #as a library for other scripts to access.

    if len(sys.argv) == 2:
        arg_array = sys.argv[1]
        command_line_args = arg_array.split(" ")

    else:
        command_line_args = sys.argv[1:]

    int_command_line_args = [int(arg) for arg in command_line_args]
    the_rule_num = int_command_line_args[0]
    rule_radius = int_command_line_args[1]
    conf_num = int_command_line_args[2]
    conf_length = int_command_line_args[3]
    this_ngens = int_command_line_args[4]

    evolution = evolve(the_rule_num, rule_radius, conf_num, conf_length, this_ngens)
    print(str(evolution))


if __name__ == "__main__":
    main()   
      
