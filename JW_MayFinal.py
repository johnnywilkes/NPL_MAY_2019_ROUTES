#!/usr/bin/env python3

#Sys is needed to input what file to parse.
import sys

#function to get filename from sys arguement else use a default time.
def txt_to_str():
    #If there is a sys argument assign to variable.
    if len(sys.argv) > 1:
        vf_str_filename = sys.argv[1]
    try:
        vf_text_file = open(vf_str_filename,'r')
    
    #if this fails, print error and then try default file ('20190506_Route_Sample_1.txt').
    except:
        print('Inputed file not found, trying default file')
        print('')
        
        try:
           vf_text_file = open('20190506_Route_Sample_1.txt','r')
        #If that fails, print error and exit program.
        except:
            print('Inputted and default files not found, please run program again and select correct file/directory!')
            exit()
    
    #if successful, return file in string format back to main.
    vf_str_ouput = vf_text_file.read()
    return(vf_str_ouput)

#function to use TextFSM and Pandas to parse information from string. this entire function is in a try/except block in main.  
def textfsm_it(vf_str_ouput):
    
    #open template file and store in variable.
    vf_text_template = open('template.txt')
    vf_TSFM_table = textfsm.TextFSM(vf_text_template)
    #parse string output using template and store in string.
    vf_list_data = vf_TSFM_table.ParseText(vf_str_ouput)
    #parse the headers from the TextFSM template.
    vf_list_headers = vf_TSFM_table.header
    
    #convert list infomration into pandas dataframe.
    vf_panda_df = pandas.DataFrame(vf_list_data,columns=vf_list_headers)
    #remove duplicate lines where network/mask are the same.
    vf_panda_update = vf_panda_df.drop_duplicates(subset=['MASK','NETWORK'],keep='first')
    
    #parse out the number of entries of each protocol type to place in results dictionary.
    vf_int_connect = len(vf_panda_update.loc[vf_panda_update['PROTOCOL']=='C'])
    vf_int_EIGRP = len(vf_panda_update.loc[vf_panda_update['PROTOCOL']=='D'])
    vf_int_local = len(vf_panda_update.loc[vf_panda_update['PROTOCOL']=='L'])
    vf_int_static = len(vf_panda_update.loc[vf_panda_update['PROTOCOL']=='S'])
    vf_int_OSFP  = len(vf_panda_update.loc[vf_panda_update['PROTOCOL']=='O'])
    vf_dict_count = {'Connected':vf_int_connect,'EIGRP':vf_int_EIGRP,'Local':vf_int_local,'Static':vf_int_static,'OSPF':vf_int_OSFP}
    
    #return results dictionary to main.
    return(vf_dict_count)

#simplified function that does string `count` method as a fallback.
def str_count(vf_str_ouput):
    #use `count` string method for find the number of instances of string patterns.
    vf_int_connect = vf_str_ouput.count('C  ')
    vf_int_EIGRP = vf_str_ouput.count('D  ')
    vf_int_local = vf_str_ouput.count('L  ')
    vf_int_static = vf_str_ouput.count('S  ') + vf_str_ouput.count('S* ')
    vf_int_OSFP = vf_str_ouput.count('O  ')
    
    #add results to ditionary and pass back to main.
    vf_dict_count = {'Connected':vf_int_connect,'EIGRP':vf_int_EIGRP,'Local':vf_int_local,'Static':vf_int_static,'OSPF':vf_int_OSFP}
    return(vf_dict_count)

#function to print results.
def print_stuff(vf_dict_count):
    print('Connected Routes:',vf_dict_count['Connected'])
    print('EIGRP Routes:',vf_dict_count['EIGRP'])
    print('Local Routes:',vf_dict_count['Local'])
    print('Static Routes:',vf_dict_count['Static'])
    print('OSPF Routes:',vf_dict_count['OSPF'])
    
#Main program.       
if __name__ == '__main__':
    #export txt file to python string.
    vm_str_ouput = txt_to_str()
    #try more advanced search function that require textfsm/pandas modules to be installed, else fallback to simple string search.
    try:
        import textfsm
        import pandas
        vm_dict_count = textfsm_it(vm_str_ouput)
    except:
        print('To get a better search function you need Pandas and TextFSM to be installed.  Please use `pip install pandas` and `pip install textfsm`. Also, please make sure the TextFSM template (template.txt) is in the local directory!')
        print('')
        vm_dict_count = str_count(vm_str_ouput)
    #print dictionary of results.
    print_stuff(vm_dict_count)
