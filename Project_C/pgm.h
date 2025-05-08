// Tommaso Mingrone [SM3201286]
#ifndef PGM_H
#define PGM_H

#include <stddef.h>

// Definisce la struttura per un'immagine PGM
typedef struct {
    int width, height;   // Dimensioni dell'immagine
    unsigned char *data; // Dati dell'immagine in scala di grigi
} PGMImage;

// Crea un'immagine PGM vuota
PGMImage *createPGM(int width, int height); 

// Imposta il valore di un pixel specifico
void setPixel(PGMImage *img, int row, int col, int maxIter, int iter); 

// Salva l'immagine in un file PGM
int savePGM(const char *filename, const PGMImage *image); 

// Libera la memoria allocata per l'immagine
void freePGM(PGMImage *image); 

#endif
