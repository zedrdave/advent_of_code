#include "stdio.h"
#include "stdlib.h"
#include "math.h"

#define MEM_SIZE 10000
#define NUM_PHASES 5

int data[NUM_PHASES][MEM_SIZE+1]; // Oink oink ooooinnnk
int IP[NUM_PHASES];

#define NUM_OPS 100
void (*ops[NUM_OPS])(int);

// OOOOOOOiiink:
int input[2];
int input_ptr = 0;
int output = -1;
int max_output = 0;
int phases[5] = {5,6,7,8,9};
FILE * fp;

#define POW10(n) (int) pow(10, n)
#define MAX(a,b) a>b?a:b
int param(n, p) {
  return (data[p][IP[p]]/POW10(n+1))%10 ? data[p][IP[p]+n] : data[p][data[p][IP[p]+n]];
}
void set_param(n, val, p) {
  if ((data[p][IP[p]]/POW10(n+1))%10)
    data[p][IP[p]+n] = val;
  else
    data[p][data[p][IP[p]+n]] = val;
}

void op_add(int p) {
  set_param(3, param(1, p) + param(2, p), p);
  IP[p] += 4;
}
void op_mult(int p) {
  set_param(3, param(1, p) * param(2, p), p);
  IP[p] += 4;
}
void op_input(int p) {
  printf("using input: %d\n", input[input_ptr]);
  set_param(1, input[input_ptr++], p);
  IP[p] += 2;
}
void op_output(int p) {
  printf("output: %d\n", param(1, p));
  output = param(1, p);
  IP[p] += 2;
}
void op_jump_if_true(int p) {
  IP[p] = param(1, p) ? param(2, p) : IP[p]+3;
}
void op_jump_if_false(int p) {
  IP[p] = !param(1, p) ? param(2, p) : IP[p]+3;
}
void op_less_than(int p) {
  set_param(3, param(1, p) < param(2, p), p);
  IP[p] += 4;
}
void op_equals(int p) {
  set_param(3, param(1, p) == param(2, p), p);
  IP[p] += 4;
}

void op_err(int p) { printf("Unknown opcode: %d\n", data[p][IP[p]]); exit(-1); }

void swap(int *a, int *b) {
   int t;

   t  = *b;
   *b = *a;
   *a = t;
}

void permute(int phases[5], int l, int r)
{
    if (l == r) {
      printf("Phases: %d %d %d %d %d\n", phases[0], phases[1], phases[2], phases[3], phases[4]);

      output = 0; // first signal

      // Init each phase:
      for (int p = 0; p < 5; p++) {
        fseek(fp, 0, SEEK_SET);
        for(int i = 0; i < MEM_SIZE && fscanf(fp, "%d,", &data[p][i]) != EOF; i++ );
        data[p][MEM_SIZE-1] = 0; // Ensure termination
        IP[p] = 0;
      }
      int running = NUM_PHASES;
      int iter = 0;
      while(running > 0) {
        for (int p = 0; p < 5; p++) {
          printf("i: %d | p: %d [%d]\n", iter, p, IP[p]);

          input[0] = phases[p];
          input[1] = output;
          input_ptr = iter ? 1 : 0;

          // Execute ops until termination or output
          for (; data[p][IP[p]] != 99; ops[data[p][IP[p]] %100](p)) {
            // Debug:
            // printf("[%d] %d (%d): %d %d %d\n", IP[p], data[p][IP[p]], data[p][IP[p]] %100, data[p][IP[p]+1], data[p][IP[p]+2], data[p][IP[p]+3]);
            if (data[p][IP[p]] == 4) {// output
              ops[data[p][IP[p]]](p);
              break;
            }
          }
          if (data[p][IP[p]] == 99) {
            printf("Reached term\n");
            running--;
          }
        }
        iter++;
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
