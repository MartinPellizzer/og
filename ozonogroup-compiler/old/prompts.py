import sys 

print(len(sys.argv))
if len(sys.argv) != 3:
    print('ERR: missing INDUSTRY, APPLICATION')
    quit()

industry = sys.argv[1]
application = sys.argv[2]
# .lower().strip().replace(' ', '-')


print()
print()
print()
print()
print()

lst = ['[inserisci lista qui]']
if application == 'acque-reflue':
    lst = [ 
        "- Inattivazione di microrganismi patogeni",
        "- Rimozione di contaminanti organici",
        "- Diminuzione di solidi sospesi",
        "- Abbattimento di odori sgradevoli",
        "- Eliminazione di sostanze coloranti",
        "- Decadimento di disinfettati chimici",
        "- Riduzione di prodotti farmaceutici",
        "- Rimozione di pesticidi ed erbicidi",
        "- Ossidazione di metalli pesanti"
    ]
elif application == 'attrezzature':
    lst = [ 
        "- Inattivazione di microbi",
        "- Abbattimento di muffe e lieviti",
        "- Estirpazione di alghe da serbatoi",
        "- Eliminazione di odori sgradevoli",
        "- Degradazione di disinfettati chimici",
        "- Rimozione di residui di pesticidi",
        "- Riduzione di residui di erbicidi",
    ]
elif application == 'aria-ambienti':
    lst = [ 
        "- Inattivazione di batteri e virus",
        "- Abbattimento di muffe e funghi",
        "- Controllo di parassiti e insetti",
        "- Eliminazione di odori sgradevoli",
        "- Degradazione di composti chimici",
        "- Diminuzione di gas tossici",
        "- Riduzione di composti organici volatili (cov)",
    ]
elif application == 'prodotti-alimentari':
    lst = [ 
        "- Inattivazione di microrganismi patogeni",
        "- Controllo di parassiti e insetti",
        "- Rimozione di contaminanti organici",
        "- Abbattimento di odori sgradevoli",
        "- Decadimento di disinfettati chimici",
        "- Riduzione di prodotti farmaceutici",
        "- Rimozione di pesticidi ed erbicidi",
        "- Ossidazione di metalli pesanti"
    ]
elif application == 'acqua-processo':
    lst = [ 
        "- Inattivazione di batteri e virus",
        "- Controllo di muffe",
        "- Estirpazione di alghe",
        "- Rimozione di contaminanti organici",
        "- Abbattimento di odori sgradevoli",
        "- Decadimento di disinfettati chimici",
        "- Rimozione di pesticidi ed erbicidi",
        "- Ossidazione di metalli pesanti"
    ]

# Rimozione dei contaminanti organici.
# Eliminazione di batteri e virus.
# Riduzione di odori sgradevoli.
# Controllo delle alghe nell'acqua di processo.
# Eliminazione dei sapori indesiderati.
# Riduzione dei batteri sulle superfici.
# Declorazione dell'acqua.
# Inibizione della crescita dei biofilm.
# Rimozione delle impurità sospese.
# Controllo della concentrazione batterica.
# Eliminazione di microrganismi patogeni.
# Controllo della presenza di lieviti.
# Eliminazione di microrganismi indesiderati.
# Inattivazione di enzimi indesiderati.
# Riduzione della necessità di additivi chimici.
# Controllo delle infezioni microbiologiche.
# Eliminazione di contaminanti organici volatili.



riassunto = f'''RIASSUNTO

        Scrivi una sezione per un articolo usando i dati forniti dalla tabella precedente.
        La sezione deve essere lunga meno di 300 parole.
        Non scrivere in formato lista. Scrivi in formato discorsivo.
        Usa frasi semplici, con una struttura dritta e in voce attiva.
        Non aggiungere opinioni, scrivi solo i fatti.

        La prima frase di questa sezione deve essere la seguente:

    '''
lst_print = "\n".join(lst)

application = application.strip().lower().replace('-', ' ')

num = 3
i = 0 

print(f'''{i}. GENERAL

    Lista 30 applicazioni dell'ozono nell'industria {industry}. 
    Non aggiungere descrizioni.
''')
print(f'''-----------------------------------------------------------''')
i += 1

print(f'''{i}. APPLICAZIONI

    Lista di 30 applicazioni dell'ozono per il trattamento di {application} nell'industria {industry}. 
    Non aggiungere descrizioni.
''')
print(f'''-----------------------------------------------------------''')
i += 1

num = 3
tmp_lst = '[insert list here]'
try:
    tmp_lst = [f'{num} ' + x.split(' di ')[1] for x in lst]
    tmp_lst = ', '.join(tmp_lst)
except: pass
print(f'''{i}. LISTA PROBLEMI

    dammi un elenco di {tmp_lst} che si trovano in {application} nell'industria {industry} che l'ozono riesce ad eliminare. dammi solo i nomi, no le descrizioni.
''')
print(f'''-----------------------------------------------------------''')
i += 1


if application == 'acque-reflue':


    print(f'''
        {i}.
        Date la seguente lista di applicazioni dell'ozono per il trattamento delle {application} nell'industria {industry}, 
        dai 3-5 esempi per ogni elemento della lista.

        {lst_print}

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

    print(f'''{i}. RIASSUNTO
        {riassunto}
    
        L\'ozono viene utilizzato per il trattamento delle acque reflue nell'industria {industry}.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1


elif application.strip().lower().replace(' ', '-') == 'attrezzature':



    print(f'''{i}. TABELLA
        Crea una tabella a 2 colonne. Nella prima colonna scrivi gli elementi della seguente lista:

        {lst_print}

        Nella seconda colonna metti gli elementi delle liste della tua ultima risposta nelle giuste celle.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1

    print(f'''{i}. RIASSUNTO
        {riassunto}
    
        L\'ozono viene utilizzato per il trattamento delle attrezzature nell'industria {industry}.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1

    print(f'''{i}. LISTA ATTREZZATURE
        Dammi una lista di 10 {application} più comuni nell'industria {industry} dove si può utilizzare l'ozono per la sanificazione.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1


elif application.strip().lower().replace(' ', '-') == 'aria-ambienti':



    print(f'''{i}. TABELLA
        Crea una tabella a 2 colonne. Nella prima colonna scrivi gli elementi della seguente lista:

        {lst_print}

        Nella seconda colonna metti gli elementi delle liste della tua ultima risposta nelle giuste celle.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1

    print(f'''{i}. RIASSUNTO
        {riassunto}
    
        L\'ozono viene utilizzato per il trattamento degli ambienti nell'industria {industry}.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1

    print(f'''{i}. LISTA AMBIENTI
        Dammi una lista di 10 ambienti più comuni nell'industria {industry} dove si può utilizzare l'ozono per la sanificazione.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1


elif application.strip().lower().replace(' ', '-') == 'prodotti-alimentari':



    print(f'''{i}. TABELLA
        Crea una tabella a 2 colonne. Nella prima colonna scrivi gli elementi della seguente lista:

        {lst_print}

        Nella seconda colonna metti gli elementi delle liste della tua ultima risposta nelle giuste celle.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1

    print(f'''{i}. RIASSUNTO
        {riassunto}
    
        L\'ozono viene utilizzato per il trattamento dei prodotti alimentari nell'industria {industry}.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1

    print(f'''{i}. LISTA PRODOTTI
        Dammi una lista di 10 prodotti alimentari più comuni nell'industria {industry}.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1
    

elif application.strip().lower().replace(' ', '-') == 'acqua-processo':

    

    print(f'''{i}. TABELLA
        Crea una tabella a 2 colonne. Nella prima colonna scrivi gli elementi della seguente lista:

        {lst_print}

        Nella seconda colonna metti gli elementi delle liste della tua ultima risposta nelle giuste celle.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1

    print(f'''{i}. RIASSUNTO
        {riassunto}
    
        L\'ozono viene utilizzato per il trattamento dell'acqua di processo nell'industria {industry}.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1

    print(f'''{i}. LISTA PRODOTTI
        Dammi una lista di 10 prodotti alimentari più comuni nell'industria {industry}.
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1

    print(f'''{i}. INTRO
        Riassumi il seguente testo in meno di 200 parole in modo discorsivo e non con liste:
    ''')
    print(f'''-----------------------------------------------------------''')
    i += 1


def paragraphs():
    print('''
Write 3 paragraphs.

In the first paragraph, write about the effectiveness of ozone sanitization in eliminating pathogenic microorganisms, including bacteria, viruses, molds, fungi, and spores.
In the second paragraph, write about the effectiveness of ozone sanitization in removing unpleasant and unwanted odors.
In the third paragraph, write about the effectiveness of ozone sanitization in naturally repelling pest insects, including flies, mosquitoes, fleas, cockroaches, ants, bedbugs, moths, and small rodents.

Include as much data, info and numbers possible. 
Do not add opinions, write only objective data.
Use the metric system for numbers.
    ''')

# - Rimozione di allergeni

# dammi un elenco di 3-5:

# - batteri e virus
# - muffe e lieviti
# - odori sgradevoli
# - disinfettati chimici
# - pesticidi
# - erbicidi
# che si trovano in attrazzature nell'industria vitivinicola.

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





dammi una lista di 30 applicazioni della sanificazione ad ozono nella soffitta della casa

dammi una lista di insetti presenti nella soffitta della casa che l'ozono può sanificare

scrivi un paragrafo di 100 parole utilizzando i dati forniti nella lista precedente.
comincia il paragrafo con le seguenti parole:  Il gas O3 allontana insetti infestanti che spesso si trovano nella soffitta della casa, come 

scrivimi 5 liste che riguardano la sanificazione ad ozono.
nella lista 1, elenca 5 odori sgradevoli che si trovano nella soffitta della casa.
nella lista 2, elenca 5 microbi che si trovano nella soffitta della casa.
nella lista 3, elenca 5 superfici  che si trovano nella soffitta della casa.
nella lista 4, elenca 5 oggetti  che si trovano nella soffitta della casa.
nella lista 5, elenca 5 insetti  che si trovano nella soffitta della casa.
non aggiungere descrizioni agli elementi delle liste.
scrivi sempre in minuscolo (lowercase).

scrivimi una tabella a 2 colonne utilizzando i dati delle precedenti liste.
nella colonna 1, elenca: odori, microbi, superfici, oggetti, insetti.
nella colonna 2, elenca i corrispettivi dati in un unica cella.
il titolo della colonna 1 è: Tipologia Utilizzo 
il titolo della colonna 2 è: Applicazioni Sanificazione




homepage for a website about ozone saintization in the food processing industry, scientific style, brand color blue, primary backgroud color white, simple layout

beautiful food processing plant in fields, external view, clear blue sky



####################################################
CASE STUDY

chat gpt

write an engaging and seo friendly one mage case study about a polished concrete project completed by our contractor client for a manufacturing facility, using the following bullet points privided by the client:



magazine back cover about cultivating mushrooms, write the brand address, contact info, and call to action with phone number


man in white coat, blue gloves, and blue mask assessing the quality of bottles of wine in a cellar, soft light, 8k

frustrated male sanitization operator with white coat, blue gloves, and blue mask looking at toxic chemical sanitizers in a storage room, soft light, 8k



----------------------------------------------------------------------------

scrivi 5 liste.

nella lista 1, scrivi i batteri più comuni e problematici presenti nell'industria salumiera. 
nella lista 2, scrivi i virus più comuni e problematici presenti nell'industria salumiera. 
nella lista 3, scrivi i muffe più comuni e problematici presenti nell'industria salumiera. 
nella lista 4, scrivi i parassiti più comuni e problematici presenti nell'industria salumiera. 
nella lista 5, scrivi gli odori più comuni e problematici presenti nell'industria salumiera. 

ordina i patogeni delle liste dal più frequente a qello meno frequente. dammi sono i nomi, non aggiungere descrizioni.

----------------------------------------------------------------------------

Lista 1: Batteri più comuni nell'industria salumiera

Listeria monocytogenes
Salmonella
Escherichia coli (E. coli)
Staphylococcus aureus
Clostridium botulinum

Lista 2: Virus più comuni nell'industria salumiera

Norovirus
Hepatitis A
Rotavirus
Adenovirus
Calicivirus

Lista 3: Muffe più comuni nell'industria salumiera

Aspergillus flavus
Penicillium
Mucor
Rhizopus
Alternaria

Lista 4: Parassiti più comuni nell'industria salumiera

Trichinella spiralis
Toxoplasma gondii
Taenia solium
Anisakis
Cryptosporidium

Lista 5: Odori più comuni nell'industria salumiera

Odore di ammoniaca
Odore di muffa
Odore di acido acetico
Odore sgradevole di putrefazione
Odore di zolfo

----------------------------------------------------------------------------

scrivi un paragrafo di 5 righe che riassuma il seguente testo:


### Batteri


L'ozono elimina i batteri tipici dell'industria lattiero casearia, come Escherichia coli e Staphylococcus aureus, contribuendo a garantire la sicurezza microbiologica dei prodotti lattieri.

I batteri più comuni presenti nell'industria lattiero-casearia che si possono eliminare con l'ozono sono elencati nella seguente lista.

- Escherichia coli
- Listeria monocytogenes
- Salmonella spp.
- Staphylococcus aureus
- Clostridium spp.

### Virus

L'ozono inattiva i virus tipici dell'industria lattiero casearia, come Norovirus e Hepatitis A virus, fornendo un efficace controllo della contaminazione virale nei processi di produzione.

I virus più comuni presenti nell'industria lattiero-casearia che si possono inattivare con l'ozono sono elencati nella seguente lista.

- Norovirus
- Hepatitis A virus
- Rotavirus
- Enteric viruses
- Calicivirus

### Muffe

L'ozono ossida le muffe tipiche dell'industria lattiero casearia, come Penicillium spp. e Aspergillus spp., contribuendo a preservare la qualità del prodotto e a prevenire la formazione di micotossine indesiderate.

Le muffe più comuni presenti nell'industria lattiero-casearia che si possono ossidare con l'ozono sono elencati nella seguente lista.

- Penicillium spp.
- Aspergillus spp.
- Geotrichum candidum
- Mucor spp.
- Rhizopus spp.

### Parassiti

L'ozono repelle i parassiti tipici dell'industria lattiero casearia, come Cryptosporidium parvum e Giardia lamblia, svolgendo un ruolo cruciale nella prevenzione delle contaminazioni parassitarie.

I parassiti più comuni presenti nell'industria lattiero-casearia che si possono repellere con l'ozono sono elencati nella seguente lista.

- Cryptosporidium parvum
- Giardia lamblia
- Entamoeba histolytica
- Taenia spp.
- Toxoplasma gondii

### Odori

L'ozono disgrega gli odori tipici dell'industria lattiero casearia, come ammoniaca e acido lattico, migliorando la qualità sensoriale dei prodotti lattieri e garantendo una migliore accettabilità da parte dei consumatori.

Gli odori più comuni presenti nell'industria lattiero-casearia che si possono disgregare con l'ozono sono elencati nella seguente lista.

- Ammoniaca
- Acido lattico
- Rancidità
- Butirro
- Muffa