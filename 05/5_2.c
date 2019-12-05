#include "stdio.h"
#include "stdlib.h"

#define MEM_SIZE 10000
int data[MEM_SIZE+1]; // Oink oink

#define NUM_OPS 100
int* (*ops[NUM_OPS])(int *);

int input = -1;

int *op_add(int *a) {
  data[a[3]] = ((a[0]/100)%10 ? a[1] : data[a[1]]) + ((a[0]/1000)%10 ? a[2] : data[a[2]]);
  return a+4;
}
int *op_mult(int *a) {
  data[a[3]] = ((a[0]/100)%10 ? a[1] : data[a[1]]) * ((a[0]/1000)%10 ? a[2] : data[a[2]]);
  return a+4;
}
int *op_input(int *a) {
  data[a[1]] = input;
  return a+2;
}
int *op_output(int *a) {
  printf("%d", ((a[0]/100)%10 ? a[1] : data[a[1]]));
  return a+2;
}
int *op_jump_if_true(int *a) {
  if (! ((a[0]/100)%10 ? a[1] : data[a[1]])) return a+3;
  int *new_IP = data;
  new_IP += (a[0]/1000)%10 ? a[2] : data[a[2]];
  return new_IP;
}
int *op_jump_if_false(int *a) {
  if ((a[0]/100)%10 ? a[1] : data[a[1]]) return a+3;
  int *new_IP = data;
  new_IP += (a[0]/1000)%10 ? a[2] : data[a[2]];
  return new_IP;
}
int *op_less_than(int *a) {
  data[a[3]] = (((a[0]/100)%10 ? a[1] : data[a[1]]) < ((a[0]/1000)%10 ? a[2] : data[a[2]]));
  return a+4;
}
int *op_equals(int *a) {
  data[a[3]] = (((a[0]/100)%10 ? a[1] : data[a[1]]) == ((a[0]/1000)%10 ? a[2] : data[a[2]]));
  return a+4;
}

int *op_end(int *a) { return (int *) -1; }
int *op_err(int *a) { printf("Unknown opcode: %d\n", a[0]); exit(-1); }

int main(int argc, char *argv[])
{
  input = atoi(argv[1]);

  FILE * fp = fopen ("input.txt","r");

  for( int i = 0; i < NUM_OPS; i++, ops[i] = op_err);
  ops[1] = op_add;
  ops[2] = op_mult;
  ops[3] = op_input;
  ops[4] = op_output;
  ops[5] = op_jump_if_true;
  ops[6] = op_jump_if_false;
  ops[7] = op_less_than;
  ops[8] = op_equals;
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
  for (int *new_IP = 0; IP[0] != 99; IP = ops[IP[0] %100]( IP )) {
    // printf("%d | new_IP: %p\n", IP[0], IP);
  }

    // if (data[0] == TARGET) {
    //   printf("TARGET REACHED (%d) for init: %d\n", data[0], init_vn);
    //   return 0;
    // }
  // }
  printf("\n");
  // printf("pos 4: %d", data[4]);
  // return -2;
}
