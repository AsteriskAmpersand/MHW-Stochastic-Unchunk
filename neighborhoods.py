# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:39:19 2020

@author: AsteriskAmpersand
"""

transitionGraph = {
        0:set([0, 13, 3, 9, 10]),
        1:set([5, 1, 14, 7, 12]),
        2:set([11, 8, 2, 5, 6]),
        3:set([0, 3, 9, 13, 15]),
        4:set([12, 10, 4, 13, 7]),
        5:set([8, 5, 1, 14, 2]),
        6:set([9, 6, 11, 15, 2]),
        7:set([1, 7, 12, 14, 4]),
        8:set([2, 11, 5, 8, 14]),
        9:set([3, 6, 9, 15, 0]),
        10:set([4, 0, 13, 10, 12]),
        11:set([6, 2, 11, 8, 15]),
        12:set([7, 4, 12, 10, 1]),
        13:set([10, 0, 13, 3, 4]),
        14:set([5, 7, 1, 14, 8]),
        15:set([9, 6, 15, 11, 3]),
     }
sortedTuple = lambda x: tuple(sorted(list(x)))
def remove(setV,item):
    setV.remove(item)
    return setV
def omit(family):
    return set((sortedTuple(remove(set(family),element))for element in family))

neighborhood1 = {t:set([e for n in transitionGraph[t] 
                            for e in transitionGraph[n]])
                for t in transitionGraph}
neighborhood2 = {t:set([e for n in neighborhood1[t] 
                            for e in transitionGraph[n]])
                for t in neighborhood1}
neighborhood3 = {t:set([e for n in neighborhood2[t] 
                            for e in transitionGraph[n]])
                for t in neighborhood2}
neighborhood4 = {t:set([e for n in neighborhood3[t] 
                            for e in transitionGraph[n]])
                for t in neighborhood3}
neighborhoods = [{t:set([t]) for t in transitionGraph},
                neighborhood1,neighborhood2,neighborhood3,neighborhood4
                ]

class neighborhood(set):
    def unitary(self):
        return len(self)==1
            
def centeredNeighborhood(center,degree = None):
        if degree is None:
            return neighborhood(neighborhood1[center])
        else:
            degree = min(degree,4)
            return neighborhood(neighborhoods[degree][center])
cn = centeredNeighborhood

def generateInvertedContention():
    paterSet = {sortedTuple(transitionGraph[t]):[t] for t in transitionGraph}
    for t in transitionGraph:
        previous = [transitionGraph[t]]
        for _ in range(5):
            np = []
            for tupling in previous:
                anterior = omit(tupling)
                for group in anterior:
                    if t in group:
                        np.append(group)
                        if group not in paterSet:
                            paterSet[group]=set()
                        paterSet[group].add(t)
            previous = np
    return paterSet

invertedContention = generateInvertedContention()
 
def inverseSolve(neighboringSet):
    return invertedContention[sortedTuple(neighboringSet)]