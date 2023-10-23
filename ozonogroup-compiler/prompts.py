import sys 

print(len(sys.argv))
if len(sys.argv) != 2:
    print('ERR: missing INDUSTRY')
    quit()

industry = sys.argv[1]


print()
print()
print()
print()
print()

i = 0 
print(f'''
{i}.
Lista 30 applicazioni dell'ozono nell'industria {industry}. 
Non aggiungere descrizioni.
''')
print(f'''-----------------------------------------------------------''')
i += 1


print(f'''
{i}.
Lista di applicazioni dell'ozono per il trattamento delle acque reflue nell'industria {industry}. 
Non aggiungere descrizioni.
''')
print(f'''-----------------------------------------------------------''')
i += 1

print(f'''
{i}.
Date la seguente lista di applicazioni dell'ozono per il trattamento delle acque reflue nell'industria {industry}, 
dai 3-5 esempi per ogni elemento della lista.

- Inattivazione di microrganismi patogeni
- Rimozione di contaminanti organici
- Diminuzione di solidi sospesi
- Abbattimento di odori sgradevoli
- Eliminazione di sostanze coloranti
- Decadimento di disinfettati chimici
- Riduzione di prodotti farmaceutici
- Rimozione di pesticidi ed erbicidi
- Ossidazione di metalli pesanti

Usa il minore numero di parole possibili per gli esempi.
''')
print(f'''-----------------------------------------------------------''')

print(f'''
{i}.
Date la seguente lista di applicazioni dell'ozono per il trattamento delle acque reflue nell'industria {industry}, 
dai 3-5 esempi per ogni elemento della lista.

- Inattivazione di microrganismi patogeni
- Rimozione di contaminanti organici
- Diminuzione di solidi sospesi
- Abbattimento di odori sgradevoli
- Eliminazione di sostanze coloranti
- Decadimento di disinfettati chimici
- Riduzione di prodotti farmaceutici
- Rimozione di pesticidi ed erbicidi
- Ossidazione di metalli pesanti

Usa il minore numero di parole possibili per gli esempi.
''')
print(f'''-----------------------------------------------------------''')
i += 1


print(f'''
{i}.
Utilizzantdo la lista precedente, formatta i dati in una tabella a 2 colonne.
I titoli delle 2 colonne sono: Applicazione, Esempi
''')
print(f'''-----------------------------------------------------------''')
i += 1

print(f'''
{i}.
Scrivi una sezione per un articolo usando i dati forniti dalla tabella precedente.
La sezione deve essere lunga meno di 200 parole.
Non scrivere in formato lista. Scrivi in formato discorsivo.
Usa frasi semplici, con una struttura dritta e in voce attiva.
Non aggiungere opinioni, scrivi solo i fatti.

La prima frase di questa sezione deve essere la seguente:

"L'ozono viene utilizzato per il trattamento delle acque reflue nell'industria {industry}."
''')
print(f'''-----------------------------------------------------------''')
i += 1


# print(f'''
# Utilizzantdo i seguenti elementi della seguente lista:

# - Inattivazione di microrganismi patogeni
# - Rimozione di composti organici
# - Trattamento di solidi sospesi
# - Eliminazione di odori sgradevoli
# - Eliminazione di sostanze coloranti
# - Degradazione di disinfettanti chimici
# - Rimozione di pesticidi
# - Rimozione di erbicidi
# - Ossidazione di metalli pesanti

# Riguardanti il trattamento delle acque reflue nell'industria {industry}, crea una tabella.

# La tabella deve avere solo 2 colonne. 
# Nella prima colonna scrivi gli elementi di questa lista.
# Nella seconda colonna scrivi 3-5 esempi relativa agli elementi della prima colonna nella stessa cella. 
# Non numerare gli esempi. Usa meno parole possibili.

# Metti tutti i dati in formato tabella. 
# ''')
# print(f'''-----------------------------------------------------------''')


# - **Inattivazione di microrganismi patogeni:** Batteri, virus, lieviti.
# - **Rimozione di composti organici:** Idrocarburi, composti fenolici, solventi.
# - **Trattamento di solidi sospesi:** Solidi sospesi, sedimenti, particelle in sospensione.
# - **Eliminazione di odori sgradevoli:** Odori di zolfo, ammoniaca, acri.
# - **Eliminazione di sostanze coloranti:** Coloranti naturali, coloranti artificiali, pigmenti.
# - **Degradazione di disinfettanti chimici:** Cloro, cloramine, biossido di cloro.
# - **Rimozione di pesticidi:** Fungicidi, insetticidi, erbicidi.
# - **Rimozione di erbicidi:** Glyphosate, Atrazine, Simazine.
# - **Ossidazione di metalli pesanti:** Piombo, cadmio, mercurio.

# Utilizzantdo i seguenti elementi della seguente lista:

# - Inattivazione di microrganismi patogeni
# - Rimozione di composti organici
# - Trattamento di solidi sospesi
# - Eliminazione di odori sgradevoli
# - Eliminazione di sostanze coloranti
# - Degradazione di disinfettanti chimici
# - Rimozione di pesticidi
# - Rimozione di erbicidi
# - Ossidazione di metalli pesanti

# Riguardanti il trattamento delle acque reflue nell'industria vino, crea una tabella.

# La tabella deve avere solo 2 colonne.
# Nella prima colonna scrivi gli elementi di questa lista.
# Nella seconda colonna scrivi 3-5 esempi tutti nella stessa cella, relativi ad ogni corrispettivo elemento della prima colonna.
# Non numerare gli esempi. Usa meno parole possibili.



# Ossidazione di composti fenolici
# Abbrunimento di azoto ammoniacale
# Rimozione di cloro residuo
# Eliminazione di composti aromatici
# Eliminazione di tensioattivi
# Rimozione di composti clorurati

# Riduzione della DQO (Domanda Chimica di Ossigeno)
# Trattamento di acque reflue industriali


# Ossidazione dei contaminanti
# Rimozione di sostanze organiche
# Sterilizzazione delle acque reflue
# Riduzione del carico inquinante
# Eliminazione di odori sgradevoli
# Inattivazione di microrganismi patogeni
# Abbrunimento dei composti organici
# Decolorazione delle acque reflue
# Rimozione di pesticidi e erbicidi
# Trattamento di acque reflue ad alta concentrazione di solidi sospesi
# Eliminazione di metalli pesanti
# Abbattimento di sostanze tossiche
# Ossidazione di composti fenolici
# Rimozione di contaminanti emergenti
# Trattamento delle acque di lavaggio
# Abbrunimento di azoto ammoniacale
# Sterilizzazione delle acque di scarico
# Riduzione della DQO (Domanda Chimica di Ossigeno)
# Eliminazione di sostanze coloranti
# Inattivazione di batteri e virus
# Abbrunimento di sostanze organiche complesse
# Rimozione di cloro residuo
# Trattamento di acque reflue industriali
# Eliminazione di composti aromatici
# Riduzione del carico batterico
# Ossidazione di composti organici refrattari
# Eliminazione di tensioattivi
# Abbrunimento di fenoli
# Trattamento di acque reflue di processo
# Rimozione di composti clorurati





# per ogni elemento della seguente lista:

# Disinfezione degli strumenti e attrezzature agricole.
# Pulizia delle serre e delle aree di lavorazione.
# Trattamento delle superfici di impianti di ventilazione e aria condizionata.
# Sanificazione delle pareti e pavimenti delle strutture di coltivazione.
# Sterilizzazione delle attrezzature per la raccolta dei funghi.
# Disinfezione delle confezioni e imballaggi.
# Sanitizzazione dei camion per il trasporto dei funghi.
# Pulizia delle superfici delle aree di stoccaggio.
# Sterilizzazione delle superfici di laboratori di ricerca fungicola.

# scrivi 3-5 esempi nella stessa cella. non numerare gli esempi. usa meno parole possibili.

# metti tutti i dati in formato tabella. la tabella deve avere solo 2 colonne.



# scrivi una sezione per una articolo usando i dati forniti dalla tabella precedente. la sezione deve essere lunga meno di 200 parole. non scrivere in formato lista. scrivi in formato discorsivo. usa frasi semplici, con una struttura dritta e in voce attiva. non aggiungere opinioni, scrivi solo i fatti.


# Ecco una lista di problemi di contaminazione dell'acqua di processo nell'industria fungicoltura:

# 1. Contaminazione batterica
# 2. Contaminazione da virus
# 3. Contaminazione da microrganismi nocivi
# 4. Contaminazione da funghi indesiderati
# 5. Contaminazione chimica da pesticidi
# 6. Contaminazione da metalli pesanti
# 7. Contaminazione da agenti inquinanti ambientali
# 8. Contaminazione da sostanze organiche non desiderate
# 9. Contaminazione da particelle sospese
# 10. Contaminazione da nutrienti eccessivi o carenti
# 11. Contaminazione da batteri nocivi
# 12. Contaminazione da parassiti acquatici
# 13. Contaminazione da scarti organici di processo
# 14. Contaminazione da scarichi industriali
# 15. Contaminazione da contaminanti emergenti
# 16. Contaminazione da sedimenti e detriti



# Contaminazione batterica
# Contaminazione da funghi patogeni
# Contaminazione da virus
# Contaminazione da alghe
# Contaminazione da metalli pesanti
# Contaminazione da pesticidi
# Contaminazione da sostanze organiche nocive
# Contaminazione da sedimenti e particelle sospese
# Contaminazione da sostanze chimiche industriali
# Contaminazione da microbi indesiderati