class Relation:
    def __init__(self, type, fro, to, score, wm_score=0):
        self.type = type
        self.fro = fro
        self.to = to
        self.score = score
        self.key = f"{type.label}-{fro.name}-{to.name}"
        self.wm_score = wm_score

    def toDict(self):
        return {"fro" : self.fro.name,
                "to": self.to.name,
                "key": self.key,
                "type": self.type.label,
                "score": self.score,
                "wm_score": self.wm_score}

    def calcWmScore(self, wm):
        self.wm_score = wm.checkSim(self.fro.name, self.to.name)

    def calcFinalScore(self):
        a = 0.7
        self.final = self.score*a + (1-a)*self.wm_score

    def remove(self):
        self.fro.relations.remove(self)
        self.to.relations.remove(self)

    def addToNodes(self):
        self.fro.addRelation(self)
        self.to.addRelation(self)

class RelationType:
    def __init__(self, label, description, masks):
        self.label = label
        self.info = description.replace("\'", "")
        self.masks = masks
        self.mask = ""
        if len(masks) > 0:
            self.mask = masks[0]

    def getMasks(self, object1, object2):
        return [mask.replace("OBJECT1", object1)
                    .replace("OBJECT2", object2)
                for mask in self.masks]