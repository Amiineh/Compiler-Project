void add(int a, int b)
{
    int c;
    c =a+   b;
    return ;
}

int Add(int a, int b)
{
    return 3;
}

void main(void) {
    int x;
    x = Add(add(2, 4), 3);
}
EOF
