# SubitoParserPublic

## Introduzione

Questo script python, da eseguire perpetuamente, ricerca ogni X secondi le keyword su subito.it per nuovi annunci, per poi mandare all'utente un messaggio attraverso un bot che sfrutta le API di Telegram. Un file JSON tiene traccia degli annunci già trovati.

## Setup

Su Telegram, contattare [BotFather](https://t.me/BotFather), inviare un messaggio "/newbot" e seguire i passaggi. Al termine, verrà fornito un token.  
Ora è necessario sapere il chatID dell'utente, per ottenere questo serve mandare un messaggio al bot telegram appena creato e visitare https://api.telegram.org/bot<TOKEN>/getUpdates, dove <TOKEN> è il token fornito da BotFather. Nella risposta JSON, annotare il numero nel campo "id".  
Questi due dati ottenuti devono essere sostituiti all'interno del codice, oltre ovviamente ai termini di ricerca desiderati.
