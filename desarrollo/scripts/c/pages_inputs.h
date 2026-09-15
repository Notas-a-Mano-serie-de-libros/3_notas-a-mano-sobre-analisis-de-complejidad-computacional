#ifndef PAGES_INPUTS_H
#define PAGES_INPUTS_H
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int *valores; int cantidad, filas, columnas; } Entrada;
static void entrada_error(const char *mensaje) { fprintf(stderr, "%s\n", mensaje); exit(1); }
static int entrada_entero(int argc, char **argv, int indice, int defecto) {
    if (indice >= argc) return defecto;
    if (!strcmp(argv[indice], "true")) return 1;
    if (!strcmp(argv[indice], "false")) return 0;
    char *fin; errno = 0;
    long valor = strtol(argv[indice], &fin, 10);
    while (isspace((unsigned char)*fin)) fin++;
    if (fin == argv[indice] || *fin || errno || valor < INT_MIN || valor > INT_MAX) entrada_error("La entrada debe ser un entero de 32 bits.");
    return (int)valor;
}
static Entrada entrada_arreglo(int argc, char **argv, int indice, const char *defecto, int matriz) {
    const char *s = indice < argc ? argv[indice] : defecto;
    int *valores = calloc(4096, sizeof(int));
    if (!valores) entrada_error("No hay memoria suficiente.");
    Entrada e = {valores, 0, 0, 0};
    int nivel = 0, anterior = -1, columnas = 0, espera = 1, cerrado = 0;
    while (isspace((unsigned char)*s)) s++;
    if (*s != '{') entrada_error("Usa llaves para las entradas C.");
    while (*s) {
        if (isspace((unsigned char)*s)) { s++; continue; }
        if (cerrado) entrada_error("Hay contenido después del arreglo.");
        if (*s == '{') {
            if (nivel && (!matriz || nivel != 1 || !espera)) entrada_error("Separador o dimensiones inválidos.");
            nivel++;
            if (nivel > (matriz ? 2 : 1)) entrada_error("Dimensiones inválidas.");
            if (matriz && nivel == 2) { e.filas++; columnas = 0; }
            espera = 1; s++; continue;
        }
        if (*s == '}') {
            if (matriz && nivel == 2) {
                if (anterior >= 0 && columnas != anterior) entrada_error("Las filas deben tener la misma longitud.");
                anterior = columnas; e.columnas = columnas;
            }
            if (--nivel < 0) entrada_error("Llaves inválidas.");
            if (!nivel) cerrado = 1;
            espera = 0; s++; continue;
        }
        if (*s == ',') { if (espera) entrada_error("Separador inválido."); espera = 1; s++; continue; }
        if (!espera || nivel != (matriz ? 2 : 1)) entrada_error("Formato de entrada inválido.");
        char *fin; errno = 0; long v = strtol(s, &fin, 10);
        if (fin == s || errno || v < INT_MIN || v > INT_MAX || e.cantidad == 4096) entrada_error("Valores inválidos o entrada demasiado grande (máximo 4096 enteros).");
        e.valores[e.cantidad++] = (int)v; columnas++; s = fin; espera = 0;
    }
    if (nivel || !cerrado) entrada_error("Faltan llaves.");
    if (!matriz) { e.filas = 1; e.columnas = e.cantidad; }
    if (matriz && (!e.filas || !e.columnas)) entrada_error("La matriz debe tener filas y columnas.");
    return e;
}
#endif
