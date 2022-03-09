import ast
import scripts.node as sn
from scripts.relation import *
from scripts.word_model import *
from scripts.bert import *
from queue import Queue
import scripts.html_generator as gen
import matplotlib.pyplot as plt
import numpy as np


def loadDict(filename):
    file = open(filename, "r")
    contents = file.read()
    file.close()

    dictionary = ast.literal_eval(contents)
    return dictionary

def init(model, wm, fileLoc=".."):
    nodes = loadDict(f"{fileLoc}/resources/words.txt")
    q = Queue()
    for node in nodes.keys():
        nodes[node] = sn.Node(node, model, wm, q)

    relation_types = loadDict(f"{fileLoc}/resources/relations.txt")
    relation_types = list(map(lambda x: RelationType(x, relation_types[x]["description"], relation_types[x]["masks"]), relation_types.keys()))
    relations = []

    keys = list(nodes.keys())
    print(keys)
    its = 0
    for k in keys:
        q.put(k)

    while not q.empty() and its < 2000:
        key = q.get()
        n = nodes[key]
        n.findRelations(relation_types, nodes, relations)
        its = its + 1
        if (its % 10 == 0):
            print(its)

    # for key in keys:
    #     n = nodes[key]
    #     n.findRelations(relation_types, nodes, relations)
    #     its = its - 1
    #     if(its % 10 == 0):
    #         print(its)

    writeRelationsToFile(relations, "../relations_saved.txt")
    htmlgen = gen.HTMLGenerator(fileLoc)
    htmlgen.generateHTMLs(nodes, relation_types)

def getStatistics(relations):
    print(np.cov([x.score for x in relations], [x.wm_score for x in relations]))
    print(np.corrcoef([x.score for x in relations], [x.wm_score for x in relations]))
    plt.scatter([x.score for x in relations], [x.wm_score for x in relations])
    plt.show()

def getTestObject():
    n = sn.Node("kitchen")
    items = ["knife", "cabinet", "stove", "microwave"]
    type = RelationType("AtLocation", "", "")
    nodes = [n]
    relations = []
    for i in items:
        ni = sn.Node(i)
        r = Relation(type, ni, n, 0)
        n.addRelation(r)
        nodes.append(ni)
        relations.append(r)
    return n, nodes, relations

def writeRelationsToFile(relations, filename):
    file = open(filename, "w")
    rep = [r.toDict() for r in relations]
    str_rep = repr(rep)
    file.write(str_rep)
    file.close()

def loadRelations(filename):
    loaded = loadDict(filename)
    relation_types = loadRelationTypes()
    relations = {}
    nodes = {}
    for r in loaded:
        if(not r["fro"] in nodes):
            nodes[r["fro"]] = sn.Node(r["fro"])
        if (not r["to"] in nodes):
            nodes[r["to"]] = sn.Node(r["to"])
        rel = Relation(relation_types[r["type"]], nodes[r["fro"]], nodes[r["to"]], r["score"], r["wm_score"])
        rel.calcFinalScore()
        rel.addToNodes()
        relations[rel.key] = rel
    return nodes, relations.values()

def loadRelationTypes():
    relation_types = loadDict("../resources/relations.txt")
    relation_types = {x: RelationType(x, relation_types[x]["description"],
                                   relation_types[x]["masks"]) for x in relation_types.keys()}
    return relation_types


if __name__ == "__main__":
    file = "../relations_saved.txt"

    wm = WordModel()
    wm.loadWv()
    model = BertModel().model
    init(model, wm)

    # nodes, relations = loadRelations(file)
    # relation_types = loadRelationTypes()
    # print(len(nodes))
    # print(len(relations))

    # htmlgen = gen.HTMLGenerator()
    # htmlgen.generateHTMLs(nodes, [type for k, type in relation_types.items()])

    # getStatistics(relations)
    # writeRelationsToFile(relations, file)

    # n, nodes, relations = getTestObject()
    # writeRelationsToFile(relations, file)
