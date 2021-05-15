import math

def Matrix4X4_New(entry):
    entry = [[0 for i in range(4)] for j in range(4)]
    entry[0][0] = 1.0
    entry[0][1] = 0.0
    entry[0][2] = 0.0
    entry[0][3] = 0.0
    entry[1][0] = 0.0
    entry[1][1] = 1.0
    entry[1][2] = 0.0
    entry[1][3] = 0.0
    entry[2][0] = 0.0
    entry[2][1] = 0.0
    entry[2][2] = 1.0
    entry[2][3] = 0.0
    entry[3][0] = 0.0
    entry[3][1] = 0.0
    entry[3][2] = 0.0
    entry[3][3] = 1.0

def Matrix4X4_Copy(entry_From, entry_To):
	for i in range(4):
		for j in range(4):
			entry_To[i][j] = entry_From[i][j]

def Matrix4X4_SetToIdentity(entry):
    entry[0][0] = 1.0
    entry[0][1] = 0.0
    entry[0][2] = 0.0
    entry[0][3] = 0.0
    entry[1][0] = 0.0
    entry[1][1] = 1.0
    entry[1][2] = 0.0
    entry[1][3] = 0.0
    entry[2][0] = 0.0
    entry[2][1] = 0.0
    entry[2][2] = 1.0
    entry[2][3] = 0.0
    entry[3][0] = 0.0
    entry[3][1] = 0.0
    entry[3][2] = 0.0
    entry[3][3] = 1.0

def Matrix4X4_PostMultBy(entry, m):
    r = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            r[i][j] = 0

    for i in range(4):
        for j in range(4):
            for k in range(4):
                r[i][j] += entry[i][k] * m[k][j]

    for i in range(4):
        for j in range(4):
            entry[i][j] = r[i][j]

def Matrix4X4_Scale(entry, k):
	for i in range(4):
		for j in range(4):
			entry[i][j] = entry[i][j] * k

def Matrix4X4_Determinant(entry):
    value = entry[0][3] * entry[1][2] * entry[2][1] * entry[3][0]-entry[0][2] * entry[1][3] * entry[2][1] * entry[3][0]-entry[0][3] * entry[1][1] * entry[2][2] * entry[3][0]+entry[0][1] * entry[1][3]    * entry[2][2] * entry[3][0]+ entry[0][2] * entry[1][1] * entry[2][3] * entry[3][0]-entry[0][1] * entry[1][2] * entry[2][3] * entry[3][0]-entry[0][3] * entry[1][2] * entry[2][0] * entry[3][1]+entry[0][2] * entry[1][3] * entry[2][0] * entry[3][1] + entry[0][3] * entry[1][0] * entry[2][2] * entry[3][1]-entry[0][0] * entry[1][3] * entry[2][2] * entry[3][1]-entry[0][2] * entry[1][0] * entry[2][3] * entry[3][1]+entry[0][0] * entry[1][2] * entry[2][3] * entry[3][1] +	entry[0][3] * entry[1][1] * entry[2][0] * entry[3][2]-entry[0][1] * entry[1][3] * entry[2][0] * entry[3][2]-entry[0][3] * entry[1][0] * entry[2][1] * entry[3][2]+entry[0][0] * entry[1][3] * entry[2][1] * entry[3][2] + entry[0][1] * entry[1][0] * entry[2][3] * entry[3][2]-entry[0][0] * entry[1][1] * entry[2][3] * entry[3][2]-entry[0][2] * entry[1][1] * entry[2][0] * entry[3][3]+entry[0][1] * entry[1][2] * entry[2][0] * entry[3][3] +	entry[0][2] * entry[1][0] * entry[2][1] * entry[3][3]-entry[0][0] * entry[1][2] * entry[2][1] * entry[3][3]-entry[0][1] * entry[1][0] * entry[2][2] * entry[3][3]+entry[0][0] * entry[1][1]    * entry[2][2] * entry[3][3]
    return value

def Matrix4X4_Inverse(entry):
    determinant = Matrix4X4_Determinant(entry)
    if abs(determinant) < 0.0001:
        return
    r = [[0 for i in range(4)] for j in range(4)]
    r[0][0] = entry[1][2]*entry[2][3]*entry[3][1] - entry[1][3]*entry[2][2]*entry[3][1] + entry[1][3]*entry[2][1]*entry[3][2] - entry[1][1]*entry[2][3]*entry[3][2] - entry[1][2]*entry[2][1]*entry[3][3] + entry[1][1]*entry[2][2]*entry[3][3]
    r[0][1] = entry[0][3]*entry[2][2]*entry[3][1] - entry[0][2]*entry[2][3]*entry[3][1] - entry[0][3]*entry[2][1]*entry[3][2] + entry[0][1]*entry[2][3]*entry[3][2] + entry[0][2]*entry[2][1]*entry[3][3] - entry[0][1]*entry[2][2]*entry[3][3]
    r[0][2] = entry[0][2]*entry[1][3]*entry[3][1] - entry[0][3]*entry[1][2]*entry[3][1] + entry[0][3]*entry[1][1]*entry[3][2] - entry[0][1]*entry[1][3]*entry[3][2] - entry[0][2]*entry[1][1]*entry[3][3] + entry[0][1]*entry[1][2]*entry[3][3]
    r[0][3] = entry[0][3]*entry[1][2]*entry[2][1] - entry[0][2]*entry[1][3]*entry[2][1] - entry[0][3]*entry[1][1]*entry[2][2] + entry[0][1]*entry[1][3]*entry[2][2] + entry[0][2]*entry[1][1]*entry[2][3] - entry[0][1]*entry[1][2]*entry[2][3]
    r[1][0] = entry[1][3]*entry[2][2]*entry[3][0] - entry[1][2]*entry[2][3]*entry[3][0] - entry[1][3]*entry[2][0]*entry[3][2] + entry[1][0]*entry[2][3]*entry[3][2] + entry[1][2]*entry[2][0]*entry[3][3] - entry[1][0]*entry[2][2]*entry[3][3]
    r[1][1] = entry[0][2]*entry[2][3]*entry[3][0] - entry[0][3]*entry[2][2]*entry[3][0] + entry[0][3]*entry[2][0]*entry[3][2] - entry[0][0]*entry[2][3]*entry[3][2] - entry[0][2]*entry[2][0]*entry[3][3] + entry[0][0]*entry[2][2]*entry[3][3]
    r[1][2] = entry[0][3]*entry[1][2]*entry[3][0] - entry[0][2]*entry[1][3]*entry[3][0] - entry[0][3]*entry[1][0]*entry[3][2] + entry[0][0]*entry[1][3]*entry[3][2] + entry[0][2]*entry[1][0]*entry[3][3] - entry[0][0]*entry[1][2]*entry[3][3]
    r[1][3] = entry[0][2]*entry[1][3]*entry[2][0] - entry[0][3]*entry[1][2]*entry[2][0] + entry[0][3]*entry[1][0]*entry[2][2] - entry[0][0]*entry[1][3]*entry[2][2] - entry[0][2]*entry[1][0]*entry[2][3] + entry[0][0]*entry[1][2]*entry[2][3]
    r[2][0] = entry[1][1]*entry[2][3]*entry[3][0] - entry[1][3]*entry[2][1]*entry[3][0] + entry[1][3]*entry[2][0]*entry[3][1] - entry[1][0]*entry[2][3]*entry[3][1] - entry[1][1]*entry[2][0]*entry[3][3] + entry[1][0]*entry[2][1]*entry[3][3]
    r[2][1] = entry[0][3]*entry[2][1]*entry[3][0] - entry[0][1]*entry[2][3]*entry[3][0] - entry[0][3]*entry[2][0]*entry[3][1] + entry[0][0]*entry[2][3]*entry[3][1] + entry[0][1]*entry[2][0]*entry[3][3] - entry[0][0]*entry[2][1]*entry[3][3]
    r[2][2] = entry[0][1]*entry[1][3]*entry[3][0] - entry[0][3]*entry[1][1]*entry[3][0] + entry[0][3]*entry[1][0]*entry[3][1] - entry[0][0]*entry[1][3]*entry[3][1] - entry[0][1]*entry[1][0]*entry[3][3] + entry[0][0]*entry[1][1]*entry[3][3]
    r[2][3] = entry[0][3]*entry[1][1]*entry[2][0] - entry[0][1]*entry[1][3]*entry[2][0] - entry[0][3]*entry[1][0]*entry[2][1] + entry[0][0]*entry[1][3]*entry[2][1] + entry[0][1]*entry[1][0]*entry[2][3] - entry[0][0]*entry[1][1]*entry[2][3]
    r[3][0] = entry[1][2]*entry[2][1]*entry[3][0] - entry[1][1]*entry[2][2]*entry[3][0] - entry[1][2]*entry[2][0]*entry[3][1] + entry[1][0]*entry[2][2]*entry[3][1] + entry[1][1]*entry[2][0]*entry[3][2] - entry[1][0]*entry[2][1]*entry[3][2]
    r[3][1] = entry[0][1]*entry[2][2]*entry[3][0] - entry[0][2]*entry[2][1]*entry[3][0] + entry[0][2]*entry[2][0]*entry[3][1] - entry[0][0]*entry[2][2]*entry[3][1] - entry[0][1]*entry[2][0]*entry[3][2] + entry[0][0]*entry[2][1]*entry[3][2]
    r[3][2] = entry[0][2]*entry[1][1]*entry[3][0] - entry[0][1]*entry[1][2]*entry[3][0] - entry[0][2]*entry[1][0]*entry[3][1] + entry[0][0]*entry[1][2]*entry[3][1] + entry[0][1]*entry[1][0]*entry[3][2] - entry[0][0]*entry[1][1]*entry[3][2]
    r[3][3] = entry[0][1]*entry[1][2]*entry[2][0] - entry[0][2]*entry[1][1]*entry[2][0] + entry[0][2]*entry[1][0]*entry[2][1] - entry[0][0]*entry[1][2]*entry[2][1] - entry[0][1]*entry[1][0]*entry[2][2] + entry[0][0]*entry[1][1]*entry[2][2]


    for i in range(4):
	    for j in range(4):
	        entry[i][j] = r[i][j]
    Matrix4X4_Scale(entry, 1.0 / determinant)


def Matrix4X4_GetOrigin(entry, origin):
    origin[0] = entry[3][0]
    origin[1] = entry[3][1]
    origin[2] = entry[3][2]

def Matrix4X4_GetXAxis(entry, XAxis):
	XAxis[0] = entry[0][0]
	XAxis[1] = entry[0][1]
	XAxis[2] = entry[0][2]

def Matrix4X4_GetYAxis(entry, YAxis):
	YAxis[0] = entry[1][0]
	YAxis[1] = entry[1][1]
	YAxis[2] = entry[1][2]

def Matrix4X4_GetZAxis(entry, ZAxis):
	ZAxis[0] = entry[2][0]
	ZAxis[1] = entry[2][1]
	ZAxis[2] = entry[2][2]

def Matrix4X4_Translation(entry, x, y, z):
	entry[3][0] = entry[3][0] + x
	entry[3][1] = entry[3][1] + y
	entry[3][2] = entry[3][2] + z

def Matrix4X4_RotationByX(entry, angle):
    mat = [[0 for i in range(4)] for j in range(4)]
    Matrix4X4_New(mat)
    mat[1][1] = math.cos(angle)
    mat[1][2] = math.sin(angle)
    mat[2][1] = -math.sin(angle)
    mat[2][2] = math.cos(angle)
    Matrix4X4_PostMultBy(entry, mat)

def Matrix4X4_RotationByY(entry, angle):
    mat = [[0 for i in range(4)] for j in range(4)]
    Matrix4X4_New(mat)
    mat[0][0] = math.cos(angle)
    mat[0][2] = math.sin(angle)
    mat[2][0] = -math.sin(angle)
    mat[2][2] = math.cos(angle)
    Matrix4X4_PostMultBy(entry, mat)

def Matrix4X4_RotationByZ(entry, angle):
    mat = [[0 for i in range(4)] for j in range(4)]
    Matrix4X4_New(mat)
    mat[0][0] = math.cos(angle)
    mat[0][1] = math.sin(angle)
    mat[1][0] = -math.sin(angle)
    mat[1][1] = math.cos(angle)
    Matrix4X4_PostMultBy(entry, mat)

def Matrix4X4_Rotation(entry, angle, axis):
    mat = [[0 for i in range(4)] for j in range(4)]
    Matrix4X4_New(mat)
    x = axis[0]
    y = axis[1]
    z = axis[2]
    s = math.sin(angle)
    c = math.cos(angle)
    t = 1 - c
    mat[0][0] = 1 + t * (x*x - 1)
    mat[0][1] = z * s + t * x * y
    mat[0][2] = -y * s + t * x * z
    mat[0][3] = 0
    mat[1][0] = -z * s + t * x * y
    mat[1][1] = 1 + t * (y * y - 1)
    mat[1][2] = x * s + t * y * z
    mat[1][3] = 0
    mat[2][0] = y * s + t * x * z
    mat[2][1] = -x * s + t * y * z
    mat[2][2] = 1 + t * (z * z - 1)
    mat[2][3] = 0
    mat[3][0] = 0
    mat[3][1] = 0
    mat[3][2] = 0
    mat[3][3] = 1
    Matrix4X4_PostMultBy(entry, mat)

def Matrix4X4_SetCoordSystem(entry, pt, axisX, axisY, axisZ):
    entry[3][0] = pt[0]
    entry[3][1] = pt[1]
    entry[3][2] = pt[2]
    entry[0][0] = axisX[0]
    entry[0][1] = axisX[1]
    entry[0][2] = axisX[2]
    entry[1][0] = axisY[0]
    entry[1][1] = axisY[1]
    entry[1][2] = axisY[2]
    entry[2][0] = axisZ[0]
    entry[2][1] = axisZ[1]
    entry[2][2] = axisZ[2]