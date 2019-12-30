import os
from subprocess import Popen, PIPE

"""
this script will run the TERp program according to one or multiple param files
"""

# modify these before executing
path_param = "/Users/mehec/nlp/approbas/prj/terp_scores/"
path_terp = "/Users/mehec/nlp/approbas/prj/terp-master/bin/"
mode_terp = "terp"


list_param = [param for param in os.listdir(
    path_param) if param[-6:] == ".param"]


for param in list_param:
    res = Popen("%s%s %s%s" % (path_terp, mode_terp, path_param, param),
                stdout=PIPE, shell=True).stdout.read()
    print(res)
