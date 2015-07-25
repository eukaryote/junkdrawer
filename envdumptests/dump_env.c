#include <unistd.h>
#include <stdio.h>


int main(int argc, char **argv, char** envp)
{
  char** env;
  for (env = envp; *env != 0; env++)
  {
    char* curr_env = *env;
    printf("%s\n", curr_env);
  }
  return 0;
}
