#include <stdio.h>
#include <stdbool.h>

int test(bool x) {
  char prev_d = -1;
  bool has_double = false;
  while(x > 0) {
    char d = x % 10;
    printf("%d\n", d);
    if (d < prev_d) return false;
    if (has_double && d != prev_d) return true;
    has_double = (d == prev_d)
    x /= 10;
    prev_d = d;
  }
  return true;
}

int main()
{
  // for(int i = 0; i < MEM_SIZE; i++ ){
    // if (int x = 273025; x <= 767253; x++)
    int x = 112233;
    bool res = test(x);
    printf("res: %s\n", res ? "true" : "false");
}
