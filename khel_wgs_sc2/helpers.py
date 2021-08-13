from workflow.WF_1_import_demos.WF_1_import_demos import run_script_1
from workflow.WF_2_parse_run_data.WF_2_parse_run_data import run_script_2
from workflow.WF_3_compile_fasta.WF_3_compile_fasta import run_script_3
from workflow.WF_4_parse_nextclade.WF_4_parse_nextclade import run_script_4
from workflow.WF_5_parse_pangolin.WF_5_parse_pangolin import run_script_5
from workflow.WF_6_build_epi_report.WF_6_build_epi_report import run_script_6
from workflow.WF_7_send_epi_report.WF_7_send_epi_report import run_script_7
from workflow.WF_8_build_nextstrain.WF_8_build_nextstrain import run_script_8
from workflow.epi_isl.epi_isl import run_epi_isl
from workflow.gisaid.gisaid import run_gisaid
from workflow.outside_lab.outside_lab import run_outside_lab
from workflow.query.query import run_query
from workflow.refresh.refresh import run_refresh
import pyodbc
import logging
import time


def config_logger(log_name):
    logger = logging.getLogger(__name__)
    # unfortunately, the script and IDE see the structure differently, so we have to force a try-except block here
    try:
        actual = 'ide'
        # IDE
        f_handler = logging.FileHandler('khel_wgs_sc2/khel_wgs_sc2/logs/' + log_name + '.txt', 'w+')
        actual = 'windows'
        # windows
        f_handler = logging.FileHandler('logs/' + log_name + '.txt', 'w+')
    except FileNotFoundError:
        if actual == 'ide':
            f_handler = logging.FileHandler('logs/' + log_name + '.txt', 'w+')
        else:
            f_handler = logging.FileHandler('khel_wgs_sc2/khel_wgs_sc2/logs/' + log_name + '.txt', 'w+')
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    logger.info("Logger configured.")
    return logger


def run(u_input):
    try:
        if u_input.strip().lower() == 'start':
            tracker = 1
            while True:
                try:
                    # configure logger
                    logger = config_logger('khel_wgs_sc2')
                    # run script
                    if tracker == 1:
                        run_script_1(logger)
                        tracker += 1
                    elif tracker == 2:
                        run_script_2(logger)
                        tracker += 1
                    elif tracker == 3:
                        run_script_3(logger)
                        tracker += 1
                    elif tracker == 4:
                        run_script_4(logger)
                        tracker += 1
                    elif tracker == 5:
                        run_script_5(logger)
                        tracker += 1
                    else:
                        print("\n ___________________________________________________\n|  _______________________________________________  |\n| |\033[4m      SARS-CoV-2 daily workflow complete!      \033[0m| |\n|___________________________________________________|\n")
                        return True

                # catch errors and perform logic here
                except pyodbc.IntegrityError as i:
                    print(i)
                    print("\nThis usually happens when the run data has already been imported into the database")
                    time.sleep(5)
                except Exception as i:
                    print(i)
                    time.sleep(5)

        elif u_input.strip().lower() == '1':
            # configure logger
            logger = config_logger('import_demos')
            # run script
            run_script_1(logger)
            return True

        elif u_input.strip().lower() == '2':
            # configure logger
            logger = config_logger('parse_run_data')
            # run script
            run_script_2(logger)
            return True

        elif u_input.strip().lower() == '3':
            # configure logger
            logger = config_logger('compile_fasta')
            # run script
            run_script_3(logger)
            return True

        elif u_input.strip().lower() == '4':
            # configure logger
            logger = config_logger('parse_nextclade')
            # run script
            run_script_4(logger)
            return True

        elif u_input.strip().lower() == '5':
            # configure logger
            logger = config_logger('parse_pangolin')
            # run script
            run_script_5(logger)
            return True

        elif u_input.strip().lower() == '6':
            # configure logger
            logger = config_logger('build_epi')
            run_script_6(logger)
            return True

        elif u_input.strip().lower() == '7':
            # configure logger
            logger = config_logger('send_epi')
            run_script_7(logger)
            return True

        elif u_input.strip().lower() == '8':
            # configure logger
            logger = config_logger('build_nextstrain')
            run_script_8(logger)
            return True

        elif u_input.strip().lower() == 'refresh':
            # configure logger
            logger = config_logger('refresh')
            # run script
            run_refresh(logger)
            return True
        
        elif u_input.strip().lower() == 'query':
            # configure logger
            logger = config_logger('query')
            # run script
            run_query(logger)
            return True
        
        elif u_input.strip().lower() == 'outside lab':
            # configure logger
            logger = config_logger('outside_lab')
            # run script
            run_outside_lab(logger)
            return True

        elif u_input.strip().lower() == 'gisaid':
            # configure logger
            logger = config_logger('gisaid')
            # run script
            run_gisaid(logger)
            return True

        elif u_input.strip().lower() == 'epi isl':
            # configure logger
            logger = config_logger('epi_isl')
            # run script
            run_epi_isl(logger)
            return True
        
        elif u_input.strip().lower() == 'q':
            return False
        
        else:
            raise ValueError("Invalid input!")

    except Exception as i:
        print(i)
        time.sleep(2)
        return True
        