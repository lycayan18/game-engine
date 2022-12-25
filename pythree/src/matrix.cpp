#include <math.h>
#include "matrix.h"

#ifndef M_PI
    #define M_PI 3.14159265358979323846
#endif

// Helper function
// So many arguments for convenient vector passing without memory allocations
float dot4(float a0, float a1, float a2, float a3,
           float b0, float b1, float b2, float b3)
{
    return a0 * b0 + a1 * b1 + a2 * b2 + a3 * b3;
}

void mat4Multiply(float *dest, float *a, float *b)
{
    // Create a new array of floats and save result into it
    // This can be useful to avoid problems when dest == a or dest == b
    float out[16];

    for(unsigned int i = 0; i < 16; i++)
    {
        unsigned int col = i % 4;
        unsigned int row = i / 4;

        out[i] = dot4(a[0 + row * 4], a[1 + row * 4], a[2 + row * 4], a[3 + row * 4],
                      b[col + 0 * 4], b[col + 1 * 4], b[col + 2 * 4], b[col + 3 * 4]);
    }

    for(unsigned int i = 0; i < 16; i++)
    {
        dest[i] = out[i];
    }
}

void mat4FromRotation(float *dest, float x, float y, float z)
{
    float rotationX[16];
    float rotationY[16];
    float rotationZ[16];

    mat4RotationX(rotationX, x);
    mat4RotationY(rotationY, y);
    mat4RotationZ(rotationZ, z);

    // dest = (rotationZ * rotationY) * rotationX
    mat4Multiply(dest, rotationZ, rotationY);
    mat4Multiply(dest, dest, rotationX);
}

void mat4RotationX(float *dest, float a)
{
    float s = sinf(a);
    float c = cosf(a);

    dest[0] = 1.0f;
    dest[1] = 0.0f;
    dest[2] = 0.0f;
    dest[3] = 0.0f;
    dest[4] = 0.0f;
    dest[5] = c;
    dest[6] = -s;
    dest[7] = 0.0f;
    dest[8] = 0.0f;
    dest[9] = s;
    dest[10] = c;
    dest[11] = 0.0f;
    dest[12] = 0.0f;
    dest[13] = 0.0f;
    dest[14] = 0.0f;
    dest[15] = 1.0f;
}

void mat4RotationY(float *dest, float a)
{
    float s = sinf(a);
    float c = cosf(a);

    dest[0] = c;
    dest[1] = 0.0f;
    dest[2] = s;
    dest[3] = 0.0f;
    dest[4] = 0.0f;
    dest[5] = 1.0f;
    dest[6] = 0.0f;
    dest[7] = 0.0f;
    dest[8] = -s;
    dest[9] = 0.0f;
    dest[10] = c;
    dest[11] = 0.0f;
    dest[12] = 0.0f;
    dest[13] = 0.0f;
    dest[14] = 0.0f;
    dest[15] = 1.0f;
}

void mat4RotationZ(float *dest, float a)
{
    float s = sinf(a);
    float c = cosf(a);

    dest[0] = c;
    dest[1] = -s;
    dest[2] = 0.0f;
    dest[3] = 0.0f;
    dest[4] = s;
    dest[5] = c;
    dest[6] = 0.0f;
    dest[7] = 0.0f;
    dest[8] = 0.0f;
    dest[9] = 0.0f;
    dest[10] = 1.0f;
    dest[12] = 0.0f;
    dest[13] = 0.0f;
    dest[14] = 0.0f;
    dest[15] = 1.0f;
}

void mat4Shift(float *dest, float x, float y, float z)
{
    dest[3] += x;
    dest[7] += y;
    dest[11] += z;
}

void mat4Scale(float *dest, float x, float y, float z)
{
    dest[0] *= x;
    dest[5] *= y;
    dest[10] *= z;
}

void mat4FromIdentity(float *dest)
{
    /*
    Every fifth element is set to 1, the rest are set to 0

    The indices:
    0   1   2   3
    4   5   6   7
    8   9   10  11
    12  13  14  15

    Identity matrix:
    1   0   0   0
    0   1   0   0
    0   0   1   0
    0   0   0   1
    */

    for(unsigned int i = 0; i < 16; i++)
    {
        if(i % 5 == 0)
        {
            dest[i] = 1.0f;
        }
        else
        {
            dest[i] = 0.0f;
        }
    }
}

void mat4FromPerspective(float *dest, float fovy, float aspect, float near, float far)
{
    const float f = 1.0 / tanf(fovy * 0.5f * M_PI / 180.0f);

    dest[0] = f / aspect;
    dest[1] = 0.0f;
    dest[2] = 0.0f;
    dest[3] = 0.0f;
    dest[4] = 0.0f;
    dest[5] = f;
    dest[6] = 0.0f;
    dest[7] = 0.0f;
    dest[8] = 0.0f;
    dest[9] = 0.0f;
    dest[11] = -1.0f;
    dest[12] = 0.0f;
    dest[13] = 0.0f;
    dest[15] = 0.0f;

    if (far != INFINITY)
    {
        const float nf = 1.0 / (near - far);

        dest[10] = (far + near) * nf;
        dest[14] = 2.0f * far * near * nf;
    }
    else
    {
        dest[10] = -1.0f;
        dest[14] = -2.0f * near;
    }
}
