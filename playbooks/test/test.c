#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    int i;
    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-a") == 0) {
            printf("red2net test successful!\n");
            return 0;
        }
    }
    printf("Failed!\n");
    return 1;
}
