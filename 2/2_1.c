#include "stdio.h"
#define MEM_SIZE 1000 // Oink oink

int main()
{
  int size_d;
  int d[MEM_SIZE];
  FILE * fp = fopen ("input.txt","r");
  for(size_d = 0; size_d < MEM_SIZE && fscanf(fp, "%d,", &d[size_d]) != EOF; size_d++ );
  d[1] = 12;
  d[2] = 2;

  for(int *ip = d; (size_d -= 4) > 0; ip += 4) {
    printf("[%d]: ", ip[0]);
    if (ip[0] == 99) {
      printf("RETURN: %d\n", d[0]);
      return 0;
    }
    if (ip[0] < 1 || ip[0] > 2) {
      printf("Unknown opcode\n");
      return -1;
    }

    printf("d[%d] <- %d %c %d\n", ip[3], d[ip[1]], "+*"[ip[0]-1], d[ip[2]]);
    d[ip[3]] = ip[0] == 1 ?  d[ip[1]] + d[ip[2]] :  d[ip[1]] * d[ip[2]];
  }

  printf("Did not reach end-of-program\n");
  return -2;
}
