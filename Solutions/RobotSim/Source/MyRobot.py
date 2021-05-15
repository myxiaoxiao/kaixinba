import MyVector3d
import MyMatrix4X4
import MyRobotNode
import MyRobotLinks
import math

def Robot_Init(RobotLinks, rots, Node6xAxis, points, initAngles):
    MyRobotLinks.RobotLinks_New(RobotLinks)
    for i in range(6):
        node = [1,2,3,4,5,6,7,8,9,10]
        MyRobotLinks.RobotLinks_GetNode(RobotLinks, i + 1, node)
        MyRobotNode.RobotNode_SetValue(node, points[i * 3], points[i * 3 + 1], points[i * 3 + 2], rots[i * 3], rots[i * 3 + 1], rots[i * 3 + 2], initAngles[i + 1])
        MyRobotLinks.RobotLinks_SetNode(RobotLinks,  i + 1, node)

    MyRobotLinks.RobotLinks_set_Node6XAxis(RobotLinks, Node6xAxis)
    return True

def Robot_CalculatelTransformation(transfrom, fromValue, to):
	MyMatrix4X4.Matrix4X4_Copy(fromValue, transfrom)
	MyMatrix4X4.Matrix4X4_Inverse(transfrom)
	MyMatrix4X4.Matrix4X4_PostMultBy(transfrom, to)

def Robot_CalculateMatrix(RobotLinks, index, mat):
    node = [1,2,3,4,5,6,7,8,9,10]
    MyRobotLinks.RobotLinks_GetNode(RobotLinks, index, node)
    XAxis = [1,0,0]
    YAxis = [0,1,0]
    ZAxis = [0,0,1]
    origin = [0,0,0]
    if (index == 1 or index == 4 or index == 6):
        MyRobotNode.RobotNode_get_RotVector(node, ZAxis)
        MyRobotNode.RobotNode_get_Point(node, origin)
        MyRobotNode.RobotNode_get_RotVector2(node, XAxis)
        MyVector3d.Vector3d_CrossOfAB(YAxis, ZAxis, XAxis)
        MyVector3d.Vector3d_Identify(YAxis)
    elif (index == 2 or index == 3 or index == 5):
        MyRobotNode.RobotNode_get_Point(node, origin)
        MyRobotNode.RobotNode_get_RotVector(node, XAxis)

        node2 = [1,2,3,4,5,6,7,8,9,10]
        MyRobotLinks.RobotLinks_GetNode(RobotLinks, index + 1, node2)

        node2_Point = [0,0,0]
        MyRobotNode.RobotNode_get_Point(node2, node2_Point)
        node_Point = [0,0,0]
        MyRobotNode.RobotNode_get_Point(node, node_Point)

        MyVector3d.Vector3d_GapOfAB(ZAxis, node2_Point, node_Point)
        MyVector3d.Vector3d_CrossOfAB(YAxis, ZAxis, XAxis)
        MyVector3d.Vector3d_Identify(YAxis)

    MyMatrix4X4.Matrix4X4_SetCoordSystem(mat, origin, XAxis, YAxis, ZAxis)

def Robot_CalculateAngle(fromValue, to, normal):
	MyVector3d.Vector3d_Identify(fromValue)
	MyVector3d.Vector3d_Identify(to)
	result = MyVector3d.Vector3d_MultiplyOfAB(fromValue, to)
	if (result > 1.0):
		result = 1.0
	elif (result < -1.0):
		result = -1.0
	angle = math.acos(result)
	crossVector = [0,0,0]
	MyVector3d.Vector3d_CrossOfAB(crossVector, fromValue, to)
	MyVector3d.Vector3d_Identify(crossVector)
	MyVector3d.Vector3d_Identify(normal)
	value = MyVector3d.Vector3d_MultiplyOfAB(crossVector, normal)
	if (abs(value - 1) < 0.0001):
		return angle
	else:
		return -angle

def Robot_CalculateAngle2(fromValue, to):
    MyVector3d.Vector3d_Identify(fromValue)
    MyVector3d.Vector3d_Identify(to)
    result = MyVector3d.Vector3d_MultiplyOfAB(fromValue, to)
    if (result > 1.0):
        result = 1.0
    elif (result < -1.0):
        result = -1.0

    return math.acos(result)

def Robot_CalculateCirsPoints(circlePlaneNormal, cen1, radius1, cen2, radius2):
    cen1_cen2 = [0,0,0]
    MyVector3d.Vector3d_GapOfAB(cen1_cen2, cen1, cen2)
    distance = MyVector3d.Vector3d_Length(cen1_cen2)
    if (distance < radius1 + radius2):
        a = (radius1 * radius1 - radius2 * radius2 +distance * distance) / (2 * distance)
        c = math.sqrt(radius1 * radius1 - a * a)
        R1ToR2 = [0,0,0]
        MyVector3d.Vector3d_GapOfAB(R1ToR2, cen2, cen1)
        MyVector3d.Vector3d_Identify(R1ToR2)
        R1ToR2_a = [0,0,0]
        MyVector3d.Vector3d_MultiplyOfK(R1ToR2_a, R1ToR2, a)
        middlePoint = [0,0,0]
        MyVector3d.Vector3d_SumOfAB(middlePoint, cen1, R1ToR2_a)

        nextMiddle = [0,0,0]
        MyVector3d.Vector3d_CrossOfAB(nextMiddle, circlePlaneNormal, R1ToR2)
        MyVector3d.Vector3d_Identify(nextMiddle)

        nextMiddle_c = [0,0,0]
        MyVector3d.Vector3d_MultiplyOfK(nextMiddle_c, nextMiddle, c)
        up = [0,0,0]
        MyVector3d.Vector3d_SumOfAB(up, middlePoint, nextMiddle_c)
        down = [0,0,0]
        MyVector3d.Vector3d_GapOfAB(down, middlePoint, nextMiddle_c)

        upPoint = [0,0,0]
        MyVector3d.Vector3d_Set(upPoint, up[0], up[1], up[2])
        downPoint = [0,0,0]
        MyVector3d.Vector3d_Set(downPoint, down[0], down[1], down[2])

        pointsCount = 2
        point1 = [0,0,0]
        point2 = [0,0,0]
        point1[0] = upPoint[0]
        point1[1] = upPoint[1]
        point1[2] = upPoint[2]
        point2[0] = downPoint[0]
        point2[1] = downPoint[1]
        point2[2] = downPoint[2]
        return (pointsCount, point1, point2)
    elif (distance == radius1 + radius2):
        R1ToR2 = [0,0,0]
        MyVector3d.Vector3d_GapOfAB(R1ToR2, cen2, cen1)
        MyVector3d.Vector3d_Identify(R1ToR2)

        R1ToR2_radius1 = [0,0,0]
        MyVector3d.Vector3d_MultiplyOfK(R1ToR2_radius1, R1ToR2, radius1)
        middle = [0,0,0]
        MyVector3d.Vector3d_SumOfAB(middle, cen1, R1ToR2_radius1)
        pointsCount = 1
        point1[0] = middle[0]
        point1[1] = middle[1]
        point1[2] = middle[2]
        return (pointsCount, point1, None)
    else:
        pointsCount = 0
        return (pointsCount, None, None)

def Robot_CalculateQ2(node2, node3, pointsCount, point1, point2, normal):
    if (pointsCount == 1):
        node3_Point = [0,0,0]
        MyRobotNode.RobotNode_get_Point(node3, node3_Point)

        node2_Point = [0,0,0]
        MyRobotNode.RobotNode_get_Point(node2, node2_Point)

        V2To3 = [0,0,0]
        MyVector3d.Vector3d_GapOfAB(V2To3, node3_Point, node2_Point)
        TestV1 = [0,0,0]
        MyVector3d.Vector3d_GapOfAB(TestV1, point1, node2_Point)

        return Robot_CalculateAngle2(V2To3, TestV1)
    else:
        node3_Point = [0,0,0]
        MyRobotNode.RobotNode_get_Point(node3, node3_Point)

        node2_Point = [0,0,0]
        MyRobotNode.RobotNode_get_Point(node2, node2_Point)

        V2To3 = [0,0,0]
        MyVector3d.Vector3d_GapOfAB(V2To3, node3_Point, node2_Point)

        TestV1 = [0,0,0]
        MyVector3d.Vector3d_GapOfAB(TestV1, point1, node2_Point)
        TestV2 = [0,0,0]
        MyVector3d.Vector3d_GapOfAB(TestV2, point2, node2_Point)
        angle1 = Robot_CalculateAngle2(V2To3, TestV1)
        angle2 = Robot_CalculateAngle2(V2To3, TestV2)
        if (abs(angle1) < abs(angle2)):
            corssVector = [0,0,0]
            MyVector3d.Vector3d_CrossOfAB(corssVector, V2To3, TestV1)
            MyVector3d.Vector3d_Identify(corssVector)
            MyVector3d.Vector3d_Identify(normal)

            value = MyVector3d.Vector3d_MultiplyOfAB(corssVector, normal)
            if (abs(value - 1) < 0.0001):
                return angle1
            else:
                return -angle1
        else:
            corssVector = [0,0,0]
            MyVector3d.Vector3d_CrossOfAB(corssVector, V2To3, TestV2)
            MyVector3d.Vector3d_Identify(corssVector)
            MyVector3d.Vector3d_Identify(normal)

            value = MyVector3d.Vector3d_MultiplyOfAB(corssVector, normal)
            if (abs(value - 1) < 0.0001):
                return angle2
            else:
                return -angle2

def CalculateQ3(node3, node5, newPointYZ, normal):
    node5_Point = [0,0,0]
    MyRobotNode.RobotNode_get_Point(node5, node5_Point)

    node3_Point = [0,0,0]
    MyRobotNode.RobotNode_get_Point(node3, node3_Point)

    V3To5 = [0,0,0]
    MyVector3d.Vector3d_GapOfAB(V3To5, node5_Point, node3_Point)
    MyVector3d.Vector3d_Identify(V3To5)

    TestV = [0,0,0]
    MyVector3d.Vector3d_GapOfAB(TestV, newPointYZ, node3_Point)
    MyVector3d.Vector3d_Identify(TestV)

    angle = Robot_CalculateAngle2(V3To5, TestV)
    corssVector = [0,0,0]
    MyVector3d.Vector3d_CrossOfAB(corssVector, V3To5, TestV)
    MyVector3d.Vector3d_Identify(corssVector)
    MyVector3d.Vector3d_Identify(normal)

    value = MyVector3d.Vector3d_MultiplyOfAB(corssVector, normal)
    if (abs(value - 1) < 0.0001):
        return angle
    else:
        return -angle

def Robot_Transform(RobotLinks, newT6Matrix):
	node1 = [1,2,3,4,5,6,7,8,9,10]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 1, node1)
	node2 = [1,2,3,4,5,6,7,8,9,10]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 2, node2)
	node3 = [1,2,3,4,5,6,7,8,9,10]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 3, node3)
	node4 = [1,2,3,4,5,6,7,8,9,10]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 4, node4)
	node5 = [1,2,3,4,5,6,7,8,9,10]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 5, node5)
	node6 = [1,2,3,4,5,6,7,8,9,10]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 6, node6)
	
	node6_Point = [0,0,0]

    # 1 calculate position of T5
	newOrigin = [0,0,0]
	MyMatrix4X4.Matrix4X4_GetOrigin(newT6Matrix, newOrigin)
	newZAxis = [0,0,0]
	MyMatrix4X4.Matrix4X4_GetZAxis(newT6Matrix, newZAxis)

	(_, length5) = MyRobotLinks.RobotLinks_GetNodeLength(RobotLinks, 5)

	point5Target = [0,0,0]
	newZAxis_length5 = [0,0,0]
	MyVector3d.Vector3d_MultiplyOfK(newZAxis_length5, newZAxis, length5)
	MyVector3d.Vector3d_GapOfAB(point5Target, newOrigin, newZAxis_length5)

	# 2 calculate theta1(Q1), T2 - 6 Rot(Q1)------------------------------------------
	V5Target = [0,0,0]
	node1_Point = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node1, node1_Point)
	MyVector3d.Vector3d_GapOfAB(V5Target, point5Target, node1_Point)
	V5Target[2] = 0
	MyVector3d.Vector3d_Identify(V5Target)

	node5_Point = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node5, node5_Point)
	MyRobotNode.RobotNode_get_Point(node1, node1_Point)
	V5 = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node1, node1_Point)
	MyVector3d.Vector3d_GapOfAB(V5, node5_Point, node1_Point)
	V5[2] = 0
	MyVector3d.Vector3d_Identify(V5)

	node1_RotVector = [0,0,0]
	MyRobotNode.RobotNode_get_RotVector(node1, node1_RotVector)
	Q1 = Robot_CalculateAngle(V5, V5Target, node1_RotVector)
	MyRobotNode.RobotNode_Rotate2(node1, node1_RotVector, Q1)
	MyRobotNode.RobotNode_Rotate(node2, node1_Point, node1_RotVector, Q1)
	MyRobotNode.RobotNode_Rotate(node3, node1_Point, node1_RotVector, Q1)
	MyRobotNode.RobotNode_Rotate(node4, node1_Point, node1_RotVector, Q1)
	MyRobotNode.RobotNode_Rotate(node5, node1_Point, node1_RotVector, Q1)

	MyRobotNode.RobotNode_get_Point(node6, node6_Point)

	MyRobotNode.RobotNode_Rotate(node6, node1_Point, node1_RotVector, Q1)
    
    

	newPointYZ = [0,0,0]
	MyVector3d.Vector3d_Copy(point5Target, newPointYZ)

	# 4 calculate theta2(Q2), T3 - 6 Rot(Q2)
	(_, length2) = MyRobotLinks.RobotLinks_GetNodeLength(RobotLinks, 2)

	node3_Point = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node3, node3_Point)
	MyRobotNode.RobotNode_get_Point(node5, node5_Point)
	node5_Point_node3_Point = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(node5_Point_node3_Point, node5_Point, node3_Point)
	length3 = MyVector3d.Vector3d_Length(node5_Point_node3_Point)

	node2_RotVector = [0,0,0]
	MyRobotNode.RobotNode_get_RotVector(node2, node2_RotVector)
	MyRobotNode.RobotNode_get_RotVector(node1, node1_RotVector)
	node2_Point = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node2, node2_Point)
	point1 = [0,0,0]
	point2 = [0,0,0]
	pointsCount = 0
	(pointsCount, point1, point2) = Robot_CalculateCirsPoints(node2_RotVector, node2_Point, length2, newPointYZ, length3)
	if (pointsCount == 0):
		MyRobotNode.RobotNode_get_Point(node1, node1_Point)
		MyRobotNode.RobotNode_get_RotVector(node1, node1_RotVector)
		MyRobotNode.RobotNode_Rotate2(node1, node1_RotVector, -Q1)
		MyRobotNode.RobotNode_Rotate(node2, node1_Point, node1_RotVector, -Q1)
		MyRobotNode.RobotNode_Rotate(node3, node1_Point, node1_RotVector, -Q1)
		MyRobotNode.RobotNode_Rotate(node4, node1_Point, node1_RotVector, -Q1)
		MyRobotNode.RobotNode_Rotate(node5, node1_Point, node1_RotVector, -Q1)
		MyRobotNode.RobotNode_Rotate(node6, node1_Point, node1_RotVector, -Q1)
		return False

	Q2 = Robot_CalculateQ2(node2, node3, pointsCount, point1, point2, node2_RotVector)
	MyRobotNode.RobotNode_get_Point(node2, node2_Point)
	MyRobotNode.RobotNode_get_RotVector(node2, node2_RotVector)
	MyRobotNode.RobotNode_Rotate2(node2, node2_RotVector, Q2)
	MyRobotNode.RobotNode_Rotate(node3, node2_Point, node2_RotVector, Q2)
	MyRobotNode.RobotNode_Rotate(node4, node2_Point, node2_RotVector, Q2)
	MyRobotNode.RobotNode_Rotate(node5, node2_Point, node2_RotVector, Q2)
	MyRobotNode.RobotNode_Rotate(node6, node2_Point, node2_RotVector, Q2)

	# 5 calculate theta3(Q3), T4 - 6 Rot(Q3)
	node3_RotVector = [0,0,0]
	MyRobotNode.RobotNode_get_RotVector(node3, node3_RotVector)
	MyRobotNode.RobotNode_get_Point(node3, node3_Point)
	Q3 = CalculateQ3(node3, node5, newPointYZ, node3_RotVector)
	MyRobotNode.RobotNode_Rotate2(node3, node3_RotVector, Q3)
	MyRobotNode.RobotNode_Rotate(node4, node3_Point, node3_RotVector, Q3)
	MyRobotNode.RobotNode_Rotate(node5, node3_Point, node3_RotVector, Q3)
	MyRobotNode.RobotNode_Rotate(node6, node3_Point, node3_RotVector, Q3)

	# 8 calculate Q5, T6 Rot(Q5)

	MyRobotNode.RobotNode_get_Point(node6, node6_Point)
	node4_RotVector = [0,0,0]
	MyRobotNode.RobotNode_get_RotVector(node4, node4_RotVector)
	V5To6 = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node5, node5_Point)
	MyVector3d.Vector3d_GapOfAB(V5To6, node6_Point, node5_Point)
	Q5_5To4 = Robot_CalculateAngle2(V5To6, node4_RotVector)
	Q5_NewTo4 = Robot_CalculateAngle2(newZAxis, node4_RotVector)
	Q5 = Q5_NewTo4 - Q5_5To4
	node5_RotVector = [0,0,0]
	MyRobotNode.RobotNode_get_RotVector(node5, node5_RotVector)
	MyRobotNode.RobotNode_Rotate2(node5, node5_RotVector, Q5)
	MyRobotNode.RobotNode_Rotate(node6, node5_Point, node5_RotVector, Q5)

	# 7 calculate Q4, T5 - 6 Rot(Q4)+
	dExtendLength = length5 * math.cos(Q5_NewTo4)
	node4_RotVector_ExtendLength = [0,0,0]
	MyVector3d.Vector3d_MultiplyOfK(node4_RotVector_ExtendLength, node4_RotVector, dExtendLength)
	MyRobotNode.RobotNode_get_Point(node5, node5_Point)
	nextCeneter = [0,0,0]
	MyVector3d.Vector3d_SumOfAB(nextCeneter, node5_Point, node4_RotVector_ExtendLength)
	from5 = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node6, node6_Point)
	MyVector3d.Vector3d_GapOfAB(from5, node6_Point, nextCeneter)
	MyVector3d.Vector3d_Identify(from5)
	to5 = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(to5, newOrigin, nextCeneter)
	MyVector3d.Vector3d_Identify(to5)

	node4_Point = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node4, node4_Point)
	MyRobotNode.RobotNode_get_RotVector(node4, node4_RotVector)
	Q4 = Robot_CalculateAngle(from5, to5, node4_RotVector)
	MyRobotNode.RobotNode_Rotate2(node4, node4_RotVector, Q4)
	MyRobotNode.RobotNode_Rotate(node5, node4_Point, node4_RotVector, Q4)
	MyRobotNode.RobotNode_Rotate(node6, node4_Point, node4_RotVector, Q4)

	# 9 calculate Q6, T6 Rot(Q6)
	Node6XAxis = [0,0,0]
	MyRobotLinks.RobotLinks_get_Node6XAxis(RobotLinks, Node6XAxis)
	newAxis = [0,0,0]
	MyMatrix4X4.Matrix4X4_GetXAxis(newT6Matrix, newAxis)
	node6_RotVector = [0,0,0]
	MyRobotNode.RobotNode_get_RotVector(node6, node6_RotVector)
	Q6 = Robot_CalculateAngle(Node6XAxis, newAxis, node6_RotVector)
	MyRobotNode.RobotNode_Rotate2(node6, node6_RotVector, Q6)
	MyRobotLinks.RobotLinks_set_Node6XAxis(RobotLinks, newAxis)

	MyRobotLinks.RobotLinks_SetNode(RobotLinks, 1, node1)
	MyRobotLinks.RobotLinks_SetNode(RobotLinks, 2, node2)
	MyRobotLinks.RobotLinks_SetNode(RobotLinks, 3, node3)
	MyRobotLinks.RobotLinks_SetNode(RobotLinks, 4, node4)
	MyRobotLinks.RobotLinks_SetNode(RobotLinks, 5, node5)
	MyRobotLinks.RobotLinks_SetNode(RobotLinks, 6, node6)

	return True

def Robot_Execute2(RobotLinks, newT6Matrix):
	oldMat1 = [[0 for i in range(4)] for j in range(4)]
	Robot_CalculateMatrix(RobotLinks, 1, oldMat1)
	oldMat2 = [[0 for i in range(4)] for j in range(4)]
	Robot_CalculateMatrix(RobotLinks, 2, oldMat2)
	oldMat3 = [[0 for i in range(4)] for j in range(4)]
	Robot_CalculateMatrix(RobotLinks, 3, oldMat3)
	oldMat4 = [[0 for i in range(4)] for j in range(4)]
	Robot_CalculateMatrix(RobotLinks, 4, oldMat4)
	oldMat5 = [[0 for i in range(4)] for j in range(4)]
	Robot_CalculateMatrix(RobotLinks, 5, oldMat5)
	oldMat6 = [[0 for i in range(4)] for j in range(4)]
	Robot_CalculateMatrix(RobotLinks, 6, oldMat6)
	Robot_Transform(RobotLinks, newT6Matrix)

def Robot_Execute(RobotLinks, origin, ZAxis, angles):
	XAxis = [0,0,0]
	MyVector3d.Vector3d_kXAxis(XAxis)
	temp = [0,0,0]
	MyVector3d.Vector3d_CrossOfAB(temp, XAxis, ZAxis)
	temp_Length = MyVector3d.Vector3d_Length(temp)
	if (abs(temp_Length) < 0.0001):
		YAxis = [0,0,0]
		MyVector3d.Vector3d_kYAxis(YAxis)
		MyVector3d.Vector3d_CrossOfAB(XAxis, ZAxis, YAxis)
	else:
		MyVector3d.Vector3d_Copy(temp, XAxis)
	YAxis = [0,0,0]
	MyVector3d.Vector3d_CrossOfAB(YAxis, ZAxis, XAxis)

	newT6Matrix = [[0 for i in range(4)] for j in range(4)]
	MyMatrix4X4.Matrix4X4_SetToIdentity(newT6Matrix)
	MyMatrix4X4.Matrix4X4_SetCoordSystem(newT6Matrix, origin, XAxis, YAxis, ZAxis)

	Robot_Execute2(RobotLinks, newT6Matrix)
	for i in range(6):
		node = [0,1,2,3,4,5,6,7,8,9]
		MyRobotLinks.RobotLinks_GetNode(RobotLinks, i + 1, node)
		angles[i] = MyRobotNode.RobotNode_get_MotorAngle(node)

def Robot_ControlRotator(RobotLinks, nodeIndex, angle):
	node1 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 1, node1)
	node2 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 2, node2)
	node3 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 3, node3)
	node4 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 4, node4)
	node5 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 5, node5)
	node6 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 6, node6)

	if (nodeIndex == 6):
		origin = [0,0,0]
		MyRobotNode.RobotNode_get_Point(node6, origin)
		rotator = [0,0,0]
		MyRobotNode.RobotNode_get_RotVector(node6, rotator)
		MyRobotNode.RobotNode_Rotate2(node6, rotator, angle)

	if (nodeIndex == 5):
		origin = [0,0,0]
		MyRobotNode.RobotNode_get_Point(node5, origin)
		rotator = [0,0,0]
		MyRobotNode.RobotNode_get_RotVector(node5, rotator)
		MyRobotNode.RobotNode_Rotate2(node5, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node6, origin, rotator, angle)

	if (nodeIndex == 4):
		origin = [0,0,0]
		MyRobotNode.RobotNode_get_Point(node4, origin)
		rotator = [0,0,0]
		MyRobotNode.RobotNode_get_RotVector(node4, rotator)
		MyRobotNode.RobotNode_Rotate2(node4, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node5, origin, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node6, origin, rotator, angle)

	if (nodeIndex == 3):
		origin = [0,0,0]
		MyRobotNode.RobotNode_get_Point(node3, origin)
		rotator = [0,0,0]
		MyRobotNode.RobotNode_get_RotVector(node3, rotator)
		MyRobotNode.RobotNode_Rotate2(node3, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node4, origin, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node5, origin, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node6, origin, rotator, angle)

	if (nodeIndex == 2):
		origin = [0,0,0]
		MyRobotNode.RobotNode_get_Point(node2, origin)
		rotator = [0,0,0]
		MyRobotNode.RobotNode_get_RotVector(node2, rotator)
		MyRobotNode.RobotNode_Rotate2(node2, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node3, origin, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node4, origin, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node5, origin, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node6, origin, rotator, angle)

	if (nodeIndex == 1):
		origin = [0,0,0]
		MyRobotNode.RobotNode_get_Point(node1, origin)
		rotator = [0,0,0]
		MyRobotNode.RobotNode_get_RotVector(node1, rotator)
		MyRobotNode.RobotNode_Rotate2(node1, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node2, origin, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node3, origin, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node4, origin, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node5, origin, rotator, angle)
		MyRobotNode.RobotNode_Rotate(node6, origin, rotator, angle)


#########################################
#(_,n5y,_)(_,n4y,_)(_,n3y,n3z)
#      X0------Y0--------XPI-
#						     -
#							  -
#							   |
#								|Y0 (_,_,n2z)
#								|
#								|
#								|X0 (_,_,n1z)
#								|
#								|
#								|X0 (_,_,n0z)
#								|
#								_-Z0(_,_,baseZ)
#								|
#
##############################################

def Robot_Create(baseZ, n0z, n1z, n2z, n3y, n3z, n4y, n5y):
	point0 = [0,0,baseZ]
	point1 = [0,0,n0z]
	point2 = [0,0,n1z]
	point3 = [0,0,n2z]
	point4 = [0,n3y,n3z]
	point5 = [0,n4y,n3z]
	point6 = [0,n5y,n3z]
	rotAxises0 = [0,0,-1]
	rotAxises1 = [1,0,0]
	rotAxises2 = [1,0,0]
	rotAxises3 = [0,1,0]
	rotAxises4 = [1,0,0]
	rotAxises5 = [0,1,0]
	rotAxises6 = [1,0,0]
	initAngles = [0,0,0,0,3.1415926,0,0]

	angles = [1,2,3,4,5,6]
	angles[0] = initAngles[1]
	angles[1] = initAngles[2]
	angles[2] = initAngles[3]
	angles[3] = initAngles[4]
	angles[4] = initAngles[5]
	angles[5] = initAngles[6]

	v1 = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(v1, point1, point0)
	MyVector3d.Vector3d_Identify(v1)
	v2 = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(v2, point2, point1)
	MyVector3d.Vector3d_Identify(v2)
	v3 = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(v3, point3, point2)
	MyVector3d.Vector3d_Identify(v3)
	v4 = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(v4, point4, point3)
	MyVector3d.Vector3d_Identify(v4)
	v5 = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(v5, point5, point4)
	MyVector3d.Vector3d_Identify(v5)
	v6 = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(v6, point6, point5)
	MyVector3d.Vector3d_Identify(v6)

	vectors = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
	vectors[0] = rotAxises0[0]
	vectors[1] = rotAxises0[1]
	vectors[2] = rotAxises0[2]
	vectors[3] = rotAxises1[0]
	vectors[4] = rotAxises1[1]
	vectors[5] = rotAxises1[2]
	vectors[6] = rotAxises2[0]
	vectors[7] = rotAxises2[1]
	vectors[8] = rotAxises2[2]
	vectors[9] = rotAxises3[0]
	vectors[10] = rotAxises3[1]
	vectors[11] = rotAxises3[2]
	vectors[12] = rotAxises4[0]
	vectors[13] = rotAxises4[1]
	vectors[14] = rotAxises4[2]
	vectors[15] = rotAxises5[0]
	vectors[16] = rotAxises5[1]
	vectors[17] = rotAxises5[2]

	initPoints = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
	initPoints[0] = point1[0]
	initPoints[1] = point1[1]
	initPoints[2] = point1[2]
	initPoints[3] = point2[0]
	initPoints[4] = point2[1]
	initPoints[5] = point2[2]
	initPoints[6] = point3[0]
	initPoints[7] = point3[1]
	initPoints[8] = point3[2]
	initPoints[9] = point4[0]
	initPoints[10] = point4[1]
	initPoints[11] = point4[2]
	initPoints[12] = point5[0]
	initPoints[13] = point5[1]
	initPoints[14] = point5[2]
	initPoints[15] = point6[0]
	initPoints[16] = point6[1]
	initPoints[17] = point6[2]

	RobotLinks = []
	for i in range(63):
		RobotLinks.append(i)
	Robot_Init(RobotLinks, vectors, rotAxises6, initPoints, initAngles)
	return (RobotLinks,angles)

def Robot_ExecuteXYZIJK(RobotLinks, x, y, z, i, j, k, fromAngles):
	origin = [0,0,0]
	origin[0] = x
	origin[1] = y
	origin[2] = z
	ZAxis = [0,0,0]
	ZAxis[0] = i
	ZAxis[1] = j
	ZAxis[2] = k

	toAngles = [1,2,3,4,5,6]
	Robot_Execute(RobotLinks, origin, ZAxis, toAngles)

	rotations = [1,2,3,4,5,6]
	for i in range(6):
		rotations[i] = (toAngles[i] - fromAngles[i]) * 180 / 3.14159265358979323846
		fromAngles[i] = toAngles[i]

	# debug to print node position
	node1 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 1, node1)
	origin1 = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node1, origin1)

	node2 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 2, node2)
	origin2 = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node2, origin2)

	node3 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 3, node3)
	origin3 = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node3, origin3)

	node4 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 4, node4)
	origin4 = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node4, origin4)

	node5 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 5, node5)
	origin5 = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node5, origin5)

	node6 = [0,1,2,3,4,5,6,7,8,9]
	MyRobotLinks.RobotLinks_GetNode(RobotLinks, 6, node6)
	origin6 = [0,0,0]
	MyRobotNode.RobotNode_get_Point(node6, origin6)

	with open("D:\\test.txt","w") as f:
		f.write("data.push([" + str(origin1[0]) + ", " + str(origin1[1]) + ", " + str(origin1[2]) + "]);\n")
		f.write("data.push([" + str(origin2[0]) + ", " + str(origin2[1]) + ", " + str(origin2[2]) + "]);\n")
		f.write("data.push([" + str(origin3[0]) + ", " + str(origin3[1]) + ", " + str(origin3[2]) + "]);\n")
		f.write("data.push([" + str(origin4[0]) + ", " + str(origin4[1]) + ", " + str(origin4[2]) + "]);\n")
		f.write("data.push([" + str(origin5[0]) + ", " + str(origin5[1]) + ", " + str(origin5[2]) + "]);\n")
		f.write("data.push([" + str(origin6[0]) + ", " + str(origin6[1]) + ", " + str(origin6[2]) + "]);\n")

if __name__ == '__main__':

	(RobotLinks,angles) = Robot_Create(-146.5, 10, 100, 220, 99.5, 335, 222, 324)
	Robot_ExecuteXYZIJK(RobotLinks, 40,211.6748,158.03,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,40,211.6748,154.03,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,40,211.6748,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,42.437,214.0861,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,44.729,216.6358,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,46.868,219.315,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,48.8467,222.1147,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,50.6584,225.0253,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,52.2969,228.0367,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,53.7565,231.1388,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,55.0324,234.321,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,56.12,237.5722,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,57.0158,240.8815,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,57.7166,244.2374,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,58.2201,247.6286,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,58.5244,251.0434,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,58.6287,254.4702,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,58.5324,257.8972,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,58.2361,261.3127,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,57.7406,264.7051,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,57.0476,268.0627,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,56.1596,271.374,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,55.0796,274.6278,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,53.8112,277.8129,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,52.3588,280.9184,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,50.7274,283.9337,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,48.9225,286.8485,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,46.9503,289.6528,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,44.8176,292.3371,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,42.5317,294.8921,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,40.1003,297.3091,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,37.5318,299.5799,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,34.8349,301.6966,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,32.019,303.6521,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,29.0935,305.4397,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,26.0686,307.0532,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,22.9545,308.4871,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,19.762,309.7366,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,16.5018,310.7973,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,13.1853,311.6657,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,9.8236,312.3387,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,6.4284,312.8141,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,3.0112,313.0902,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-0.4163,313.1661,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-3.8424,313.0415,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-7.2554,312.7169,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-10.6435,312.1934,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-13.9953,311.4727,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-17.2992,310.5573,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-20.5439,309.4504,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-23.7184,308.1557,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-26.8118,306.6777,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-29.8135,305.0214,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-32.7133,303.1924,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-35.5012,301.1971,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-38.1677,299.0423,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-40.7037,296.7353,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-43.1005,294.284,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-45.3499,291.6968,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-47.4443,288.9825,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-49.3764,286.1505,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-51.1397,283.2103,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-52.7282,280.1722,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-54.1363,277.0463,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-55.3593,273.8436,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-56.3931,270.5748,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-57.2339,267.2511,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-57.8791,263.884,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-58.3264,260.485,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-58.5742,257.0656,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-58.6218,253.6376,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-58.4689,250.2126,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-58.116,246.8025,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-57.5645,243.4188,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-56.8161,240.0731,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-55.8734,236.7769,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-54.7397,233.5414,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-53.4188,230.3778,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-51.9152,227.2967,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-50.2341,224.3088,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-48.3813,221.4243,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-46.363,218.653,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-44.1862,216.0044,150,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-44.1862,216.0044,154.03,0,0,-1,angles)
	Robot_ExecuteXYZIJK(RobotLinks,-44.1862,216.0044,158.03,0,0,-1,angles)
	