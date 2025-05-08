// Tommaso Mingrone [SM3201286]
#include "pgm.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

// Crea una nuova immagine PGM con le dimensioni specificate
PGMImage *createPGM(int width, int height) {
    PGMImage *img = malloc(sizeof(PGMImage)); // Alloca memoria per la struttura dell'immagine
    img->width = width; // Imposta la larghezza dell'immagine
    img->height = height; // Imposta l'altezza dell'immagine
    img->data = malloc(width * height * sizeof(unsigned char)); // Alloca memoria per i pixel dell'immagine
    return img; // Restituisce il puntatore all'immagine PGM creata
}

// Imposta il valore di un pixel specifico nell'immagine PGM
void setPixel(PGMImage *img, int row, int col, int maxIter, int iter) {
    if (iter == maxIter) {
        img->data[row * img->width + col] = 255; // Imposta il pixel a bianco se il punto è interno all'insieme di Mandelbrot
    } else {
        double scale = log(iter) / log(maxIter); // Calcola la scala di grigi
        img->data[row * img->width + col] = (unsigned char)(255 * scale); // Imposta il pixel sulla scala di grigi corrispondente
    }
}

// Salva l'immagine PGM nel file specificato
int savePGM(const char *filename, const PGMImage *image) {
    
    /* 
    O_RDWR: Apre il file per la lettura e la scrittura.
    O_CREAT: Crea il file se non esiste.
    O_TRUNC: Se il file esiste già, tronca il file alla lunghezza di 0, cancellando il suo contenuto precedente.
    0666: Imposta i permessi del file.
    */
    
    int fd = open(filename, O_RDWR | O_CREAT | O_TRUNC, 0666); 
    if (fd == -1) {
        perror("Errore nell'apertura del file");
        return 0; // Restituisce 0 in caso di errore nell'apertura del file
    }

    // Calcola la lunghezza dell'intestazione del file PGM
    char header[100];
    int header_length = snprintf(header, sizeof(header), "P5\n%d %d\n255\n", image->width, image->height);

    // Calcola la dimensione totale del file (intestazione + dati dell'immagine)
    size_t file_size = header_length + (image->width * image->height);

    // Imposta la dimensione del file
    if (ftruncate(fd, file_size) == -1) {
        perror("Errore nel troncamento del file");
        close(fd);
        return 0;
    }

    // Mappa il file in memoria
    char *map = mmap(0, file_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) {
        perror("Errore nel mapping del file");
        close(fd);
        return 0;
    }

    // Scrive l'intestazione del file PGM nella mappatura
    memcpy(map, header, header_length);

    // Scrive i dati dell'immagine subito dopo l'intestazione
    memcpy(map + header_length, image->data, image->width * image->height);

    // Check che le modifiche siano scritte sul file
    if (msync(map, file_size, MS_SYNC) == -1) {
        perror("Errore nella sincronizzazione della memoria mappata");
        munmap(map, file_size);
        close(fd);
        return 0;
    }

    // Libera la mappatura
    if (munmap(map, file_size) == -1) {
        perror("Errore nel liberare la mappatura");
        close(fd);
        return 0;
    }

    // Chiusura del file descriptor
    close(fd);
    return 1; // Restituisce 1 se il salvataggio è avvenuto con successo
}

// Libera la memoria allocata per l'immagine PGM
void freePGM(PGMImage *image) {
    free(image->data);
    free(image);
}

