import CA
import pandas as pd
from numpy import arange


class CAExperiment(object):
    #label -- what we are calling this particular experiment (corresponds to what we have in the .pdf file)
    #rule -- the CA rule to use
    #rule_radius -- the radius for the CA file
    #initial_ensemble -- the list of initial configurations to use
    #config_length -- the length of each configuration in the ensemble
    #num_generations -- the number of generations to run the CA
    #func_list -- the functions to apply to the spacetime diagrams
    #var_list -- a list of the variable name for each function (crucial)
    #measurement_log -- a data frame holding the relevant measurements from each spacetime diagram
    #report_file -- the .csv file to which we write the report

    def __init__(self,label=None,rule=None,rule_radius=0,init_ensemble = [],config_length=0,num_generations = 0,
                 func_list=[], var_list=[],measurement_log=[],report_file=None):
        self.label = label
        self.rule = rule
        self.rule_radius=rule_radius
        self.init_ensemble = init_ensemble
        self.config_length = config_length
        self.num_generations = num_generations
        self.func_list=func_list
        self.var_list = var_list
        self.measurement_log = pd.DataFrame()
        self.measurement_log.columns = var_list
        self.report_file = report_file

    def set_label(self,label_to_use):
        '''
        set_label, sets the label we want

        ARGS:
        label_to_use, the label that we want to use for this experiment

        RETURNS:

        '''
        self.label = label_to_use

    def get_label(self):
        return self.label

    #TODO: make it  set radius also. 

    def set_rule(self,rule_list):
        '''
        set_rule_list, sets the rules in the rule_list

        ARGS:
        rule_list, a list of CA rules to use in the experiment

        RETURNS:

        '''
        self.rule = rule_list
        self.rule_number = CA.bin_to_dec(rule_list)

    
        
    def get_radius(self):
        '''
        get_rule_list, returns the current list of rules in the experiment

        ARGS:


        RETURNS:
        rule_list, a list of CA rules to use in the experiment

        '''
        return self.radius

    def set_radius(self,radius):
        '''
        set_rule_list, sets the rules in the rule_list

        ARGS:
        rule_list, a list of CA rules to use in the experiment

        RETURNS:

        '''
        self.radius = radius
        
    def get_rule(self):
        '''
        get_rule_list, returns the current list of rules in the experiment

        ARGS:


        RETURNS:
        rule_list, a list of CA rules to use in the experiment

        '''
        return self.rule

    
    def get_num_generations(self):
        '''
        get_init_ensemble, returns the current ensemble being used

        ARGS:

        RETURNS:
        init_ensemble, a list of configurations being used as the initial configurations in the experiment
        '''
        return self.num_generations

    def set_num_generations(self, num_generations):
        '''
        set_init_ensemble, sets the rules in the init_ensemble

        ARGS:
        initial_ensemble, a list of configurations to use  as initial configurations in the experiment

        RETURNS:

        '''
        self.num_generations = num_generations

    def set_init_ensemble(self, init_ensemble):
        '''
        set_init_ensemble, sets the rules in the init_ensemble

        ARGS:
        initial_ensemble, a list of configurations to use  as initial configurations in the experiment

        RETURNS:

        '''
        self.init_ensemble = init_ensemble
        self.config_length = len(init_ensemble[0])


    def get_initial_ensemble(self):
        '''
        get_init_ensemble, returns the current ensemble being used

        ARGS:

        RETURNS:
        init_ensemble, a list of configurations being used as the initial configurations in the experiment
        '''
        return self.initial_ensemble

    def read_initial_ensemble(self, init_ensemble_file):
        '''
        read_init_ensemble, takes an input file (.txt) of numbers and converts those to configurations

        ARGS:
        init_ensemble, a file object containing configurations being used as the initial configurations in the experiment
        first line should be configuration length

        RETURNS:

        '''
        #reset the ensemble since it is going to be whatever is in the file
        self.init_ensemble = []
        temp_ensemble = []
        f = init_ensemble_file.readlines()
        #the first line should be the configuration length
        config_length_to_use = f[0]
        #set the configuration length of the object
        self.config_length = config_length_to_use
        for i in range(1,len(f)):
            #first get the config number
            config_num = int(f[i])
            config_to_add = CA.make_config(config_num, config_length_to_use)
            temp_ensemble.append(config_to_add)
        self.set_init_ensemble(temp_ensemble)



    def write_initial_ensemble(self, init_ensemble_file):
        '''
        write_init_ensemble, takes a list of configurations and writes them to a file

        ARGS:
        init_ensemble_file, a file to which the configuration numbers should be written
        RETURNS:

        '''
        pass

    #TODO: functions to get, set, read, write list of functions to write
    #TODO: function to add functions to a function list (useful if, for instance, iterating over rows or columns in the space time diagram)
    #these will need to be python -- isn't another good way to store them
    #pickle if intending to reuse functions (NOTE: be careful with pickle! never run untrusted pickled code!)
    #each function also needs a variable list
    #the variable list should be added at the same time as the function, and should be a list of the same size as the ouput of the function

    def set_func_list(self, func_list):
        '''
        set_func_list, takes a list of functions and makes it be the set of functions we are using

        ARGS:
        func_list, a list of functions to use

        RETURNS:

        '''
        self.func_list = func_list

    def get_func_list(self):
        '''
        get_func_list, gives the list of functions currently being used

        ARGS:

        RETURNS:
        func_list, the list of functions being used
        '''
        return self.func_list

    def read_func_list(self, pickled_file):
        '''
        read_func_list, takes a list of

        ARGS:

        RETURNS:
        func_list, the list of functions being used
        '''
        pass

    def write_func_list(selfself,pickled_file):
        pass

    def add_func(self, func_to_add, var_to_add):
        '''
        add_func, add a function to the current func_list

        ARGS: func, a function to add

        RETURNS:

        '''
        append(self.func_list,func_to_add)
        append(self.var_list, var_to_add)

    def add_funcs(self,funcs_to_add,vars_to_add):
        '''
        add_funcs, add a list of functions to the current func_list

        ARGS: func, a function to add

        RETURNS:

        '''
        self.func_list =  self.func_list + funcs_to_add
        self.vars_list = self.vars_list + vars_to_add

    #TODO: Also need to get and set variable names.
    #When setting, it should change the "columns" attribute of measurement_log

    def set_var_list(self,var_list):
        self.var_list = var_list
        self.measurement_log = pd.DataFrame(columns=var_list)

    def get_var_names(self,vars_list):
        return vars_list

    def set_report_file(self,report_file):
        self.report_file = report_file

    def get_report_file(self,report_file):
        return self.report_file

    #I think we should be able to combine the
    #run experiment and log measurements function, so
    #that running an experiment automatically logs the measurements. 

    def run_experiment(self):
        '''
        run_experiment, creates a list of spacetime diagrams for a set of rules and initial configurations

        ARGS: func, a function to add

        RETURNS: data_log, a list of space-time diagrams for these initial configurations

        '''
        rule_to_use=self.rule
        radius_to_use = self.radius
        init_ensemble_to_use = self.init_ensemble
        data_log = []
        for config in init_ensemble_to_use:
            data = CA.evolve(rule_to_use,self.rule_radius,config,self.config_length,self.num_generations)
            data_log.append(data)
        #now we log the measurements, determined by functions
        temp_measurement_log = pd.DataFrame(columns=self.var_list,index=arange(0,len(data_log)))
        #loop over each spacetime diagram in the experiment log
        #create counter for data frame location (row number)
        i = 0
        for diagram in data_log:
            #create a row with necessary information for header
            #this could probably be handled better.
            row_to_add = []
            #for each function, evaluate it on the diagram
            for func in self.func_list:
                data_to_add = func(diagram)
                #check to see how to add it on
                if data_to_add is list:
                    row_to_add = row_to_add + data_to_add
                else:
                    row_to_add.append(data_to_add)
            #add the row to the data set
            temp_measurement_log.loc[i] = row_to_add
            #increment the variable to keep the row index correct
            i = i + 1
        self.measurement_log = temp_measurement_log
        return temp_measurement_log

        
    def log_measurements(self,experiment_log):
        #we will always start with the rule number, the radius, the configuration number, and the configuration length
        #I am thinking that we can do away with this
        # if the experimenter wants to add these vars, they can do it themselves
        set_vars = ['rule','radius','config','config_length']
        #add the experimenter's defined variables onto the list
        useful_vars = set_vars + self.var_list

        temp_measurement_log = pd.DataFrame(columns=useful_vars,index=arange(0,len(experiment_log)))
        #loop over each spacetime diagram in the experiment log
        #create counter for data frame location (row number)
        i = 0
        #certain things will always be in the row, determined by set_vars
        for diagram in experiment_log:
            #create a row with necessary information for header
            #this could probably be handled better.
            row_to_add = [self.rule, self.radius, diagram[0], len(diagram[0])]
            #for each function, evaluate it on the diagram
            #todo: Gracefully catch errors and avoid adding them to log.
            for func in self.func_list:
                data_to_add = func(diagram)
                #check to see how to add it on
                if data_to_add is list:
                    row_to_add = row_to_add + data_to_add
                else:
                    row_to_add.append(data_to_add)
            #add the row to the data set
            temp_measurement_log.loc[i] = row_to_add
            #increment the variable to keep the row index correct
            i = i + 1
        self.measurement_log = temp_measurement_log
        return temp_measurement_log

    def write_report(self, file_to_write=None):
        #if no file is supplied, use the label to create the file name
        if file_to_write == None:
            if self.report_file==None:
               name_to_write = str(self.label) + ".csv"
               file_to_write = open(name_to_write, 'w+')
            else:
                file_to_write = self.report_file
        #TODO: Write code to delete column counting all rows.
        self.measurement_log.to_csv(file_to_write)
        


