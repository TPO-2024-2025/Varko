# :yellow_square: Predlog projekta

| Prejšnji dokument |          Trenutni dokument           | Naslednji dokument [:arrow_forward:](02_Osnutek_sistema_1_porocilo_o_stanju.md) |
| :---------------- | :----------------------------------: | ------------------------------------------------------------------------------: |
|                   | :yellow_square: **Predlog projekta** |                   :orange_square: **Osnutek sistema**<br>(1. poročilo o stanju) |


# Povzetek projekta
Projekt se osredotoča na razvoj napredne pametne integracije, katere cilj je povečati varnost objektov med časom odsotnosti lastnikov. Podatki raziskav potrjujejo, da največ vlomov poteka ravno v času, ko objekt je oz. izgleda prazen. To poudarja potrebo po rešitvah, ki presegajo tradicionalne metode, kot so stalno prižgane luči ali zanašanje na redne preglede s strani znancev. Nova rešitev temelji na združevanju lokacijskih podatkov uporabnikov in obstoječega Home Assistant ekosistema, ki omogoča integracijo s pametnimi napravami v objektu.

Sistem deluje na principu zaznavanja morebitne prisotnosti neželenih oseb med odsotnostjo vseh uporabnikov objekta, saj v tem primeru sistem sproži preventivne ukrepe - aktivacija pametnih naprav v objektu, ki oddajajo svetlobo in/ali zvok, s čimer se ustvari vtis, da je v objektu nekdo prisoten. Ta dinamičen odziv, prilagojen glede na čas dneva in razpoložljive naprave, omogoča prilagodljivost in zanesljivost brez nepotrebne porabe energije.

Grafični vmesnik nudi uporabnikom enostavno nastavitev sistema in prilagajanje ukrepov glede na kontekst situacije. Končni uporabniki – posamezniki, družine in podjetja, ki že uporabljajo Home Assistant – bodo imeli tako na voljo stroškovno učinkovito in energetsko varčno rešitev, ki bistveno povečuje občutek varnosti in zmanjšuje možnost vloma.

# 1 Projektna ideja

### Ozadje

Podatki raziskav kažejo, da več kot 70% vlomov poteka v času odsotnosti lastnikov oziroma prebivajočih. ([Vir](https://www.simplyinsurance.com/home-invasion-statistics/)) 

Na trgu obstaja mnogo rešitev za zagotavljanje varnosti objektov, nekateri izmed njih se tudi integrirajo s sistemi za pametne domove.

V ekosistemu Home Assistant obstaja že mnogo integracij z varnostnimi sistemi (npr. kamere, alarmi, ipd.). Obstaja tudi [integracija](https://github.com/slashback100/presence_simulation), ki omogoča enostavno oponašanje uporabe naprav ko uporabnika ni v objektu, ampak to dela ves čas aktivacije, ne glede na okoliščine.

### Področje in motivacija

Čas, ko v objektu ni nobenega prebivalca, predstavlja najbolj verjetni časovni okvir za vlome, saj je pogosto že na daleč vidno, da je hiša prazna. Pogosti rešitvi sta stalno puščanje prižganih naprav, kar je energijsko potratno, in/ali prošnja znancu za občasen pregled, kar ni popolnoma zanesljivo.

Vsaka od teh rešitev prinese slabosti, ki pa jih odpravimo z implementacijo namenske pametne integracije, ki bi v v primeru zaznave potencialnih vlomilcev vklopila pametne naprave v objektu, ki bi signalizirale prisotnost v domu. Tak sistem je ne le bolj zanesljiv, temveč tudi stroškovno učinkovitejši.

### Namen

Integracija poskuša doseči boljši način zmanjšanja verjetnosti vloma v objekt. Če v času odsotnosti vseh uporabnikov objekta sistem med nadzorom okolice zazna pristnost potencialnih vlomilcev, aktivira različne preventivne ukrepe, kot so prižiganje luči, vklop televizorja, premikanje senčil ali drugih pametnih naprav. S tem odvrne potencialne vlomilce in poveča varnost objekta brez neposrednega posredovanja uporabnika.

### Cilji

Končni rezultat projekta je delujoča integracija za namen pasivne varnosti, ki implementira naslednje funkcionalnosti:

- uporaba lokacije uporabnikov za zaznavanje prisotnosti
- integracija s pametnimi napravami v objektu (npr. kamere, luči, zvočniki)
- grafični vmesnik za nastavitve nadzora sistema glede na kontekst situacije in podprte naprave (npr. podnevi je zvok televizije bolj opazen indikator kot svetloba luči) in ročno aktivacijo sistema oponašanja prisotnosti
- zaznava morebitno neželenih oseb preko video nadzora
- pošiljanje opozorila

### Smernice za rešitev

Z našo implementacijo bi želeli zmanjšati število vlomov in uporabnikom povečati občutek varnosti. Strmimo k temu, da bo sistem enostaven za uporabo in zanesljiv pri delovanju.

Prav tako rešitev ne sme porabljati prekomerne količine energije.

### Končni uporabniki

Končni uporabniki so uporabniki ekosistema Home Assistant, torej posamezniki, družine ali podjetja, ki želijo izboljšati preventivno varnost objekta, pri čemer ne želijo prekomerno porabljati energije ali se zanašati na druge akterje. Večina uporabnikov Home Assistant se že spozna na delovanje avtomacij na podlagi uporabnikove lokacije. V okviru dokumentacije jim moramo zagotoviti enostavna navodila za vzpostavitev vseh potrebnih komponent za predvideno delovanje sistema.

# 2 Potrebe naročnika

## 2.1 Opis naročnika, deležnikov in želene izkušnje

### Primarni naročnik

Lastnik nepremičnine, opremljene z pametnimi napravami, ki želi varno in udobno okolje, tudi ko je odsoten.

### **Sekundarni deležniki**

Uporabniki objekta, sosedje, varnostne službe, zavarovalnice.

### **Želje deležnikov**

- **Lastnik** želi, da v primeru nevarnosti vloma naprave v objektu simulirajo prisotnost ljudi, s čimer se odvrne vlomilce od nadaljnjih dejanj, kar prepreči materialno in drugo škodo.
- **Uporabniki objekta** želijo, da je objekt ob njihovi vrnitvi varen in udoben.
- **Varnostne službe ter zavarovalnice** želijo zmanjšati tveganje vlomov in poškodb.

### **Želena izkušnja**

Brezhibno delovanje sistema, ki ne zahteva veliko vzdrževanja. Po začetni nastavitvi je sposoben avtonomnega delovanja brez kakršnekoli interakcije uporabnika.

## 2.2 Uporabniške zahteve

- **Zgodba 1** - Kot lastnik objekta želim, da se pametne naprave avtomatsko vklopijo, ko sem izven cone objekta in je zaznana nezaželjena oseba, da pozidana nepremičnina daje vtis, kot da je nekdo v njej.
    
    **Test 1** - Glede na to, da sem prišel v aktivacijsko cono in da je v njeni bližini nezaželjena oseba, ko sistem zazna mojo lokacijo in nezaželjeno osebo, vklopijo v naprej nastavljene pametne naprave.
    
- **Zgodba 2** - Kot lastnik pozidane nepremičnine želim, da se ob zapustitvi aktivacijske cone sistem deaktivira, da prihranim energijo.
    
    **Test 2** - Glede na to, da sem zapustil aktivacijsko cono pozidane nepremičnine, ko sistem zazna mojo lokacijo, potem se sistem deaktivira.
    
- **Zgodba 3** - Kot lastnik pozidane nepremičnine želim, da sistem omogoča ročno nastavitev cone oddaljenosti za aktivacijo naprav, da lahko prilagodim obnašanje sistema glede na moje potrebe.
    
    **Test 3** - Glede na to, da sem v nastavitvah sistema spremenil cono oddaljenosti, ko se nahajam v nastavljeni coni, potem se sistem vklopi.
    
- **Zgodba 4** - Kot lastnik pozidane nepremičnine želim imeti možnost ročne aktivacije sistema prek mobilne aplikacije, tudi ko sistem ni aktiviran in nezaželjena oseba ni zaznana, da lahko pozidano nepremičnino kadarkoli hitro zaščitim.
    
    **Test 4** - Glede na to, da sistem ni aktiviran in ni zaznana nobena nezaželjena oseba, ko v aplikaciji pritisnem gumb za začetek simulacije prisotnosti, potem se sistem aktivira in pametne naprave prižgejo, kot da bi bila ob prižganem sistemu zaznana nezaželjena oseba.
    
- **Zgodba 5** - Kot administrator sistema želim v aplikaciji imeti nadzor nad seznamom "skupina uporabnikov", kjer lahko dodajam ali odstranjujem osebe, da zagotovim, da samo zaupanja vredne osebe vplivajo na delovanje sistema.
    
    **Test 5.1** - Glede na to, da dodam novo osebo v sekcijo "skupina uporabnikov", ko shranim spremembe, potem je oseba dodana in sistem upošteva njeno lokacijo.
    
    **Test 5.2** - Glede na to, da odstranim člana iz seznama “skupina uporabnikov”, ko shranim spremembe, potem se njegova lokacija ne upošteva več pri aktivaciji sistema.
    
- **Zgodba 6** - Kot lastnik pozidane nepremičnine želim ročno izbrati, katere pametne naprave se vklopijo ob aktiviranem sistemu in zaznavi nezaželjene osebe, da prilagodim obnašanje sistema glede na trenutne potrebe ali energetsko učinkovitost.
    
    **Test 6.1** - Glede na to, da sem v nastavitvah dodal novo napravo, ko sistem aktivira simulacijo, potem se ta pametna naprava prižge.
    
    **Test 6.2** - Glede na to, da sem v aplikacij iz seznama aktivnih naprav eno odstranil, ko sistem aktivira simulacijo, potem se odstranjena pametna naprava ne vklopi.
    
- **Zgodba 7** - Kot lastnik pozidane nepremičnine želim prejemati obvestilo v mobilni aplikaciji, če se sistem aktivira ob zaznavi nezaželjene osebe, da se zavedam morebitnih nezaželjenih oseb v bližini.
    
    **Test 7** - Glede na to, da se nezaželjena oseba približuje pozidani nepremičnini in sistem to zazna, potem prejmem obvestilo o sprožitvi sistema.

# 3 Cilji projekta

## 3.1 Opis težave in koristi sistema

### Težava naročnika

Naročniki se pogosto, ko so odsotni, soočajo s tveganjem vloma. Klasični varnostni sistemi, kot so alarmi in kamere, pogosto ne preprečijo poskusa vloma, saj vlomilci pogosto kot tarčo izberejo navzven prazne objekte.

### Koristi sistema

Razvita integracija v ekosistem Home Assistant bo v primeru zaznave prisotnosti neželenih oseb in istočasne odsotnosti uporabnikov simulirala njihovo prisotnost z upravljanjem pametnih naprav v objektu. Upravljanje pri tem prilagodi glede na kontekst situacije (npr. podnevi je zvok bolj opazen indikator kot svetloba luči, ki se v sončni svetlobi na daleč manj opazijo).

### Splošna izkušnja uporabnika

Razvit sistem bo zagotavljal:

- večji občutek varnosti uporabnikov in objekta,
- avtomatsko delovanje sistema brez potrebe po ročnem vklapljanju (čeprav to omogočamo),
- stroškovno učinkovito rešitev v primerjavi s kompleksnimi varnostnimi sistemi ali preprostimi ukrepi, kot so na primer nenehno prižgane luči.

## 3.2 Cilji projekta

### Izdelki projekta

Projekt je namenjen razvoju večih komponent sistema:

- sistem v obliki integracije za ekosistem Home Assistant, ki dostopa do lokacij uporabnikov, varnostnih kamer in drugih naprav v objektu,
- grafični uporabniški vmesnik, kjer uporabnik nadzoruje in prilagaja nastavitve sistema,
- dokumentacija in navodila za uporabo sistema.

Pravilnost razvitega sistema bomo preverjali s testnimi scenariji, v katerih preverimo zanesljivost sistema - zaznavanja gibanje in aktivacije simulacije prisotnosti.

### Merljivi in preverljivi cilji

Cilji, ki jih bomo skozi razvoj morali doseči:

- sistem se aktivira čim hitreje (v roku 1 minute) po zaznavi osebe na kameri,
- sistem uporablja lokacijske podatke uporabnikov iz sistema Home Assistant,
- s sistemom se integrira vsaj eno pametno napravo v objektu (na primer luči, TV, …)
- uporabnik je zmožen preko grafičnega uporabniškega vmesnika nadzorovati in spreminjati nastavitve sistema,
- sistem podpira dodajanje in sinhronizacijo večih uporabnikov.

# 4 Opis sistema

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/opis_sistema_1.png" alt="Opis sistema" width="1000">
</p>

Uporabniki imajo na svojem pametnem telefonu naloženo aplikacijo Home Assistant, ki v sistem sporoča njihovo lokacijo.

Glede na nastavitve in prejete lokacije se poslovna logika odloča, kdaj bo aktivirala varnostni sistem. 

Ob aktivaciji sistema kamera zažene video prenos preko protokola RTSP, ki ga sprejema vsebnik Docker z naloženim sistemom [Frigate](https://github.com/blakeblackshear/frigate) za prepoznavo ljudi. Ko ta na posnetku prepozna osebo, pošlje signal MQTT do drugega vsebnika Docker, ki poganja posrednika komunkacije MQTT. Ta ima nalogo posredništva sporočil MQTT med sistemom Frigate, sistemom HomeAssistant (v katerem deluje integracija), in napravami v objektu, katere integracija upravlja.

Ko je naša integracija je obveščena ob prejetju MQTT signala, na podlagi nastavitev varnostnega sistema določi ukrepe - preko protokola MQTT upravlja naprave v objektu. Simulacijo prisotnosti lahko uporabnik aktivira tudi ročno iz uporabniškega vmesnika.

# 5 Predlagan pristop

## 5.1 Osnutek delovanja

Sistem bo na podlagi lokacije uporabnikov določil, kdaj se mora aktivirati. Lokacija uporabnikov se bo pridobivala s pomočjo v Home Assistant že vgrajene podpore za sledenje lokacije uporabnikov preko, s strani uporabnika določenih, lokacijskih con, ki bodo sužile kot meje za določanje prisotnosti uprabnikov.

V primeru odsotnosti vseh uporabnikov objekta bo prešel v način “samodejnega varnostnega načina”. Varnostna kamera bo spremljala okolico in preko RTSP protokola prenašala posnetek v živo, do katerega bo dostopal sistem Frigate. Ta bo izvajal detekcijo oseb ter bo ob zaznavi sprožil dogodek preko MQTT.

Če bo v času do vrnitve vsaj enega uporabnika zaznano gibanje, bo sistem Frigate poslal zahtevo preko MQTT za samodejno proženje ustreznih ukrepov v obliki upravljanja naprav, povezanih z integracijo, s čimer bo ustvaril vtis prisotnosti ljudi v objektu. Prav tako bo sistem uporabnikom poslal obvestilo o prožitvi sistema.

## 5.2 Uporabljene komponente sistema, namestitev in testiranje

### Uporabljene platforme, knjižnice in orodja

Za razvoj sistema bomo uporabili različne platforme, orodja in knjižnice, ki omogočajo enostavno integracijo, obdelavo videa in avtomatizacijo procesov:

- **Home Assistant**: centralna platforma, ki bo povezovala uporabniško lokacijo, integracije z napravami in izvajala avtomatizirano simulacijo prisotnosti prebivajočih glede na MQTT dogodke
- **Zone detection** (vgrajen v Home Assistant): mehanizem za določanje prisotnosti uporabnikov na podlagi geolokacije in vnaprej določenih območij, ki bo omogočal preklapljanje sistema med aktivnim nadzorom doma (ob odsotnosti prebivajočih) in izklopljenim nadzorom (ob prisotnosti prebivajočih)
- **Frigate**: odprtokodna rešitev za analizo videoposnetkov v realnem času, ki bo omogočala zaznavanje oseb na podlagi video toka s kamer
- **Docker in Docker Compose**: okolje za enostavno namestitev in upravljanje komponent sistema v izoliranih vsebnikih
- **RTSP**: protokol za prenos video toka s kamer v sistem za obdelavo slik in zaznavanje oseb (uporablja ga Frigate)
- **MQTT**: protokol za sporočanje dogodkov, ki bo omogočal komunikacijo med Frigate in Home Assistant za sprožitev avtomatizacij

Za zagotovitev delovanja sistema so potrebne naslednje naprave in zahteve:

- naprava za izvedbo Docker Compose (npr. osebni računalnik),
- dostop do omrežja,
- kamera s podporo RTSP,
- mobilni telefon z nameščeno aplikacijo Companion App (Home Assistant),
- pametne naprave, ki so podprte v sklopu našega sistema (pametne luči in televizija).

### Namestitev

Za uspešno namestitev sistema je potrebno vzpostaviti in skonfigurirati naslednje komponente:

- **Home Assistant**: uporabi se uradna slika Docker za platformo Home Assistant. Potrebna konfiguracija vključuje definicijo poti do konfiguracijske mape, nastavitve ustreznih vrat za dostop do platforme ter druge sistemske nastavitve.
- **Frigate**: uporabi se uradna slika Docker za sistem procesiranja video vsebin Frigate. Potrebna konfiguracija vključuje določanje poti za video tok (IP kamere, ki prenaša video preko RTSP protokola), nastavitev vrat za dostop do uporabniškega vmesnika, ter omogočenje dostopa do omrežja obdelovanje video vsebin v realnem času.
- **MQTT Broker**: uporabi se ločen vsebnik Docker za posrednika MQTT, saj vsebniška različica sistema Home Assistant nima podpore posredništva MQTT sporočil. Potrebna konfiguracija vključuje nastavitev ustreznih vrat za povezovanje z drugimi napravami, določitev poti do konfiguracijskih datotek, ter omogočenje dostopa do omrežja za komunikacijo med sistemom Home Assistant, sistemom Frigate in drugimi napravami v objektu.
- **Mobilna aplikacija**: za pridobivanje uporabniške lokacije in uprabljanje z nastavitvami sistema se uporablja mobilno aplikacijo Home Assistant, ki je dostopna za mobilna operacijska sistema iOS in Android.

Za enostavno upravljanje glavnih komponent sistema (Home Assistant, Frigate, posrednik MQTT) se uporabi Docker Compose, ki omogoča enostaven zagon in povezovanje večih vsebnikov. Vse ustrezne nastavitve, vključno z vrati, potmi do konfiguracijskih datotek in parametri za posamezne komponente, so tako definirane v .yaml datoteki, kar bo omogočilo enostavnejšo konfiguracijo, tako med razvojem kot za končne uporabnike.

### Testiranje

Testiranje sistema bo potekalo v več nivojih:

- **Testi enot** za testiranje ukrepov zalednega sistema s simulacijami dogodkov
- **Integracijski testi**: preverili bomo povezljivost vseh komponent sistema: lokacija, Home Assistant, kamera, Frigate, MQTT, integracije z lučmi in televizijo. V primeru dostopa do dejanskih pametnih naprav bomo za testiranje uporabili njih, sicer bomo njihovo delovanje simulirali.
- **Stresno testiranje**: po uspešno opravljenih integracijskih testih bomo izvedli še testiranje ob povečanih obremenitvah sistema (na primer sistem Frigate testiramo pod različnimi zahtevnimi pogoji video prenosa).
- **Uporabniško testiranje**: po zaključeni implementaciji sistema bomo izvedli še teste, s katerimi bomo preverili ali sistem izpolnjuje pričakvanja in potrebe naročnika, ki so bile definirane z uporabniškimi zgodbami.

### Ocenjevanje ustreznosti testne strategije

Ustreznost testne strategije bomo ovrednostili z naslednjimi točkami:

- **pokritost kode s testi**: s testi mora biti pokrit čim večji delež kode,
- **testiranje vseh podprtih integracij**: vsaj 1 pozitiven in negativen test napisan za vsako možno integracijo s sistemom,

Sistem mora biti testiran v čimbolj realnih pogojih, da se zagotovi zanesljivo delovanje (na primer testiranje zaznavanja oseb mora delovati tudi v primeru da je v okviru kamere viden le del človeka).

# 6 Vodenje projekta

Projektno vodenje bo potekalo z inspiracijo [Scrum-ov](https://www.scrum.org/resources/what-scrum-module). Sprinti se bodo v veliki meri ujemali z roki oddaje posamezne iteracije. Na ta način bomo poskrbeli, da bo delo ekipe znotraj sprinta čim bolj usklajeno sprotnimi zahtevami projekta.

Seznam želja funkcionalnosti predlaganega sistema zajema:

- prilagajanje delovanja glede na oddaljenost lastnika Home Assistant instance,
- odzivanje na senzorje, povezane na Home Assistant instanco,
- možnost ročnega upravljanja.

**Minimalni delujoč sistem**, ki ga nameravamo razviti v naslednji iteraciji zajema naslednje funkcijonalnosti:

- Ročna aktivacija sistema preko mobilne naprave
- Integracija z eno pametno napravo

## 6.1 Usklajevanje ekipe

### Sestanki ekipe

Ekipa se bo vedo sestajala enkrat na teden proti koncu tedna.

Sestanki se bodo odvijali pred koncem vsakega sprinta za pregled dela, ki ga je še potrebno dokončati, in ob začetku vsakega sprinta za pregled možnih izboljšav glede na prejšnjem sprintu, ter pregled izzivov, ki jih bomo v danem sprintu poizkusili rešiti.

Po potrebi se lahko posamezni člani v primerih nejasnosti ali potrebe po pomoči drugih članov med seboj domenijo za dodatne termine sestankov.

### Cilj sestankov

Cilj tedenskih sestankov je usklajevanje do sedaj opravljenih nalog z ekipo. Po sestankih je jasno, kaj je bilo do sedaj narejeno, in kaj nas še čaka v tekočem sprintu.
Cilj sestankov ob koncu sprinta je, da z ekipo skupaj pogledamo izdelek ob koncu sprinta in drug drugemu izpostavimo morebitne pomankljivosti in s tem zagotovimo boljšo kvaliteto izdelka ob koncu sprinta.

Cilj sestankov ob začetku sprinta je, da imamo jasno določene cilje novega sprinta. Poleg tega je cilj tudi, da lahko vsi člani ekipe pred vsemi predstavijo svoje predloge za izboljšave dela v prihajajočih sprintih.

## 6.2 Projektni načrt

### Razdelitev dela in namestništev

| OPRAVILA | Jaka Čelik | Tara Majkič | Jaka Pelko | Klemen Remec | Miha Vintar |
| --- | --- | --- | --- | --- | --- |
| **1 Predlog projekta** | —————— | —————— | —————— | —————— | —————— |
| 1.1 Projektna ideja | 20% | 20% | 20% | 20% | 20% |
| 1.2 Zajem zahtev | 10% | 10% | 10% | 10% | 60% |
| 1.3 Tehnični načrt projekta | 5% | 5% | 35% | 35% | 20% |
| 1.4 Razdelitev vlog članov skupine | 18% | 18% | 18% | 18% | 28% |
| 1.5 Finančni in časovni načrt projekta | 25% | 25% | 0% | 40% | 10% |
| 1.6 Opredelitev tveganj | 0% | 50% | 50% | 0% | 0% |
| **2 Osnutek sistema** | —————— | —————— | —————— | —————— | —————— |
| 2.1 Vzpostavitev okolja | 0% | 0% | 50% | 0% | 50% |
| 2.2 Retrospektiva in načrt iteracije | 20% | 20% | 20% | 20% | 20% |
| 2.3 Izdelava osnovnega delujočega sistema (prototipa) | 30% | 30% | 5% | 30% | 5% |
| 2.4 Izdelava poročila o stanju | 20% | 20% | 20% | 20% | 20% |
| **3 Izvedljiv sistem** | —————— | —————— | —————— | —————— | —————— |
| 3.1 Retrospektiva in načrt iteracije | 20% | 20% | 20% | 20% | 20% |
| 3.2 Izdelava arhitekturnega načrta | 5% | 40% | 10% | 40% | 5% |
| 3.3 Izdelava poročila o stanju | 20% | 20% | 20% | 20% | 20% |
| 3.4 Zaledni sistem in njegovo testiranje | 0% | 5% | 5% | 5% | 85% |
| 3.5 Uporabniški vmesnik (frontend) in njegovo testiranje | 90% | 10% | 0% | 0% | 0% |
| 3.6 Integracija pametnih naprav in njihovo testiranje | 5% | 0% | 45% | 45% | 5% |
| **4 Končna izdaja** | —————— | —————— | —————— | —————— | —————— |
| 4.1 Retrospektiva in načrt iteracije | 20% | 20% | 20% | 20% | 20% |
| 4.2 Izdelava končnega poročila | 18% | 18% | 18% | 28% | 18% |
| 4.3 Izdelava končne dokumentacije | 30% | 30% | 0% | 40% | 0% |
| 4.4 Uporabniško testiranje | 0% | 0% | 50% | 0% | 50% |
| **Vodenje projektne ekipe** | 0% | 0% | 0% | 0% | 100% |

Namestništva so definirana v poglavju 7.

### Ganttov diagram

| OPRAVILA | sprint | začetek | konec | trajanje (delovni dnevi) | drsni čas (delovni dnevi) | odvisen od |
| --- | --- | --- | --- | --- | --- | --- |
| **1 Predlog projekta** | —————— | —————— | —————— | —————— | —————— | —————— |
| ==1.1 Projektna ideja== | 1 | 24.2 | 25.2 | 2  | 2 | / |
| 1.2 Zajem zahtev | 1 | 24.2 | 25.2 | 2 | 13 | / |
| 1.3 Tehnični načrt projekta | 1 | 26.2 | 3.3 | 4 | 9 | 1.1, 1.2 |
| ==1.4 Razdelitev vlog članov skupine== | 1 | 26.2 | 26.2 | 1 | 2 | 1.1 |
| ==1.5 Finančni in časovni načrt projekta== | 1 | 27.2 | 12.3 | 10 | 2 | 1.1, 1.4 |
| 1.6 Opredelitev tveganj | 1 | 26.2 | 4.3 | 5 | 8 | 1.1 |
| **2 Osnutek sistema** | —————— | —————— | —————— | —————— | —————— | —————— |
| 2.1 Vzpostavitev okolja | 2 | 17.3 | 18.3 | 2 | 1 | 1.5 |
| ==2.2 Retrospektiva in načrt iteracije== | 2 | 17.3 | 17.3 | 1 | 1 | 1.3, 1.5, 1.6 |
| ==2.3 Izdelava osnovnega delujočega sistema (prototipa)== | 2 | 19.3 | 1.4 | 10 | 1 | 2.1, 2.2 |
| ==2.4 Izdelava poročila o stanju== | 2 | 2.4 | 3.4 | 2 | 1 | 2.3 |
| **3 Izvedljiv sistem** | —————— | —————— | —————— | —————— | —————— | —————— |
| ==3.1 Retrospektiva in načrt iteracije== | 3 | 7.4 | 7.4 | 1 | 0 | 2.4 |
| ==3.2 Izdelava arhitekturnega načrta== | 3 | 8.4 | 10.4 | 3 | 0 | 3.1 |
| ==3.3 Izdelava poročila o stanju== | 4 | 30.4 | 30.4 | 1 | 0 | 3.5, 3.6 |
| ==3.4 Zaledni sistem in njegovo testiranje== | 3 | 11.4 | 18.4 | 6 | 0 | 3.2 |
| 3.5 Uporabniški vmesnik (frontend) in njegovo testiranje | 4 | 22.4 | 29.4 | 6 | 0 | 3.4 |
| ==3.6 Integracija pametnih naprav in njihovo testiranje== | 4 | 22.4 | 29.4 | 6 | 0 | 3.4 |
| **4 Končna izdaja** | —————— | —————— | —————— | —————— | —————— | —————— |
| ==4.1 Retrospektiva in načrt iteracije== | 5 | 5.5 | 5.5 | 1 | 4 | 3.3 |
| 4.2 Izdelava končnega poročila | 5 | 13.5 | 15.5 | 3 | 6 | 4.4 |
| ==4.3 Izdelava končne dokumentacije== | 5 | 13.5 | 19.5 | 5 | 4 | 4.4 |
| ==4.4 Uporabniško testiranje== | 5 | 6.5 | 12.5 | 5 | 4 | 4.1 |
| **Vodenje projektne ekipe** | / | 24.2 | 19.5 | 59  | / | / |

Sktivnosti na kritični poti so pobarvane z rumeno barvo.

Vseskupaj $54$ dni iz kritične poti * $5$ študentov = $270$ ŠČD oz. ŠČU dela.
Glede na razporeditev dela pride $223$ ŠČD oz. ŠČU dela na kritični poti.

Po dnevih natančno:

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/gantt_1.png" alt="Dnevni Ganntov diagram">
</p>

Po tednih natančno:

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/gantt_2.png" alt="Tedenski Ganntov diagram" width="600">
</p>

### Diagram PERT

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/pert_1.png" alt="Pertov diagram">
</p>

## 6.3 Finančni načrt

Finančni načrt projekta smo ocenili z metodo COCOMO 2, pri katerem smo predpostavili zgodnji model načrta (early design model), ki se uporablja za grobe ocene stroškov projekta pred končno definicijo arhitekture.

Zahtevnost v enoti ČM (človek meseci) se izračuna po formuli:

$$
zahtevnost=A*Obseg^B*M
$$

Parametru $A$ smo po izbranem modelu predpostavili vrednost $2.94$.

### Ocena obsega

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/cocomo_1.png" alt="COCOMO 2 - Ocena obsega" width="1000">
</p>

- Lokacija uporabnika (EI): lokacije uporabnikov, se pošilja v obliki točnih koordinat ali po območjih, ki jih določi uporabnik.
- Uporabniške nastavitve (EI): uporabnik uporablja nastavitve integracije, ki se hranijo v sistemu Home Assistant. Tam lahko določa, kateri deli sistema bodo vklopljeni in pravila samodejnega vklopa glede na stanje lokacij uporabnikov.
- Signal prepoznave ljudi (EI): Docker vsebnik, ki izvaja prepoznavo ljudi na video pronosu, je potrebno pred uporabo nastaviti.
- Uporabniške nastavitve (ILF): Home Assistant omogoča hranjenje nastavitev integracije, kjer nastavi želeno delovanje sistema glede na lokacije uporabnikov, omogočenih pametnih naprav v objektu, …
- Nastavitve Docker vsebnika (EIF): Docker vsebnik je potrebno nastaviti za pravilno delovanje (IP naslov video prenosa iz kamere, naslov pošiljanja signalov, nastavitve prepoznave ljudi, …)
- Nastavitve mobilne aplikacije (EIF): uporabnik mora mobilni aplikaciji v nastavitvah dati dovoljenje za uporabo lokacije.
- Pametni sistem za upravljanje naprav (EQ): glavna poslovna logika sistema, ki določa upravljanje pametnih naprav glede na pridobljene podatke iz Docker vsebnika in lokacijah uporabnikov.
- Upravljanje pametnih naprav (EO): glede na uporabniške nastavitve sistema ta upravlja njihovo delovanje.

Obseg in uteži so določeni z uporabo pomožnih tabel:

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/cocomo_2.png" alt="COCOMO 2 - Tabele uteži obsega" width="560">
</p>
<p align="center">
  <img src="gradivo/img/Predlog%20projekta/cocomo_3.png" alt="COCOMO 2 - Tabele uteži obsega" width="620">
</p>
<p align="center">
  <img src="gradivo/img/Predlog%20projekta/cocomo_4.png" alt="COCOMO 2 - Tabele uteži obsega" width="700">
</p>

Oceno števila vrstic na podlagi števila funkcijskih točk pa smo ocenili s pomočjo tabele https://www.qsm.com/resources/function-point-languages-table. Ker je v rezultatih raziskave razloženo, da se v primeru, da izbranega programskega jezika ni med navedenimi, sklicujemo na ocene podobnih programskih jezikov. Izbrani programski jezik Python je ocenjen iz raziskave https://www.semanticscholar.org/paper/Function-points-as-a-universal-software-metric-Jones/e90dd4a2750df4d52918a610ba9fb2b013153508 (tabela 14.3) kot najbolj podoben jezikoma C++ (povprečna ocena 50) in Java (povprečna ocena 53), zato smo za SLOC oceno Pythona vzeli kar njuno povprečje.

### Ocena parametra B

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/cocomo_5.png" alt="COCOMO 2 - Ocena parametra B" width="300">
</p>

- PREC: stopnja precedenčnosti je ocenjena kot “Nizko”, saj ekipa še nikoli ni delala na projektu, ki se ukvarja z avtomatizacijo pametnega doma.
- FLEX: stopnja fleksibilnosti zahtev je ocenjena kot “Nizko”, saj se bodo zahteve kljub vnaprejšnji analizi skozi spoznavanje z zmožnostmi okolja zagotovo spreminjale.
- RESL: stopnja pripravljenosti na tveganja je ocenjena kot “Nominalno”, saj se kljub analizi tveganj zavedamo možnosti nepričakovanih tveganj zaradi pomanjkanja vpogleda v proces nadaljnega razvoja.
- TEAM: stopnja uigranosti skupine je ocenjena kot “Visoko”, saj je velik delež ekipe že sodeloval v projektih, primerljivih s tem.
- PMAT: zrelostni nivo razvojnega procesa po modelu CMM je bil ocenjen s analizo CMM:

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/cocomo_6.png" alt="COCOMO 2 - CMM" width="350">
</p>

Vrednosti PMAT so v razponu od 0-100%, kjer 0% pomeni, da aktivnosti skoraj nikoli ne izvajamo oz. za naš projekt ni smiseln, 100% pa pomeni, da aktivnost izvajamo neprenehoma.

Razponi uteži za vrednosti ostalih parametrov so podane v tabeli:

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/cocomo_7.png" alt="COCOMO 2 - Ocena Tabela uteži B" width="800">
</p>

### Ocena parametra M

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/cocomo_8.png" alt="COCOMO 2 - Ocena parametra M" width="350">
</p>

- PERS: stopnja usposobljenosti članov razvojne skupine je ocenjena kot “Visoka”, saj je ekipa sestavljena iz članov z relativno veliko predhodnimi izkušnjami na večini panog razvoja programske opreme.
- PREX: izkušnje članov z uporabljeno tehnologijo je ocenjena kot “Nizka”, saj se kljub mnogim izkušnjah članov na različnih področjih razvoja programske opreme nihče ni srečal s to specifično panogo razvoja programske opreme.
- RCPX: ocena kompleksnosti projekta je ocenjena kot “Nominalna”, saj je sistem sestavljen tako iz enostavno nastavljivih kot tudi bolj kompleksnih komponent.
- RUSE: potreba po izdelavi ponovno uporabnih komponent je ocenjena kot “Zelo nizka”, saj bo razvit sistem uporabljen le v specifičnem scenariju.
- PDIF: spremenljivost platforme in omejitve časovne in prostorske učinkovitosti aplikacije so ocenjene kot “Visoka”, saj se platforma še vedno razvija, poleg tega uporabljamo zunanje razvit sistem prepoznave ljudi v video posnetkih, ki se lahko (vsaj v teoriji) poljubno spremeni.
- SCED: krčenje oziroma raztezanje predvidene porabe časa glede na oceno, pridobljeno v zgodnejših fazah metode COCOMO II smo ocenili z vrednostjo $1.0$.
- FCIL: razpoložljivost razvojnih orodij in komunikacijskih sredstev je ocenjena kot “Izjemno visoka”, saj so vsa potrebna razvojna orodja prosto dostopna, učinkovita komunikacija pa ne poteka le preko elektronskih kanalov (Teams, Discord, …) temveč tudi v živo.

Razponi uteži na podlagi vrednosti so določeni v določeni pomožni tabeli:

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/cocomo_9.png" alt="COCOMO 2 - Tabela uteži M" width="800">
</p>

### Izračun zahtevnosti

<p align="center">
  <img src="gradivo/img/Predlog%20projekta/cocomo_10.png" alt="COCOMO 2 - Ocena zahtevnsti" width="250">
</p>

Skupna zahtevnost projekta znaša dobrih 280 študentskih človek-dni oz. študentskih človek-ur, saj predvidevamo 1 uro dela na dan. Urno postavko smo določili kot 20€ na uro, zaradi česar celoten strošek plač v času razvoja ocenjujemo na dobrih 5600€.

Ocena neposrednih stroškov:

- plače: dobrih 5600€ (izračun iz COCOMO 2)
- računalniški sistemi: 0€ (vsi člani ekipe imamo lastne računalnike)
- pametne naprave za testiranje integracij: 0€ (kamere v telefonih/računalnikih, ostalo testirano z navideznimi napravami oz. napravami, ki jih člani ekipe že imajo doma)

Ocena posrednih stroškov:

- kavica za asistenta: 0.6€ za vsak sestanek

# 7 Ekipa

## **7.1 Predznanje**

### Klemen Remec

Znanje: okolje .NET, razvoj Android aplikacij, upravljanje podatkovnih baz.

Izkušnje: 3 leta študentskega dela (full-stack), Android aplikacija, drugi osebni projekti in hekatoni

Notranja motivacija: spoznavanje novih ekosistemov razvoja programske opreme

### **Tara Majkič**

Znanje: osnove frontend in backend razvoja spletnih aplikacij, razni programski jeziki (Java, C, C#, Golang, itd).

Izkušnje: razvita spletna aplikacija in 3d video igra.

Notranja motivacija: želja po pridobitvi praktične izkušnje pri razvoju programske opreme od načrtovanja do implementacije.

### Miha Vintar

Znanje: osnove frontend razvoja, napredno znanje backend razvoja spletnih aplikacij, napredno znanje v programskih jezikih Java in Go.

Izkušnje: študentsko delo pri DevRev, narejen portfolio.

Notranja motivacija: Home Assistant sicer ni bil eden izmed mojih privilegijev ampak obožujem izziv.

### Jaka Pelko

Znanje: razvoj spletnih aplikacij (frontend, backend), delo s podatkovnimi bazami, umetna inteligenca

Izkušnje: študentsko delo pri Aviat Networks (full-stack), študentsko delo pri NT Systems (embedded), lastni projekti

Notranja motivacija: želja po uporabi in nadgradnji obstoječega znanja na odprtokodnem projektu, ki ga do sedaj nisem poznal; pridobivanje izkušenj na področju avtomatizacije pametnega doma

### Jaka Čelik

Znanje: razvoj spletnih in mobilnih aplikacij (React, React Native, Swift) ter 3D video iger (C#, C++).

Izkušnje:  lastni projekti (mobilne aplikacije), študijske naloge (spletna aplikacija).

Notranja motivacija: Zanimanje za avtomatizacijo doma in želja po znanju integracije takega sistema.

## **7.2 Vloge**

**Vsi člani sodelujejo pri**:

- razvoju projektne ideje
- razdelitvi vlog dela
- retrospektivah in načrtih iteracij
- izdelavah poročil o stanju

### Miha Vintar

**Projektni vodja, scrum master in vodja zalednega sistema**:

- vodenje projekta (nadomešča Klemen Remec)
- zajem zahtev (nadomešča Klemen Remec)
- vzpostavitev okolja (nadomešča Jaka Pelko)
- zaledni sistemi in njegovo testiranje (nadomeščata Jaka Pelko in Tara Majkič)
- uporabniško testiranje (nadomešča Jaka Pelko)

### Klemen Remec

**Vodja dokumentacije in načrtovanja**:

- izdelava finančnega načrta (nadomešča Miha Vintar)
- izdelava prototipa (nadomeščata Jaka Čelik in Tara Majkič)
- integracija pametnih naprav in njihovo testiranje (nadomešča Jaka Pelko)
- izdelava arhitekturnega načrta (nadomešča Tara Majkič)
- izdelava končne dokumentacije (nadomeščata Jaka Čelik in Tara Majkič)

### Tara Majkič

**Sistemski analitik**:

- časovni načrt projekta (nadomešča Jaka Čelik)
- opredelitev tveganj (nadomešča Jaka Pelko)
- izdelava prototipa (nadomeščata Jaka Čelik in Klemen Remec)
- izdelava arhitekturnega načrta (nadomešča Klemen Remec)
- izdelava končne dokumentacije (nadomeščata Jaka Čelik in Klemen Remec)

### Jaka Pelko

**Vodja ekipe za integracijo z zunanjimi napravami**:

- opredelitev tveganj (nadomešča Tara Majkič)
- vzpostavitev okolja (nadomešča Miha Vintar)
- integracija pametnih naprav in njihovo testiranje (nadomešča Klemen Remec)
- uporabniško testiranje (nadomešča Miha Vintar)

### Jaka Čelik

**Vodja ekipe za uporabniški vmesnik**:

- časovni načrt projekta (nadomešča Tara Majkič)
- izdelava prototipa (nadomeščata Tara Majkič in Klemen Remec)
- uporabniški vmesnik (nadomeščata Tara Majkič in Miha Vintar)
- izdelava dokumentacije sistema (nadomeščata Jaka Pelko in Klemen Remec)

# 8 Omejitve in tveganja

## 8.1 Analiza tveganj

| Tveganje | Vpliv na | Vrsta tveganja | Opis | Verjetnost | Učinek |
| --- | --- | --- | --- | --- | --- |
| **T1** - Slab projektni plan | projekt, izdelek | zahteve | Specifikacije aplikacije so nejasne, ni jasnih ciljev projekta ali/in razvijalci nimajo dovolj informacij za izvedbo. | nizka | zmeren |
| **T2** - Izguba osebja | projekt | ljudje | Član skupine zapusti skupino ali je dolgotrajno odsoten in ne more nadaljevati projekta. | zelo nizka | dopusten |
| **T3** - Podcenjena velikost projekta | projekt, izdelek | ljudje, ocene | Nekateri člani skupine se projekta na začetku lotevajo preveč sproščeno in ne vložijo dovolj truda, kar lahko privede do časovne stiske proti koncu in oteži pravočasno dokončanje. | nizka | zmeren |
| **T4** - Okvara strojne opreme | projekt | orodja | Kritična napaka računalnika enega izmed članov razvojne skupine; član ne more razvijati. | zelo nizka | dopusten |
| **T5** - Neenotnost razvojne ekipe | projekt, izdelek | ljudje, organizacija | V skupini prihaja do nesoglasij glede pristopa k delu, kar povzroča napetosti med člani in ogroža enotnost ekipe. | zmerna | zmeren |
| **T6** - Pomanjkanje znanja | izdelek | ljudje, tehnologija | Skupina si je izbrala novo tehnologijo, ki jo nihče ne obvlada; izkaže se za prevelik izziv za kratko časovno obdobje. | zmerna | zmeren |
| **T7** - Zamuda pri specifikacijah | projekt, izdelek | ljudje, zahteve | Člani razvojne skupine ne pripisujejo dovolj velike teže pripravi projektnega načrta. | nizka | zmeren |
| **T8** - Konkurenčni izdelek | posel, projekt | organizacija, zahteve | Trenutno je v razvoju več konkurenčnih izdelkov; to zmanjša možnosti uspeha izdelka. | nizka | zanemarljiv |
| **T9** - Spremembe zahtev naročnika med razvojem | projekt | zahteve | Naročnik med potekom projekta večkrat spremeni svoje zahteve, kar vpliva na hitrost dostave izdelka in motivacijo ekipe. | zelo nizka | zmeren |
| **T10** - Neustrezna arhitektura | izdelek | tehnologija | Arhitektura sistema je slabo zasnovana, kar lahko vodi težav pri skalabilnosti, vzdrževanju in delovanju izdelka. | zmerna | usoden |
| **T11** - Težave s kakovostjo kode | izdelek | tehnologija | Koda je slabo strukturirana oziroma nepregledna, kar lahko vodi do težav pri vzdrževanju in počasnejšega razvoja. | zelo nizka | dopusten |
| **T12** - Težave z združljivostjo | projekt, izdelek | tehnologija, orodja | Aplikacija ne deluje oziroma se sesuje na določenih napravah ali operacijskih sistemih; omejene funkcionalnosti in slaba uporabniška izkušnja. | nizka | usoden |
| **T13** - Pomanjkanje testiranja | izdelek | tehnologija | Programska oprema ni dovolj preizkušena, zato vsebuje napake, ki resno vplivajo na stabilnost in delovanje. | zelo nizka | usoden |
| **T14** - Varnostna tveganja | posel | tehnologija | Programska oprema ni ustrezno zaščitena pred zunanjimi napadi in zlorabo podatkov. | zelo visoka | usoden |
| **T15** - Slaba komunikacija v ekipi | projekt | ljudje, organizacija | Napačno razumevanje, podvajanje dela ali neusklajenost pri implementaciji funkcionalnosti; člani ekipe se ne sestajajo dovolj pogosto. | zelo nizka | dopusten |
| **T16** - Neustrezno vodenje projekta | projekt | organizacija | Projektni vodja ni sposoben učinkovito usmerjati ekipe, jih motivirati, spremljati napredka in obvladovati tveganj. | zelo nizka | zmeren |
| **T17** - Slabo dokumentiran projekt | projekt | organizacija | Dokumentacija projekta je pomanjkljiva ali nejasna, to lahko otežuje razvoj, vzdrževanje in odpravljanje napak. | nizka | dopusten |
| **T18** - Neprimerna izbira tehnologije | projekt, izdelek | tehnologija | Izbrana je zastarela ali neprimerna tehnologija, kar lahko vpliva na učinkovitost, skalabilnost, kompleksnost sistema, kakor tudi na razvojni proces. | zmerna | usoden |
| **T19** - Nejasne zahteve naročnika | projekt, izdelek | zahteve | Naročnik ne poda jasnih zahtev projekta oziroma končne rešitve, to lahko vodi do napačne interpretacije lastnosti sistema s strani razvijalcev in posledično nezadovoljstvo naročnka s končno implementacijo. | visoka | usoden |
| **T20** - Težave z uporabo aplikacije | izdelek | tehnologija | Neustrezna namestitev sistema s strani končnega uporabika lahko vodi do počasnega delovanja ali celo nedelovanja sistema. | nizka | resen |
| **T21** - Pravne težave | posel | organizacija | Razvit sistem ne upošteva ustrezne zakonodaje, kar lahko povzroči pravne posledice za organizacijo. | visoka | resen |
| **T22** - Težave s skalabilnostjo rešitve | izdelek | tehnologija | Rešitev ni oziroma je slabo skalabilna, kar lahko vodi do suboptimalnega delovanja. | zmerna | zmeren |
| **T23** - Neupoštevanje zahtev naročnika | izdelek | zahteve | Dejanska implementacija sistema in pričakovanja naročnika se ne skladajo. | nizka | resen |
| **T24** - Nejasna odgovornost v ekipi | projekt | ljudje, organizacija | Slabo določene odgovornosti in dodelitve nalog lahko povzročijo nepotrebno podvajanje dela ali zanemarjanje določenih nalog.  | zelo nizka | zmeren |
| **T25** - Težave pri integraciji podsistemov | projekt | tehnologija, orodja | Prisotne so težave pri povezovanju različnih komponent sistema. | visoka | dopusten |

Za določitev stopnje izpostavljenosti tveganjem potrebujemo matriko izpostavljenosti tveganj. V našem predlogu projekta bomo uporabili kar matriko, ki je bila predstavljena na vajah. Spodnja tabela prikazuje tveganja, razvrščena po padajoči stopnji izpostavljenosti. Izbrali smo dvanajst tveganj, ki jih bomo podrobneje analizirali in zanje opisali strategije obravnavanja.

| Tveganje | Verjetnost | Učinek | Izpostavljenost | Opis strategije | Vrsta strategije |
| --- | --- | --- | --- | --- | --- |
| **T14** - Varnostna tveganja | zelo visoka | usoden | visoka | Uvedejo se redni varnostni pregledi in testiranja ranljivosti. Prav tako se morajo člani skupine pred razvojem ustrezno izobraziti na področju varnosti in zaščite podatkov. | minimize |
| **T19** - Nejasne zahteve naročnika | visoka | usoden | visoka | Pred začetkom projekta se izvede natančna analiza zahtev naročnika z jasnim zapisom vsega, kar je potrebno za projekt.  | avoid |
| **T10** - Neustrezna arhitektura | zmerna | usoden | srednje visoka | Pred začetkom razvoja rešitve se pripravi osnovni načrt arhitekture, da zagotovimo, da so vsi deli sistema kompatibilni. Arhitektura mora biti čim bolj modularna, saj se kasneje lahko določene komponente zamenjajo oziroma dodajo. | avoid |
| **T12** - Težave z združljivostjo | nizka | usoden | srednje visoka | Pred začetkom razvoja se analizira združljivost ključnih komponent in ustrezno prilagodi načrt. Med razvojem se sistem redno testira na različnih napravah, da se hitro zazna in odpravi morebitne težave. Uporablja se dobro podprte tehnologije. | minimize |
| **T21** - Pravne težave | visoka | resen | srednje visoka | Ne bomo se pripravljali na ta scenarij, saj nimamo izkušenj na pravnem področju in gre za šolski projekt z omejenim časom razvoja. | accept |
| **T18** - Neprimerna izbira tehnologije | zmerna | usoden | srednje visoka | V fazi izbire uporabljenih tehnologij se izbere ustrezne in nezastarele tehnologije, ki imajo aktivno podporo skupnosti.   | avoid |
| **T5** - Neenotnost razvojne ekipe | zmerna | zmeren | srednja | Vodja skupine identificira želje posameznikov in razporedi delo v skladu z njihovimi željami. Uvede se dnevne sestanke ob kavi za povezovanje članov skupine. Morebitne konflikte se čimprej razreši. | avoid |
| **T6** - Pomanjkanje znanja | zmerna | zmeren | srednja | Pred začetkom razvoja se vsak član posveti pridobivanju osnovnega razumevanja platform in orodij, s katerimi se bo delalo. Poleg tega si vsak član pridobi poglobljeno znanje na področju svojih nalog. | minimize |
| **T13** - Pomanjkanje testiranja | zelo nizka | usoden | srednja | Za zagotavljanje zanesljivosti sistema se pred uvedbo izvede temeljito testiranje. Preveri se delovanje avtomatizacij, odzivnost naprav in stabilnost integracij. V primeru odkritih napak oziroma nepravilnosti, se osredotoči na njihovo odpravo. | avoid |
| **T20** - Težave z uporabo aplikacije | nizka | resen | srednja | Pripravi se natančna in ustreza dokumentacija za namestitev, konfiguracijo in uporabo sistema ter možnost zbiranja povratnih informacij uporabnikov. | minimize |
| **T22** - Težave s skalabilnostjo rešitve | zmerna | zmeren | srednja | Rešitev se zasnuje z mislijo na prihodnjo rast in razširitev, pri čemer se uporabljajo modularne in standardizirane tehnologije. Pred uvedbo sistema se izvajajo obremenitveni testi, ki pomagajo optimizirati delovanje in usmeriti nadaljnji razvoj. | minimize |
| **T23** - Neupoštevanje zahtev naročnika | nizka | resen | srednja | Organizirajo se redni sestanki z naročnikom, kjer se preverja ali projekt ustreza njihovim pričakovanjem. V primeru neskladja se prilagodi načrt projekta. | avoid |

### OWASP tehnična tveganja

| Tveganje | Vpliv na | Vrsta tveganja | Opis | Verjetnost | Učinek | Izpostavljenost | Opis strategije | Vrsta strategije |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Kriptografske napake](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/) | posel | tehnologija | Uporabljeni so zastareli ali neustrezni šifrirni algoritmi, prenos podatkov brez ustrezne zaščite (npr. brez TLS). V našem primeru bi takšne pomanjkljivosti morebitnim napadalcem lahko omogočile prestrezanje videa nadzorne kamere. | visoka | resen | srednje visoka | Ne bomo se pripravljali na ta scenarij, saj imamo omejen čas za implementacijo sistema, osredotočili se bomo na osnovno delovanje. | accept |
| [Varnostno pomankljiv dizajn](https://owasp.org/Top10/A04_2021-Insecure_Design/) | posel | tehnologija | Sistem je neustrezno načrtovan, saj ima varnostne ranljivosti, ki morebitnim napadalcem omogočajo nepooblaščen dostop in upravljanje z njim. V našem primeru bi napadalec lahko prižigal oziroma ugašal luči, predvajal glasbo ali ponaredil RTSP video tok (npr. z nekim statičnim videom) ter tako onemogočil zaznavanje oseb v bližini. | zmerna | resen | srednje visoka | Na začetku se dobro premisli in zasnuje arhitekturo in delovanje sistema, z velikim poudarkom na varnosti. Med razvojem se uvede ustrezne algoritme za preprečevanje nepooblaščenega dostopa in se izvaja redne varnostne teste. | avoid |
| [Ranljive in zastarele komponente](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/) | projekt, izdelek | tehnologija, orodja | Pred začetkom implementacije ni bila narejena natančna analiza komponent sistema. Uporablja se nevarne ali zastarele komponente (npr. knjižnice, integracije), ki zaradi pomanjkanja popravkov in posodobitev ustvarijo tveganje za naš sistem. | nizka | zmeren | srednje nizka | V fazi načrtovanja sistema se izvede dobro raziskavo predvidenih komponent, kjer se ovrednoti njihovo ustreznost glede varnosti. Med razvojem projekta se redno spremlja nove različice komponent in sistem ustrezno nadgradi z namenom preprečevanja varnostnih tveganj. | minimize |

## 8.2 Omejitve

Pri načrtovanju varnostnega sistema je pomembno upoštevati različne omejitve, ki vplivajo na njegovo delovanje in sprejemljivost v družbi:

- **Pravne in politične omejitve:** Sistem mora biti skladen z zakonodajo, kot je GDPR. Za uporabo sistema se mora uporabnik strinjati s sledenjem njegove lokacije in obdelavo video posnetkov iz varnostnih kamer.
- **Družbene omejitve:** Pogosto proženje varnostnega sistema lahko povzroči nelagodje sosedom, saj simulacija prisotnosti vsebuje zvočne ali svetlobne efekte.
- **Etične omejitve:** Sistem ne sme omogočati nadzora brez privolitve oseb, katerih podatki se obdelujejo. Prav tako mora preprečevati morebitno zlorabo, kot je nepooblaščeno snemanje ali sledenje.

Kar zadeva dostop do podatkov, storitev in virov, ne pričakujemo večjih težav. Uporabniška lokacija in video prenos bodo dostopni preko ustreznih integracij. Vse uporabljene storitve in orodja so odprtokodna, kar omogoča enostaven dostop brez večjih omejitev in zagotavlja fleksibilnost pri implementaciji sistema.