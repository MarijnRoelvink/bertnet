import scripts.relation as sr
import re

class Node:
    def __init__(self, name, model = None, wm = None, q = None):
        self.name = name
        self.relations = {}
        self.model = model
        self.wm = wm
        self.q = q

    def addRelation(self, relation):
        if relation.key not in self.relations:
            self.relations[relation.key] = relation

    @staticmethod
    def isValid(node):
        isValid = re.match("\W", node) is None
        isValid = isValid and node != ""
        return isValid

    def addAssociations(self, type, mask, nodes, relations, fro = True):
        associations = self.model(mask, top_k=40)
        res = []
        for x in associations:
            node = x["token_str"].replace(" ", "").lower()
            if(Node.isValid(node)):
                #Add word to node list if it didn't exist
                if (not node in nodes):
                    nodes[node] = Node(node, self.model, self.wm, self.q)
                    self.q.put(node)
                rel = sr.Relation(type, nodes[node], self, x["score"])
                if fro:
                    rel = sr.Relation(type, self, nodes[node], x["score"])
                rel.calcWmScore(self.wm)
                rel.calcFinalScore()
                res.append(rel)

        res = self.filterRelations(res)
        for rel in res:
            if rel.key not in self.relations:
                relations.append(rel)
                rel.addToNodes()




    def findRelations(self, relation_types, nodes, relations):
        #Only use relation types with masks
        types = filter(lambda x: len(x.masks) > 0, relation_types)
        for type in types:
            # MASK - relation - OBJECT
            masks = type.getMasks(self.model.tokenizer.mask_token, self.name)
            for mask in masks:
                self.addAssociations(type, mask, nodes, relations, fro = False)
            masks = type.getMasks(self.name, self.model.tokenizer.mask_token)
            for mask in masks:
                self.addAssociations(type, mask, nodes, relations)

    def filterRelations(self, rels):
        res = filter(lambda x: x.wm_score > 0.99, rels)
        res = filter(lambda x: x.final > 0.1, res)
        return list(res)