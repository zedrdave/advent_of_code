#include "stdio.h"
#include "stdlib.h"

#define MEM_SIZE 10000
int data[MEM_SIZE+1]; // Oink oink

#define NUM_OPS 100
int (*ops[NUM_OPS])(int *);

int op_add(int *a) {
  // printf("Param 1: %d\n", ((a[0]/100)%10 ? a[1] : data[a[1]]));
  // printf("Param 2: %d\n", ((a[0]/100)%10 ? a[2] : data[a[2]]));
  // printf("res: %d\n", ((a[0]/100)%10 ? a[1] : data[a[1]]) + ((a[0]/1000)%10 ? a[2] : data[a[2]]));
  data[a[3]] = ((a[0]/100)%10 ? a[1] : data[a[1]]) + ((a[0]/1000)%10 ? a[2] : data[a[2]]);
  return 4;
}
int op_mult(int *a) {
  data[a[3]] = ((a[0]/100)%10 ? a[1] : data[a[1]]) * ((a[0]/1000)%10 ? a[2] : data[a[2]]);
  return 4;
}
int op_input(int *a) {
  data[a[1]] = 1; // hardcoded input
  return 2;
}
int op_output(int *a) {
  printf("%d", ((a[0]/100)%10 ? a[1] : data[a[1]]));
  return 2;
}
int op_end(int *a) { return 0; }
int op_err(int *a) { printf("Unknown opcode: %d\n", a[0]); exit(-1); }

int main()
{
  FILE * fp = fopen ("input.txt","r");

  for( int i = 0; i < NUM_OPS; i++, ops[i] = op_err);
  ops[1] = op_add;
  ops[2] = op_mult;
  ops[3] = op_input;
  ops[4] = op_output;
  ops[99] = op_end;

  // for(int init_vn = 0; init_vn < 100*100; init_vn++) {

    // Reinit data from file:
    // fseek(fp, 0, SEEK_SET);
  for(int i = 0; i < MEM_SIZE && fscanf(fp, "%d,", &data[i]) != EOF; i++ );
  data[MEM_SIZE] = 0; // Ensure termination

  // data[1] = init_vn / 100;
  // data[2] = init_vn % 100;

  // Execute ops until termination
  int *IP = data;
  for (int op_size = 0; (op_size = ops[IP[0] %100]( IP )); IP += op_size);

    // if (data[0] == TARGET) {
    //   printf("TARGET REACHED (%d) for init: %d\n", data[0], init_vn);
    //   return 0;
    // }
  // }
  printf("\n");
  // printf("pos 4: %d", data[4]);
  // return -2;
}
