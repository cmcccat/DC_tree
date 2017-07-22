import matplotlib.pyplot as plt
#绘制点模型,定义文本框和箭头格式
#分支节点,boxstyle是样式,fc是不透明度
decisionNode = dict(boxstyle = "sawtooth", fc ="0.8")
#叶节点
leafNode = dict(boxstyle="round4",fc= "0.8")
arrow_args = dict(arrowstyle="<-")
#给createPlot子节点绘图添加注释。具体解释：nodeTxt：节点显示的内容；xy：起点位置；xycoords/xytext：坐标说明？；xytext：显示字符的位置
#va/ha：显示的位置？；bbox：方框样式；arrow：箭头参数，字典类型数据
def plotNode(nodeText, centerPt,parentPt, nodeType):
    createPlot.axl.annotate(nodeText,xy=parentPt,xycoords='axes fraction',xytext = centerPt,textcoords= 'axes fraction',va = "center",ha ="center",bbox=nodeType,arrowprops=arrow_args)

def createPlot(inTree):
    fig = plt.figure(1,facecolor='white')
    fig.clf()
    #去除标尺用的
    axprops = dict(xticks =[],yticks =[])
    #frmeon:边框
    createPlot.axl = plt.subplot(111,frameon = False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW;plotTree.yOff = 1.0;
    plotTree(inTree,(0.5,1.0),'')
    plt.show()

#获取叶子节点的数目
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        #判断节点类型是否为字典（有子节点）
        if type(secondDict[key]).__name__ =='dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:numLeafs += 1
    return numLeafs

#获取树深
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:thisDepth = 1
        if thisDepth > maxDepth:maxDepth = thisDepth
    return maxDepth

#测试树模型
def retrieveTree(i):
    listOfTrees = [{'no surfacing':{0:'no',1:{'flippers':{0:'no',1:'yes'}}}},
                   {'no surfacing':{0:'no',1:{'flippers':{0:{'head':{0:'no',1:'yes'}},1:'no'}}}}]
    return  listOfTrees[i]

#在父子节点之间填充文本信息
def plotMidText(cntrPt,parenPt,txtString):
    xMid = (parenPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parenPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    #指定位置绘制文本
    createPlot.axl.text(xMid,yMid,txtString)

def plotTree(myTree,parentPt,nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    #一开始在中心位置，而中心文本相对于x有半个身位偏移
    cntrPt = (plotTree.xOff +(1.0 + float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
    #中间属性值
    plotMidText(cntrPt,parentPt,nodeTxt)
    plotNode(firstStr,cntrPt,parentPt,decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            #迭代更新
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            #将x偏移右移一个标准身位
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),cntrPt,leafNode)
            plotMidText((plotTree.xOff,plotTree.yOff),cntrPt,str(key))
    plotTree.yOff = plotTree.yOff +1.0/plotTree.totalD

