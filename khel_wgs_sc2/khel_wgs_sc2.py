from helpers import *

if __name__ == "__main__":
    print("\n ___________________________________________________\n|  _______________________________________________  |\n| |\033[4m    SARS-CoV-2 daily workflow runner script    \033[0m| |\n|___________________________________________________|\n")
    ask = True
    while ask:
        u_input = input("\n\nIf you'd like to run the whole workflow, enter 'start'.\n\nIf you'd like to run just a part of the workflow:\nenter '1' to import demographics\
            \nenter '2' to parse the clearlabs run data\nenter '3' to compile the fasta file\nenter '4' to parse the nextclade file\nenter '5' to parse the pangolin file\
            \nenter '6' to build the daily epi report\nenter '7' to send the daily epi report\nenter '8' to build a nextstrain report\n\nOther options:\
            \nenter 'refresh' to roll back the database to the most current version of an excel file\nenter 'query' to get a specific snapshot of the database\
            \nenter 'outside lab' to import a data template submitted from an outside lab\nenter 'gisaid' to produce template and fasta files from a list of hsn's\
            \nenter 'epi isl' to update all isl numbers for samples submitted to gisaid\n\nenter 'q' to quit\n--> ")
        ask = run(u_input)
        

