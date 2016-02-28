#include <Block.h>
#include <dispatch/dispatch.h>

int f(int x) {
  int result = (x / 42);
  dispatch_main();

  return result;
}
