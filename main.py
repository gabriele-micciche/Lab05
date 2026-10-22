import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    nuovo_strumento = ft.Text("Aggiungi nuovo strumento", size=24)
    tipo = ft.TextField(label = "Tipo")
    marca = ft.TextField(label="Marca")
    anno = ft.TextField(label="Anno")
    valore = ft.TextField( value = "0", label="Valore", )

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aggiungi_strumento(e):
        # 1. Lettura e pulizia delle stringhe
        tipo_str = tipo.value.strip()
        marca_str = marca.value.strip()
        anno_str = anno.value.strip()
        valore_str = valore.value.strip()

        # 2. Controllo se qualche campo è vuoto
        if not tipo_str or not marca_str or not anno_str or not valore_str:
            alert.show_alert("Errore nella compilazione")
            return

        # 3. Conversione numerica sicura
        try:
            anno_num = int(anno_str)
            valore_num = float(valore_str)
        except ValueError:
            alert.show_alert("Anno e valore devono essere numeri")
            return

        if valore_num < 0:
            alert.show_alert("Valore invalido")
            return

        # 4. Aggiunta al deposito
        deposito.aggiungi_strumento(tipo_str, marca_str, anno_num, valore_num)

        # Svuotiamo i campi di testo
        tipo.value = ""
        marca.value = ""
        anno.value = ""
        valore.value = "0"

        # Aggiorniamo la lista visualizzata
        aggiorna_lista_strumenti()


    def incrementa_valore(e):
        # Leggiamo il valore attuale e lo convertiamo in numero
        try:
            val_attuale = float(valore.value)

            # Incrementiamo e riassegniamo il nuovo valore sotto forma di testo
            valore.value = str(val_attuale + 1)

            # Mostriamo la modifica a schermo
            page.update()
        except ValueError:
            alert.show_alert("Valore invalido")

    def diminusci_valore(e):
        # Leggiamo il valore attuale e lo convertiamo in numero
        try:
            val_attuale = float(valore.value)

            if val_attuale > 0:
                valore.value = str(val_attuale - 1)
                # Aggiorniamo la pagina a schermo
                page.update()
        except ValueError:
            alert.show_alert("Valore invalido")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    aggiungi_bottone = ft.CupertinoButton("Aggiungi Strumento", on_click=aggiungi_strumento)
    piu = ft.CupertinoButton("+", color="green", on_click=incrementa_valore)
    meno = ft.CupertinoButton("-", color="red", on_click=diminusci_valore)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        nuovo_strumento,
        ft.Row(spacing=20,
               controls=[tipo, marca, anno, meno, valore, piu],
               alignment=ft.MainAxisAlignment.CENTER),
        aggiungi_bottone,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
