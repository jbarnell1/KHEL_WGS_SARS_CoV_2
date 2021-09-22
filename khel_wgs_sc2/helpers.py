from workflow.WF_1_import_demos.WF_1_import_demos import run_script_1
from workflow.WF_2_parse_run_data.WF_2_parse_run_data import run_script_2
from workflow.WF_3_compile_fasta.WF_3_compile_fasta import run_script_3
from workflow.WF_4_parse_nextclade.WF_4_parse_nextclade import run_script_4
from workflow.WF_5_parse_pangolin.WF_5_parse_pangolin import run_script_5
from workflow.WF_6_build_epi_report.WF_6_build_epi_report import run_script_6
from workflow.WF_7_send_epi_report.WF_7_send_epi_report import run_script_7
from workflow.WF_8_build_nextstrain.WF_8_build_nextstrain import run_script_8
from workflow.WF_9_send_fastas.WF_9_send_fastas import run_script_9
from workflow.epi_isl.epi_isl import run_epi_isl
from workflow.gisaid.gisaid import run_gisaid
from workflow.outside_lab.outside_lab import run_outside_lab
from workflow.plotter.plotter import run_plotter
from workflow.query.query import run_query
from workflow.refresh.refresh import run_refresh
import pyodbc
import time


def run():
    print("\n ___________________________________________________\n|  _______________________________________________  |\n| |\033[4m    SARS-CoV-2 daily workflow runner script    \033[0m| |\n|___________________________________________________|\n")
    ask = True
    day = False
    while ask:
        u_input = input("\n\nIf you'd like to run the whole workflow, enter 'start'.\n\nIf you'd like to run just a part of the workflow:\nenter '1' to import demographics\
            \nenter '2' to parse the clearlabs run data\nenter '3' to compile the fasta file\nenter '4' to parse the nextclade file\nenter '5' to parse the pangolin file\
            \nenter '6' to build the daily epi report\nenter '7' to send the daily epi report\nenter '8' to build a nextstrain report\nenter '9' to build a passing fasta file for a given date\
            \n\nOther options:\
            \nenter 'refresh' to roll back the database to the most current version of an excel file\nenter 'plotter' to get an interactive dashboard of the database\
            \nenter 'query' to get a specific snapshot of the database\
            \nenter 'outside lab' to import a data template submitted from an outside lab\nenter 'gisaid' to produce template and fasta files from a list of hsn's\
            \nenter 'epi isl' to update all isl numbers for samples submitted to gisaid\n\nenter 'q' to quit\n--> ")
        try:
            if u_input.strip().lower() == 'start':
                tracker = 1
                while True:
                    try:
                        # run script
                        if tracker == 1:
                            run_script_1()
                            tracker += 1
                        elif tracker == 2:
                            day = run_script_2()
                            tracker += 1
                        elif tracker == 3:
                            compiled_fasta_path = run_script_3()
                            tracker += 1
                        elif tracker == 4:
                            run_script_4(compiled_fasta_path)
                            tracker += 1
                        elif tracker == 5:
                            run_script_5(compiled_fasta_path)
                            tracker += 1
                        else:
                            print("\n ___________________________________________________\n|  _______________________________________________  |\n| |\033[4m      SARS-CoV-2 daily workflow complete!      \033[0m| |\n|___________________________________________________|\n")
                            break

                    # catch errors and perform logic here
                    except pyodbc.IntegrityError as i:
                        print(i)
                        print("\nThis usually happens when the run data has already been imported into the database")
                        time.sleep(5)
                    except Exception as i:
                        print(i)
                        time.sleep(5)

            elif u_input.strip().lower() == '1':
                # run script
                run_script_1()
                
            elif u_input.strip().lower() == '2':
                # run script
                run_script_2()
                
            elif u_input.strip().lower() == '3':
                # run script
                run_script_3()
                
            elif u_input.strip().lower() == '4':
                # run script
                run_script_4("single_step")
                
            elif u_input.strip().lower() == '5':
                # run script
                run_script_5("single_step")
                
            elif u_input.strip().lower() == '6':
                run_script_6()
                
            elif u_input.strip().lower() == '7':
                run_script_7()
                
            elif u_input.strip().lower() == '8':
                run_script_8()

            elif u_input.strip().lower() == '9':
                run_script_9(day)
            
            elif u_input.strip().lower() == 'refresh':
                # run script
                run_refresh()

            elif u_input.strip().lower() == 'plotter':
                # run script
                run_plotter()
                
            elif u_input.strip().lower() == 'query':
                # run script
                run_query()
                
            elif u_input.strip().lower() == 'outside lab':
                # run script
                run_outside_lab()

            elif u_input.strip().lower() == 'gisaid':
                # run script
                run_gisaid()
            
            elif u_input.strip().lower() == 'epi isl':
                # run script
                run_epi_isl()
                
            elif u_input.strip().lower() == 'q':
                ask = False
            
            else:
                raise ValueError("Invalid input!")

        except Exception as i:
            print(i, str(type(i)))
            time.sleep(2)
            
            