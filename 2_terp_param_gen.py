import os

"""
this script will generate param files for the TERp program
"""

# modify these before executing
path_trans = "/Users/mehec/nlp/approbas/prj/data/"
path_output = "/Users/mehec/nlp/approbas/prj/terp_scores/"
output_formats = "sum param nist pra html"

if not os.path.isdir(path_output):
    os.makedirs(path_output)

list_trans = [trans for trans in os.listdir(
    path_trans) if trans[-6:] == ".trans"]

list_ref = [trans for trans in list_trans if trans[-9:-6] == "ref"]
list_hyp = [trans.replace("ref", "hyp") for trans in list_ref]

for i in range(len(list_ref)):
    text = "Reference File (filename)                : %s%s\n" % (
        path_trans, list_ref[i])
    text = "%sHypothesis File (filename)               : %s%s\n" % (
        text, path_trans, list_hyp[i])
    text = "%sOutput Formats (list)                    : %s\n" % (
        text, output_formats)
    text = "%sOutput Prefix (filename)                 : %sterp.%s." % (
        text, path_output, list_ref[i][:-10])
    with open("%s%s.param" % (path_output, list_ref[i][:-10]), "w") as f:
        f.write(text)
