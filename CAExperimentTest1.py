#This is a working proof of concept for the CAExperiment class
#Lots of stuff to add/improve

from CAExperimentClass import *
import CA

CAExA1 = CAExperiment()
CAExA1.set_label("A1")


#create Wolfram Rule 30
wolfram_rule30_table = CA.make_rule_table(30,1)

CAExA1.set_rule(wolfram_rule30_table)
CAExA1.set_radius(1)

#randomly generate an initial ensemble of 100 configurations of length 100 
our_init_ensemble = CA.random_initial_ensemble(100,100)
CAExA1.set_init_ensemble(our_init_ensemble)
#CAExA1.set_config_length(100)

#set the number of generations
CAExA1.set_num_generations(10)

#define the functions whose measurements we want to take.
#typically these would be written in a separate module rather than
#being done in the experiment file

def rule_num(orbit):
    return 30

def rule_radius(orbit):
    return 1

def init_config_num(orbit):
    return CA.bin_to_dec(orbit[0])

def config_length(orbit):
    return 100

#This just returns the density of the initial configuration
def init_config_density(orbit):
    init_density = CA.config_density(orbit[0])
    return init_density

#this is a basic measurement of how the configuration density changed
#across the iterations

def config_density_change(orbit):
    init_density = CA.config_density(orbit[0])
    final_density = CA.config_density(orbit[-1])
    density_change = final_density - init_density
    return density_change

#set the function list and the variables to use
CAExA1.set_func_list([rule_num, rule_radius, init_config_num, config_length,
                      init_config_density, config_density_change])
CAExA1.set_var_list(["rule_num", "rule_radius", "init_config_num",
                     "config_length","initial_density","configuration_density_change"])

#create the file
CAExA1report = open('CAEx1report.csv','w+')
CAExA1.set_report_file(CAExA1report)

#run the experiment and keep the findings 
CAExA1.run_experiment()
CAExA1.write_report()
print(str(CAExA1.measurement_log.head()))



