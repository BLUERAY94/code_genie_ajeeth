# 1 "D:\\Code_genie\\Pycparcer\\pycparser-main\\pycparser-main\\examples\\c_files\\basic.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "D:\\Code_genie\\Pycparcer\\pycparser-main\\pycparser-main\\examples\\c_files\\basic.c"
# 1 "D:\\Code_genie\\Pycparcer\\pycparser-main\\pycparser-main\\examples\\c_files\\memmgr.h" 1
# 72 "D:\\Code_genie\\Pycparcer\\pycparser-main\\pycparser-main\\examples\\c_files\\memmgr.h"
typedef unsigned char byte;
typedef unsigned long ulong;






void memmgr_init();



void* memmgr_alloc(ulong nbytes);



void memmgr_free(void* ap);




void memmgr_print_stats();
# 2 "D:\\Code_genie\\Pycparcer\\pycparser-main\\pycparser-main\\examples\\c_files\\basic.c" 2
int s=4234;

extern int variable = 42;

int foo() {}
void func_dumy1()
{
  foo();
}
int main() {
  foo();
  return 0;
}
