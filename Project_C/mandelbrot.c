// Tommaso Mingrone [SM3201286]
#include "mandelbrot.h"
#include <stdlib.h>
#include <complex.h>
#include <omp.h>

// Inizializzazione dell'insieme di Mandelbrot con dimensioni, iterazioni massime e raggio
MandelbrotSet initMandelbrotSet(int nrows, int ncols, int maxIter) {
    MandelbrotSet set;
    set.nrows = nrows;     // Imposta il numero di righe dell'immagine
    set.ncols = ncols;     // Imposta il numero di colonne dell'immagine
    set.maxIter = maxIter; // Imposta il numero massimo di iterazioni per punto
    set.radius = 2;        // Imposta il raggio di default a 2

    // Allocazione dinamica della matrice per memorizzare il numero di iterazioni per ogni punto
    set.iterations = malloc(nrows * sizeof(int*));
    for (int i = 0; i < nrows; i++) {
        set.iterations[i] = malloc(ncols * sizeof(int));
    }
    return set;
}

// Calcolo dell'insieme di Mandelbrot
void calculateMandelbrot(MandelbrotSet *set) {
    #pragma omp parallel for collapse(2) // Parallelizzazione del ciclo con OpenMP
    for (int row = 0; row < set->nrows; row++) {
        for (int col = 0; col < set->ncols; col++) {

            // Conversione delle coordinate pixel in coordinate del piano complesso
            double x0 = -2.0 + 3.0 * col / (set->ncols - 1);
            double y0 = -1.0 + 2.0 * row / (set->nrows - 1);
            complex double c = x0 + y0 * I;
            complex double z = 0.0 + 0.0 * I;
            int iter = 0;

            // Iterazione per il calcolo dell'appartenenza al set di Mandelbrot
            while (cabs(z) <= set->radius && iter < set->maxIter) {
                z = z * z + c; // Iterazione di Mandelbrot
                iter++;
            }

            // Memorizzazione del numero di iterazioni necessarie
            set->iterations[row][col] = iter;
        }
    }
}

// Libera la memoria allocata per l'insieme di Mandelbrot
void freeMandelbrotSet(MandelbrotSet *set) {
    for (int i = 0; i < set->nrows; i++) {
        free(set->iterations[i]); // Libera ogni riga della matrice
    }
    free(set->iterations); // Libera la memoria della matrice
}
