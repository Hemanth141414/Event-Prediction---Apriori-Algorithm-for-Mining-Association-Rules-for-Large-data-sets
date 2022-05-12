import csv
import sys
import collections

from itertools import combinations

class AssociationRuleApriori:
    def __init__(self, marketBaskets, minSupport, minConf):
        self.marketBaskets = marketBaskets
        self.itemSetSupp = collections.defaultdict(int)
        self.itemSetL = []
        self.minSupport = minSupport
        self.minConf = minConf
        self.AssoaRules = []

    def AprioriFunc(self, lk):
        ck = set()
        for iele in lk:
            i = set(iele)
            for jele in lk:
                j = set(jele)
                common = i.intersection(j)
                if len(common) == len(j) - 1:
                    jthItem = j.difference(common).pop()
                    ithItem = i.difference(common).pop()
                    if ithItem < jthItem:
                        #candidate = frozenset(i.add(jthItem))
                        iret = set(iele)
                        iret.add(jthItem)
                        candidate = tuple(sorted(iret))
                        ck.add(candidate)
        return ck
        
    def CalcSupp(self, candidate):
        count = 0
        #ckey = ",".join(c)
        if candidate in self.itemSetSupp:
            return self.itemSetSupp[candidate]
        for basket in self.marketBaskets:
            trig = True
            for item in candidate:
                if item not in basket:
                    trig = False
                    break
            if trig:
                count = count + 1
        supp = float(count) / len(self.marketBaskets)
        self.itemSetSupp[candidate] = supp
        return supp

    def computeAscRule(self):
        for itemset in self.itemSetL:
            if not len(itemset) <= 1:
                possCandis = combinations(itemset, len(itemset) - 1)
                for possCdt in possCandis:
                    rCdt = tuple(set(itemset).difference(set(possCdt)))
                    conf = self.itemSetSupp[itemset] / self.itemSetSupp[possCdt]
                    if conf >= self.minConf:
                        lCdt = ', '.join(possCdt)
                        aRule = "[{}] => [{}]".format(lCdt, rCdt[0])
                        self.AssoaRules.append([aRule, conf, self.CalcSupp(itemset)])
        if len(self.AssoaRules) > 0:
            self.AssoaRules.sort(reverse = True, key = self.ruleSort)

    def ruleSort(self, e):
        return e[1]

    def ExecApriori(self):
        lk = set()
        retSet = list()
        firstTime = True
        itemSet = set()
        for basket in self.marketBaskets:
            for item in basket:
                itemSet.add(item)
        ck = self.getCandidateC1(itemSet)      
        while True:
            if not firstTime:
                ck = self.AprioriFunc(lk)
            firstTime = False    
            lkApr = set()
            for candidate in ck:
                candiSupp = self.CalcSupp(candidate)
                if  candiSupp >= self.minSupport:
                    lkApr.add(candidate)
                    retSet.append(candidate)

            lk = lkApr
            if len(lk) < 1:
                break
        retSet.sort(reverse = True, key = self.myFunc)
        self.itemSetL = retSet

    def getCandidateC1(self, itemSet):
        c1 = set()
        for item in itemSet:
            #adding initial elememts as tuples with(,) as set only takes iterable which is encountered later.
            c1.add((item,))
        return c1
        
    
    def myFunc(self, e):
        return self.CalcSupp(e)
        
    

def fileRead(filename):
    marketBaskets = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            if reader.line_num > 1:
                marketBaskets.append(row)
    return marketBaskets


def fileWrite(minSup, minConf, itemSetL, AssoaRules):
    with open('output.txt', 'wt') as out:
        minsupp = float(minSup)*100
        freqMessage = "==Frequent itemsets (min_sup={0}%)\n".format(minsupp)
        out.write(freqMessage)
        for itemSet in itemSetL:
            itemMessage = ", ".join(itemSet)
            itemSupp = ara.CalcSupp(itemSet)*100
            freqMessage = "[{0}], {1:.3f}%".format(itemMessage, itemSupp)
            out.write(freqMessage + '\n')
        out.write("\n")
        minconf = float(minConf)*100
        confMessage = "==High-confidence association rules (min_conf={0}%)\n".format(minconf)
        out.write(confMessage)
        for rule in AssoaRules:
            aRule = rule[0] 
            conf = rule[1]*100
            sup = rule[2]*100
            confMessage = "{0} (Conf: {1:.3f}%, Supp: {2:.3f}%)".format(aRule, conf, sup)
            out.write(confMessage + '\n')


if __name__ == "__main__":
    filename = sys.argv[1]
    minSupportp = float(sys.argv[2])
    minConf = float(sys.argv[3])
    marketBaskets = fileRead(filename)
    ara = AssociationRuleApriori(marketBaskets, minSupportp, minConf)
    ara.ExecApriori()
    ara.computeAscRule()
    fileWrite(minSupportp, minConf, ara.itemSetL, ara.AssoaRules)
