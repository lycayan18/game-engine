#ifndef MATRIX_H
#define MATRIX_H

/*
 * Matrix 4x4 operations.
*/

void mat4FromPerspective(float *dest, float fovy, float aspect, float near, float far);
void mat4Multiply(float *dest, float *a, float *b);
void mat4FromIdentity(float *dest);
void mat4FromRotation(float *dest, float x, float y, float z);
void mat4RotationX(float *dest, float a);
void mat4RotationY(float *dest, float a);
void mat4RotationZ(float *dest, float a);
void mat4Shift(float *dest, float x, float y, float z);
void mat4Scale(float *dest, float x, float y, float z);

#endif // MATRIX_H
