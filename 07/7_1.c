#include "stdio.h"
#include "stdlib.h"
#include "math.h"

#define MEM_SIZE 10000
int data[MEM_SIZE+1]; // Oink oink

#define NUM_OPS 100
void (*ops[NUM_OPS])(void);

// OOOOOOOiiink:
int IP = 0;
int input[2];
int input_ptr = 0;
int output = -1;
int max_output = 0;
int phases[5] = {0,1,2,3,4};
FILE * fp;

#define POW10(n) (int) pow(10, n)
#define MAX(a,b) a>b?a:b
int param(n) {
  return (data[IP]/POW10(n+1))%10 ? data[IP+n] : data[data[IP+n]];
}
void set_param(n, val) {
  if ((data[IP]/POW10(n+1))%10)
    data[IP+n] = val;
  else
    data[data[IP+n]] = val;
}

void op_add() {
  set_param(3, param(1) + param(2));
  IP += 4;
}
void op_mult() {
  set_param(3, param(1) * param(2));
  IP += 4;
}
void op_input() {
  printf("using input: %d\n", input[input_ptr]);
  set_param(1, input[input_ptr++]);
  IP += 2;
}
void op_output() {
  printf("output: %d\n", param(1));
  output = param(1);
  IP += 2;
}
void op_jump_if_true() {
  IP = param(1) ? param(2) : IP+3;
}
void op_jump_if_false() {
  IP = !param(1) ? param(2) : IP+3;
}
void op_less_than() {
  set_param(3, param(1) < param(2));
  IP += 4;
}
void op_equals() {
  set_param(3, param(1) == param(2));
  IP += 4;
}

void op_err() { printf("Unknown opcode: %d\n", data[IP]); exit(-1); }

void swap(int *a, int *b) {
   int t;

   t  = *b;
   *b = *a;
   *a = t;
}

void permute(int phases[5], int l, int r)
{
    if (l == r) {
      output = 0;
      printf("Phases: %d %d %d %d %d\n", phases[0], phases[1], phases[2], phases[3], phases[4]);
      for (int i = 0; i < 5; i++) {
        input[0] = phases[i];
        input[1] = output;
        input_ptr = 0;

        // Reinit data from file:
        fseek(fp, 0, SEEK_SET);
        for(int i = 0; i < MEM_SIZE && fscanf(fp, "%d,", &data[i]) != EOF; i++ );
        data[MEM_SIZE] = 0; // Ensure termination
        IP = 0;

        // Execute ops until termination
        for (IP = 0; data[IP] != 99; ops[data[IP] %100]()) {
          // Debug:
          // printf("[%d] %d (%d): %d %d %d\n", IP, data[IP], data[IP] %100, data[IP+1], data[IP+2], data[IP+3]);
        }
      }
      max_output = MAX(max_output, output);
      printf("max output: %d\n", max_output);
    }
    else {
        // Permutations:
        for (int i = l; i <= r; i++)
        {
            swap(phases+l, phases+i);
            permute(phases, l+1, r);
            swap(phases+l, phases+i);
        }
    }
}

int main(int argc, char *argv[])
{
  // input = atoi(argv[1]);

  fp = fopen ("input.txt","r");

  for( int i = 0; i < NUM_OPS; ops[i++] = op_err);
  ops[1] = op_add;
  ops[2] = op_mult;
  ops[3] = op_input;
  ops[4] = op_output;
  ops[5] = op_jump_if_true;
  ops[6] = op_jump_if_false;
  ops[7] = op_less_than;
  ops[8] = op_equals;

  permute(phases, 0, 4);

  printf("\n");
}


//15163975
