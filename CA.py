"""
Description:
    Functions that generate and evolve a cellular automaton over a given
    radius (neighborhood).
Original Authors:
    Bailey Stillman & Dr.Andrew Penland (2018)
Edits done by:
    David Walsh (2019)
"""

import math
import sys
import random


def bin_to_dec(bin_string):
    """Converts a number (as a string type) from binary to decimal

    Args:
        bin_string: String representing the binary value

    Returns:
        binary_value: Positive integer representing decimal value
    """
    bin_string = bin_string[::-1]
    tot = 0
    n = len(bin_string)
    # add the appropriate power of 2 at each step
    for i in range(n):
        tot += int(bin_string[(n - 1) - i]) * 2 ** i
    return tot


def dec_to_bin(num, nbits=8):
    """Converts a number from decimal to binary (as a list)

    Args:
        num: Integer representing the decimal value
        nbits: Integer representing number of bits that will be returned

    Returns:
        binary_value: Positive integer representing decimal value
    """
    new_num = num
    bin = []
    for j in range(nbits):
        # create the appropriate power of 2 for the current step
        current_bin_mark = 2**(nbits-1-j)
        # check to see if you can subtract this power of 2; if so,
        # then subtract it and append 1
        if new_num >= current_bin_mark:
            bin.append(1)
            new_num = new_num - current_bin_mark
        # if you can't subtract, append 0
        else:
            bin.append(0)
    return bin[::-1]


def make_rule_table(num, radius):
    """
    Takes a integer and a radius and generates the CA rule table

    Args:
        num: An integer representing the CA rule number
        radius: The neighborhood in which the CA evolves

    Returns:
        A list representing the CA rule table
    """
    # convert the number to the appropriate binary number
    binary_form = dec_to_bin(num, 2**(2*radius+1))
    # make the binary number readable as a lookup table (reverse it)
    the_table = binary_form[::-1]
    return the_table


def make_config(num, config_length):
    """
    Generates the configuration for the CA

    Args:
        num: An integer representing the CA rule
        config_length: An integer representing the length of the CA

    Returns:
        A list representing the configuration
    """
    # convert the number to the appropriate binary number
    binary_form = dec_to_bin(num, config_length)
    # make the binary number readable as a configuration (reverse it)
    the_config = binary_form[::-1]
    return the_config


def config_density(config):
    """
    Returns the total number of binary 1's in the configuration.

    Args:
        config: A list representing the configuration of the CA

     Returns:
        The number of binary 1's in the configuration divided by the
        length of the configuration
    """
    return float(sum(config))/float((len(config)))


def evolve_one_step(rule_table, config_to_update):
    """
    A helper function for the evolve function. Applies a given rule to a
    given CA configuration (both expressed as lists). A table is used so the
    call to the convert table function doesn't have to be called every time
    evolve is called.

    Args:
        rule_table: A list that expressed the CA rule table
        config_to_update: A lis that expresses the configuration of the CA

    Returns:
        new_config: A list containing the new CA configuration
    """
    old_config = config_to_update
    new_config = []
    config_length = len(config_to_update)
    # the expression below recovers the radius r,
    # using the fact that in a symmetric rule table
    # the length is equal to 2**(2*r-1)
    radius = int(math.floor((math.log(len(rule_table), 2) - 1)/2))
    for i in range(config_length):
        local_config = []
        for j in range(i - radius, i + radius + 1):
            local_config.append(old_config[j % config_length])
        cell_update = rule_table[bin_to_dec(local_config)]
        new_config.append(cell_update)
    return new_config


def evolve(rule_num, radius, config_num, config_length, ngens):
    """
    Applies a given rule to a given configuration (both expressed as
    integers).

    Args:
        rule_num: The CA rule number
        radius: The neighborhood in which the CA evolves
        config_num: The configuration number
        config_length: Length of the CA configuration
        ngens: The number of generations for the CA to evolve

    Returns:
        orbit:
    """
    # check to see if we got the ``rule number version'' as an integer
    # or as a list
    if type(rule_num) is int:
        rule_table_to_use = make_rule_table(rule_num, radius)
    else:
        rule_table_to_use = rule_num
    orbit = []
    if type(config_num) is int:
        init_config = make_config(config_num, config_length)
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


def random_initial_config(config_length):
    """
    Generates a random initial configuration of a given length

    Args:
        config_length: The length of the CA configuration

    Returns:
        config: A list of a randomly generated CA configuration
    """
    config = [random.choice([0, 1]) for i in range(config_length)]
    return config


def random_initial_ensemble(config_length, size):
    """
    Generates an initial ensemble of a randomly chosen configuration

    Args:
        config_length:
        size:

    Returns:
        initial_ensemble: A list representing the ensemble of the randomly
        chosen configuration.
    """
    i = 0
    initial_ensemble = []
    while i < size:
        config_to_consider = random_initial_config(config_length)
        if not(config_to_consider in initial_ensemble):
            initial_ensemble.append(config_to_consider)
            i = i+1
    return initial_ensemble


def random_rule_table(radius):
    """Make a random rule table of a given length

    Args:
        radius: The radius (neighborhood) in which the CA evolves

    Returns:
        config: The rule table given the length
    """

    config = [random.choice([0, 1]) for i in range(2**(2*radius+1))]
    return config


def take_sequence(orbit_to_use, cell_to_strip):
    """
    Takes a sequence from an orbit by taking the values at a specified cell.

    Args:
        orbit_to_use: The orbit to use
        cell_to_strip: The cell to generate a sequence from

    Returns:
        A list of a sequence from an orbit at the specified cell.
    """
    return [value[cell_to_strip] for value in orbit_to_use]


def generate_ca_sequence(rule_num, radius, config_num, config_length, ngens,
                         cell_to_strip=0):
    """
    Takes an initial configuration, a CA rule, and returns the binary
    sequence given by stripping out the values at a particular cell.

    Args:
          rule_num: The CA rule number
          radius: The neighborhood in which the CA evolves.
          config_num: The configuration number
          config_length: Length of the configuration
          ngens: Number of generations for the CA to evolve
          cell_to_strip: The cell in which to generate the sequence from

    Returns:
         sequence: The binary sequence of the stripped values at the
         specified cell
    """
    orbit = evolve(rule_num, radius, config_num, config_length, ngens)
    sequence = take_sequence(orbit, cell_to_strip)
    return sequence


def main(the_rule_num, rule_radius, conf_num, conf_length, this_ngens):
    # we need to parse the individual arguments in the string we were given
    # then convert those to integers
    # then run the program with those arguments
    # then return the output
    # in practice, this will probably never pop up, since we will probably
    # always be calling this as a library for other scripts to access.

    # if len(sys.argv) == 2:
    #     arg_array = sys.argv[1]
    #     command_line_args = arg_array.split(" ")
    #
    # else:
    #     command_line_args = sys.argv[1:]
    #
    # int_command_line_args = [int(arg) for arg in command_line_args]
    # the_rule_num = int_command_line_args[0]
    # rule_radius = int_command_line_args[1]
    # conf_num = int_command_line_args[2]
    # conf_length = int_command_line_args[3]
    # this_ngens = int_command_line_args[4]

    evolution = evolve(the_rule_num, rule_radius, conf_num, conf_length,
                       this_ngens)

    return evolution


"""
Main
"""
if __name__ == "__main__":
    # main()
    pass

