#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 3 || strcmp(argv[1], "-t") != 0) {
        printf("Usage: %s -t <ip_address>\n", argv[0]);
        return 1;
    }

    char *ip_address = argv[2];

    char command[100];
    sprintf(command, "ping -c 3 %s", ip_address); // 3 paket ping gönder
    system(command);

    return 0;
}
