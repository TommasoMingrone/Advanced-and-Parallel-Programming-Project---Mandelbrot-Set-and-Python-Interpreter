// Tommaso Mingrone [SM3201286]
#ifndef MANDELBROT_H
#define MANDELBROT_H

#include <stdbool.h>

// Definisce la struttura per rappresentare l'insieme di Mandelbrot
typedef struct {
    int nrows;          // Numero di righe dell'immagine (risoluzione verticale)
    int ncols;          // Numero di colonne dell'immagine (risoluzione orizzontale)
    int maxIter;        // Numero massimo di iterazioni per determinare l'appartenenza all'insieme di Mandelbrot
    double radius;      // Raggio usato nella condizione di fuga
    int **iterations;   // Matrice per memorizzare il numero di iterazioni per ogni punto nell'immagine
} MandelbrotSet;

// Inizializza il MandelbrotSet
MandelbrotSet initMandelbrotSet(int nrows, int ncols, int maxIter);

// Calcola il frattale di Mandelbrot
void calculateMandelbrot(MandelbrotSet *set);

// Libera la memoria allocata per MandelbrotSet
void freeMandelbrotSet(MandelbrotSet *set);

#endif
