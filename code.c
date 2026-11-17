// int x = 10;
// if (x > 5) {
//   int y = 20;
//   y = y + 1;
// } else {
//   int z = 30;
// }
//========================================================================
funct int soma(int a, int b) {
    redire a + b;
}

int resultado = soma(10, 20);
int contador = 0;

dum (contador < 5) {
    resultado = resultado + contador * 2;
    contador = contador + 1;
}

si (resultado >= 30) {
    resultado = resultado * 2;
}
alitersi (resultado == 20) {
    resultado = resultado - 5;
}
aliter {
    resultado = 0;
}