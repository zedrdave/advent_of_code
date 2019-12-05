#include "stdio.h"
#include "stdlib.h"
#include "math.h"

#define MEM_SIZE 10000
int data[MEM_SIZE+1]; // Oink oink

#define NUM_OPS 100
void (*ops[NUM_OPS])(void);

// OOOOOOOiiink:
int IP = 0;
int input = -1;

int pow10(n) { return (int) pow(10, n) }
// #define POW10(n) (n==1 ? 100 : (n==2 ? 1000 : 10000))
#define PARAM(n) ((data[IP]/pow10(n))%10 ? data[IP+n] : data[data[IP+n]])
#define SET_PARAM(n, val) if ((data[IP]/pow10(n))%10) data[IP+n] = val; else data[data[IP+n]] = val;


void op_add(void) {
  SET_PARAM(3, PARAM(1) + PARAM(2));
  IP += 4;
}
void op_mult() {
  SET_PARAM(3, PARAM(1) * PARAM(2));
  IP += 4;
}
void op_input() {
  SET_PARAM(1, input);
  IP += 2;
}
void op_output() {
  printf("%d", PARAM(1));
  IP += 2;
}
void op_jump_if_true() {
  IP = PARAM(1) ? PARAM(2) : IP+3;
}
void op_jump_if_false() {
  IP = !PARAM(1) ? PARAM(2) : IP+3;
}
void op_less_than() {
  SET_PARAM(3, PARAM(1) < PARAM(2));
  IP += 4;
}
void op_equals() {
  SET_PARAM(3, PARAM(1) == PARAM(2));
  IP += 4;
}

void op_err() { printf("Unknown opcode: %d\n", data[IP]); exit(-1); }

int main(int argc, char *argv[])
{
  input = atoi(argv[1]);

  FILE * fp = fopen ("input.txt","r");

  for( int i = 0; i < NUM_OPS; ops[i++] = op_err);
  ops[1] = op_add;
  ops[2] = op_mult;
  ops[3] = op_input;
  ops[4] = op_output;
  ops[5] = op_jump_if_true;
  ops[6] = op_jump_if_false;
  ops[7] = op_less_than;
  ops[8] = op_equals;

  // Reinit data from file:
  // fseek(fp, 0, SEEK_SET);
  for(int i = 0; i < MEM_SIZE && fscanf(fp, "%d,", &data[i]) != EOF; i++ );
  data[MEM_SIZE] = 0; // Ensure termination

  // Execute ops until termination
  for (IP = 0; data[IP] != 99; ops[data[IP] %100]()) {
    printf("[%d] %d (%d): %d %d %d\n", IP, data[IP], data[IP] %100, data[IP+1], data[IP+2], data[IP+3]);
  }

  printf("\n");
}

//15163975
