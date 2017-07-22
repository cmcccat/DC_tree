import trees
import treePlotter
myDat,labels = trees.createDataSet()
'''
print(myDat)
print(labels)
print(trees.calcShannonEnt(myDat))
print(trees.splitDataSet(myDat,0,1))
print(trees.splitDataSet(myDat,0,0))
print(trees.chooseBestFeatureToSplit(myDat))
print(trees.createTree(myDat,labels))

myTree = treePlotter.retrieveTree(0)
myTree['no surfacing'][3]='maybe'
treePlotter.createPlot(myTree)
'''
trees.readfile2tree('lenses.txt')