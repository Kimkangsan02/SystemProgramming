#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int main() {
    int num = 0;
    int temp1 = 0;
    int temp2 = 0;
    int temp3 = 0;
    float temperature;
    int weather = 0;
    

    FILE* file;
    char line[255];
    char* linePtr;

    // Open the file
    file = fopen("weather.txt", "r");
    if (file == NULL) {
        printf("Error opening the file(weather.txt).\n");
        return 1;
    }

    // Read
    while ((linePtr = fgets(line, sizeof(line), file)) != NULL) {
        //printf("%s", linePtr);
        if (num == 0) {
            temp1 = atoi(linePtr);
        }
        else if (num == 1) {
            temp2 = atoi(linePtr);
        }
        else if (num == 2) {
            weather = atoi(linePtr);
        }
        num++;
    }
    // Close the file
    fclose(file);
    temp3 = temp1 + temp2;
    temperature = temp3;
    temperature /= 2;
    

    // Weather: 0(sunny), 1(cloudy), 2(rainy), 3(snowy)

    if (weather == 0) {
        if (temperature >= 30) {
            temperature += 4;
        }
        else if (temperature >= 20 && temperature < 30) {
            temperature += 3;
        }
        else if (temperature >= 10 && temperature < 20) {
            temperature += 1;
        }
    }
    else if ((weather == 2) || (weather == 3)) {
        if (temperature >= 30) {
            temperature -= 4;
        }
        else if (temperature >= 20 && temperature < 30) {
            temperature -= 3;
        }
        else if (temperature >= 10 && temperature < 20) {
            temperature -= 3;
        }
        else if (temperature >= 0 && temperature < 10) {
            temperature -= 4.5;
        }
    }
    

    // Clothes
    //패딩(1), 코트(2), 후리스(3), 재킷(4), 후드(5), 가디건(6)
    //맨투맨(1), 후드(2), 니트(3), 셔츠(4), 긴팔(5), 반팔(6), 민소매(7)
    //청바지(1), 면바지(2), 슬랙스(3), 롱스커트(4), 숏 팬츠(5), 미니스커트(6)

    int clothes_1;
    int clothes_2;
    int clothes_3;

    //printf("%d\n", weather);
    //printf("%f\n", temperature);

    srand(time(NULL));

    // Excute
    if (temperature < 0) {
        //very cold
        temp3 = 0;
        clothes_1 = (rand() % 2)+1;
        clothes_2 = (rand() % 3)+1;
        clothes_3 = (rand() % 2)+1;
        while (clothes_1 == 5 && clothes_2 == 2)
        {
            clothes_1 = (rand() % 2) + 1;
            clothes_2 = (rand() % 3) + 1;
        }
        /*
        clothes_1[0] = 1;
        clothes_1[1] = 2;
        clothes_1[2] = 0;
        clothes_1[3] = 0;

        clothes_2[0] = 1;
        clothes_2[1] = 2;
        clothes_2[2] = 3;
        clothes_2[3] = 0;

        clothes_3[0] = 1;
        clothes_3[1] = 2;
        clothes_3[2] = 0;
        clothes_3[3] = 0;
        */
    }
    else if (temperature >= 0 && temperature < 10) {
        //cold
        temp3 = 1;
        clothes_1 = (rand() % 3) + 1;
        clothes_2 = (rand() % 3) + 1;
        clothes_3 = (rand() % 3) + 1;
        while (clothes_1 == 5 && clothes_2 == 2)
        {
            clothes_1 = (rand() % 3) + 1;
            clothes_2 = (rand() % 3) + 1;
        }
        /*
        clothes_1[0] = 1;
        clothes_1[1] = 2;
        clothes_1[2] = 3;
        clothes_1[3] = 0;

        clothes_2[0] = 1;
        clothes_2[1] = 2;
        clothes_2[2] = 3;
        clothes_2[3] = 0;

        clothes_3[0] = 1;
        clothes_3[1] = 2;
        clothes_3[2] = 3;
        clothes_3[3] = 0;
        */
    }
    else if (temperature >= 10 && temperature < 20) {
        //cool
        temp3 = 2;
        clothes_1 = (rand() % 3) + 4;
        clothes_2 = (rand() % 3) + 1;
        clothes_3 = (rand() % 3) + 1;
        while (clothes_1 == 5 && clothes_2 == 2)
        {
            clothes_1 = (rand() % 3) + 4;
            clothes_2 = (rand() % 3) + 1;
        }
        /*
        clothes_1[0] = 4;
        clothes_1[1] = 5;
        clothes_1[2] = 6;
        clothes_1[3] = 0;

        clothes_2[0] = 1;
        clothes_2[1] = 2;
        clothes_2[2] = 3;
        clothes_2[3] = 0;

        clothes_3[0] = 1;
        clothes_3[1] = 2;
        clothes_3[2] = 3;
        clothes_3[3] = 0;
        */
    }
    else if (temperature >= 20 && temperature < 25) {
        //mild
        temp3 = 3;
        clothes_1 = 6;
        clothes_2 = (rand() % 3) + 1;
        clothes_3 = (rand() % 4) + 1;
        /*
        clothes_1[0] = 6;
        clothes_1[1] = 0;
        clothes_1[2] = 0;
        clothes_1[3] = 0;

        clothes_2[0] = 1;
        clothes_2[1] = 2;
        clothes_2[2] = 3;
        clothes_2[3] = 0;

        clothes_3[0] = 1;
        clothes_3[1] = 2;
        clothes_3[2] = 3;
        clothes_3[3] = 4;
        */
    }
    else if (temperature >= 25 && temperature < 30) {
        //warm
        temp3 = 4;
        clothes_1 = 0;
        clothes_2 = (rand() % 3) + 4;
        clothes_3 = (rand() % 4) + 3;
        /*
        clothes_1[0] = 0;
        clothes_1[1] = 0;
        clothes_1[2] = 0;
        clothes_1[3] = 0;

        clothes_2[0] = 4;
        clothes_2[1] = 5;
        clothes_2[2] = 6;
        clothes_2[3] = 0;

        clothes_3[0] = 3;
        clothes_3[1] = 4;
        clothes_3[2] = 5;
        clothes_3[3] = 6;
        */
    }
    else if (temperature >= 30) {
        //hot
        temp3 = 5;
        clothes_1 = 0;
        clothes_2 = (rand() % 2) + 6;
        clothes_3 = (rand() % 2) + 5;
        /*
        clothes_1[0] = 0;
        clothes_1[1] = 0;
        clothes_1[2] = 0;
        clothes_1[3] = 0;

        clothes_2[0] = 6;
        clothes_2[1] = 7;
        clothes_2[2] = 0;
        clothes_2[3] = 0;

        clothes_3[0] = 5;
        clothes_3[1] = 6;
        clothes_3[2] = 0;
        clothes_3[3] = 0;
        */
    }


    //printf("%d, %d, %d\n", clothes_1, clothes_2, clothes_3);


    file = fopen("clothes.txt", "w");
    if (file == NULL) {
        printf("Error opening the file(clothes.txt).\n");
        return 1;
    }

    // Write
    fprintf(file, "%d\n", clothes_1);
    fprintf(file, "%d\n", clothes_2);
    fprintf(file, "%d\n", clothes_3);
    if (weather == 2) {
        fprintf(file, "%d", 1);
    }
    else {
        fprintf(file, "%d", 0);
    }

    // Close the file
    fclose(file);


    return 0;
}
