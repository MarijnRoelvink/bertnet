import re
import os
import glob

class HTMLGenerator():

    def __init__(self, filePath = ".."):
        self.filePath = filePath

    def emptyOut(self):
        files = glob.glob('../out/*')
        for f in files:
            os.remove(f)

    def generateHTMLs(self, nodes, types):
        self.emptyOut()
        its = len(nodes)
        for k, n in nodes.items():
            self.generateHTML(n, types)
            its = its - 1
            if (its % 10 == 0):
                print(its)

    def generateHTML(self, node, types):
        file = open(f"{self.filePath}/resources/node_template.html", "r")
        contents = file.read()
        file.close()
        contents = contents.replace("$name$", node.name)
        contents = contents.replace("$relations$", "[" +  ", ".join([ f"{{'fro': '{x.fro.name}', 'to': '{x.to.name}', 'type': '{x.type.label}', 'score': {x.score}, 'wm_score': {x.wm_score}, 'final': {x.final}}}" for x in node.relations.values()]) + "]")
        contents = contents.replace("$relation_types$", "[" +  ", ".join([ f"{{'label': '{x.label}', 'info': '{x.info}', 'mask': '{x.mask}'}}" for x in types]) + "]")

        res = open(f"{self.filePath}/out/{node.name}.html", "w")
        res.write(contents)
        res.close()

    def generateHTMLLoop(self, contents, arr, arr_label):
        arr_vars = []
        if(len(arr) > 0):
            arr_vars = arr[0].keys()
        loop_part = contents.split(f"$for:{arr_label}$")[1].split(f"$endfor:{arr_label}$")[0]
        loop_parts = ""
        for x in arr:
            loop_str = loop_part
            for arr_var in arr_vars:
                loop_str = loop_str.replace(f"${arr_label}.{arr_var}$", x[arr_var])
            loop_parts = loop_parts + "\n" + loop_str
        contents = re.sub(r"\$for:relations\$[\s\S]*\$endfor:relations\$", loop_parts, contents)
        return contents