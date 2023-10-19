#include <stdio.h>


int main() {
  // Sum of n numbers
  int n;
  int sum = 0;
  scanf("%d", &n);
  int x;
  int i;
  for (i = 1; i <= n; i++) {
    scanf("%d", &x);
    sum = sum + x;
  }
  printf("%d\n", sum);
  return 0;
}
