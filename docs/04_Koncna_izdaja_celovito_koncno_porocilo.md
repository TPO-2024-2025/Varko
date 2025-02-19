# :blue_square: Končna izdaja (celovito končno poročilo)

| [:arrow_backward:](03_Izvedljiv_sistem_2_porocilo_o_stanju.md) Prejšnji dokument |                       Trenutni dokument                       | Naslednji dokument |
| :------------------------------------------------------------------------------- | :-----------------------------------------------------------: | -----------------: |
| :green_square: **Izvedljiv sistem**<br>(2. poročilo o stanju)                    | :blue_square: **Končna izdaja**<br>(celovito končno poročilo) |                    |

![Terminski načrt](https://teaching.lavbic.net/plantuml/svg/dPR1Rk8m48RlVehHza0NAPGOabOhL5LjjrArAxLQxQceXu6Or2JOA3PqOTL7w5lrmNOS0YMGacg53p3C_F_uypZAXR6OsHYLjV3bjyWcKfb4WiAtryn-OQndx28LvopFk9OOPpY1lmp0oeb8fHBv3u2VzFLAfpg3en5tdpnwevLTHQbkGQ4NLuacAQekSPZ4cPwfgAWLPwDW5Eqg1ZUNPz-lYdBCClsyxrhAcSXK6AittVsFpp3LHaGV2LHkCfNnaztiz8NrJWfwZ9YgAJfsWnqbcw4oz9TGbZMUP2HWfBKTw3yiHHNFC1PWKZRDfB9cYAc0Po6IT46IQ6TPX0i28efccI7PSeItUU2rknxtGPfoa5Pba6y5MMCLxdZ-QHvsFHCLgU0eQWiS3TOPNQzTa-7M1ndh11v-aC3kCpqMGmlvk1fO5N3gYh5-Bo_ujg5__a3JAwn8G2xdE4OrHfYIu4HOX6FURl7Mrzv9NdJ-24yudGfb06r9jR6dMc7KRFx2PKJtm8evpC4aiobDKxC9npvO4GcrvOC6-jV-8wHeQ0C1q46PIidRvK1cIBqlvHmFQF6I5g2ArdHeAywgOK0eEaFF0xy5r6E6GqaiF8-WDPltX2JLCQ4Xj8brLaKtUIF77MUhvAvjPsthh_QmPyoTSHvW_Rieme8-MU76g-padxOw1u_4ZH_hFs2ivtHbzjHMdJtimDrhhBDDX5SGkJDgviR6I6F5vBD0WWsGRetl6WUTnbHd-krLfWZQvQhnhEnrskeU9EAkspkHIi622g-X4cnJwLHGkLtEYVTOpWikkrYwrLZ23PQp6kCr5bwF9MW51x6uzOw57y3IgS4IRcFfLc3veTNRgtBtr3N_oLdnUTtj2NUf9BcFSEE-sKl9YeUrK7Zu3gL2hq3IhK7YymsJ_USMuH33oWTks0eFjXVIOko2TFENZ7y0 "Terminski načrt")

Končno poročilo naj bo edini vir za pregled poljubnega vidika projekta. Pričakuje se, da vsebuje posodobljene podatke o dodani vrednosti za naročnika iz [predloga projekta](01_Predlog_projekta.md), opredelitvi problema iz [1. poročila o stanju](02_Osnutek_sistema_1_porocilo_o_stanju.md) in opis sistema iz [2. poročila o stanju](03_Izvedljiv_sistem_2_porocilo_o_stanju.md). Razdelek [**9 Refleksija**](#9-refleksija) predstavlja retrospektiven pogled na celoten pogled. Vsebino iz prejšnjih poročil lahko ponovno uporabite, vključno z uporabniškimi zgodbami, primeri uporabe, kontekstnim diagramom in osrednjimi arhitekturnimi pogledi.

## :page_with_curl: Opisni naslov, osredotočen na prednosti za naročnika

## :information_desk_person: Ime ekipe: Člani ekipe

## 1 Uvod

### Začetni odstavek

- Kaj je projekt?
  - Kakšna je motivacija za ta projekt?
- Kaj je pri tem izvirnega?
  - Še kakšen vidik za orientacijo bralca?

### 1.1 Izzivi

- Na kratko opišite glavne izzive za ekipo.
  - Kako ste jih naslovili?
  - Je bila tehnologija ekipi znana ali nova?

### 1.2 Poudarki

- Izpostavite, kaj ste v okviru projekta dosegli.

### 1.3 Spremembe

- Povzemite vse večje spremembe predloga katerega koli vidika projekta med semestrom.
- Vključite datum, motivacijo, opis in posledice vsake spremembe.

## 2 Potrebe naročnika

- Kdo je primarni naročnik (zunaj ekipe)?
  - Opišite dejanskega naročnika.
- Kdo so sekundarni deležniki?
- Kaj so deležniki želeli? Zakaj?
- Kakšna je njihova želena splošna izkušnja?

### 2.1 Uporabniške zahteve

- Zapišite **SMART** uporabniške zgodbe s pomočjo predloge "Kot **_\<vloga\>_** želim **_\<akcija\>_**, da **_\<posledica\>_**."
- Za uporabniške zgodbe zapišite teste sprejemljivosti z uporabo predloge "Glede **\<pogoj\>**, ko **\<akcija\>**, potem **\<posledica\>**."

## 3 Cilji projekta

- Za katero težavo naročnika ste se odločili, da jo boste obravnavali?
  - Brez tehničnih podrobnosti opišite koristi sistema za naročnika.
  - Kako bodo koristi podprle želeno splošno izkušnjo naročnika?
  - Kako ste potrdili ustreznost vaše ideje?

### 3.1 Primeri uporabe

- Zapišite primer uporabe za vsak osrednji cilj primarnega oz. sekundarnega naročnika.
- Pri vsakem primeru uporabe opredelitev naslov, cilj uporabnika in osnovni tok. Izberite opisne naslove primerov uporabe.
- Pri alternativnih tokih dogodkov, ki ste jih implementirali, zapišite zgolj naslov, opis v enem stavku in kako se alternativni tok povezuje s pripadajočim osnovnim tokom.

### 3.2 Merila uspeha

- Kako veste, ali je naročnik dobil želene koristi?
- Katera merila uspeha so pomembna naročniku?

## 4 Opis sistema

### 4.1 Pregled sistema

- Predstavite sistem in glavne izzive.
  - Povzemite utemeljitve izbranih načrtovalskih odločitev.
  - Narišite kontekstni diagram, ki prikazuje, kako sistem sodeluje z zunanjimi storitvami, podatkovnimi bazami ipd. Jasno označite meje sistema.
- Na kratko pojasnite zunanje interakcije sistema.

### 4.2 Osrednji arhitekturni pogledi

- Za vsak pogled zagotovite osrednji diagram.
- Za arhitekturne elemente v diagramu dodajte katalog elementov z imenom in namenom vsakega elementa.
- Za vsak element določite enega člana ekipe (tudi, če je več članov ekipe prispevalo k elementu), ki bo njen skrbnik.

## 5 Končno stanje

- Kaj deluje? Vključite posnetke zaslona.
- Katere teste ste izvedli?
- Ocenite ustreznost testov.
- Koliko vrstic kode ste napisali (vse skupaj)?

## 6 Vodenje projekta

- Opišite uporabljen razvojni proces.
- Kateri so bili ključni dogodki med projektom? Vključite tudi datume.
- Še kaj drugega?

### 6.1 Usklajevanje ekipe

- Kdaj in kako pogosto se je ekipa sestajala?
- Kako ste komunicirali?
- Kaj ste dosegli med sestanki?

### 6.2 Projektni načrt

- Povzetek razdelitve projekta na aktivnosti s seznamom izdelkov, vključno z Ganttovim diagramom in grafom PERT.

### 6.3 Finančni načrt

- Finančni načrt projekta po metodi COCOMO II.

## 7 Ekipa

### 7.1 Predznanje

- Kakšno je bilo predznanje ekipe?
  - Kakšne predhodne delovne izkušnje pri razvoju programske opreme?
  - Je kateri član ekipe že razvil kaj podobnega?
  - Ali so bila orodja ekipi znana ali nova?

### 7.2 Vloge

- Kakšne so bile vloge članov ekipe pri projektu?
- Kaj je prispeval vsak član ekipe?
- Za določitev posameznih prispevkov uporabite kataloge elementov.
- Navedite grobo oceno prispevka posameznega člana ekipe v odstotkih.

## 8 Omejitve in tveganja

- Ali so bile kakšne družbene, etične, politične ali pravne omejitve?
- Ali ste imeli dostop do podatkov, storitev in virov, ki ste jih potrebovali?
- Ali je bilo še kaj drugega, kar ste potrebovali?

## 9 Refleksija

- Kaj ste se naučili pri tem projektu?
- Kaj je šlo po pričakovanjih?
  - Katero od vaših praks bi opredelili kot najboljšo prakso?
- Kaj ni šlo po pričakovanjih?
- Kaj ne deluje in kako ste to rešili?
  - Kakšne težave ste imeli pri funkcionalnostih, ki jih niste implementirali?

## 9.1 Priporočila

- Kaj bi naredili drugače?
- Kaj svetujete ostalim ekipam?
- Kaj bi priporočili naročniku?
