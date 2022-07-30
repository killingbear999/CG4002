#ifndef _LAYER2_
#define _LAYER2_

#include "ap_axi_sdata.h"
#include "ap_int.h"
#include <inttypes.h>

#define N1 30
#define N2 15

#define DWIDTH 32
typedef ap_axiu<DWIDTH, 0, 0, 0> axis_t;

typedef float DataType;

const int DataTypeSize = sizeof(DataType) * 8;

typedef ap_uint<DataTypeSize> DataTypeInt;

typedef union converter {
  DataType d;
  uint32_t i;
} converter_t;

template <typename T> void kernel_layer2(T a[N1], T c[N2]);

#endif
