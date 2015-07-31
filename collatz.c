#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>
#include <limits.h>
#include <errno.h>
#include <string.h>
#include <assert.h>

typedef unsigned long long int ULLI;

static ULLI const MAX = (ULLONG_MAX - 1) / 3;

ULLI parse_initial(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s INT\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    errno = 0;
    ULLI val = strtoull(argv[1], NULL, 10);
    if (errno) {
        fprintf(stderr, "%s: parameter %s: %s\n",
                argv[0], argv[1], strerror(errno));
    }
    return val;
}


ULLI collatz(ULLI value, bool verbose) {
    ULLI steps = 0;
    while (1) {
        if (verbose) {
            printf("%llu\n", value);
        }
        assert(value < MAX);
        if (value == 1) {
            break;
        }
        if (value % 2 == 0) {
            value = value / 2;
        } else {
            value = 3 * value + 1;
        }
        steps++;
    }
    return steps;
}



int main(int argc, char **argv) {
    ULLI value = parse_initial(argc, argv);
    bool verbose = strcmp(argv[0], "collatzc") != 0;
    ULLI steps = collatz(value, verbose);
    printf("[%llu -> 1]: %llu iterations\n", value, steps);
    return EXIT_SUCCESS;
}
