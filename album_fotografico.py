import csv
def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO
    album={ }
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lettore=csv.DictReader(file)
            #tolgo gli spazi dai nomi della prima riga (le chiavi)
            nomi = []
            for nome in lettore.fieldnames:
                nome = nome.strip()
                nomi.append(nome)
            lettore.fieldnames = nomi
            for riga in lettore:
                anno=int(riga['anno'])

                #se non esiste lo creo
                if anno not in album:
                    album[anno]=[ ]
                #creo foto
                foto={
                    'codice':riga['codice'],
                    'titolo':riga['titolo'],
                    'autore':riga['autore'],
                    'mese':int(riga['mese']),
                    'anno':anno
                }
                album[anno].append(foto)
        return album

    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    # verifica mese
    if mese < 1 or mese > 12:
        return None
    #controllo se il codice c'è già
    for anno_album in album:
        for foto in album[anno_album]:
            if foto['codice']==codice:
                return None
    #controllo che il file esiste
    try:
        file=open(file_path,'r',encoding='utf-8')
        file.close()
    except FileNotFoundError:
        return None
    #creo foto
    foto={
        'codice':codice,
        'titolo':titolo,
        'autore':autore,
        'mese':mese,
        'anno':anno
    }
    #se l'anno non esiste lo creo
    if anno not in album:
        album[anno]=[ ]
    #aggiungo la foto
    album[anno].append(foto)
    #aggiungo foto al file
    file=open(file_path,'a',encoding='utf-8')
    file.write(codice+','+titolo+','+autore+','+mese+','+anno+'\n')
    file.close()
    return foto



def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO
    for anno in album:
        for foto in album[anno]:
            if foto['codice']==codice:
               return foto['codice']+','+foto['titolo']+','+foto['autore']+','+str(foto['mese'])+','+str(foto['anno'])
    return None



def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO
    titolianno=[]
    for anno_album in album:
        if anno_album==anno:
            for foto in album[anno_album]:
                titolianno.append(foto['titolo'])
    if titolianno==[]:
        return None
    titolianno.sort()
    return titolianno




def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
