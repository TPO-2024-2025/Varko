# :green_square: Izvedljiv sistem (2. poročilo o stanju)

| [:arrow_backward:](02_Osnutek_sistema_1_porocilo_o_stanju.md) Prejšnji dokument |                       Trenutni dokument                       | Naslednji dokument [:arrow_forward:](04_Koncna_izdaja_celovito_koncno_porocilo.md) |
| :------------------------------------------------------------------------------ | :-----------------------------------------------------------: | ---------------------------------------------------------------------------------: |
| :orange_square: **Osnutek sistema**<br>(1. poročilo o stanju)                   | :green_square: **Izvedljiv sistem**<br>(2. poročilo o stanju) |                      :blue_square: **Končna izdaja**<br>(celovito končno poročilo) |

## Pametna integracija Varko

Skupina 20:
- Jaka Čelik
- Tara Majkič
- Jaka Pelko
- Klemen Remec
- Miha Vintar

# 1 Uvod

## 1.1 Poudarki

### Načrtovanje iteracije

Ob začetku iteracije smo določili okvirni načrt dela, ki ga moramo opraviti.

Glavni cilj te iteracije je predstavljala izdelava delujočega izdelka, ki vsebuje večinoma dokončane implementacije tako zalednega sistema kot uporabniškega vmesnika in integracije s pametnimi napravami. Prav tako je bil eden od ciljev pisanje testov enot končne implementacije.

Poleg tega je cilj te iteracije tudi, da se vzpostavi CI cevovod, ki bo skrbel za kvaliteto kode in stabilnost glavne razvojne veje na GitHub-u z avtomatskim testiranjem.

Za zaključek iteracije smo načrtovali izdelavo poročila o izvedljivem sistemu, v katerem obrazložimo narejeno delo te iteracije.

### Doseženi cilji iteracije

Ekipa je dosegla zastavljeni cilj, torej končni produkt te iteracije vsebuje povečini delujoč izdelek, ki je testiran in tako z manjšimi dodelavami ter pripravo končne dokumentacije pripravljen na izdajo.

## 1.2 Spremembe

Plan smo med iteracijo zaradi težav dobave zvočnika popravili, tako da integracijo zvočnika, za katerega predvidevamo podoben postopek integracije kot za luč, prestavljamo med delovne naloge naslednje iteracije. Pri tem ne predvidevamo nobenih zamud ali blokad ostalih delovnih nalog prihodnje iteracije.

# 2 Potrebe naročnika

### Opis problemske domene

Uporabniki imajo na svojem pametnem telefonu naloženo aplikacijo Home Assistant, ki v sistem sporoča njihovo lokacijo.

Administrator sistema določi, kateri uporabniki objekta bodo tretirani kot uporabniki sistema tako, da jih v nastavitvah integracije, ki morajo biti pregledne in enostavne za uporabo, doda v skupino uporabnikov.

Lokacija uporabnikov se bo pridobivala s pomočjo v Home Assistant že vgrajene podpore za sledenje lokacije uporabnikov preko lokacijskih con, ki bodo služile kot meje za določanje prisotnosti uprabnikov. Administrator sistema v nastavitvah integracije določi, katero že določeno lokacijsko cono bo sistem uporabljal.

Sistem bo na podlagi lokacije uporabnikov čakal na pogoje za njegovo aktivacijo. Sistem se aktivira, ko se vsi uporabniki, dodani v skupino uporabnikov, nahajajo izven določene lokacijske cone.

Kamere pošiljajo video prenos v omrežje preko protokola RTSP, ki ga sprejema vsebnik Docker z naloženim sistemom Frigate za prepoznavo ljudi. Sistem Frigate je namenjen prepoznavi subjektov, v tem primeru ljudi, v video prenosu, ki ga dobi iz nastavljenih kamer okoli varovanega objekta.

Ko na video prenosu prepozna osebo, pošlje sporočilo MQTT do drugega vsebnika Docker, ki poganja posrednika komunkacije MQTT. Ta ima nalogo posredništva sporočil MQTT med sistemom Frigate, sistemom Home Assistant (v katerem deluje integracija), in napravami v objektu, katere integracija upravlja.

MQTT posrednik prepošlje obvestilo o prepoznavi osebe sistemu, ki ob prejetju tega signala na podlagi nastavitev varnostnega sistema zažene primerne ukrepe, kar se mora zgoditi v čim krajšem zamiku od zaznave osebe v sistemu Frigate. Administrator v času nastavitve sistema dodaja in odstranjuje naprave, za katere želi, da jih sistem v primeru ukrepanja uporabi za simulacijo prisotnosti uporabnikov. Prav tako lahko naprave (začasno) aktivira in deaktivira, če jih želi vključiti ali izključiti iz uporabe. Tako ima administrator kar največji nadzor nad uporabo naprav, povezanih v sistem.

Sistem uporabnikom tudi pošlje obvestilo o prožitvi sistema za informiranost uporabnikov o stanju delovanja sistema.

Simulacijo prisotnosti lahko administrator sistema aktivira oziroma deaktivira tudi ročno iz uporabniškega vmesnika. To omogoča ne le testiranje sistema ob začetni namestitvi, temveč tudi predstavlja varnostni mehanizem v primeru neželenega delovanja sistema.

# 3 Cilji projekta

Čas, ko v objektu ni nobenega prebivalca, predstavlja najbolj verjetni časovni okvir za vlome, saj je pogosto že na daleč vidno, da je hiša prazna. Pogosti rešitvi sta stalno puščanje prižganih naprav, kar je energijsko potratno, in/ali prošnja znancu za občasen pregled okolice, kar ni popolnoma zanesljivo.

Integracija poskuša doseči boljši način zmanjšanja verjetnosti vloma v objekt. Če v času odsotnosti vseh uporabnikov objekta sistem med nadzorom okolice zazna pristnost potencialnih vlomilcev, aktivira različne preventivne ukrepe, kot so prižiganje luči, vklop televizorja, premikanje senčil ali drugih pametnih naprav. S tem odvrne potencialne vlomilce in poveča varnost objekta brez neposrednega posredovanja uporabnika.

Vse funkcionalne in nefunkcionalne zahteve so opisane in ovrednotene [v istem poglavju prejšnjega poročila](https://github.com/TPO-2024-2025/Projekt-20/blob/main/docs/02_Osnutek_sistema_1_porocilo_o_stanju.md#3-cilji-projekta).

# 4 Opis sistema

## 4.1 Pregled sistema

### Predstavitev sistema

Integracija Varko povezuje mnoge komponente v enovit varnostni sistem. Spodaj je prikazan splošen blokovni diagram sistema.

<p align="center">
  <img src="gradivo/img/Osnutek%20sistema/opis_sistema.png" alt="Opis sistema" width="1000">
</p>

Sistem Frigate je namenjen prepoznavi ljudi v video prenosu, ki ga zagotavljajo nameščene kamere preko RTSP protokola. V primeru zaznave ljudi to preko MQTT protokola javi sistemu Mosquitto.

Sistem Mosquitto je posrednik sporočil protokola MQTT, po katerem poteka večina komunnikacije med sistemi znotraj naše rešitve. V primeru prejetja sporočila o zaznavi ljudi s strani sistema Frigate to sporoči sistemu Home Assistant.

Poslovna logika razvite integracije se ob prejetju sporočila o zaznavi ljudi odloči o ukrepanju, kar naredi na podlagi uporabniških nastavitev integracije ter lokacij uporabnikov, ki jih priskrbi sistem Home Assistant preko mobilne aplikacije. V primeru pravih pogojev integracija zažene varnostni odziv - simulacijo prisotnosti uporabnikov objekta preko aktivacije integriranih pametnih naprav, za kar se uporabi protokol MQTT (sporočila se posredujejo preko sistema Mosquitto).

Stanje sistema lahko administrator sistema kadarkoli nastavi tudi ročno iz uporabniškega vmesnika.

### Načrtovalski vzorci

Pri trenutni implementaciji smo se poslužili nekaterih načrtovalski vzorcev, saj so omogočili ne le ponovno uporabo določenih delov kode, temveč tudi večjo preglednost implementacije. Izbrani vzorci so:

**Decorator**

Vzorec `decorator` smo uporabili za lažje [upravljanje z dodajanjem in odstranjevanjem Home Assistant storitev](https://github.com/TPO-2024-2025/Projekt-20/blob/b093a67c51fdb78dc1214e81a0a3696de97a1773/src/custom_components/varko/decorators.py#L9-L11) ter za [preverjanje avtorizacije](https://github.com/TPO-2024-2025/Projekt-20/blob/b093a67c51fdb78dc1214e81a0a3696de97a1773/src/custom_components/varko/decorators.py#L14-L34). Implementacije Home Assistant storitev smo ovili z dekoratorjem, ki je poskrbel, da se servis avtomatsko doda in odstrani z Home Assistant instance. Prav tako smo določene storitve ovili z dekoratorjem, ki je poskrbel, da to storitev lahko kličejo samo administratorji.

**Singleton**

Vzorec `singleton` smo uporabili pri [implementaciji posameznih managerjev](https://github.com/TPO-2024-2025/Projekt-20/blob/b093a67c51fdb78dc1214e81a0a3696de97a1773/src/custom_components/varko/services/device_manager.py#L19-L30). Te so odgovorni za svoje področje (recimo za upravljanje z skupinami, napravami, …). Z vzorcem singleton smo poskrbeli, da je vedno ustvarjena največ ena instanca posameznega managerja. S tem smo omogočili avtomatsko dodajanje in odstranjevanje storitev s pomočjo zgoraj omenjenega `decorator` vzorca.

**State**

Vzorec `state` smo uporabili za [prehajanje med stanji](https://github.com/TPO-2024-2025/Projekt-20/blob/b093a67c51fdb78dc1214e81a0a3696de97a1773/src/custom_components/varko/services/state_manager.py#L20-L93) znotraj naše integracije. Z njim smo zagotovili pravilno prehajanje med stanji sistema in ob enem ohranili kodo pregledno in enostavno.

### Izzivi implementacije

Izzivi, ki so se med razvojem razvojem sistema pojavili, so bili redki.

Eden izmed izzivov, s katerimi smo se soočili pri implementaciji logike za upravljanje s conami, je bila zahteva, da mora biti sledena naprava uporabnika sistema SUS priključena na isto omrežje kot strežnik, na katerem deluje Home Assistant. Ta pogoj je razvoj in testiranje nekoliko otežil. Rešitev omenjene težave v tej razvojni fazi še ni bila izvedena, je pa načrtovana za eno izmed prihodnjih različic sistema.

Nekaj težav se je pojavilo tudi zaradi neintuitivnega življenjskega cikla integracije sistema Home Assistant, natančneje njenih metapodatkov.

## 4.2 Osrednji arhiterkturni pogledi

### Namestitveni diagram

Slika predstavlja namestitveni diagram Varko Home Assistant integracije. `Brskalnik` in `Telefon` nista ovita v posebno okolje saj delujeta na večini operacijskih sistemov. `Telefon` se uporablja za zaznavanje lokacije uporabnika.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_namestitveni.png" alt="Namestitveni diagram">
</p>

### Paketni diagram

Na spodnji sliki je predstavljen paketni diagram, ki prikazuje poenostavljen logični pregled nad sistemom.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_paketni.png" alt="Paketni diagram">
</p>

### Komponentni diagram

Spodnji diagram prikazuje komponentni diagram.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_komponentni.png" alt="Komponentni diagram">
</p>

### Diagram prehodov stanj

Spodnji diagram prikazuje diagram prehodov stanj, kjer so označena tri glavna stanja sistema Varko (`ACTIVE`, `READY`, `IDLE`) in ustrezni prehodi med njimi. Za uporabo tovrstnega diagrama smo se odločili zaradi narave našega sistema. Celotno delovanje in interakcije z zunanjimi napravami so namreč odvisne od trenutnega stanja, poleg tega pa smo v implementaciji uporabili načrtovalski vzorec State.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_stanj.png" alt="Diagram prehodov stanj">
</p>

### Razredni diagram

Spodnji diagram prikazuje razredno strukturo implementiranega sistema.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_razredni.png" alt="Razredni diagram">
</p>

# 5 Trenutno stanje

### Delovanje sistema

Cilji iteracije so večinoma ostali isti kot v procesu načrtovanja iteracije. Kot že opisano v uvodu, se je skozi razvojni proces zaradi težav dobave zvočnika cilj testiranja integracije zvočnika zamaknil v naslednjo itreracijo.

Na spodnih slikah je prikazano trenutno stanje Home Assistant kontrolne plošče naše integracije:

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/ui_general.png" alt="Kontrolna plošča">
</p>

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/ui_detail.png" alt="Odprt meni kontrolne plošče">
</p>

Na dani [povezavi](https://drive.google.com/file/d/1jkdYJKgqECaB8Iw7G31vEh_gptoYXKOg/view) je dostopen video, na katerem pokažemo delovanje integracije - natančneje ročne aktivacije in deaktivacije sistema, in s tem posledično tudi simulacije prisotnosti (ta v danem primeru prižge luč).

Diagrami sestave razvitega sistema in izzivi pri razvoju so vidni v 4. poglavju (opis sistema).

### Testiranje

V času razvojnega procesa smo testirali posamezne gradnike prototipa sistema.

En od ciljev iteracije je bila priprava zbirke testov enot, s katerimi bi lažje zagotavljali kakovost produkta in sebi olajšali proces razvoja.

Skupno je bilo napisanih 78 testov enot, ki testirajo funkcionalnosti sistema.

Testiranje se izvaja avtomatično preko Github Actions, ki se poženejo na vsakem Pull Requestu. Tako se še pred združitvijo kode na glavno vejo preverja novo-napisano kodo.

### Statistika končne implementacije prototipa sistema

Do končne implementacije prototipa sistema smo napisali 4025 vrstic kode, od tega 82% v Pythonu, 6% v JavaScriptu, 2% v HTML, 4% v CSS, ostalo pa so konfiguracijske datoteke, potrebne za delovanje sistemov. Razlika med številoma vrstic kode prototipa in razvite implementacije tako znaša 3245 vrstic kode.

# 6 Vodenje projekta

Glavni cilj za naslednjo iteracijo je preiti iz implementiranega prototipa z omejenimi funkcionalnostmi do implementirane in testirane Home Assistant integracije, ki je skladna z zastavljenimi zahtevami, navedenimi v 3. poglavju.

Dnevnik sprememb smo vodili v sklopu funkcije [GitHub Issues](https://github.com/TPO-2024-2025/Projekt-20/issues), kjer smo zapisovali potrebne informacije o delovnih nalogah, kot so opis, dodeljeni razvijalec, čas dodelitve in dokončanja naloge, itd., in delno v sklopu [GitHub Pull Requests](https://github.com/TPO-2024-2025/Projekt-20/pulls), kjer se vidijo spremembe, ki so bile skozi razvoj posameznih delov sistema potrebne za končno omišljeno delovanje.

## 6.1 Projektni načrt

### Ganttov diagram

Časovni načrt po dnevih natančno:

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/gannt_dnevi.png" alt="Ganntov diagram po dnevih">
</p>

Časovni načrt po tednih natančno:

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/gannt_tedni.png" alt="Ganntov diagram po dnevih">
</p>

### Pertov diagram

<p align="center">
  <img src="gradivo/img/Osnutek sistema/pert.png" alt="Pertov diagram">
</p>

# 7 Ekipa
**Vsi člani so sodelovali pri**:

- retrospektivi in načrtu iteracije
- razdelitvi vlog dela
- izdelavi poročila o stanju

### Miha Vintar

**Projektni vodja, scrum master in vodja zalednega sistema**:

- vodenje projekta
- vzpostavitev okolja Home Assistant
- definicija funkcionalnih zahtev
- implementacija poslovne logike, povezane s skupinami uporabnikov
- definicija uporabljenih načrtovalskih vzorcev
- izdelava namestitvenega diagrama
- implementacija CI cevovoda
- izdelava dokumentacije

### Klemen Remec

**Vodja dokumentacije in načrtovanja**:

- vzpostavitev osnutka integracije
- definicija aplikacijskega programskega vmesnika integracije
- implementacija poslovne logike, povezane z upravljanjem prehodov med stanji
- izdelava in pregled dokumentacije

### Tara Majkič

**Sistemski analitik**:

- časovni načrt projekta
- implementacija prototipa poslovne logike
- predstavitev funkcionalnih zahtev
- implementacija poslovne logike, povezane z upravljanjem naprav
- izdelava paketnega diagrama
- izdelava dokumentacije

### Jaka Pelko

**Vodja ekipe za integracijo z zunanjimi napravami**:

- vzpostavitev okolja Frigate
- vzpostavitev okolja MQTT posrednika
- definicija nefunkcionalnih zahtev sistema
- predstavitev funkcionalnih zahtev
- implementacija poslovne logike, povezane z lokacijskimi conami
- izdelava diagrama prehodov stanj
- izdelava dokumentacije

### Jaka Čelik

**Vodja ekipe za uporabniški vmesnik**:

- izdelava prototipa uporabniškega vmesnika
- predstavitev funkcionalnih zahtev
- implementacija uporabniškega vmesnika
- izdelava komponentnega diagrama
- izdelava dokumentacije

Podrobnejša delitev nalog je bila definirana v [predlogu poročila, natančeneje v 6. poglavju (Vodenje projekta)](https://github.com/TPO-2024-2025/Projekt-20/blob/main/docs/01_Predlog_projekta.md#62-projektni-na%C4%8Drt).

# 8 Refleksija

### Izzivi

Izziv je predstavljala predvsem organizacija dela, da smo se razvijalci med seboj čim manj čakali ali popravljali implementacije za nazaj. To smo reševali sproti, s tem da smo agilno prilagajali vrstni red delovnih nalog, ki so morale biti opravljene čim prej.

Prav tako smo zaradi nepričakovanih zamud pri implementaciji istočasno zaključevali razvojni proces in že izdelovali poročilo. To iteracijo s tem nismo imeli tako velikih problemov, predvsem smo zaključevali vzpostavljanje procesa testiranja kode, sicer pa smo, ko se je implementacija v tem času vseeno nekoliko spreminjala, neaktualne dele poročil in grafov morali popravljati. Ob začetku naslednje iteracije si bomo poskusili postaviti tesnejše roke za posamezne delovne naloge, in upoštevali potreben dodaten čas za zaključne popravke.

### Uspehi

Kljub izzivom smo iteracijo zaključili uspešno še pred zaključnim rokom. Implementiran sistem implementira zamišljene funkcionalnosti, prav tako smo dosegli višjo raven razumevanja možnosti uporabe načrtovalskih vzorcev za namen preglednejše in lažje vzdržljive kode.
