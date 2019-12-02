#include "stdio.h"
#include "stdlib.h"


#define TARGET 19690720

#define MEM_SIZE 1000
int data[MEM_SIZE+1]; // Oink oink

#define NUM_OPS 100
typedef int OPCODE[4];
int (*ops[NUM_OPS])(OPCODE);

int op_add(OPCODE a) { data[a[3]] = data[a[1]] + data[a[2]]; return 1; }
int op_mult(OPCODE a) { data[a[3]] = data[a[1]] * data[a[2]]; return 1; }
int op_end(OPCODE a) { return 0; }
int op_err(OPCODE a) { printf("Unknown opcode: %d\n", a[0]); exit(-1); }

int main()
{
  FILE * fp = fopen ("input.txt","r");

  for( int i = 0; i < NUM_OPS; i++, ops[i] = op_err);
  ops[1] = op_add;
  ops[2] = op_mult;
  ops[99] = op_end;

  for(int init_vn = 0; init_vn < 100*100; init_vn++) {

    // Reinit data from file:
    fseek(fp, 0, SEEK_SET);
    for(int i = 0; i < MEM_SIZE && fscanf(fp, "%d,", &data[i]) != EOF; i++ );
    data[MEM_SIZE] = 0; // Ensure termination
    
    data[1] = init_vn / 100;
    data[2] = init_vn % 100;

    // Execute ops until termination
    for(OPCODE *IP = (OPCODE *) data; ops[*IP[0]] ( *IP ); IP++);

    if (data[0] == TARGET) {
      printf("TARGET REACHED (%d) for init: %d\n", data[0], init_vn);
      return 0;
    }
  }

  printf("No solution\n");
  return -2;
}
