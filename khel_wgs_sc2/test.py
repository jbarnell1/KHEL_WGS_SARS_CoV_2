import re
import json
import os

class workflow_obj():

    def __init__(self, u_input):
        self.u_input = u_input

    def get_json(self):
        print("Importing data from cache...")
        # get relative path to json cache file
        dirname = os.path.dirname(os.path.abspath(__file__))
        folders = dirname.split("\\")
        top_pkg_folder = "\\".join(folders[0:-1])
        path_to_cache = top_pkg_folder + "\\data\\cache.json"

        with open(path_to_cache, 'r') as json_cache:
            full_cache = json.load(json_cache)
        working_cache = full_cache[u_input]
        for key, val in working_cache.items():
            if "query" in str(key):
                if not hasattr(self, key):
                    setattr(self, key, "".join(val))
            else:
                if not hasattr(self, key):
                    setattr(self, key, val)

if __name__ == "__main__":
#     s = "hello {1}, {0}"
#     print(s)
#     lst = [["l1.1", "l1.2"], ["l2.1", "l2.2"]]
#     # lst_dict = {'{0}':0, '{1}':1}
#     # for i in range(len(lst)):
#     #     new_s = s
#     #     for key in lst_dict.keys():
#     #         new_s = new_s.replace(key, lst[i][lst_dict[key]])
#     #     print(new_s)



#     # for i in range(len(lst)):
#     #     my_string = s
#     #     mapping = [ ('{0}', 0), ('{1}', 1 )]
#     #     for k, v in mapping:
#     #         my_string = my_string.replace(k, lst[i][v])
#     #     print(my_string)



# ####################### THIS ONE ##############################################
#     # lst_trak = ['{0}', '{1}']
#     lst_trak = re.findall("({.*?})", s)
#     for i in range(len(lst)):
#         fin = s
#         for item in lst_trak:
#             fin = fin.replace(item, lst[i][int(item[1])])
#         print(fin)
    u_input = input("enter a workflow name:\n-->")
    obj = workflow_obj(u_input)
    obj.get_json()
    
    print(obj.__dict__)


