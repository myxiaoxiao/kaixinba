import MyVector3d
import MyMatrix4X4
import MyRobotNode

def RobotLinks_New(RobotLinks):
	node1 = [1,2,3,4,5,6,7,8,9,10]
	node2 = [1,2,3,4,5,6,7,8,9,10]
	node3 = [1,2,3,4,5,6,7,8,9,10]
	node4 = [1,2,3,4,5,6,7,8,9,10]
	node5 = [1,2,3,4,5,6,7,8,9,10]
	node6 = [1,2,3,4,5,6,7,8,9,10]

	# 1
	MyRobotNode.RobotNode_New(node1, 0, 0, 0)
	# 2
	MyRobotNode.RobotNode_New(node2, 0, 0, 0)
	# 3
	MyRobotNode.RobotNode_New(node3, 0, 0, 0)
	# 4
	MyRobotNode.RobotNode_New(node4, 0, 0, 0)
	# 5
	MyRobotNode.RobotNode_New(node5, 0, 0, 0)
	# 6
	MyRobotNode.RobotNode_New(node6, 0, 0, 0)

	for i in range(10):
		RobotLinks[i] = node1[i]

	for i in range(10):
		RobotLinks[i + 10] = node2[i]

	for i in range(10):
		RobotLinks[i + 20] = node3[i]

	for i in range(10):
		RobotLinks[i + 30] = node4[i]

	for i in range(10):
		RobotLinks[i + 40] = node5[i]

	for i in range(10):
		RobotLinks[i + 50] = node6[i]

def RobotLinks_GetNode(RobotLinks, index, node):
	if index == 1:
		for i in range(10):
			node[i] = RobotLinks[i]
	elif index == 2:
		for i in range(10):
			node[i] = RobotLinks[i + 10]
	elif index == 3:
		for i in range(10):
			node[i] = RobotLinks[i + 20]
	elif index == 4:
		for i in range(10):
			node[i] = RobotLinks[i + 30]
	elif index == 5:
		for i in range(10):
			node[i] = RobotLinks[i + 40]
	elif index == 6:
		for i in range(10):
			node[i] = RobotLinks[i + 50]

def RobotLinks_SetNode(RobotLinks, index, node):
	if index == 1:
		for i in range(10):
			RobotLinks[i] = node[i]
	elif index == 2:
		for i in range(10):
			RobotLinks[i + 10] = node[i]
	elif index == 3:
		for i in range(10):
			RobotLinks[i + 20] = node[i]
	elif index == 4:
		for i in range(10):
			RobotLinks[i + 30] = node[i]
	elif index == 5:
		for i in range(10):
			RobotLinks[i + 40] = node[i]
	elif index == 6:
		for i in range(10):
			RobotLinks[i + 50] = node[i]

def RobotLinks_GetNodeLength(RobotLinks, index):
	if index == 6:
		return (False, 0)
	node = [1,2,3,4,5,6,7,8,9,10]
	RobotLinks_GetNode(RobotLinks, index, node)
	NextNode = [1,2,3,4,5,6,7,8,9,10]
	RobotLinks_GetNode(RobotLinks, index + 1, NextNode)

	nextNodePoint = [0,0,0]
	MyRobotNode.RobotNode_get_Point(NextNode, nextNodePoint)

	nodePoint = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node, nodePoint)

	tempVector = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(tempVector, nextNodePoint, nodePoint)
	_length = MyVector3d.Vector3d_Length(tempVector)
	return (True, _length)

def RobotLinks_get_Node6XAxis(RobotLinks, node6XAxis):
	node6XAxis[2] = RobotLinks[62]
	node6XAxis[1] = RobotLinks[61]
	node6XAxis[0] = RobotLinks[60]

def RobotLinks_set_Node6XAxis(RobotLinks, node6XAxis):
	RobotLinks[62] = node6XAxis[2]
	RobotLinks[61] = node6XAxis[1]
	RobotLinks[60] = node6XAxis[0]