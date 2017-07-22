from numpy import *
from math import log
import treePlotter
#计算香浓熵 -sum(p*log(p))
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
        shannonEnt = 0.0
        for key in labelCounts:
            #计算类别概率
            prob = float(labelCounts[key])/numEntries
            shannonEnt -= prob *log(prob,2)
    return shannonEnt

#创建测试数据集
def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet, labels

#按照给定特征划分数据集
def splitDataSet(dataSet,axis,value):
    retDataSet = [] #创建新的list对象
    #可以看出去掉了选定特征数据集
    for featVec in  dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

#通过最大化信息增益
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        #取一列数据
        featList = [example[i] for example in dataSet]
        #转为set,创建唯一的分类标签
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

#多数表决法决定叶子节点归属
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(),key = lambda item:item[1],reverse= 1)
    return sortedClassCount[0][0]

#创建树的函数代码
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    #count统计出现某字符的次数，如果标签一致那么次数和样本数相等，返回
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    #只有一类数据的时候（无法划分）：多数表决法
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    #挑选划分特征
    bestFeat = chooseBestFeatureToSplit(dataSet)
    besFeatLabel = labels[bestFeat]
    #迭代树
    myTree = {besFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueValues = set(featValues)
    #实际上是针对每一个子类别划分
    for value in uniqueValues:
        subLabels = labels[:]
        myTree[besFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

#读取隐形眼睛数据文件数据生成树
def readfile2tree(filename):
    fr = open(filename)
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age','prescript','astigmatic','tearRate']
    lensesTree = createTree(lenses,lensesLabels)
    treePlotter.createPlot(lensesTree)
    return lensesTree