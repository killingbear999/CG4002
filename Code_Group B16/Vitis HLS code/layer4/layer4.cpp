#include "layer4.h"
#include "hls_stream.h"
#include "weight4.h"
#include "bias4.h"

template <typename T> void kernel_layer4(T a[N1], T out[N2]) {
loop1:
	for (int i = 0; i < N2; i++) {
	loop2:
		DataType sum = 0;
		//neuron
		for (int j = 0; j < N1; j++) {
			sum += a[j] * weight[j][i];
		}
		sum += bias[i];
		out[i] = sum;
	}
  return;
}

extern "C" {
void layer4_accel(hls::stream<axis_t> &in, hls::stream<axis_t> &out) {
#pragma HLS INTERFACE s_axilite port = return bundle = control
#pragma HLS INTERFACE axis port = in
#pragma HLS INTERFACE axis port = out

  DataType l_A[N1];
  DataType l_C[N2];

  int j_limit = 32 / DataTypeSize;
  int i_limit = N1 / j_limit;
  int o_limit = N2 / j_limit;
  converter_t converter;

load_A:
  for (int i = 0; i < i_limit; i++) {
    axis_t temp = in.read();
    for (int j = 0; j < j_limit; j++) {
      int high = j * DataTypeSize + DataTypeSize - 1;
      int low = j * DataTypeSize;
      int index = i + j;

      converter.i = temp.data.range(high, low);
      l_A[index] = converter.d;
    }
  }

  kernel_layer4<DataType>(l_A, l_C);

writeC:
  for (int i = 0; i < o_limit; i++) {
    axis_t temp;
    for (int j = 0; j < j_limit; j++) {
      int high = j * DataTypeSize + DataTypeSize - 1;
      int low = j * DataTypeSize;
      converter.d = l_C[i + j];
      temp.data.range(high, low) = converter.i;
    }
    ap_uint<1> last = 0;
    if (i == o_limit - 1) {
      last = 1;
    }
    temp.last = last;
    temp.keep = -1; // enabling all bytes
    out.write(temp);
  }
}
}
