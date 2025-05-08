// Tommaso Mingrone [SM3201286]
#include <stdio.h>
#include <stdlib.h>
#include "mandelbrot.h"
#include "pgm.h"

int main(int argc, char *argv[]) {

    // Verifica che siano stati passati il numero corretto di argomenti
    if (argc != 4) {
        fprintf(stderr, "Uso: %s <nome file> <max iterazioni> <risoluzione verticale>\n", argv[0]);
        return 1; // Termina con un errore se gli argomenti non sono corretti
    }

    // Estrae gli argomenti dalla riga di comando
    char *filename = argv[1];
    int maxIterazioni = atoi(argv[2]); // Conversione del terzo argomento da linea di comando in un intero per le iterazioni massime
    int nrows = atoi(argv[3]); // Conversione del quarto argomento da linea di comando in un intero per la risoluzione verticale dell'immagine
    int ncols = (int)(1.5 * nrows); // Conversione esplicita a intero e calcola la larghezza come 1.5 volte l'altezza

    // Verifica la validità degli argomenti passati
    if (maxIterazioni <= 0 || nrows <= 0) {
        fprintf(stderr, "Errore: Valori non validi per iterazioni o risoluzione.\n");
        return 1; // Termina con un errore se le iterazioni o la risoluzione sono non valide
    }

    // Inizializza e calcola l'insieme di Mandelbrot
    MandelbrotSet set = initMandelbrotSet(nrows, ncols, maxIterazioni);
    calculateMandelbrot(&set);

    // Crea l'immagine PGM
    PGMImage *image = createPGM(ncols, nrows);

    // Impostazione dei pixel dell'immagine basata sulle iterazioni di Mandelbrot
    for (int row = 0; row < nrows; row++) {
        for (int col = 0; col < ncols; col++) {
            setPixel(image, row, col, maxIterazioni, set.iterations[row][col]);
        }
    }

    // Salvataggio dell'immagine e gestione degli errori con un codice diverso da 0
    if (!savePGM(filename, image)) {
        fprintf(stderr, "Errore: Impossibile salvare l'immagine.\n");
        return 1; // Termina con un errore se il salvataggio non riesce
    }

    // Pulizia della memoria e terminazione del programma
    freePGM(image); // Libera la memoria dell'immagine
    freeMandelbrotSet(&set); // Libera la memoria dell'insieme di Mandelbrot
    printf("L' immagine '%s' è stata creata con successo.\n", filename);
    return 0; // Termina con successo
}