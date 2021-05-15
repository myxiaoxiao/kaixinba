// RobotEngine.cpp : �������̨Ӧ�ó������ڵ㡣
//

#include "stdafx.h"
#include <math.h>
#include <stdio.h>

//#define _Delta 0.0001;
//#define _PI 3.14159265358979323846;

float _A_E_Step_Angle = 360.0 / 20000.0;
float _F_Step_Angle = 360.0 / 12800.0;
float _RobotLinks[63];
float _backAngles[6];

void Vector3d_kXAxis(float xyz[3])
{
	xyz[0] = 1;
	xyz[1] = 0;
	xyz[2] = 0;
}

void Vector3d_kYAxis(float xyz[3])
{
	xyz[0] = 0;
	xyz[1] = 1;
	xyz[2] = 0;
}

void Vector3d_kZAxis(float xyz[3])
{
	xyz[0] = 0;
	xyz[1] = 0;
	xyz[2] = 1;
}

void Vector3d_kZero(float xyz[3])
{
	xyz[0] = 0;
	xyz[1] = 0;
	xyz[2] = 0;
}

void Vector3d_Set(float xyz[3], float x, float y, float z)
{
	xyz[0] = x;
	xyz[1] = y;
	xyz[2] = z;
}

float Vector3d_MultiplyOfAB(float xyz_A[3], float xyz_B[3])
{
	return xyz_A[0] * xyz_B[0] + xyz_A[1] * xyz_B[1] + xyz_A[2] * xyz_B[2];
}

void Vector3d_MultiplyOfK(float xyzM[3], float xyz[3], float K)
{
	xyzM[0] = xyz[0] * K;
	xyzM[1] = xyz[1] * K;
	xyzM[2] = xyz[2] * K;
}

void Vector3d_Copy(float xyz_copyFrom[3], float xyz_copyTo[3])
{
	xyz_copyTo[0] = xyz_copyFrom[0];
	xyz_copyTo[1] = xyz_copyFrom[1];
	xyz_copyTo[2] = xyz_copyFrom[2];
}

void Vector3d_GapOfAB(float xyz_Gap[3], float xyz_A[3], float xyz_B[3])
{
	xyz_Gap[0] = xyz_A[0] - xyz_B[0];
	xyz_Gap[1] = xyz_A[1] - xyz_B[1];
	xyz_Gap[2] = xyz_A[2] - xyz_B[2];
}

void Vector3d_SumOfAB(float xyz_Sum[3], float xyz_A[3], float xyz_B[3])
{
	xyz_Sum[0] = xyz_A[0] + xyz_B[0];
	xyz_Sum[1] = xyz_A[1] + xyz_B[1];
	xyz_Sum[2] = xyz_A[2] + xyz_B[2];
}

void Vector3d_CrossOfAB(float xyz[3], float xyz_A[3], float xyz_B[3])
{
	xyz[0] = xyz_A[1] * xyz_B[2] - xyz_A[2] * xyz_B[1];
	xyz[1] = xyz_A[2] * xyz_B[0] - xyz_A[0] * xyz_B[2];
	xyz[2] = xyz_A[0] * xyz_B[1] - xyz_A[1] * xyz_B[0];
}

float Vector3d_Length(float xyz[3])
{
	float re = Vector3d_MultiplyOfAB(xyz, xyz);
	return sqrt(re);
}

float Vector3d_CrossAngleOfAB(float xyz_A[3], float xyz_B[3])
{
	float a = Vector3d_MultiplyOfAB(xyz_A, xyz_B);
	float b = Vector3d_MultiplyOfAB(xyz_A, xyz_A);
	float c = Vector3d_MultiplyOfAB(xyz_B, xyz_B);
	float result = a / (sqrt(b) * sqrt(c));
	if (result > 1.0)
		result = 1.0;
	else if (result < -1.0)
		result = -1.0;

	return acos(result);
}

void Vector3d_Translate(float xyz[3], float xyz_offset[3])
{
	xyz[0] = xyz[0] + xyz_offset[0];
	xyz[1] = xyz[1] + xyz_offset[1];
	xyz[2] = xyz[2] + xyz_offset[2];
}

void Vector3d_Identify(float xyz[3])
{
	float L = Vector3d_Length(xyz);
	Vector3d_MultiplyOfK(xyz, xyz, 1.0 / L);
}

void Vector3d_RotateBy(float xyz[3], float RefV[3], float Angle)
{
	float Axis[3];
	Vector3d_Copy(RefV, Axis);
	Vector3d_Identify(Axis);

	float AlongAxis[3];
	float tempAlongAxis = Vector3d_MultiplyOfAB(xyz, Axis);
	Vector3d_MultiplyOfK(AlongAxis, Axis, tempAlongAxis);

	float AxisXInRotPlane[3];
	Vector3d_GapOfAB(AxisXInRotPlane, xyz, AlongAxis);

	float AxisYInRotPlane[3];
	Vector3d_CrossOfAB(AxisYInRotPlane, Axis, AxisXInRotPlane);

	float InRotPlane[3];
	float InRotPlane_1[3];
	float InRotPlane_2[3];
	Vector3d_MultiplyOfK(InRotPlane_1, AxisXInRotPlane, cos(Angle));
	Vector3d_MultiplyOfK(InRotPlane_2, AxisYInRotPlane, sin(Angle));
	Vector3d_SumOfAB(InRotPlane, InRotPlane_1, InRotPlane_2);

	Vector3d_SumOfAB(xyz, AlongAxis, InRotPlane);
}

void Matrix4X4_New(float entry[4][4])
{
	entry[0][0] = 1.0; entry[0][1] = 0.0; entry[0][2] = 0.0; entry[0][3] = 0.0;
	entry[1][0] = 0.0; entry[1][1] = 1.0; entry[1][2] = 0.0; entry[1][3] = 0.0;
	entry[2][0] = 0.0; entry[2][1] = 0.0; entry[2][2] = 1.0; entry[2][3] = 0.0;
	entry[3][0] = 0.0; entry[3][1] = 0.0; entry[3][2] = 0.0; entry[3][3] = 1.0;
}

void Matrix4X4_Copy(float entry_From[4][4], float entry_To[4][4])
{
	for (int i = 0; i < 4; i ++)
	{
		for (int j = 0; j < 4; j ++)
		{
			entry_To[i][j] = entry_From[i][j];
		}
	}
}

void Matrix4X4_SetToIdentity(float entry[4][4])
{
	entry[0][0] = 1.0; entry[0][1] = 0.0; entry[0][2] = 0.0; entry[0][3] = 0.0;
	entry[1][0] = 0.0; entry[1][1] = 1.0; entry[1][2] = 0.0; entry[1][3] = 0.0;
	entry[2][0] = 0.0; entry[2][1] = 0.0; entry[2][2] = 1.0; entry[2][3] = 0.0;
	entry[3][0] = 0.0; entry[3][1] = 0.0; entry[3][2] = 0.0; entry[3][3] = 1.0;
}

void Matrix4X4_PostMultBy(float entry[4][4], float m[4][4])
{
	float r[4][4];
	for (int i = 0; i < 4; i ++)
	{
		for (int j = 0; j < 4; j ++)
		{
			r[i][j] = 0;
		}
	}

	for (int i = 0; i < 4; i ++)
	{
		for (int j = 0; j < 4; j ++)
		{
			for (int k = 0; k < 4; k ++)
			{
				r[i][j] += entry[i][k] * m[k][j];
			}
		}
	}

	for (int i = 0; i < 4; i ++)
	{
		for (int j = 0; j < 4; j ++)
		{
			entry[i][j] = r[i][j];
		}
	}
}

void Matrix4X4_Scale(float entry[4][4], float k)
{
	for (int i = 0; i < 4; i ++)
	{
		for (int j = 0; j < 4; j ++)
		{
			entry[i][j] *= k;
		}
	}
}

float Matrix4X4_Determinant(float entry[4][4])
{
	float value;
	value =
		entry[0][3] * entry[1][2] * entry[2][1] * entry[3][0]-entry[0][2] * entry[1][3] * entry[2][1] * entry[3][0]-entry[0][3] * entry[1][1] * entry[2][2] * entry[3][0]+entry[0][1] * entry[1][3]    * entry[2][2] * entry[3][0]+
		entry[0][2] * entry[1][1] * entry[2][3] * entry[3][0]-entry[0][1] * entry[1][2] * entry[2][3] * entry[3][0]-entry[0][3] * entry[1][2] * entry[2][0] * entry[3][1]+entry[0][2] * entry[1][3]    * entry[2][0] * entry[3][1]+
		entry[0][3] * entry[1][0] * entry[2][2] * entry[3][1]-entry[0][0] * entry[1][3] * entry[2][2] * entry[3][1]-entry[0][2] * entry[1][0] * entry[2][3] * entry[3][1]+entry[0][0] * entry[1][2]    * entry[2][3] * entry[3][1]+
		entry[0][3] * entry[1][1] * entry[2][0] * entry[3][2]-entry[0][1] * entry[1][3] * entry[2][0] * entry[3][2]-entry[0][3] * entry[1][0] * entry[2][1] * entry[3][2]+entry[0][0] * entry[1][3]    * entry[2][1] * entry[3][2]+
		entry[0][1] * entry[1][0] * entry[2][3] * entry[3][2]-entry[0][0] * entry[1][1] * entry[2][3] * entry[3][2]-entry[0][2] * entry[1][1] * entry[2][0] * entry[3][3]+entry[0][1] * entry[1][2]    * entry[2][0] * entry[3][3]+
		entry[0][2] * entry[1][0] * entry[2][1] * entry[3][3]-entry[0][0] * entry[1][2] * entry[2][1] * entry[3][3]-entry[0][1] * entry[1][0] * entry[2][2] * entry[3][3]+entry[0][0] * entry[1][1]    * entry[2][2] * entry[3][3];
	return value;
}

void Matrix4X4_Inverse(float entry[4][4])
{
	float determinant = Matrix4X4_Determinant(entry);
	if (abs(determinant) < 0.0001)
	{
		return;
	}

	float r[4][4];

	r[0][0] = entry[1][2]*entry[2][3]*entry[3][1] - entry[1][3]*entry[2][2]*entry[3][1] + entry[1][3]*entry[2][1]*entry[3][2] - entry[1][1]*entry[2][3]*entry[3][2] - entry[1][2]*entry[2][1]*entry[3][3] + entry[1][1]*entry[2][2]*entry[3][3];
	r[0][1] = entry[0][3]*entry[2][2]*entry[3][1] - entry[0][2]*entry[2][3]*entry[3][1] - entry[0][3]*entry[2][1]*entry[3][2] + entry[0][1]*entry[2][3]*entry[3][2] + entry[0][2]*entry[2][1]*entry[3][3] - entry[0][1]*entry[2][2]*entry[3][3];
	r[0][2] = entry[0][2]*entry[1][3]*entry[3][1] - entry[0][3]*entry[1][2]*entry[3][1] + entry[0][3]*entry[1][1]*entry[3][2] - entry[0][1]*entry[1][3]*entry[3][2] - entry[0][2]*entry[1][1]*entry[3][3] + entry[0][1]*entry[1][2]*entry[3][3];
	r[0][3] = entry[0][3]*entry[1][2]*entry[2][1] - entry[0][2]*entry[1][3]*entry[2][1] - entry[0][3]*entry[1][1]*entry[2][2] + entry[0][1]*entry[1][3]*entry[2][2] + entry[0][2]*entry[1][1]*entry[2][3] - entry[0][1]*entry[1][2]*entry[2][3];
	r[1][0] = entry[1][3]*entry[2][2]*entry[3][0] - entry[1][2]*entry[2][3]*entry[3][0] - entry[1][3]*entry[2][0]*entry[3][2] + entry[1][0]*entry[2][3]*entry[3][2] + entry[1][2]*entry[2][0]*entry[3][3] - entry[1][0]*entry[2][2]*entry[3][3];
	r[1][1] = entry[0][2]*entry[2][3]*entry[3][0] - entry[0][3]*entry[2][2]*entry[3][0] + entry[0][3]*entry[2][0]*entry[3][2] - entry[0][0]*entry[2][3]*entry[3][2] - entry[0][2]*entry[2][0]*entry[3][3] + entry[0][0]*entry[2][2]*entry[3][3];
	r[1][2] = entry[0][3]*entry[1][2]*entry[3][0] - entry[0][2]*entry[1][3]*entry[3][0] - entry[0][3]*entry[1][0]*entry[3][2] + entry[0][0]*entry[1][3]*entry[3][2] + entry[0][2]*entry[1][0]*entry[3][3] - entry[0][0]*entry[1][2]*entry[3][3];
	r[1][3] = entry[0][2]*entry[1][3]*entry[2][0] - entry[0][3]*entry[1][2]*entry[2][0] + entry[0][3]*entry[1][0]*entry[2][2] - entry[0][0]*entry[1][3]*entry[2][2] - entry[0][2]*entry[1][0]*entry[2][3] + entry[0][0]*entry[1][2]*entry[2][3];
	r[2][0] = entry[1][1]*entry[2][3]*entry[3][0] - entry[1][3]*entry[2][1]*entry[3][0] + entry[1][3]*entry[2][0]*entry[3][1] - entry[1][0]*entry[2][3]*entry[3][1] - entry[1][1]*entry[2][0]*entry[3][3] + entry[1][0]*entry[2][1]*entry[3][3];
	r[2][1] = entry[0][3]*entry[2][1]*entry[3][0] - entry[0][1]*entry[2][3]*entry[3][0] - entry[0][3]*entry[2][0]*entry[3][1] + entry[0][0]*entry[2][3]*entry[3][1] + entry[0][1]*entry[2][0]*entry[3][3] - entry[0][0]*entry[2][1]*entry[3][3];
	r[2][2] = entry[0][1]*entry[1][3]*entry[3][0] - entry[0][3]*entry[1][1]*entry[3][0] + entry[0][3]*entry[1][0]*entry[3][1] - entry[0][0]*entry[1][3]*entry[3][1] - entry[0][1]*entry[1][0]*entry[3][3] + entry[0][0]*entry[1][1]*entry[3][3];
	r[2][3] = entry[0][3]*entry[1][1]*entry[2][0] - entry[0][1]*entry[1][3]*entry[2][0] - entry[0][3]*entry[1][0]*entry[2][1] + entry[0][0]*entry[1][3]*entry[2][1] + entry[0][1]*entry[1][0]*entry[2][3] - entry[0][0]*entry[1][1]*entry[2][3];
	r[3][0] = entry[1][2]*entry[2][1]*entry[3][0] - entry[1][1]*entry[2][2]*entry[3][0] - entry[1][2]*entry[2][0]*entry[3][1] + entry[1][0]*entry[2][2]*entry[3][1] + entry[1][1]*entry[2][0]*entry[3][2] - entry[1][0]*entry[2][1]*entry[3][2];
	r[3][1] = entry[0][1]*entry[2][2]*entry[3][0] - entry[0][2]*entry[2][1]*entry[3][0] + entry[0][2]*entry[2][0]*entry[3][1] - entry[0][0]*entry[2][2]*entry[3][1] - entry[0][1]*entry[2][0]*entry[3][2] + entry[0][0]*entry[2][1]*entry[3][2];
	r[3][2] = entry[0][2]*entry[1][1]*entry[3][0] - entry[0][1]*entry[1][2]*entry[3][0] - entry[0][2]*entry[1][0]*entry[3][1] + entry[0][0]*entry[1][2]*entry[3][1] + entry[0][1]*entry[1][0]*entry[3][2] - entry[0][0]*entry[1][1]*entry[3][2];
	r[3][3] = entry[0][1]*entry[1][2]*entry[2][0] - entry[0][2]*entry[1][1]*entry[2][0] + entry[0][2]*entry[1][0]*entry[2][1] - entry[0][0]*entry[1][2]*entry[2][1] - entry[0][1]*entry[1][0]*entry[2][2] + entry[0][0]*entry[1][1]*entry[2][2];


	for (int i = 0; i < 4; i ++)
	{
		for (int j = 0; j < 4; j ++)
		{
			entry[i][j] = r[i][j];
		}
	}

	Matrix4X4_Scale(entry, 1.0 / determinant);
}


void Matrix4X4_GetOrigin(float entry[4][4], float origin[3])
{
	origin[0] = entry[3][0];
	origin[1] = entry[3][1];
	origin[2] = entry[3][2];
}

void Matrix4X4_GetXAxis(float entry[4][4], float XAxis[3])
{
	XAxis[0] = entry[0][0];
	XAxis[1] = entry[0][1];
	XAxis[2] = entry[0][2];
}

void Matrix4X4_GetYAxis(float entry[4][4], float YAxis[3])
{
	YAxis[0] = entry[1][0];
	YAxis[1] = entry[1][1];
	YAxis[2] = entry[1][2];
}

void Matrix4X4_GetZAxis(float entry[4][4], float ZAxis[3])
{
	ZAxis[0] = entry[2][0];
	ZAxis[1] = entry[2][1];
	ZAxis[2] = entry[2][2];
}

void Matrix4X4_Translation(float entry[4][4], float x, float y, float z)
{
	entry[3][0] += x;
	entry[3][1] += y;
	entry[3][2] += z;
}

void Matrix4X4_RotationByX(float entry[4][4], float angle)
{
	float mat[4][4];
	Matrix4X4_New(mat);
	mat[1][1] = cos(angle); mat[1][2] = sin(angle);
	mat[2][1] = -sin(angle); mat[2][2] = cos(angle);

	Matrix4X4_PostMultBy(entry, mat);
}

void Matrix4X4_RotationByY(float entry[4][4], float angle)
{
	float mat[4][4];
	Matrix4X4_New(mat);
	mat[0][0] = cos(angle); mat[0][2] = sin(angle);
	mat[2][0] = -sin(angle); mat[2][2] = cos(angle);

	Matrix4X4_PostMultBy(entry, mat);
}

void Matrix4X4_RotationByZ(float entry[4][4], float angle)
{
	float mat[4][4];
	Matrix4X4_New(mat);
	mat[0][0] = cos(angle); mat[0][1] = sin(angle);
	mat[1][0] = -sin(angle); mat[1][1] = cos(angle);

	Matrix4X4_PostMultBy(entry, mat);
}

void Matrix4X4_Rotation(float entry[4][4], float angle, float axis[3])
{
	float mat[4][4];
	Matrix4X4_New(mat);

	float x, y, z, s, c, t;
	x = axis[0];
	y = axis[1];
	z = axis[2];

	s = sin(angle);
	c = cos(angle);
	t = 1 - c;

	mat[0][0] = 1 + t * (x*x - 1); mat[0][1] = z * s + t * x * y;mat[0][2] = -y * s + t * x * z; mat[0][3] = 0;
	mat[1][0] = -z * s + t * x * y ; mat[1][1] = 1 + t * (y * y - 1);mat[1][2] = x * s + t * y * z; mat[1][3] = 0;
	mat[2][0] = y * s + t * x * z; mat[2][1] = -x * s + t * y * z;mat[2][2] = 1 + t * (z * z - 1); mat[2][3] = 0;
	mat[3][0] = 0; mat[3][1] = 0;mat[3][2] = 0; mat[3][3] = 1;

	Matrix4X4_PostMultBy(entry, mat);
}

void Matrix4X4_SetCoordSystem(float entry[4][4], float pt[3], float axisX[3], float axisY[3], float axisZ[3])
{
	entry[3][0] = pt[0]; entry[3][1] = pt[1]; entry[3][2] = pt[2];
	entry[0][0] = axisX[0]; entry[0][1] = axisX[1]; entry[0][2] = axisX[2];
	entry[1][0] = axisY[0]; entry[1][1] = axisY[1]; entry[1][2] = axisY[2];
	entry[2][0] = axisZ[0]; entry[2][1] = axisZ[1]; entry[2][2] = axisZ[2];
}

void Vector3d_TransformBy(float xyz[3], float mat[4][4])
{
	float r[3];
	r[0] = xyz[0];
	r[1] = xyz[1];
	r[2] = xyz[2];

	float r2[3];
	r2[0] = 0;
	r2[1] = 0;
	r2[2] = 0;
	for (int i = 0; i < 3; i ++)
	{
		for (int j = 0; j < 3; j ++)
		{
			r2[i] += r[j] * mat[j][i];
		}
	}

	xyz[0] = r2[0];
	xyz[1] = r2[1];
	xyz[2] = r2[2];
}

void Point3d_New(float xyz[3])
{
	xyz[0] = 0;
	xyz[1] = 0;
	xyz[2] = 0;
}


void Point3d_TransformBy (float xyz[3], float mat[4][4])
{
	float r[4];
	r[0] = xyz[0];
	r[1] = xyz[1];
	r[2] = xyz[2];
	r[3] = 1.0;

	float r2[4];
	r2[0] = 0;
	r2[1] = 0;
	r2[2] = 0;
	r2[3] = 0;
	for (int j = 0; j < 4; j ++)
	{
		for (int i = 0; i < 4; i ++)
		{
			r2[j] += r[i] * mat[i][j];
		}
	}

	xyz[0] = r2[0];
	xyz[1] = r2[1];
	xyz[2] = r2[2];
}

void RobotNode_get_Point(float Origin_RotVector_RotVector2_motorAngle[10], float Origin[3])
{
	Origin[0] = Origin_RotVector_RotVector2_motorAngle[0];
	Origin[1] = Origin_RotVector_RotVector2_motorAngle[1];
	Origin[2] = Origin_RotVector_RotVector2_motorAngle[2];
}

void RobotNode_get_RotVector(float Origin_RotVector_RotVector2_motorAngle[10], float RotVector[3])
{
	RotVector[0] = Origin_RotVector_RotVector2_motorAngle[3];
	RotVector[1] = Origin_RotVector_RotVector2_motorAngle[4];
	RotVector[2] = Origin_RotVector_RotVector2_motorAngle[5];
}

void RobotNode_get_RotVector2(float Origin_RotVector_RotVector2_motorAngle[10], float RotVector2[3])
{
	RotVector2[0] = Origin_RotVector_RotVector2_motorAngle[6];
	RotVector2[1] = Origin_RotVector_RotVector2_motorAngle[7];
	RotVector2[2] = Origin_RotVector_RotVector2_motorAngle[8];
}

float RobotNode_get_MotorAngle(float Origin_RotVector_RotVector2_motorAngle[10])
{
	return Origin_RotVector_RotVector2_motorAngle[9];
}

void RobotNode_SetValue(float Origin_RotVector_RotVector2_motorAngle[10], float x, float y, float z, float x2, float y2, float z2, float initAngle)
{
	Origin_RotVector_RotVector2_motorAngle[0] = x;
	Origin_RotVector_RotVector2_motorAngle[1] = y;
	Origin_RotVector_RotVector2_motorAngle[2] = z;

	float Temp_RotVector[3];
	Temp_RotVector[0] = x2;
	Temp_RotVector[1] = y2;
	Temp_RotVector[2] = z2;
	Origin_RotVector_RotVector2_motorAngle[3] = x2;
	Origin_RotVector_RotVector2_motorAngle[4] = y2;
	Origin_RotVector_RotVector2_motorAngle[5] = z2;

	float Temp_RotVector2[3];
	Vector3d_kXAxis(Temp_RotVector2);
	Origin_RotVector_RotVector2_motorAngle[6] = Temp_RotVector2[0];
	Origin_RotVector_RotVector2_motorAngle[7] = Temp_RotVector2[1];
	Origin_RotVector_RotVector2_motorAngle[8] = Temp_RotVector2[2];

	float Temp_RotVector2XRotVector = Vector3d_MultiplyOfAB(Temp_RotVector2, Temp_RotVector);
	if(abs(Temp_RotVector2XRotVector - 1.0) < 0.0001 || abs(Temp_RotVector2XRotVector + 1.0) < 0.0001)
	{
		float Temp_YAxis[3];
		Vector3d_kYAxis(Temp_YAxis);
		Vector3d_CrossOfAB(Temp_RotVector2, Temp_RotVector, Temp_YAxis);
		Origin_RotVector_RotVector2_motorAngle[6] = Temp_RotVector2[0];
		Origin_RotVector_RotVector2_motorAngle[7] = Temp_RotVector2[1];
		Origin_RotVector_RotVector2_motorAngle[8] = Temp_RotVector2[2];
	}
	else
	{
		float Temp_Vector[3];
		Vector3d_CrossOfAB(Temp_Vector, Temp_RotVector, Temp_RotVector2);
		Vector3d_Copy(Temp_Vector, Temp_RotVector2);
		Origin_RotVector_RotVector2_motorAngle[6] = Temp_RotVector2[0];
		Origin_RotVector_RotVector2_motorAngle[7] = Temp_RotVector2[1];
		Origin_RotVector_RotVector2_motorAngle[8] = Temp_RotVector2[2];
	}

	Origin_RotVector_RotVector2_motorAngle[9] = initAngle;
}

void RobotNode_Rotate(float Origin_RotVector_RotVector2_motorAngle[10], float basePt[3], float axis[3], float angle)
{
	float Origin[3];
	Origin[0] = Origin_RotVector_RotVector2_motorAngle[0];
	Origin[1] = Origin_RotVector_RotVector2_motorAngle[1];
	Origin[2] = Origin_RotVector_RotVector2_motorAngle[2];

    float temp[3];
	Vector3d_GapOfAB(temp, Origin, basePt);
    float _length = Vector3d_Length(temp);
	Vector3d_Identify(temp);
	Vector3d_RotateBy(temp, axis, angle);

	float temp2[3];
	Vector3d_MultiplyOfK(temp2, temp, _length);
	float result[3];
	Vector3d_SumOfAB(result, basePt, temp2);
	Vector3d_Copy(result, Origin);
	Origin_RotVector_RotVector2_motorAngle[0] = Origin[0];
	Origin_RotVector_RotVector2_motorAngle[1] = Origin[1];
	Origin_RotVector_RotVector2_motorAngle[2] = Origin[2];

	float RotVector[3];
	RotVector[0] = Origin_RotVector_RotVector2_motorAngle[3];
	RotVector[1] = Origin_RotVector_RotVector2_motorAngle[4];
	RotVector[2] = Origin_RotVector_RotVector2_motorAngle[5];
	Vector3d_RotateBy(RotVector, axis, angle);
	Origin_RotVector_RotVector2_motorAngle[3] = RotVector[0];
	Origin_RotVector_RotVector2_motorAngle[4] = RotVector[1];
	Origin_RotVector_RotVector2_motorAngle[5] = RotVector[2];

	float RotVector2[3];
	RotVector2[0] = Origin_RotVector_RotVector2_motorAngle[6];
	RotVector2[1] = Origin_RotVector_RotVector2_motorAngle[7];
	RotVector2[2] = Origin_RotVector_RotVector2_motorAngle[8];
	Vector3d_RotateBy(RotVector2, axis, angle);
	Origin_RotVector_RotVector2_motorAngle[6] = RotVector2[0];
	Origin_RotVector_RotVector2_motorAngle[7] = RotVector2[1];
	Origin_RotVector_RotVector2_motorAngle[8] = RotVector2[2];

}

void RobotNode_Rotate2(float Origin_RotVector_RotVector2_motorAngle[10], float axis[3], float angle)
{
	float RotVector2[3];
	RotVector2[0] = Origin_RotVector_RotVector2_motorAngle[6];
	RotVector2[1] = Origin_RotVector_RotVector2_motorAngle[7];
	RotVector2[2] = Origin_RotVector_RotVector2_motorAngle[8];
	Vector3d_RotateBy(RotVector2, axis, angle);
	Origin_RotVector_RotVector2_motorAngle[6] = RotVector2[0];
	Origin_RotVector_RotVector2_motorAngle[7] = RotVector2[1];
	Origin_RotVector_RotVector2_motorAngle[8] = RotVector2[2];

	Origin_RotVector_RotVector2_motorAngle[9] += angle;
}

void RobotNode_Rotate(float point[3], float Origin_RotVector_RotVector2_motorAngle[10], float pt[3], float basePt[3], float axis[3], float angle)
{
	float temp[3];
	Vector3d_GapOfAB(temp, pt, basePt);
    float _length = Vector3d_Length(temp);
	Vector3d_Identify(temp);
	Vector3d_RotateBy(temp, axis, angle);

	float temp2[3];
	Vector3d_MultiplyOfK(temp2, temp, _length);
	float result[3];
	Vector3d_SumOfAB(result, basePt, temp2);
	Vector3d_Copy(result, point);
}

void RobotNode_New(float Origin_RotVector_RotVector2_motorAngle[10], float x, float y, float z)
{
	float Origin[3];
	Vector3d_Set(Origin, x, y, z);
	Origin_RotVector_RotVector2_motorAngle[0] = Origin[0];
	Origin_RotVector_RotVector2_motorAngle[1] = Origin[1];
	Origin_RotVector_RotVector2_motorAngle[2] = Origin[2];
	Origin_RotVector_RotVector2_motorAngle[3] = 0;
	Origin_RotVector_RotVector2_motorAngle[4] = 0;
	Origin_RotVector_RotVector2_motorAngle[5] = 0;
	Origin_RotVector_RotVector2_motorAngle[6] = 0;
	Origin_RotVector_RotVector2_motorAngle[7] = 0;
	Origin_RotVector_RotVector2_motorAngle[8] = 0;
	Origin_RotVector_RotVector2_motorAngle[9] = 0;
}

void RobotLinks_New(float RobotLinks[63])
{
	float node1[10];
	float node2[10];
	float node3[10];
	float node4[10];
	float node5[10];
	float node6[10];

	// 1
	RobotNode_New(node1, 0, 0, 0);
	// 2
	RobotNode_New(node2, 0, 0, 0);
	// 3
	RobotNode_New(node3, 0, 0, 0);
	// 4
	RobotNode_New(node4, 0, 0, 0);
	// 5
	RobotNode_New(node5, 0, 0, 0);
	// 6
	RobotNode_New(node6, 0, 0, 0);

	for (int i = 0; i < 10; i ++)
	{
		RobotLinks[i] = node1[i];
	}
	for (int i = 0; i < 10; i ++)
	{
		RobotLinks[i + 10] = node2[i];
	}
	for (int i = 0; i < 10; i ++)
	{
		RobotLinks[i + 20] = node3[i];
	}
	for (int i = 0; i < 10; i ++)
	{
		RobotLinks[i + 30] = node4[i];
	}
	for (int i = 0; i < 10; i ++)
	{
		RobotLinks[i + 40] = node5[i];
	}
	for (int i = 0; i < 10; i ++)
	{
		RobotLinks[i + 50] = node6[i];
	}
}

void RobotLinks_GetNode(float RobotLinks[63], int index, float node[10])
{
	switch (index)
	{
		case 1:
		{
			for (int i = 0; i < 10; i ++)
			{
				node[i] = RobotLinks[i];
			}
		}
		break;

		case 2:
		{
			for (int i = 0; i < 10; i ++)
			{
				node[i] = RobotLinks[i + 10];
			}
		}
		break;

		case 3:
		{
			for (int i = 0; i < 10; i ++)
			{
				node[i] = RobotLinks[i + 20];
			}
		}
		break;

		case 4:
		{
			for (int i = 0; i < 10; i ++)
			{
				node[i] = RobotLinks[i + 30];
			}
		}
		break;

		case 5:
		{
			for (int i = 0; i < 10; i ++)
			{
				node[i] = RobotLinks[i + 40];
			}
		}
		break;

		case 6:
		{
			for (int i = 0; i < 10; i ++)
			{
				node[i] = RobotLinks[i + 50];
			}
		}
		break;
	}
}

void RobotLinks_SetNode(float RobotLinks[63], int index, float node[10])
{
	switch (index)
	{
		case 1:
		{
			for (int i = 0; i < 10; i ++)
			{
				RobotLinks[i] = node[i];
			}
		}
		break;

		case 2:
		{
			for (int i = 0; i < 10; i ++)
			{
				RobotLinks[i + 10] = node[i];
			}
		}
		break;

		case 3:
		{
			for (int i = 0; i < 10; i ++)
			{
				RobotLinks[i + 20] = node[i];
			}
		}
		break;

		case 4:
		{
			for (int i = 0; i < 10; i ++)
			{
				RobotLinks[i + 30] = node[i];
			}
		}
		break;

		case 5:
		{
			for (int i = 0; i < 10; i ++)
			{
				RobotLinks[i + 40] = node[i];
			}
		}
		break;

		case 6:
		{
			for (int i = 0; i < 10; i ++)
			{
				RobotLinks[i + 50] = node[i];
			}
		}
		break;
	}
}

bool RobotLinks_GetNodeLength(float RobotLinks[63], int index, float& _length)
{
    if (index == 6)
    {
        _length = 0;
        return false;
    }

	float node[10];
	RobotLinks_GetNode(RobotLinks, index, node);
    float NextNode[10];
	RobotLinks_GetNode(RobotLinks, index + 1, NextNode);

	float nextNodePoint[3];
	RobotNode_get_Point(NextNode, nextNodePoint);

	float nodePoint[3];
	RobotNode_get_Point(node, nodePoint);

	float tempVector[3];
	Vector3d_GapOfAB(tempVector, nextNodePoint, nodePoint);
	_length = Vector3d_Length(tempVector);

    return true;
}

void RobotLinks_get_Node6XAxis(float RobotLinks[63], float node6XAxis[3])
{
	node6XAxis[2] = RobotLinks[62];
	node6XAxis[1] = RobotLinks[61];
	node6XAxis[0] = RobotLinks[60];
}

void RobotLinks_set_Node6XAxis(float RobotLinks[63], float node6XAxis[3])
{
	RobotLinks[62] = node6XAxis[2];
	RobotLinks[61] = node6XAxis[1];
	RobotLinks[60] = node6XAxis[0];
}

 bool Robot_Init(float RobotLinks[63], float rots[18], float Node6xAxis[3], float points[18], float initAngles[7])
{
	RobotLinks_New(RobotLinks);

    for (int i = 0; i < 6; i++)
    {
		float node[10];
		RobotLinks_GetNode(RobotLinks, i + 1, node);
		RobotNode_SetValue(node, points[i * 3], points[i * 3 + 1], points[i * 3 + 2], rots[i * 3], rots[i * 3 + 1], rots[i * 3 + 2], initAngles[i + 1]);
		RobotLinks_SetNode(RobotLinks,  i + 1, node);
    }

	RobotLinks_set_Node6XAxis(RobotLinks, Node6xAxis);

    return true;
}

void Robot_CalculatelTransformation(float transfrom[4][4], float from[4][4], float to[4][4])
{
	Matrix4X4_Copy(from, transfrom);
	Matrix4X4_Inverse(transfrom);
	Matrix4X4_PostMultBy(transfrom, to);
}

void Robot_CalculateMatrix(float RobotLinks[63], int index, float mat[4][4])
{
	float node[10];
	RobotLinks_GetNode(RobotLinks, index, node);
    float XAxis[3];
    float YAxis[3];
    float ZAxis[3];
    float origin[3];
    switch (index)
    {
        case 1:
        case 4:
        case 6:
            {
				RobotNode_get_RotVector(node, ZAxis);
				RobotNode_get_Point(node, origin);
				RobotNode_get_RotVector2(node, XAxis);
				Vector3d_CrossOfAB(YAxis, ZAxis, XAxis);
				Vector3d_Identify(YAxis);
            }
            break;

        case 2:
        case 3:
        case 5:
            {
				RobotNode_get_Point(node, origin);
				RobotNode_get_RotVector(node, XAxis);

				float node2[10];
				RobotLinks_GetNode(RobotLinks, index + 1, node2);

				float node2_Point[3];
				RobotNode_get_Point(node2, node2_Point);
				float node_Point[3];
				RobotNode_get_Point(node, node_Point);

				Vector3d_GapOfAB(ZAxis, node2_Point, node_Point);
				Vector3d_CrossOfAB(YAxis, ZAxis, XAxis);
				Vector3d_Identify(YAxis);
            }
            break;
    }

	Matrix4X4_SetCoordSystem(mat, origin, XAxis, YAxis, ZAxis);
}

float Robot_CalculateAngle(float from[3], float to[3], float normal[3])
{
	Vector3d_Identify(from);
	Vector3d_Identify(to);
	float result = Vector3d_MultiplyOfAB(from, to);
    if (result > 1.0)
        result = 1.0;
    else if (result < -1.0)
        result = -1.0;

    float angle = acos(result);

	float corssVector[3];
	Vector3d_CrossOfAB(corssVector, from, to);
	Vector3d_Identify(corssVector);
	Vector3d_Identify(normal);

	float value = Vector3d_MultiplyOfAB(corssVector, normal);
    if (abs(value - 1) < 0.0001)
    {
        return angle;
    }
    else
    {
        return -angle;
    }
}

float Robot_CalculateAngle(float from[3], float to[3])
{
	Vector3d_Identify(from);
	Vector3d_Identify(to);
	float result = Vector3d_MultiplyOfAB(from, to);
    if (result > 1.0)
        result = 1.0;
    else if (result < -1.0)
        result = -1.0;

    return acos(result);
}

void Robot_CalculateCirsPoints(float circlePlaneNormal[3], float cen1[3], float radius1, float cen2[3], float radius2, int& pointsCount, float point1[3], float point2[3])
{
	float cen1_cen2[3];
	Vector3d_GapOfAB(cen1_cen2, cen1, cen2);
	float distance = Vector3d_Length(cen1_cen2);
    if (distance < radius1 + radius2)
    {
        float a = (radius1 * radius1 - radius2 * radius2 +distance * distance) / (2 * distance);
        float c = sqrt(radius1 * radius1 - a * a);

		float R1ToR2[3];
		Vector3d_GapOfAB(R1ToR2, cen2, cen1);
		Vector3d_Identify(R1ToR2);
		float R1ToR2_a[3];
		Vector3d_MultiplyOfK(R1ToR2_a, R1ToR2, a);
		float middlePoint[3];
		Vector3d_SumOfAB(middlePoint, cen1, R1ToR2_a);

		float nextMiddle[3];
		Vector3d_CrossOfAB(nextMiddle, circlePlaneNormal, R1ToR2);
		Vector3d_Identify(nextMiddle);

		float nextMiddle_c[3];
		Vector3d_MultiplyOfK(nextMiddle_c, nextMiddle, c);
		float up[3];
		Vector3d_SumOfAB(up, middlePoint, nextMiddle_c);
		float down[3];
		Vector3d_GapOfAB(down, middlePoint, nextMiddle_c);

		float upPoint[3];
		Vector3d_Set(upPoint, up[0], up[1], up[2]);
		float downPoint[3];
		Vector3d_Set(downPoint, down[0], down[1], down[2]);

		pointsCount = 2;

		point1[0] = upPoint[0];
		point1[1] = upPoint[1];
		point1[2] = upPoint[2];
		point2[0] = downPoint[0];
		point2[1] = downPoint[1];
		point2[2] = downPoint[2];
    }
    else if (distance == radius1 + radius2)
    {
		float R1ToR2[3];
		Vector3d_GapOfAB(R1ToR2, cen2, cen1);
		Vector3d_Identify(R1ToR2);

		float R1ToR2_radius1[3];
		Vector3d_MultiplyOfK(R1ToR2_radius1, R1ToR2, radius1);
		float middle[3];
		Vector3d_SumOfAB(middle, cen1, R1ToR2_radius1);

		pointsCount = 1;
		point1[0] = middle[0];
		point1[1] = middle[1];
		point1[2] = middle[2];
    }
    else
    {
		pointsCount = 0;
        return;
    }
}

float Robot_CalculateQ2(float node2[10], float node3[10], int pointsCount, float point1[3], float point2[3], float normal[3])
{
    if (pointsCount == 1)
    {
		float node3_Point[3];
		RobotNode_get_Point(node3, node3_Point);

		float node2_Point[3];
		RobotNode_get_Point(node2, node2_Point);

		float V2To3[3];
		Vector3d_GapOfAB(V2To3, node3_Point, node2_Point);
		float TestV1[3];
		Vector3d_GapOfAB(TestV1, point1, node2_Point);

	    return Robot_CalculateAngle(V2To3, TestV1);
    }
    else
    {
		float node3_Point[3];
		RobotNode_get_Point(node3, node3_Point);

		float node2_Point[3];
		RobotNode_get_Point(node2, node2_Point);

		float V2To3[3];
		Vector3d_GapOfAB(V2To3, node3_Point, node2_Point);

		float TestV1[3];
		Vector3d_GapOfAB(TestV1, point1, node2_Point);
		float TestV2[3];
		Vector3d_GapOfAB(TestV2, point2, node2_Point);
	    float angle1 = Robot_CalculateAngle(V2To3, TestV1);
	    float angle2 = Robot_CalculateAngle(V2To3, TestV2);
	    if (abs(angle1) < abs(angle2))
	    {
			float corssVector[3];
			Vector3d_CrossOfAB(corssVector, V2To3, TestV1);
			Vector3d_Identify(corssVector);
			Vector3d_Identify(normal);

			float value = Vector3d_MultiplyOfAB(corssVector, normal);
		    if (abs(value - 1) < 0.0001)
		    {
			    return angle1;
		    }
		    else
		    {
			    return -angle1;
		    }
	    }
	    else
	    {
			float corssVector[3];
			Vector3d_CrossOfAB(corssVector, V2To3, TestV2);
			Vector3d_Identify(corssVector);
			Vector3d_Identify(normal);

			float value = Vector3d_MultiplyOfAB(corssVector, normal);
		    if (abs(value - 1) < 0.0001)
		    {
			    return angle2;
		    }
		    else
		    {
			    return -angle2;
		    }
	    }
    }
}

float CalculateQ3(float node3[10], float node5[10], float newPointYZ[3], float normal[3])
{
	float node5_Point[3];
	RobotNode_get_Point(node5, node5_Point);

	float node3_Point[3];
	RobotNode_get_Point(node3, node3_Point);

	float V3To5[3];
	Vector3d_GapOfAB(V3To5, node5_Point, node3_Point);
	Vector3d_Identify(V3To5);

	float TestV[3];
	Vector3d_GapOfAB(TestV, newPointYZ, node3_Point);
	Vector3d_Identify(TestV);

    float angle = Robot_CalculateAngle(V3To5, TestV);
	float corssVector[3];
	Vector3d_CrossOfAB(corssVector, V3To5, TestV);
	Vector3d_Identify(corssVector);
	Vector3d_Identify(normal);

    float value = Vector3d_MultiplyOfAB(corssVector, normal);
    if (abs(value - 1) < 0.0001)
    {
	    return angle;
    }
    else
    {
	    return -angle;
    }
}

bool Robot_Transform(float RobotLinks[63], float newT6Matrix[4][4])
{
	float node1[10];
	RobotLinks_GetNode(RobotLinks, 1, node1);
	float node2[10];
	RobotLinks_GetNode(RobotLinks, 2, node2);
	float node3[10];
	RobotLinks_GetNode(RobotLinks, 3, node3);
	float node4[10];
	RobotLinks_GetNode(RobotLinks, 4, node4);
	float node5[10];
	RobotLinks_GetNode(RobotLinks, 5, node5);
	float node6[10];
	RobotLinks_GetNode(RobotLinks, 6, node6);

        float node6_Point[3];

    // 1 calculate position of T5
	float newOrigin[3];
	Matrix4X4_GetOrigin(newT6Matrix, newOrigin);
	float newZAxis[3];
	Matrix4X4_GetZAxis(newT6Matrix, newZAxis);

    float length5 = 0;
	RobotLinks_GetNodeLength(RobotLinks, 5, length5);

    float point5Target[3];
	float newZAxis_length5[3];
	Vector3d_MultiplyOfK(newZAxis_length5, newZAxis, length5);
	Vector3d_GapOfAB(point5Target, newOrigin, newZAxis_length5);

    // 2 calculate theta1(Q1), T2 - 6 Rot(Q1)------------------------------------------
	float V5Target[3];
	float node1_Point[3];
	RobotNode_get_Point(node1, node1_Point);
	Vector3d_GapOfAB(V5Target, point5Target, node1_Point);
	V5Target[2] = 0;
	Vector3d_Identify(V5Target);

	float node5_Point[3];
	RobotNode_get_Point(node5, node5_Point);
	RobotNode_get_Point(node1, node1_Point);
	float V5[3];
	RobotNode_get_Point(node1, node1_Point);
	Vector3d_GapOfAB(V5, node5_Point, node1_Point);
	V5[2] = 0;
	Vector3d_Identify(V5);

	float node1_RotVector[3];
	RobotNode_get_RotVector(node1, node1_RotVector);
    float Q1 = Robot_CalculateAngle(V5, V5Target, node1_RotVector);
	RobotNode_Rotate2(node1, node1_RotVector, Q1);
	RobotNode_Rotate(node2, node1_Point, node1_RotVector, Q1);
	RobotNode_Rotate(node3, node1_Point, node1_RotVector, Q1);
	RobotNode_Rotate(node4, node1_Point, node1_RotVector, Q1);
	RobotNode_Rotate(node5, node1_Point, node1_RotVector, Q1);

RobotNode_get_Point(node6, node6_Point);
    
    RobotNode_Rotate(node6, node1_Point, node1_RotVector, Q1);
    
    

	float newPointYZ[3];
	Vector3d_Copy(point5Target, newPointYZ);

    // 4 calculate theta2(Q2), T3 - 6 Rot(Q2)
	float length2 = 0;
	RobotLinks_GetNodeLength(RobotLinks, 2, length2);

	float node3_Point[3];
	RobotNode_get_Point(node3, node3_Point);
	RobotNode_get_Point(node5, node5_Point);
	float node5_Point_node3_Point[3];
	Vector3d_GapOfAB(node5_Point_node3_Point, node5_Point, node3_Point);
	float length3 = Vector3d_Length(node5_Point_node3_Point);

	float node2_RotVector[3];
	RobotNode_get_RotVector(node2, node2_RotVector);
	RobotNode_get_RotVector(node1, node1_RotVector);
	float node2_Point[3];
	RobotNode_get_Point(node2, node2_Point);
	float point1[3];
	float point2[3];
	int pointsCount = 0;
	Robot_CalculateCirsPoints(node2_RotVector, node2_Point, length2, newPointYZ, length3, pointsCount, point1, point2);
    if (pointsCount == 0)
    {
		RobotNode_get_Point(node1, node1_Point);
		RobotNode_get_RotVector(node1, node1_RotVector);
		RobotNode_Rotate2(node1, node1_RotVector, -Q1);
		RobotNode_Rotate(node2, node1_Point, node1_RotVector, -Q1);
		RobotNode_Rotate(node3, node1_Point, node1_RotVector, -Q1);
		RobotNode_Rotate(node4, node1_Point, node1_RotVector, -Q1);
		RobotNode_Rotate(node5, node1_Point, node1_RotVector, -Q1);
		RobotNode_Rotate(node6, node1_Point, node1_RotVector, -Q1);

	    return false;
    }

	float Q2 = Robot_CalculateQ2(node2, node3, pointsCount, point1, point2, node2_RotVector);
	RobotNode_get_Point(node2, node2_Point);
	RobotNode_get_RotVector(node2, node2_RotVector);
	RobotNode_Rotate2(node2, node2_RotVector, Q2);
	RobotNode_Rotate(node3, node2_Point, node2_RotVector, Q2);
    RobotNode_Rotate(node4, node2_Point, node2_RotVector, Q2);
	RobotNode_Rotate(node5, node2_Point, node2_RotVector, Q2);
	RobotNode_Rotate(node6, node2_Point, node2_RotVector, Q2);

    // 5 calculate theta3(Q3), T4 - 6 Rot(Q3)
	float node3_RotVector[3];
	RobotNode_get_RotVector(node3, node3_RotVector);
	RobotNode_get_Point(node3, node3_Point);
	float Q3 = CalculateQ3(node3, node5, newPointYZ, node3_RotVector);
	RobotNode_Rotate2(node3, node3_RotVector, Q3);
	RobotNode_Rotate(node4, node3_Point, node3_RotVector, Q3);
	RobotNode_Rotate(node5, node3_Point, node3_RotVector, Q3);
	RobotNode_Rotate(node6, node3_Point, node3_RotVector, Q3);

    // 8 calculate Q5, T6 Rot(Q5)
	
	RobotNode_get_Point(node6, node6_Point);
	float node4_RotVector[3];
	RobotNode_get_RotVector(node4, node4_RotVector);
	float V5To6[3];
	RobotNode_get_Point(node5, node5_Point);
	Vector3d_GapOfAB(V5To6, node6_Point, node5_Point);
	float Q5_5To4 = Robot_CalculateAngle(V5To6, node4_RotVector);
	float Q5_NewTo4 = Robot_CalculateAngle(newZAxis, node4_RotVector);
    float Q5 = Q5_NewTo4 - Q5_5To4;
	float node5_RotVector[3];
	RobotNode_get_RotVector(node5, node5_RotVector);
	RobotNode_Rotate2(node5, node5_RotVector, Q5);
	RobotNode_Rotate(node6, node5_Point, node5_RotVector, Q5);

    // 7 calculate Q4, T5 - 6 Rot(Q4)+
	float dExtendLength = length5 * cos(Q5_NewTo4);
	float node4_RotVector_ExtendLength[3];
	Vector3d_MultiplyOfK(node4_RotVector_ExtendLength, node4_RotVector, dExtendLength);
	RobotNode_get_Point(node5, node5_Point);
	float nextCeneter[3];
	Vector3d_SumOfAB(nextCeneter, node5_Point, node4_RotVector_ExtendLength);
	float from5[3];
	RobotNode_get_Point(node6, node6_Point);
	Vector3d_GapOfAB(from5, node6_Point, nextCeneter);
	Vector3d_Identify(from5);
    float to5[3];
	Vector3d_GapOfAB(to5, newOrigin, nextCeneter);
	Vector3d_Identify(to5);

	float node4_Point[3];
	RobotNode_get_Point(node4, node4_Point);
	RobotNode_get_RotVector(node4, node4_RotVector);
	float Q4 = Robot_CalculateAngle(from5, to5, node4_RotVector);
	RobotNode_Rotate2(node4, node4_RotVector, Q4);
	RobotNode_Rotate(node5, node4_Point, node4_RotVector, Q4);
	RobotNode_Rotate(node6, node4_Point, node4_RotVector, Q4);

    // 9 calculate Q6, T6 Rot(Q6)
	float Node6XAxis[3];
	RobotLinks_get_Node6XAxis(RobotLinks, Node6XAxis);
	float newAxis[3];
	Matrix4X4_GetXAxis(newT6Matrix, newAxis);
	float node6_RotVector[3];
	RobotNode_get_RotVector(node6, node6_RotVector);
	float Q6 = Robot_CalculateAngle(Node6XAxis, newAxis, node6_RotVector);
	RobotNode_Rotate2(node6, node6_RotVector, Q6);
	RobotLinks_set_Node6XAxis(RobotLinks, newAxis);

	RobotLinks_SetNode(RobotLinks, 1, node1);
	RobotLinks_SetNode(RobotLinks, 2, node2);
	RobotLinks_SetNode(RobotLinks, 3, node3);
	RobotLinks_SetNode(RobotLinks, 4, node4);
	RobotLinks_SetNode(RobotLinks, 5, node5);
	RobotLinks_SetNode(RobotLinks, 6, node6);

    return true;
}

void Robot_Execute(float RobotLinks[63],
	float newT6Matrix[4][4])
{
	float oldMat1[4][4];
	Robot_CalculateMatrix(RobotLinks, 1, oldMat1);
	float oldMat2[4][4];
	Robot_CalculateMatrix(RobotLinks, 2, oldMat2);
	float oldMat3[4][4];
	Robot_CalculateMatrix(RobotLinks, 3, oldMat3);
	float oldMat4[4][4];
	Robot_CalculateMatrix(RobotLinks, 4, oldMat4);
	float oldMat5[4][4];
	Robot_CalculateMatrix(RobotLinks, 5, oldMat5);
	float oldMat6[4][4];
	Robot_CalculateMatrix(RobotLinks, 6, oldMat6);

        Robot_Transform(RobotLinks, newT6Matrix);
}

void Robot_Execute(float RobotLinks[63],
	float origin[3],
	float ZAxis[3],
	float angles[6])
{
	float XAxis[3];
	Vector3d_kXAxis(XAxis);
	float temp[3];
	Vector3d_CrossOfAB(temp, XAxis, ZAxis);
	float temp_Length = Vector3d_Length(temp);
	if (abs(temp_Length) < 0.0001)
	{
		float YAxis[3];
		Vector3d_kYAxis(YAxis);
		Vector3d_CrossOfAB(XAxis, ZAxis, YAxis);
	}
	else
	{
		Vector3d_Copy(temp, XAxis);
	}
	float YAxis[3];
	Vector3d_CrossOfAB(YAxis, ZAxis, XAxis);

	float newT6Matrix[4][4];
	Matrix4X4_SetToIdentity(newT6Matrix);
	Matrix4X4_SetCoordSystem(newT6Matrix, origin, XAxis, YAxis, ZAxis);

	Robot_Execute(RobotLinks, newT6Matrix);
	for (int i = 0; i < 6; i++)
	{
		float node[10];
		RobotLinks_GetNode(RobotLinks, i + 1, node);
		angles[i] = RobotNode_get_MotorAngle(node);
	}
}

void Robot_ControlRotator(float RobotLinks[63], int nodeIndex, float angle)
{
    float node1[10];
	RobotLinks_GetNode(RobotLinks, 1, node1);
	float node2[10];
	RobotLinks_GetNode(RobotLinks, 2, node2);
	float node3[10];
	RobotLinks_GetNode(RobotLinks, 3, node3);
	float node4[10];
	RobotLinks_GetNode(RobotLinks, 4, node4);
	float node5[10];
	RobotLinks_GetNode(RobotLinks, 5, node5);
	float node6[10];
	RobotLinks_GetNode(RobotLinks, 6, node6);

    switch (nodeIndex)
    {
        case 6:
            {
				float origin[3];
				RobotNode_get_Point(node6, origin);
				float rotator[3];
				RobotNode_get_RotVector(node6, rotator);
				RobotNode_Rotate2(node6, rotator, angle);
            }
            break;

        case 5:
            {
				float origin[3];
				RobotNode_get_Point(node5, origin);
				float rotator[3];
				RobotNode_get_RotVector(node5, rotator);
				RobotNode_Rotate2(node5, rotator, angle);
				RobotNode_Rotate(node6, origin, rotator, angle);
            }
            break;

        case 4:
            {
				float origin[3];
				RobotNode_get_Point(node4, origin);
				float rotator[3];
				RobotNode_get_RotVector(node4, rotator);
				RobotNode_Rotate2(node4, rotator, angle);
				RobotNode_Rotate(node5, origin, rotator, angle);
				RobotNode_Rotate(node6, origin, rotator, angle);
            }
            break;

        case 3:
            {
				float origin[3];
				RobotNode_get_Point(node3, origin);
				float rotator[3];
				RobotNode_get_RotVector(node3, rotator);
				RobotNode_Rotate2(node3, rotator, angle);
				RobotNode_Rotate(node4, origin, rotator, angle);
				RobotNode_Rotate(node5, origin, rotator, angle);
				RobotNode_Rotate(node6, origin, rotator, angle);
            }
            break;

        case 2:
            {
				float origin[3];
				RobotNode_get_Point(node2, origin);
				float rotator[3];
				RobotNode_get_RotVector(node2, rotator);
				RobotNode_Rotate2(node2, rotator, angle);
				RobotNode_Rotate(node3, origin, rotator, angle);
				RobotNode_Rotate(node4, origin, rotator, angle);
				RobotNode_Rotate(node5, origin, rotator, angle);
				RobotNode_Rotate(node6, origin, rotator, angle);
            }
            break;

        case 1:
            {
				float origin[3];
				RobotNode_get_Point(node1, origin);
				float rotator[3];
				RobotNode_get_RotVector(node1, rotator);
				RobotNode_Rotate2(node1, rotator, angle);
				RobotNode_Rotate(node2, origin, rotator, angle);
				RobotNode_Rotate(node3, origin, rotator, angle);
				RobotNode_Rotate(node4, origin, rotator, angle);
				RobotNode_Rotate(node5, origin, rotator, angle);
				RobotNode_Rotate(node6, origin, rotator, angle);
            }
            break;
    }
}
 
double _CalUnit = 100;
 void Robot_Create(float RobotLinks[63], float angles[6])
 {
    float point0[3];
	float point1[3];
	float point2[3];
	float point3[3];
	float point4[3];
	float point5[3];
	float point6[3];
	float rotAxises0[3];
	float rotAxises1[3];
	float rotAxises2[3];
	float rotAxises3[3];
	float rotAxises4[3];
	float rotAxises5[3];
	float rotAxises6[3];
	float initAngles[7];

	point0[0] = 0;
	point0[1] = 0;
	point0[2] = -146.5f;

	point1[0] = 0;
	point1[1] = 0;
	point1[2] = 10;
	
	point2[0] = 0;
	point2[1] = 0;
	point2[2] = 100;
	
	point3[0] = 0;
	point3[1] = 0;
	point3[2] = 220;
	
	point4[0] = 0;
	point4[1] = 99.5;
	point4[2] = 335;

	point5[0] = 0;
	point5[1] = 222;
	point5[2] = 335;
	
	point6[0] = 0;
	point6[1] = 324;
	point6[2] = 335;

	point0[0] *= _CalUnit;
	point0[1] *= _CalUnit;
	point0[2] *= _CalUnit;
	point1[0] *= _CalUnit;
	point1[1] *= _CalUnit;
	point1[2] *= _CalUnit;
	point2[0] *= _CalUnit;
	point2[1] *= _CalUnit;
	point2[2] *= _CalUnit;
	point3[0] *= _CalUnit;
	point3[1] *= _CalUnit;
	point3[2] *= _CalUnit;
	point4[0] *= _CalUnit;
	point4[1] *= _CalUnit;
	point4[2] *= _CalUnit;
	point5[0] *= _CalUnit;
	point5[1] *= _CalUnit;
	point5[2] *= _CalUnit;
	point6[0] *= _CalUnit;
	point6[1] *= _CalUnit;
	point6[2] *= _CalUnit;

	// z
	rotAxises0[0] = 0;
	rotAxises0[1] = 0;
	rotAxises0[2] = -1;
	// x
	rotAxises1[0] = 1;
	rotAxises1[1] = 0;
	rotAxises1[2] = 0;
	// x
	rotAxises2[0] = 1;
	rotAxises2[1] = 0;
	rotAxises2[2] = 0;
	// y
	rotAxises3[0] = 0;
	rotAxises3[1] = 1;
	rotAxises3[2] = 0;
	// x
	rotAxises4[0] = 1;
	rotAxises4[1] = 0;
	rotAxises4[2] = 0;
	// y
	rotAxises5[0] = 0;
	rotAxises5[1] = 1;
	rotAxises5[2] = 0;
	// x
	rotAxises6[0] = 1;
	rotAxises6[1] = 0;
	rotAxises6[2] = 0;

	initAngles[0] = 0;
	initAngles[1] = 0;
	initAngles[2] = 0;
	initAngles[3] = 0;
	initAngles[4] = 3.1415926f;
	initAngles[5] = 0;
	initAngles[6] = 0;

    angles[0] = initAngles[1];
    angles[1] = initAngles[2];
    angles[2] = initAngles[3];
    angles[3] = initAngles[4];
    angles[4] = initAngles[5];
    angles[5] = initAngles[6];

	float v1[3];
	Vector3d_GapOfAB(v1, point1, point0);
	Vector3d_Identify(v1);
	float v2[3];
	Vector3d_GapOfAB(v2, point2, point1);
	Vector3d_Identify(v2);
    float v3[3];
	Vector3d_GapOfAB(v3, point3, point2);
	Vector3d_Identify(v3);
	float v4[3];
	Vector3d_GapOfAB(v4, point4, point3);
	Vector3d_Identify(v4);
	float v5[3];
	Vector3d_GapOfAB(v5, point5, point4);
	Vector3d_Identify(v5);
	float v6[3];
	Vector3d_GapOfAB(v6, point6, point5);
	Vector3d_Identify(v6);

	float vectors[18];
	vectors[0] = rotAxises0[0];
	vectors[1] = rotAxises0[1];
	vectors[2] = rotAxises0[2];
	vectors[3] = rotAxises1[0];
	vectors[4] = rotAxises1[1];
	vectors[5] = rotAxises1[2];
	vectors[6] = rotAxises2[0];
	vectors[7] = rotAxises2[1];
	vectors[8] = rotAxises2[2];
	vectors[9] = rotAxises3[0];
	vectors[10] = rotAxises3[1];
	vectors[11] = rotAxises3[2];
	vectors[12] = rotAxises4[0];
	vectors[13] = rotAxises4[1];
	vectors[14] = rotAxises4[2];
	vectors[15] = rotAxises5[0];
	vectors[16] = rotAxises5[1];
	vectors[17] = rotAxises5[2];

	float initPoints[18];
	initPoints[0] = point1[0];
	initPoints[1] = point1[1];
	initPoints[2] = point1[2];
	initPoints[3] = point2[0];
	initPoints[4] = point2[1];
	initPoints[5] = point2[2];
	initPoints[6] = point3[0];
	initPoints[7] = point3[1];
	initPoints[8] = point3[2];
	initPoints[9] = point4[0];
	initPoints[10] = point4[1];
	initPoints[11] = point4[2];
	initPoints[12] = point5[0];
	initPoints[13] = point5[1];
	initPoints[14] = point5[2];
	initPoints[15] = point6[0];
	initPoints[16] = point6[1];
	initPoints[17] = point6[2];

    Robot_Init(RobotLinks, vectors, rotAxises6, initPoints, initAngles);
 }

 FILE* Data = NULL;
 void Robot_Execute(float x, float y, float z, float i, float j, float k)
 {
      float origin[3];
      origin[0] = x * _CalUnit;
      origin[1] = y * _CalUnit;
      origin[2] = z * _CalUnit;
      float ZAxis[3];
      ZAxis[0] = i;
      ZAxis[1] = j;
      ZAxis[2] = k;
      
      float angles[6];
      Robot_Execute(_RobotLinks, origin, ZAxis, angles);

	  fprintf(Data, "MotionAngle(%lf,%lf,%lf,%lf,%lf,%lf);\n", (angles[0] - _backAngles[0]) * 180 / 3.14159265358979323846,
      (angles[1] - _backAngles[1]) * 180 / 3.14159265358979323846,
      (angles[2] - _backAngles[2]) * 180 / 3.14159265358979323846,
      (angles[3] - _backAngles[3]) * 180 / 3.14159265358979323846,
      (angles[4] - _backAngles[4]) * 180 / 3.14159265358979323846,
      (angles[5] - _backAngles[5]) * 180 / 3.14159265358979323846);

	  _backAngles[0] = angles[0];
      _backAngles[1] = angles[1];
      _backAngles[2] = angles[2];
      _backAngles[3] = angles[3];
      _backAngles[4] = angles[4];
      _backAngles[5] = angles[5];
       
      /*int A_Count = (int)((angles[0] - _backAngles[0]) / _A_E_Step_Angle);
      int B_Count = (int)((angles[1] - _backAngles[1]) / _A_E_Step_Angle);
      int C_Count = (int)((angles[2] - _backAngles[2]) / _A_E_Step_Angle);
      int D_Count = (int)((angles[3] - _backAngles[3]) / _A_E_Step_Angle);
      int E_Count = (int)((angles[4] - _backAngles[4]) / _A_E_Step_Angle);
      int F_Count = (int)((angles[5] - _backAngles[5]) / _F_Step_Angle);
      
      _backAngles[0] = _backAngles[0] + A_Count * _A_E_Step_Angle;
      _backAngles[1] = _backAngles[1] + B_Count * _A_E_Step_Angle;
      _backAngles[2] = _backAngles[2] + C_Count * _A_E_Step_Angle;
      _backAngles[3] = _backAngles[3] + D_Count * _A_E_Step_Angle;
      _backAngles[4] = _backAngles[4] + E_Count * _A_E_Step_Angle;
      _backAngles[5] = _backAngles[5] + F_Count * _F_Step_Angle;

	  fprintf(Data, "MotionAngle(%lf,%lf,%lf,%lf,%lf,%lf);\n", A_Count * _A_E_Step_Angle * 180 / 3.14159265358979323846,
      B_Count * _A_E_Step_Angle * 180 / 3.14159265358979323846,
      C_Count * _A_E_Step_Angle * 180 / 3.14159265358979323846,
      D_Count * _A_E_Step_Angle * 180 / 3.14159265358979323846,
      E_Count * _A_E_Step_Angle * 180 / 3.14159265358979323846,
      F_Count * _F_Step_Angle * 180 / 3.14159265358979323846);*/
      
      /*MotionAngle();*/
 }

 //char program[100][50];
 //void Handle_Code(char code[100], int length)
 //{
	//// G1 X Y Z I J K
	//// G2 X Y Z
	//// G3 X Y Z

	//double X;
	//double Y;
	//double Z;
	//double I;
	//double J;
	//double K;
	//char strMode[20] = "";
	//char strX[20] = "";
	//char strY[20] = "";
	//char strZ[20] = "";
	//char strI[20] = "";
	//char strJ[20] = "";
	//char strK[20] = "";
	//int startIndex = 0;
	//for (int i = 0; i < length; i ++)
	//{
	//	if (code[i] == '\n')
	//		break;

	//	if (code[i] == ' ')
	//	{
	//		if (strMode[0] = '\n')
	//		{
	//			int k = 0;
	//			for (int j = 0; j < i; j ++)
	//			{
	//				strMode[k] = code[j];
	//				k ++;
	//			}
	//			strMode[k] = '\n';
	//			startIndex = i;
	//		}
	//		else 
	//	}
	//}

 //}

void Handle_Code(char codeX[100], char codeY[100], char codeZ[100], char codeI[100], char codeJ[100], char codeK[100])
{
	double x = atof(codeX);
	double y = atof(codeY);
	double z = atof(codeZ);
	double i = atof(codeI);
	double j = atof(codeJ);
	double k = atof(codeK);

	Robot_Execute(x, y, z, i, j, k);
}
 
 void Running()
 {
	Robot_Create(_RobotLinks, _backAngles);
	Robot_Execute(40,211.6748,158.03,0,0,-1);
	Robot_Execute(40,211.6748,154.03,0,0,-1);
	Robot_Execute(40,211.6748,150,0,0,-1);
	Robot_Execute(42.437,214.0861,150,0,0,-1);
	Robot_Execute(44.729,216.6358,150,0,0,-1);
	Robot_Execute(46.868,219.315,150,0,0,-1);
	Robot_Execute(48.8467,222.1147,150,0,0,-1);
	Robot_Execute(50.6584,225.0253,150,0,0,-1);
	Robot_Execute(52.2969,228.0367,150,0,0,-1);
	Robot_Execute(53.7565,231.1388,150,0,0,-1);
	Robot_Execute(55.0324,234.321,150,0,0,-1);
	Robot_Execute(56.12,237.5722,150,0,0,-1);
	Robot_Execute(57.0158,240.8815,150,0,0,-1);
	Robot_Execute(57.7166,244.2374,150,0,0,-1);
	Robot_Execute(58.2201,247.6286,150,0,0,-1);
	Robot_Execute(58.5244,251.0434,150,0,0,-1);
	Robot_Execute(58.6287,254.4702,150,0,0,-1);
	Robot_Execute(58.5324,257.8972,150,0,0,-1);
	Robot_Execute(58.2361,261.3127,150,0,0,-1);
	Robot_Execute(57.7406,264.7051,150,0,0,-1);
	Robot_Execute(57.0476,268.0627,150,0,0,-1);
	Robot_Execute(56.1596,271.374,150,0,0,-1);
	Robot_Execute(55.0796,274.6278,150,0,0,-1);
	Robot_Execute(53.8112,277.8129,150,0,0,-1);
	Robot_Execute(52.3588,280.9184,150,0,0,-1);
	Robot_Execute(50.7274,283.9337,150,0,0,-1);
	Robot_Execute(48.9225,286.8485,150,0,0,-1);
	Robot_Execute(46.9503,289.6528,150,0,0,-1);
	Robot_Execute(44.8176,292.3371,150,0,0,-1);
	Robot_Execute(42.5317,294.8921,150,0,0,-1);
	Robot_Execute(40.1003,297.3091,150,0,0,-1);
	Robot_Execute(37.5318,299.5799,150,0,0,-1);
	Robot_Execute(34.8349,301.6966,150,0,0,-1);
	Robot_Execute(32.019,303.6521,150,0,0,-1);
	Robot_Execute(29.0935,305.4397,150,0,0,-1);
	Robot_Execute(26.0686,307.0532,150,0,0,-1);
	Robot_Execute(22.9545,308.4871,150,0,0,-1);
	Robot_Execute(19.762,309.7366,150,0,0,-1);
	Robot_Execute(16.5018,310.7973,150,0,0,-1);
	Robot_Execute(13.1853,311.6657,150,0,0,-1);
	Robot_Execute(9.8236,312.3387,150,0,0,-1);
	Robot_Execute(6.4284,312.8141,150,0,0,-1);
	Robot_Execute(3.0112,313.0902,150,0,0,-1);
	Robot_Execute(-0.4163,313.1661,150,0,0,-1);
	Robot_Execute(-3.8424,313.0415,150,0,0,-1);
	Robot_Execute(-7.2554,312.7169,150,0,0,-1);
	Robot_Execute(-10.6435,312.1934,150,0,0,-1);
	Robot_Execute(-13.9953,311.4727,150,0,0,-1);
	Robot_Execute(-17.2992,310.5573,150,0,0,-1);
	Robot_Execute(-20.5439,309.4504,150,0,0,-1);
	Robot_Execute(-23.7184,308.1557,150,0,0,-1);
	Robot_Execute(-26.8118,306.6777,150,0,0,-1);
	Robot_Execute(-29.8135,305.0214,150,0,0,-1);
	Robot_Execute(-32.7133,303.1924,150,0,0,-1);
	Robot_Execute(-35.5012,301.1971,150,0,0,-1);
	Robot_Execute(-38.1677,299.0423,150,0,0,-1);
	Robot_Execute(-40.7037,296.7353,150,0,0,-1);
	Robot_Execute(-43.1005,294.284,150,0,0,-1);
	Robot_Execute(-45.3499,291.6968,150,0,0,-1);
	Robot_Execute(-47.4443,288.9825,150,0,0,-1);
	Robot_Execute(-49.3764,286.1505,150,0,0,-1);
	Robot_Execute(-51.1397,283.2103,150,0,0,-1);
	Robot_Execute(-52.7282,280.1722,150,0,0,-1);
	Robot_Execute(-54.1363,277.0463,150,0,0,-1);
	Robot_Execute(-55.3593,273.8436,150,0,0,-1);
	Robot_Execute(-56.3931,270.5748,150,0,0,-1);
	Robot_Execute(-57.2339,267.2511,150,0,0,-1);
	Robot_Execute(-57.8791,263.884,150,0,0,-1);
	Robot_Execute(-58.3264,260.485,150,0,0,-1);
	Robot_Execute(-58.5742,257.0656,150,0,0,-1);
	Robot_Execute(-58.6218,253.6376,150,0,0,-1);
	Robot_Execute(-58.4689,250.2126,150,0,0,-1);
	Robot_Execute(-58.116,246.8025,150,0,0,-1);
	Robot_Execute(-57.5645,243.4188,150,0,0,-1);
	Robot_Execute(-56.8161,240.0731,150,0,0,-1);
	Robot_Execute(-55.8734,236.7769,150,0,0,-1);
	Robot_Execute(-54.7397,233.5414,150,0,0,-1);
	Robot_Execute(-53.4188,230.3778,150,0,0,-1);
	Robot_Execute(-51.9152,227.2967,150,0,0,-1);
	Robot_Execute(-50.2341,224.3088,150,0,0,-1);
	Robot_Execute(-48.3813,221.4243,150,0,0,-1);
	Robot_Execute(-46.363,218.653,150,0,0,-1);
	Robot_Execute(-44.1862,216.0044,150,0,0,-1);
	Robot_Execute(-44.1862,216.0044,154.03,0,0,-1);
	Robot_Execute(-44.1862,216.0044,158.03,0,0,-1);
 }

int iSwitch = 1;
void loop()
{
  //delay(3000);
  
  switch (iSwitch)
  {
    case 0:
    {
      //ManualControl(1, -10);
      iSwitch = 2;
    }
    break;
    
   case 1:
   {
     //ManualControl(3, -5);
     Running();
     iSwitch = 2;
   }
   break;
    
    case 2:
    {
      //delay(1000);
    }
    break;
  }
  
  //StepMotion(40, -30, 30, 180, 90, 0);
}



int _tmain(int argc, _TCHAR* argv[])
{
	Running();
	/*Data=fopen("C:\\work\\Data.txt","w");
	loop();
	fclose(Data);*/

	return 0;
}

