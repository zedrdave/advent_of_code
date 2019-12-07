#include "stdio.h"
#include "stdlib.h"
#include "math.h"

#define MEM_SIZE 10000
#define NUM_OPS 100

#define NUM_PHASES 5

FILE *fp; // so that I can use new[] constructor with a single arg array

int max_output = 0;

#define POW10(n) (int) pow(10, n)
#define MAX(a,b) a>b?a:b

class Machine {
  public:
    int data[MEM_SIZE]; // Oink oink
    void (*ops[NUM_OPS])(void);
    int IP;
    int output;

    Machine(int phase) {
      fseek(fp, 0, SEEK_SET);
      for(int i = 0; i < MEM_SIZE && fscanf(fp, "%d,", &data[i]) != EOF; i++);
      IP = 0;

      // Init with phase input:
      set_param(1, phase);
      IP += 2;
    }

    int run(int input) {
      int output = -1;

      while (data[IP] != 99) {
        // printf("[%d] %d: %d %d %d\n", IP, data[IP], data[IP+1], data[IP+2], data[IP+3]);
        switch(data[IP] % 100) {
          case 1: // op_add() {
            set_param(3, param(1) + param(2));
            IP += 4;
          break;
          case 2: // op_mult
            set_param(3, param(1) * param(2));
            IP += 4;
          break;
          case 3: // op_input
            printf("using input: %d\n", input);
            set_param(1, input);
            IP += 2;
          break;
          case 4: // op_output
            output = param(1);
            printf("output: %d\n", output);
            IP += 2;
            return output;
          break;
          case 5: // op_jump_if_true
            IP = param(1) ? param(2) : IP+3;
          break;
          case 6: // op_jump_if_false
            IP = !param(1) ? param(2) : IP+3;
          break;
          case 7: // op_less_than
            set_param(3, param(1) < param(2));
            IP += 4;
          break;
          case 8: // op_equals
            set_param(3, param(1) == param(2));
            IP += 4;
          break;
          default: // op_err
            printf("Unknown opcode: %d\n", data[IP]);
            exit(-1);
          break;
        }
      }

      // printf("[END]\n");
      return 0;
    }

    bool is_running() {
      return(data[IP] != 99);
    }

    int param(int n) {
      return (data[IP]/POW10(n+1))%10 ? data[IP+n] : data[data[IP+n]];
    }
    void set_param(int n, int val) {
      if ((data[IP]/POW10(n+1))%10)
        data[IP+n] = val;
      else
        data[data[IP+n]] = val;
    }
};

void swap(int *a, int *b) {
   int t;
   t  = *b;
   *b = *a;
   *a = t;
}

void run_machines(int *phases) {
  printf("Phases: %d %d %d %d %d\n", phases[0], phases[1], phases[2], phases[3], phases[4]);

  // Init each phase:
  Machine machines[NUM_PHASES] = {phases[0], phases[1], phases[2], phases[3], phases[4]};

  int iter = 0;
  int output = 0; // first input
  while(machines[0].is_running()) {
    for (int p = 0; p < 5; p++) {
      // printf("iter: %d | p: %d [%d]\n", iter, p, machines[p].IP);
      output = machines[p].run(output);
      max_output = MAX(max_output, output);
    }
    iter++;
  }
  printf("max output: %d\n", max_output);

}


void permute(int phases[5], int l, int r, void (* fn)(int args[])) {
    if (l == r) {
      fn(phases);
    }
    else {
        // Permutations:
        for (int i = l; i <= r; i++)
        {
            swap(phases+l, phases+i);
            permute(phases, l+1, r, fn);
            swap(phases+l, phases+i);
        }
    }
}

int main(int argc, char *argv[])
{
  fp = fopen ("input.txt","r");

  int phases[NUM_PHASES] = {5,6,7,8,9};
  permute(phases, 0, 4, run_machines);

  printf("\n");
}

// 1047153
