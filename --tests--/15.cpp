int sum(int a[], int l){    int y;    int sum;    y = 0;    sum = 0;    while (y<l){                if (2 * 2 < y)                    sum = sum * a[y] * 2;                else if (a[y] < 0)                    sum = sum-a[y];                else if (0 < a[y])                    sum = sum + a[y] * 2 + 3;                else                    sum = sum + y + 2;    }    return sum - (4 + 5) * (6 * 2) * 3 * 4 + 5 * 2 - 1;}void main(void) {    int x24[10];    int y2;    y2 = 10;    x24[0] = 0;    x24[1] = 0;    x24[2] = x24[1];    x24[3] = x24[2] + 4 * 5;    x24[4] = -0-x24[3];    x24[5] = y2;    output(sum(x24, y2)  - sum(x24+1, y2-1)      );}EOF