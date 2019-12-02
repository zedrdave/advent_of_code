#include "stdio.h"
#define MEM_SIZE 1000 // Oink oink
#define TARGET 19690720

int main()
{
  int size_d;
  int d[MEM_SIZE];
  FILE * fp = fopen ("input.txt","r");

  for(int init_v = 0; init_v < 100; init_v++) {
    for(int init_n = 0; init_n < 100; init_n++) {
      fseek(fp, 0, SEEK_SET);
      for(size_d = 0; size_d < MEM_SIZE && fscanf(fp, "%d,", &d[size_d]) != EOF; size_d++ );

      printf("\nInit: 1: %d, 2:%d\n", init_n, init_v);
      d[1] = init_n;
      d[2] = init_v;

      for(int *ip = d; (size_d -= 4) > 0; ip += 4) {
        printf("[%d]: ", ip[0]);
        if (ip[0] == 99) {
          if (d[0] == TARGET) {
            printf("TARGET REACHED (%d) for init: %d\n", d[0], d[1]*100+d[2]);
            return 0;
          }
          printf("EOP: %d\n", d[0]);
          break;
        }
        if (ip[0] < 1 || ip[0] > 2) {
          printf("Unknown opcode\n");
          return -1;
        }

        printf("d[%d] <- %d %c %d\n", ip[3], d[ip[1]], "+*"[ip[0]-1], d[ip[2]]);
        d[ip[3]] = ip[0] == 1 ?  d[ip[1]] + d[ip[2]] :  d[ip[1]] * d[ip[2]];
      }
    }
  }

  printf("Did not reach end-of-program\n");
  return -2;
}
