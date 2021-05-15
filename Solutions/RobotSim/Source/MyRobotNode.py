import MyVector3d
import MyMatrix4X4

def RobotNode_get_Point(Origin_RotVector_RotVector2_motorAngle, Origin):
	Origin[0] = Origin_RotVector_RotVector2_motorAngle[0]
	Origin[1] = Origin_RotVector_RotVector2_motorAngle[1]
	Origin[2] = Origin_RotVector_RotVector2_motorAngle[2]

def RobotNode_get_RotVector(Origin_RotVector_RotVector2_motorAngle, RotVector):
	RotVector[0] = Origin_RotVector_RotVector2_motorAngle[3]
	RotVector[1] = Origin_RotVector_RotVector2_motorAngle[4]
	RotVector[2] = Origin_RotVector_RotVector2_motorAngle[5]

def RobotNode_get_RotVector2(Origin_RotVector_RotVector2_motorAngle, RotVector2):
	RotVector2[0] = Origin_RotVector_RotVector2_motorAngle[6]
	RotVector2[1] = Origin_RotVector_RotVector2_motorAngle[7]
	RotVector2[2] = Origin_RotVector_RotVector2_motorAngle[8]

def RobotNode_get_MotorAngle(Origin_RotVector_RotVector2_motorAngle):
	return Origin_RotVector_RotVector2_motorAngle[9]

def RobotNode_SetValue(Origin_RotVector_RotVector2_motorAngle, x, y, z, x2, y2, z2, initAngle):
	Origin_RotVector_RotVector2_motorAngle[0] = x
	Origin_RotVector_RotVector2_motorAngle[1] = y
	Origin_RotVector_RotVector2_motorAngle[2] = z

	Temp_RotVector = [0,0,0]
	Temp_RotVector[0] = x2
	Temp_RotVector[1] = y2
	Temp_RotVector[2] = z2
	Origin_RotVector_RotVector2_motorAngle[3] = x2
	Origin_RotVector_RotVector2_motorAngle[4] = y2
	Origin_RotVector_RotVector2_motorAngle[5] = z2

	Temp_RotVector2 = [0,0,0]
	MyVector3d.Vector3d_kXAxis(Temp_RotVector2)
	Origin_RotVector_RotVector2_motorAngle[6] = Temp_RotVector2[0]
	Origin_RotVector_RotVector2_motorAngle[7] = Temp_RotVector2[1]
	Origin_RotVector_RotVector2_motorAngle[8] = Temp_RotVector2[2]

	Temp_RotVector2XRotVector = MyVector3d.Vector3d_MultiplyOfAB(Temp_RotVector2, Temp_RotVector)
	if(abs(Temp_RotVector2XRotVector - 1.0) < 0.0001 or abs(Temp_RotVector2XRotVector + 1.0) < 0.0001):
		Temp_YAxis = [0,0,0]
		MyVector3d.Vector3d_kYAxis(Temp_YAxis)
		MyVector3d.Vector3d_CrossOfAB(Temp_RotVector2, Temp_RotVector, Temp_YAxis)
		Origin_RotVector_RotVector2_motorAngle[6] = Temp_RotVector2[0]
		Origin_RotVector_RotVector2_motorAngle[7] = Temp_RotVector2[1]
		Origin_RotVector_RotVector2_motorAngle[8] = Temp_RotVector2[2]
	else:
		Temp_Vector = [0,0,0]
		MyVector3d.Vector3d_CrossOfAB(Temp_Vector, Temp_RotVector, Temp_RotVector2)
		MyVector3d.Vector3d_Copy(Temp_Vector, Temp_RotVector2)
		Origin_RotVector_RotVector2_motorAngle[6] = Temp_RotVector2[0]
		Origin_RotVector_RotVector2_motorAngle[7] = Temp_RotVector2[1]
		Origin_RotVector_RotVector2_motorAngle[8] = Temp_RotVector2[2]

	Origin_RotVector_RotVector2_motorAngle[9] = initAngle

def RobotNode_Rotate(Origin_RotVector_RotVector2_motorAngle, basePt, axis, angle):
	Origin = [0,0,0]
	Origin[0] = Origin_RotVector_RotVector2_motorAngle[0]
	Origin[1] = Origin_RotVector_RotVector2_motorAngle[1]
	Origin[2] = Origin_RotVector_RotVector2_motorAngle[2]
	
	temp = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(temp, Origin, basePt)
	_length = MyVector3d.Vector3d_Length(temp)
	MyVector3d.Vector3d_Identify(temp)
	MyVector3d.Vector3d_RotateBy(temp, axis, angle)

	temp2 = [0,0,0]
	MyVector3d.Vector3d_MultiplyOfK(temp2, temp, _length)
	result = [0,0,0]
	MyVector3d.Vector3d_SumOfAB(result, basePt, temp2)
	MyVector3d.Vector3d_Copy(result, Origin)
	Origin_RotVector_RotVector2_motorAngle[0] = Origin[0]
	Origin_RotVector_RotVector2_motorAngle[1] = Origin[1]
	Origin_RotVector_RotVector2_motorAngle[2] = Origin[2]

	RotVector = [0,0,0]
	RotVector[0] = Origin_RotVector_RotVector2_motorAngle[3]
	RotVector[1] = Origin_RotVector_RotVector2_motorAngle[4]
	RotVector[2] = Origin_RotVector_RotVector2_motorAngle[5]
	MyVector3d.Vector3d_RotateBy(RotVector, axis, angle)
	Origin_RotVector_RotVector2_motorAngle[3] = RotVector[0]
	Origin_RotVector_RotVector2_motorAngle[4] = RotVector[1]
	Origin_RotVector_RotVector2_motorAngle[5] = RotVector[2]

	RotVector2 = [0,0,0]
	RotVector2[0] = Origin_RotVector_RotVector2_motorAngle[6]
	RotVector2[1] = Origin_RotVector_RotVector2_motorAngle[7]
	RotVector2[2] = Origin_RotVector_RotVector2_motorAngle[8]
	MyVector3d.Vector3d_RotateBy(RotVector2, axis, angle)
	Origin_RotVector_RotVector2_motorAngle[6] = RotVector2[0]
	Origin_RotVector_RotVector2_motorAngle[7] = RotVector2[1]
	Origin_RotVector_RotVector2_motorAngle[8] = RotVector2[2]

def RobotNode_Rotate2(Origin_RotVector_RotVector2_motorAngle, axis, angle):
	RotVector2 = [0,0,0]
	RotVector2[0] = Origin_RotVector_RotVector2_motorAngle[6]
	RotVector2[1] = Origin_RotVector_RotVector2_motorAngle[7]
	RotVector2[2] = Origin_RotVector_RotVector2_motorAngle[8]
	MyVector3d.Vector3d_RotateBy(RotVector2, axis, angle)
	Origin_RotVector_RotVector2_motorAngle[6] = RotVector2[0]
	Origin_RotVector_RotVector2_motorAngle[7] = RotVector2[1]
	Origin_RotVector_RotVector2_motorAngle[8] = RotVector2[2]
	Origin_RotVector_RotVector2_motorAngle[9] = Origin_RotVector_RotVector2_motorAngle[9] + angle

def RobotNode_Rotate3(point, Origin_RotVector_RotVector2_motorAngle, pt, basePt, axis, angle):
	temp = [0,0,0]
	MyVector3d.Vector3d_GapOfAB(temp, pt, basePt)
	_length = MyVector3d.Vector3d_Length(temp)
	MyVector3d.Vector3d_Identify(temp)
	MyVector3d.Vector3d_RotateBy(temp, axis, angle)

	temp2 = [0,0,0]
	MyVector3d.Vector3d_MultiplyOfK(temp2, temp, _length)
	result = [0,0,0]
	MyVector3d.Vector3d_SumOfAB(result, basePt, temp2)
	MyVector3d.Vector3d_Copy(result, point)

def RobotNode_New(Origin_RotVector_RotVector2_motorAngle, x, y, z):
	Origin = [0,0,0]
	MyVector3d.Vector3d_Set(Origin, x, y, z)
	Origin_RotVector_RotVector2_motorAngle[0] = Origin[0]
	Origin_RotVector_RotVector2_motorAngle[1] = Origin[1]
	Origin_RotVector_RotVector2_motorAngle[2] = Origin[2]
	Origin_RotVector_RotVector2_motorAngle[3] = 0
	Origin_RotVector_RotVector2_motorAngle[4] = 0
	Origin_RotVector_RotVector2_motorAngle[5] = 0
	Origin_RotVector_RotVector2_motorAngle[6] = 0
	Origin_RotVector_RotVector2_motorAngle[7] = 0
	Origin_RotVector_RotVector2_motorAngle[8] = 0
	Origin_RotVector_RotVector2_motorAngle[9] = 0