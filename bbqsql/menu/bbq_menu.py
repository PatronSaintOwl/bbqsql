import bbqsql

from bbqcore import bcolors
from config import RequestsConfig,bbqsqlConfig
import text
import bbqcore

try:
    import readline
except ImportError:
    pass

from copy import copy

# config params that are only used in the menu and shouldn't be passed along to BlindSQLi or other parts of bbqsql
exclude_parms = ['csv_output_file']

# main menu
class bbqMenu:
    def __init__(self):
        try:
            requests_config = RequestsConfig()
            bbqsql_config = bbqsqlConfig()

            results = None
            valid = False

            # intitial user menu
            choice = ''
            while choice not in ['99',99,'quit','exit']:
                bbqcore.show_banner()
                show_main_menu = bbqcore.CreateMenu(text.main_text, text.main_menu)
         
                 # special case of list item 99
                print '\n  99) Exit the bbqsql injection toolkit\n'
                
                rvalid = requests_config.validate()
                bvalid = bbqsql_config.validate()
                valid = rvalid and bvalid

                if results: print results

                # mainc ore menu
                choice = (raw_input(bbqcore.setprompt()))

                if choice == '1':
                    requests_config.run_config()
                
                if choice == '2':
                    bbqsql_config.run_config()
                
                if choice == '3':
                    attack_config = {}
                    attack_config.update(requests_config.get_config())
                    attack_config.update(bbqsql_config.get_config())
                    # now export attack_config to file

                if choice == '4':
                    #somehow populate this VVV tmp_config dict with stuff from file
                    tmp_config = dict()
                    bbqsql_config.set_config(tmp_config)
                    requests_config.set_config(tmp_config)
                
                if choice == '5' and valid:                                    
                    # clear out results
                    results = None

                    # combine them into one dictionary
                    attack_config = {}
                    attack_config.update(requests_config.get_config())
                    attack_config.update(bbqsql_config.get_config())
                    #delete unwanted config params before sending the config along
                    for key in exclude_parms:
                        if key in attack_config:
                            del(attack_config[key])
                    # launch attack
                    bbq = bbqsql.BlindSQLi(**attack_config)
                    results = bbq.run()
                    #output to a file if thats what they're into
                    if bbqsql_config['csv_output_file']['value'] is not None:
                        f = open(bbqsql_config['csv_output_file']['value'],'w')
                        f.write("\n".join(results))
                        f.close()
                    # delete stuff
                    del(bbq)

            bbqcore.ExitBBQ(0)
            
        # ## handle keyboard interrupts
        except KeyboardInterrupt:
            print "\n\n Cath you later " + bbqcore.bcolors.RED+"@" + bbqcore.bcolors.ENDC+" the dinner table."


if __name__ == '__main__':
    bbqMenu()
