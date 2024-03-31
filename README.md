
## README

### Monitor de Fișiere

Acest program monitorizează un folder specific pentru a detecta și gestiona modificările aduse fișierelor din interiorul său. În plus, furnizează informații detaliate despre aceste fișiere.

### Utilizare

1. **Configurare Inițială**

    - Asigurați-vă că ați instalat Python 3.x pe sistemul dvs.
    - Descărcați și salvați codul sursă în folderul dorit.

2. **Dependențe**

    - Acest program utilizează biblioteca standard Python și nu necesită dependențe suplimentare.

3. **Pornirea Programului**

    - În terminal, navigați către directorul în care ați salvat codul sursă.
    - Rulați programul utilizând comanda `python nume_program.py`.

4. **Comenzi Disponibile**

    - `commit`: Realizează o captură a stării actuale a folderului monitorizat și o înregistrează într-un fișier de commit.
    - `info <filename>`: Afișează informații detaliate despre un fișier specificat.
    - `status`: Afișează starea actuală a folderului monitorizat, evidențiind modificările.

5. **Exemplu de Utilizare**

    - `commit`: `commit` poate fi folosit pentru a face o captură a stării curente. Aceasta va fi salvată într-un fișier de commit cu marcaj de timp.
    - `info nume_fișier`: Afișează informații despre un fișier specificat, cum ar fi tipul, data de creare și data de ultimă modificare.
    - `status`: Furnizează un rezumat al stării curente a folderului monitorizat, evidențiind fișierele noi și cele șterse.

6. **Notă**

    - Programul rulează într-un thread separat pentru a monitoriza în mod continuu folderul și a detecta modificările.
    - Pentru a opri programul, închideți terminalul sau apăsați `Ctrl + C`.

### Exemple

- Pentru a face o captură a stării curente:
    ```
    Bagă șeva (commit/info <filename>/status): commit
    ```

- Pentru a obține informații despre un fișier specific:
    ```
    Bagă șeva (commit/info <filename>/status): info nume_fișier
    ```

- Pentru a verifica starea curentă a folderului monitorizat:
    ```
    Bagă șeva (commit/info <filename>/status): status
    ```

### Observații

- Programul oferă suport pentru diferite tipuri de fișiere, inclusiv imagini, fișiere text și fișiere de program.
- În timpul monitorizării, orice modificare adusă unui fișier va fi raportată în terminal.
- Fișierele de commit sunt create automat în directorul folderului monitorizat, conținând o captură a stării la momentul respectiv.

### Autor

- Programul a fost dezvoltat de [GRAUR DANILA].
