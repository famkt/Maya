from functools import partial

def skinWeightMinimiseUI():
	"""
	Reduces the maximum number of influences by rebalancing the
	removed infleunces values equally
	"""
	def skinWeightMinimise():
		maxInflu = cmds.textField(maxInfluTXT, q = 1, text = 1)
		maxInfluence = int(maxInflu)

		sel = cmds.ls(sl=True)[0]
		selShape = cmds.listRelatives(sel, s = 1)[0]
		vertNum = cmds.polyEvaluate(sel, vertex = 1)
		vertNum = vertNum - 1
		vertName = sel
		
		# get the cluster
		skinName = cmds.listConnections(selShape+'.inMesh')[0]
		cmds.select(sel+ '.vtx[0:'+str(vertNum)+']')
		
		# get the list of vertex numbers
		minRange = 0
		maxRange = vertNum

		for i in range(int(minRange),int(maxRange)+1):
			vertNumber = '%s.vtx[%s]' % (vertName,i)

			#jointEff = cmds.skinPercent('skinCluster3', vertNumber,q = True, ignoreBelow=0.00001, transform = None)
			jointEff = cmds.skinPercent(skinName, vertNumber , q = True, ignoreBelow=0.00001, transform = None)
			if len(jointEff) > maxInfluence:
				print '%s[%s] has more than 4 influences! Recalibrating...' % (vertName,i)
		
				# get the top highest numbers, pegged to the max influence using a dictionary
				myDict = {}
				for jointName in jointEff:
					jointValue = cmds.skinPercent( skinName, vertNumber, transform= jointName, query=True)
					myDict[jointValue] = {}
					myDict[jointValue][jointName] = jointValue
					
				# sort out the joints based on size
				myList = sorted(myDict.items(), key=operator.itemgetter(0), reverse = True)
				#print myList 
				
				myNewList = []
				# Find out how much points to re-distribute
				distributeValue = 0
				for i in myList[maxInfluence:]:
					addToDistributeValue = i[1][i[1].keys()[0]]
					distributeValue = distributeValue + addToDistributeValue
					influenceName = i[1].keys()[0]
					myNewList.append((influenceName,0.0))
					
				# Find out the weightage of the remaining joints to distribute to
				totalValue = 0
				for i in myList[:maxInfluence]:
					addToTotalValue = i[1][i[1].keys()[0]]
					totalValue = totalValue + addToTotalValue
					
					
				# Update the influences with the latest values
				
				for i in myList[:maxInfluence]:
					influenceName = i[1].keys()[0]
					influenceValue = i[1][i[1].keys()[0]]
					
					newInfluenceValue = influenceValue + distributeValue * influenceValue/totalValue
					# Update with the latest values
					myNewList.append((influenceName,newInfluenceValue))
					
				cmds.skinPercent( skinName,vertNumber, transformValue=myNewList, normalize= True, pruneWeights=0.00001 )
	
	if (cmds.window('Skin Weight Rebalance', exists=True)):
		cmds.deleteUI ('Skin Weight Rebalance')
	colourOverWindow= window = cmds.window( title="Rebalance Influences", iconName='Short Name', widthHeight=(250, 120) )
	cmds.columnLayout( adjustableColumn=True )  
	##creates a line to seperate the title from the functions
	cmds.text(align='left', ww= True,label='Rebalance the maximum influences from a higher to lower value')
	##build the orientated three joint chain
	cmds.text(align='left', ww= True, label='1) Select Mesh\n2) Input the new max number of influences')
	cmds.text(align='left', ww= True, label='')
	maxInfluTXT= cmds.textField(text= '3')
	cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,100),(2,100),(3,100)])
	cmds.text(label='')
	purpleBTN= cmds.button(label='Rebalance',command= partial(skinWeightMinimise))
	cmds.text(label='')

	cmds.showWindow()
