import math

def Vector3d_kXAxis(xyz):
    xyz[0] = 1
    xyz[1] = 0
    xyz[2] = 0

def Vector3d_kYAxis(xyz):
	xyz[0] = 0
	xyz[1] = 1
	xyz[2] = 0

def Vector3d_kZAxis(xyz):
	xyz[0] = 0
	xyz[1] = 0
	xyz[2] = 1

def Vector3d_kZero(xyz):
	xyz[0] = 0
	xyz[1] = 0
	xyz[2] = 0

def Vector3d_Set(xyz, x, y, z):
	xyz[0] = x
	xyz[1] = y
	xyz[2] = z

def Vector3d_MultiplyOfAB(xyz_A, xyz_B):
	return xyz_A[0] * xyz_B[0] + xyz_A[1] * xyz_B[1] + xyz_A[2] * xyz_B[2]

def Vector3d_MultiplyOfK(xyzM, xyz, K):
	xyzM[0] = xyz[0] * K
	xyzM[1] = xyz[1] * K
	xyzM[2] = xyz[2] * K

def Vector3d_Copy(xyz_copyFrom, xyz_copyTo):
	xyz_copyTo[0] = xyz_copyFrom[0]
	xyz_copyTo[1] = xyz_copyFrom[1]
	xyz_copyTo[2] = xyz_copyFrom[2]

def Vector3d_GapOfAB(xyz_Gap, xyz_A, xyz_B):
	xyz_Gap[0] = xyz_A[0] - xyz_B[0]
	xyz_Gap[1] = xyz_A[1] - xyz_B[1]
	xyz_Gap[2] = xyz_A[2] - xyz_B[2]

def Vector3d_SumOfAB(xyz_Sum, xyz_A, xyz_B):
	xyz_Sum[0] = xyz_A[0] + xyz_B[0]
	xyz_Sum[1] = xyz_A[1] + xyz_B[1]
	xyz_Sum[2] = xyz_A[2] + xyz_B[2]

def Vector3d_CrossOfAB(xyz, xyz_A, xyz_B):
	xyz[0] = xyz_A[1] * xyz_B[2] - xyz_A[2] * xyz_B[1]
	xyz[1] = xyz_A[2] * xyz_B[0] - xyz_A[0] * xyz_B[2]
	xyz[2] = xyz_A[0] * xyz_B[1] - xyz_A[1] * xyz_B[0]

def Vector3d_Length(xyz):
	re = Vector3d_MultiplyOfAB(xyz, xyz)
	return math.sqrt(re)

def Vector3d_CrossAngleOfAB(xyz_A, xyz_B):
    a = Vector3d_MultiplyOfAB(xyz_A, xyz_B)
    b = Vector3d_MultiplyOfAB(xyz_A, xyz_A)
    c = Vector3d_MultiplyOfAB(xyz_B, xyz_B)
    result = a / (math.sqrt(b) * math.sqrt(c))
    if result > 1.0:
        result = 1.0
    elif result < -1.0:
        result = -1.0
    return math.acos(result)

def Vector3d_Translate(xyz, xyz_offset):
	xyz[0] = xyz[0] + xyz_offset[0]
	xyz[1] = xyz[1] + xyz_offset[1]
	xyz[2] = xyz[2] + xyz_offset[2]

def Vector3d_Identify(xyz):
	L = Vector3d_Length(xyz)
	if abs(L) > 0.0001:
		Vector3d_MultiplyOfK(xyz, xyz, 1.0 / L)

def Vector3d_RotateBy(xyz, RefV, Angle):
	Axis = [0,0,0]
	Vector3d_Copy(RefV, Axis)
	Vector3d_Identify(Axis)

	AlongAxis = [0,0,0]
	tempAlongAxis = Vector3d_MultiplyOfAB(xyz, Axis)
	Vector3d_MultiplyOfK(AlongAxis, Axis, tempAlongAxis)

	AxisXInRotPlane = [0,0,0]
	Vector3d_GapOfAB(AxisXInRotPlane, xyz, AlongAxis)

	AxisYInRotPlane = [0,0,0]
	Vector3d_CrossOfAB(AxisYInRotPlane, Axis, AxisXInRotPlane)

	InRotPlane = [0,0,0]
	InRotPlane_1 = [0,0,0]
	InRotPlane_2 = [0,0,0]
	Vector3d_MultiplyOfK(InRotPlane_1, AxisXInRotPlane, math.cos(Angle))
	Vector3d_MultiplyOfK(InRotPlane_2, AxisYInRotPlane, math.sin(Angle))
	Vector3d_SumOfAB(InRotPlane, InRotPlane_1, InRotPlane_2)

	Vector3d_SumOfAB(xyz, AlongAxis, InRotPlane)

def Vector3d_TransformBy(xyz, mat):
	r = [0,0,0]
	r[0] = xyz[0]
	r[1] = xyz[1]
	r[2] = xyz[2]

	r2 = [0,0,0]
	r2[0] = 0
	r2[1] = 0
	r2[2] = 0
	for i in range(3):
		for j in range(3):
		    r2[i] += r[j] * mat[j][i]

	xyz[0] = r2[0]
	xyz[1] = r2[1]
	xyz[2] = r2[2]