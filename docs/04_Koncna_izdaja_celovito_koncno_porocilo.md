# :blue_square: Končna izdaja (celovito končno poročilo)

| [:arrow_backward:](03_Izvedljiv_sistem_2_porocilo_o_stanju.md) Prejšnji dokument |                       Trenutni dokument                       | Naslednji dokument |
| :------------------------------------------------------------------------------- | :-----------------------------------------------------------: | -----------------: |
| :green_square: **Izvedljiv sistem**<br>(2. poročilo o stanju)                    | :blue_square: **Končna izdaja**<br>(celovito končno poročilo) |                    |


## :page_with_curl: Zagotavljanje varnosti objekta s simulacijo prisotnosti uporabnikov

## :information_desk_person: Varko - pametna integracija za sistem Home Assistant

Skupina 20:
- Jaka Čelik
- Tara Majkič
- Jaka Pelko
- Klemen Remec
- Miha Vintar

# 1 Uvod

Home Assistant kot ena vodilnih platform za avtomatizacijo pametnih domov ponuja bogat ekosistem integracij za specifične delovne naloge. Kljub široki paleti obstoječih integracij pa na trgu manjka celovita rešitev za povečevanje varnosti objekta v času odsotnosti prebivalcev, ki bi dinamično simulirala njihovo prisotnost z uporabo integriranih pametnih naprav in upoštevala kontekst situacije, kot je čas dneva in lokacija vseh uporabnikov. Namen tega projekta je bil razviti inovativno integracijo za Home Assistant, poimenovano Varko, ki naslavlja to vrzel na trgu. V nadaljevanju tega poročila bomo podrobno predstavili projektno idejo, opredelili potrebe naročnika in uporabniške zahteve, opisali cilje projekta, predstavili arhitekturo in delovanje sistema, analizirali potek vodenja projekta ter ovrednotili izzive, s katerimi smo se skozi razvojni proces spopadali, in načine reševanja le teh.

## 1.1 Projektna ideja

### Ozadje

Podatki raziskav kažejo, da več kot 70% vlomov poteka v času odsotnosti lastnikov oziroma prebivajočih. ([Vir](https://www.simplyinsurance.com/home-invasion-statistics/)) 

Na trgu obstaja mnogo rešitev za zagotavljanje varnosti objektov preko integracij z varnostnimi sistemi (npr. kamere, alarmi, ipd.), nekateri izmed njih se tudi integrirajo s sistemi za pametne domove, kot na primer Home Assistant. Zanj obstaja tudi [integracija](https://github.com/slashback100/presence_simulation), ki omogoča enostavno oponašanje uporabe naprav ko uporabnika ni v objektu, ampak to dela ves čas aktivacije, ne glede na okoliščine.

### Področje

Čas, ko v objektu ni nobenega prebivalca, predstavlja najbolj verjetni časovni okvir za vlome, saj je pogosto že na daleč vidno, da je hiša prazna. Pogosti rešitvi sta stalno puščanje prižganih naprav, kar je energijsko potratno, in/ali prošnja znancu za občasen pregled, kar ni popolnoma zanesljivo.

### Motivacija in edinstvena ponujena priložnost

Motivacija za zagon projekta je prišla iz spoznanja, da vsaka od zgoraj naštetih rešitev prinese slabosti, ki pa jih odpravimo z implementacijo namenske pametne integracije, ki presega tradicionalne metode. Ta temelji na združevanju lokacijskih podatkov uporabnikov in obstoječega Home Assistant ekosistema, ki omogoča integracijo s pametnimi napravami v objektu. V primeru zaznave potencialnih vlomilcev (v času odsotnosti vseh uporabnikov objekta) bi le-ta vklopila integrirane pametne naprave, kar bi signaliziralo prisotnost ljudi v objektu. Tak sistem je ne le bolj zanesljiv, temveč tudi stroškovno (energetsko) učinkovitejši.

Integracije, ki upošteva potrebo po dinamičnem odzivu (npr. podnevi je zvok televizije bolj opazen indikator prisotnosti ljudi kot svetloba prižganih luči) in samodejno upošteva lokacije uporabnikov objekta za avtonomno upravljanje varnostnega mehanizma, na trgu še ni, zaradi česar smo zaznali priložnost za vstop na trg integracij z novo, unikatno rešitvijo.

### Cilji

Končni rezultat projekta je delujoča integracija za namen pasivne varnosti preko zmanjšanja števila vlomov in povečanje občutka varnosti uporabnikov objekta.

Sistem mora na podlagi danega cilja zagotavljati naslednje funkcionalnosti:

- uporaba lokacije uporabnikov za zaznavanje njihove prisotnosti v okolici objekta
- integracija s pametnimi napravami v objektu (npr. kamere, luči, zvočniki)
- zaznava morebitno neželenih oseb v okolici objekta preko video nadzora
- grafični vmesnik za nastavitve nadzora sistema glede na kontekst situacije int integrirane naprave, ter ročno aktivacijo sistema oponašanja prisotnosti
- pošiljanje opozorila ob aktivaciji in deaktivaciji sistema

Strmimo k temu, da bo sistem enostaven za uporabo in zanesljiv pri delovanju, prav tako pa rešitev ne sme porabljati prekomerne količine energije.

V okviru dokumentacije moramo uporabnikom zagotoviti enostavna navodila za vzpostavitev vseh potrebnih komponent, ki omogočajo predvideno delovanje sistema.

### Končni uporabniki

Končni uporabniki so uporabniki ekosistema Home Assistant - tako posamezniki kot tudi podjetja, ki želijo izboljšati preventivno varnost objekta, pri čemer ne želijo prekomerno porabljati energije ali se zanašati na druge manj zanesljive akterje. Večina uporabnikov sistema Home Assistant se že spozna na delovanje avtomacij na podlagi uporabnikove lokacije.

## 1.2 Izzivi

Ekipa se je z ekosistemom Home Asistant srečala prvič, kar je vplivalo na daljša obdobja raziskovanja in načrtovanja strategij implementacij. Skozi iteracije projekta smo se vse bolj spoznali z zmogljivostmi in priporočljivimi praksami implementacije integracije za dani sistem, kar je vplivalo na vse hitrejše razvojne cikle posameznih funkcionalnosti, in večje zanesljivost razvite rešitve.

Začetne težave pri vzpostavitvi okolja, kot so omejitve glede uporabe okoljskih spremenljivk v sistemu Frigate, in testirnega okolja, kot je povezava spletne kamere preko RTSP protokola na implementiran sistem, smo prav tako zaradi tega hitro odpravili.

V začetnih iteracijah še nismo imeli vzpostavljenega učinkovitega procesa kontinuirane integracije (CI), ki bi olajšala iterativen razvoj in testiranje. Zato smo kar se da hitro razvili skripto, ki vzpostavljanje Docker vsebnikov avtomatizira, in tako razbremeni razvijalce.

Med drugim se je ekipa neprestano spopadala z izzivi dobavnih rokov pametnih naprav, na katerih bi razvito integracijo lahko testirali. Tako smo npr. morali izvedbo integracije zvočnika prestaviti med delovne naloge kasnejše iteracije, vendar v tej nadaljnjih težav zaradi tega ni bilo.

Nenazadnje so se skozi vse iteracije pojavljale nepričakovane zamude (npr. pri implementaciji prototipa, implementaciji končnega produkta, itd.), zaradi česar smo istočasno zaključevali razvojni proces in že izdelovali poročila. Ta smo morali zaradi sprotnih sprememb implementacije naknadno popravljati. Izziv smo reševali z rednimi sestanki ob začetkih in koncih iteracij, kjer smo čim prej opredelili natančen plan naslednje iteracije, v katerem smo upoštevali vse na novo zaznane vire zamud in nejasnosti.

## 1.3 Poudarki

Sistem deluje na principu zaznavanja morebitne prisotnosti neželenih oseb med odsotnostjo vseh uporabnikov objekta, saj v tem primeru sistem sproži preventivne ukrepe - aktivacija pametnih naprav v objektu, ki oddajajo svetlobo in/ali zvok, s čimer se ustvari vtis, da je v objektu nekdo prisoten. Ta dinamičen odziv, prilagojen glede na čas dneva in razpoložljive naprave, omogoča prilagodljivost in zanesljivost brez nepotrebne porabe energije.

Grafični vmesnik nudi uporabnikom enostavno nastavitev sistema in prilagajanje ukrepov glede na kontekst situacije. Končni uporabniki – posamezniki ali podjetja, ki že uporabljajo Home Assistant – bodo imeli tako na voljo stroškovno učinkovito in energetsko varčno rešitev, ki bistveno povečuje občutek varnosti in zmanjšuje možnost vloma.

## 1.4 Spremembe

Večjih sprememb predloga projekta med celotnim procesom razvoja ni bilo, kar kaže na visoko prilagodljivost članov ekipe ter dobro začetno načrtovanje postopkov izvedbe projekta, in nenazadnje vodenja.

# 2 Potrebe naročnika

## 2.1 Opis naročnika, deležnikov in želene izkušnje

### Primarni naročnik

Lastnik objekta (nepremičnine), opremljene z pametnimi napravami, ki želi varno in udobno okolje, tudi med njegovo odsotnostjo (in odsotnostjo drugih uporabnikov).

### Sekundarni deležniki

Uporabniki objekta, sosedje, varnostne službe, zavarovalnice.

### Želje deležnikov

- **Lastnik objekta** želi, da v primeru nevarnosti vloma naprave v objektu simulirajo prisotnost ljudi, s čimer se odvrne vlomilce od nadaljnjih dejanj, kar prepreči materialno in drugo škodo.
- **Uporabniki objekta** želijo, da je objekt ob njihovi vrnitvi varen in udoben.
- **Varnostne službe ter zavarovalnice** želijo zmanjšati tveganje vlomov in poškodb.

### Želena izkušnja

Brezhibno delovanje sistema, ki ne zahteva veliko vzdrževanja. Po začetni nastavitvi je sposoben avtonomnega delovanja brez kakršnekoli interakcije uporabnika.

## 2.2 Uporabniške zahteve

Spodaj so opisane zaznane uporabniške zahteve v obliki uporabniških zgodb. Vsaka je najprej definirana, nato pa so našteti in opisani še sprejemni testi.

1. **Avtomatska aktivacija sistema** - Kot administrator sistema želim, da se pametne naprave avtomatsko vklopijo, ko so izven lokacijske cone objekta vsi uporabniki in je zaznana nezaželjena oseba, da objekt daje vtis prisotnosti uporabnikov.
    
    **Test 1.1** - Glede na to, da so vsi uporabniki izven lokacijske cone, in da je v bližini objekta zaznana nezaželjena oseba, se vklopijo v naprej nastavljene pametne naprave.

    **Test 1.2** - Glede na to, da so vsi uporabniki izven lokacijske cone, v bližini objekta pa ni zaznane nezaželjena oseba, se sistem ne aktivira, saj za to ni razloga.

    **Test 1.3** - Glede na to, da se v lokacijski coni nahaja vsaj en uporabnik, se sistem ob zaznavi nezaželjena oseba ne aktivira, saj je sistem mogoče zaznal uporabnika objekta.
    
2. **Avtomatska deaktivacija sistema** - Kot administrator sistema želim, da se ob prihodu kateregakoli uporabnika v lokacijsko cono sistem deaktivira, kar prepreči aktivacije sistema ob prisotnosti avtoriziranih uporabnikov in varčevanje z elektriko.
    
    **Test 2.1** - Glede na to, da je v lokacijsko cono prišel uporabnik sistem to zazna in se deaktivira.

    **Test 2.2** - Glede na to, da v lokacijski coni ni nobenega uporabnika, sistem ostane aktiviran.

3. **Ročno upravljanje sistema** - Kot administrator sistema želim, da sistem omogoča ročno aktivacijo sistema, tudi ko sistem ni aktiviran in nezaželjena oseba ni zaznana, da lahko objekt kadarkoli hitro zaščitim, ali testiram delovanje nastavitev sistema.
    
    **Test 3.1** - Glede na to, da je sistem deaktiviran in ni zaznana nobena nezaželjena oseba, imam možnost aktivacije sistema.

    **Test 3.2** - Glede na to, da je sistem aktiviran, imam možnost deaktivacije sistema, če ta že ni trenutno aktiviran.
    
4. **Nastavitev lokacijske cone** - Kot administrator sistema želim, da sistem omogoča ročno nastavitev lokacije in velikosti lokacijske cone, da lahko prilagodim obnašanje sistema svojim potrebam.
    
    **Test 4.1** - Glede na to, da sem v nastavitvah sistema spremenil lokacijsko cono, bo sistem za pravila delovanja upošteval novo-nastavljeno cono.

    **Test 4.2** - Glede na to, da sem v nastavitvah sistema želel spremeniti lokacijsko cono, a nisem v sistemu Home Assistant nobene cone definiral, bo sistem na to opozoril in onemogočil nastavljanje cone.
    
5. **Urejanje skupine uporabnikov sistema** - Kot administrator sistema želim, da sistem omogoča nadzor nad seznamom SUS, kjer lahko dodajam ali odstranjujem avtorizirane osebe - uporabnike objekta, da zagotovim, da samo zaupanja vredne osebe vplivajo na delovanje sistema.
    
    **Test 5.1** - Glede na to, da administrator doda novo osebo v SUS, sistem začne upoštevati njeno lokacijo za namen delovanja.
    
    **Test 5.2** - Glede na to, da administrator odstrani člana iz SUS, sistem preneha upoštevati njeno lokacijo za namen delovanja.

    **Test 5.3** - Glede na to, da administrator želi dodati novo osebo v SUS, ampak ta oseba še ni dodana v sistem Home Assistant, sistem ne omogoči dodajanja te osebe.
    
6. **Urejanje integriranih naprav** - Kot administrator sistema želim, da sistem omogoča izbiro pametnih naprav, ki se bodo ob aktivaciji sistema uporabile za simulacijo prisotnosti uporabnikov, kar omogoča prilagoditev obnašanja sistema glede na trenutne potrebe ali želeno energetsko učinkovitost.
    
    **Test 6.1** - Glede na to, da administrator v sistem doda novo napravo, sistem ob aktivaciji z njo upravlja za namen simulacije prisotnosti.
    
    **Test 6.2** - Glede na to, da administrator v sistem odstrani obstoječo napravo, sistem z njo ne upravlja več.
    
7. **Prejemanje obvestil o stanju sistema** - Kot uporabnik objekta želim ob aktivaciji in deaktivaciji sistema prejeti obvestilo, da se zavedam morebitnih nezaželjenih oseb v bližini oziroma njihov odhod.
    
    **Test 7.1** - Glede na to, da se nezaželjena oseba približuje objektu in sistem to zazna, potem uporabniki prejmejo obvestilo o aktivaciji sistema.

    **Test 7.2** - Glede na to, da sistem ne zazna nobene nezaželjena osebe uporabniki obvestil ne prejemajo.

    **Test 7.3** - Glede na to, da se je sistem deaktiviral, potem uporabniki prejmejo obvestilo o deaktivaciji sistema.

# 3 Cilji projekta

Čas, ko v objektu ni nobenega prebivalca, predstavlja najbolj verjetni časovni okvir za vlome, saj je pogosto že na daleč vidno, da je hiša prazna. Pogosti rešitvi sta stalno puščanje prižganih naprav, kar je energijsko potratno, in/ali prošnja znancu za občasen pregled okolice, kar ni popolnoma zanesljivo.

Integracija poskuša doseči boljši način zmanjšanja verjetnosti vloma v objekt. Če v času odsotnosti vseh uporabnikov objekta sistem med nadzorom okolice zazna pristnost potencialnih vlomilcev, aktivira različne preventivne ukrepe, kot so prižiganje luči, vklop televizorja, premikanje senčil ali drugih pametnih naprav. S tem odvrne potencialne vlomilce in poveča varnost objekta brez neposrednega posredovanja uporabnika.

Ustreznost ideje smo potrdili z raziskavo pomanjkanja obstoja ustreznejše rešitve za dani problem. Pravilnost same izvedbe bomo potrdili s testiranjem uporabe sistema v realnih razmerah, in zbirali podatke o pravilnosti delovanja sistema.

## 3.1 Funkcionalne zahteve

### 3.1.1 Specifikacija zahtev

Spodaj so naštete funkcionalne zahteve, razdeljene po prioriteti implementacije.

**Must have:**

1. Dodajanje pametne naprave
2. Aktivacija pametne naprave
3. Deaktivacija pametne naprave
4. Odstranitev pametne naprave
5. Avtomatski prehod sistema iz stanja mirovanja v stanje pripravljenosti
6. Obdelava video pretoka in detekcija oseb
7. Avtomatski prehod sistema v aktivno stanje iz stanja pripravljenosti
8. Izvajanje simulacije prisotnosti
9. Avtomatski prehod sistema iz aktivnega stanja v stanje pripravljenosti
10. Avtomatski prehod sistema iz stanja pripravljenosti v stanje mirovanja

**Should have:**

1. Določitev cone
2. Upravljanje s skupino uporabnikov
3. Pošiljanje obvestil
4. Ročni preklop sistema v aktivno stanje
5. Ročni preklop sistema v stanje mirovanja

**Could have:**

1. Aktivacija shranjevanja slik
2. Deaktivacija shranjevanja slik

**Would have:**

1. Upravljanje z nastavitvami shranjevanja videoposnetkov

### 3.1.2 Specifikacija vmesnikov

#### Zaslonske maske

[//]: # (TODO: POSODOBI ZASLOVNSKE MASKE)

Uporabniški vmesnik je izdelan kot ločena plošča v sistemu Home Assistant, kjer uporabnik dostopa do nastavitev integracije. Do nje lahko dostopa uporabnik sistema Home Assistant preko glavnega menija na levi strani kontrolne plošče.

Na spodnjih slikah je prikazana kontrolna plošča integracije, ki omogoča:
- upravljanje z integriranimi napravami - dodajanje in odvzemanje naprav iz uporabe
- upravljanje z lokacijskimi conami - določitev lokacijske cone za uporabo pri delovanju sistema
- upravljanje s skupino uporabnikov - dodajanje in odvzemanje uporabnikov sistema Home Assistant iz uporabe pri delovanju sistema
- upravljanje s stanji sistema - ročna nastavitev stanja sistema

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/ui_general.png" alt="Splošen izgled UI">
</p>

Spodnja slika predstavlja pojavno okno z menijem, ki se pojavi ob kliku na opcijo "Add device". Vsebuje vnosna polja, ki jih je potrebno pred potrditvijo izpolniti.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/ui_detail.png" alt="Izgled UI menija">
</p>

Do določenih nastavitev lahko dostopa le administrator sitema Home Assistant, do ostalih pa tudi drugi avtenticirani uporabniki. Ob poskusu nedovoljenega dostopa do funkcionalnosti se uporabniku prikaže obvestilo o premajhnih pooblastilih.

#### Vmesniki do zunanjih sistemov

Spodaj so opisani načini dostopov do osrednjega sistema - način komunikacije uporabniškega vmesnika, kamere in pametnih naprav.

##### Uporabniški vmesnik

- **Opis:** Grafični uporabniški vmesnik, preko katerega lahko uporabnik sproža akcije, ki so del naše integracije. Uporabnik komunicira z integracijo prek Home Assistant vmesnika, ki interno uporablja HTTP/HTTPS in WebSocket povezave za izvajanje storitev.
- **Vrsta povezave:** HTTP/HTTPS, WebSockets (komunikacija preko vmesnika Home Assistant)
- **Format vhoda:** Interakcija se sproži prek klica funkcije `callService` , ki pošlje ukaz z ustreznimi parametri ustrezni storitvi.
  ```jsx
  function callService(domain: string, serviceName: string, data: object) => object;
  ```
- **Format izhoda:** Klic storitve vrne objekt s kontekstom klica, ki vsebuje informacije o izvedenem dejanju.
- **Primer vhoda:**
  ```jsx
  this.hass.callService(
    "varko",
    "add_light",
    {
      device_type: "light",
      device_name: "shelly-light",
      device_id: "fcf5c4b2f131",
    },
  );
  ```
- **Primer izhoda:**
```jsx
{
  "context": {
    "id": "01JR665VF8T30RCFQPJTBNBC2Y",
    "parent_id": null,
    "user_id": "104e211446f54b83adeadeb2dd85bf0d"
  }
}
```

##### Kamere s podporo RTSP

- **Opis:** Vmesnik omogoča povezavo IP kamere s sistemom Frigate prek RTSP. Kamere pošiljajo neprekinjen video tok, ki ga Frigate obdeluje za zaznavanje oseb.
- **Vrsta povezave:** RTSP
- **Format vhoda:** Sistem Frigate potrebuje le RTSP naslov kamere s strukturo:
    - `rtsp://<uporabniško_ime>:<geslo>@<IP_naslov>:<vrata>/<pot>` ali
    - `rtsp://<IP_naslov>:<vrata>/<pot>` v primeru, da RTSP video prenos ni zaščiten z uporabniškim imenom in geslom
- **Format izhoda:** Video tok, katerega lastnosti (ločljivost, število sličic na sekundo, itd.) so odvisne od nastavitev kamere
- **Opombe:** Postopek povezave na kamero in prejem videa je avtomatiziran s strani Frigate

##### Pametne naprave

- **Opis:** Vmesnik omogoča komunikacijo med integracijo v Home Assistant in pametnimi napravami preko posrednika MQTT, ki ga upravlja Home Assistant. Pametne naprave poslušajo na določenih MQTT temah (ang. topic) in se odzivajo na prejeta sporočila. Sistem uporablja ta vmesnik za vključevanje/izključevanje naprav kot del simulacije.
- **Vrsta povezave:** MQTT (preko komponente Mosquitto)
- **Format vhoda:** Sistem objavi sporočilo na določeno temo, kjer je vsebina definirana kot JSON ali preprosta vrednost (format sporočila je odvisen od naprave)
  ```python
  async def async_publish(
      hass: HomeAssistant,
      topic: str,
      payload: PublishPayloadType,
      qos: int | None = 0,
      retain: bool | None = False,
      encoding: str | None = DEFAULT_ENCODING,
  ) -> None:
  ```
- **Format izhoda:** Naprava ob prejetem sporočilu ustrezno spremeni stanje in novo stanje sporoči preko ločene MQTT teme.
- **Primer vhoda:** `shellies/shellycolorbulb-fcf5c4b2f131/color/0/command on`
  ```python
  async_publish(self.hass, "shellies/shellycolorbulb-fcf5c4b2f131/color/0/command", "on")
  ```
- **Primer izhoda:** `shellies/shellycolorbulb-fcf5c4b2f131/color/0/state on`

## 3.2 Predstavitev nefunkcionalnih zahtev

Sledeče nefunkcionalne zahteve opredeljujejo ključne lastnosti in omejitve sistema za avtomatsko simulacijo prisotnosti, ki temelji na zaznavi oseb preko RTSP kamer in integraciji z MQTT napravami. Zahteve zajemajo vse vidike sistema - od uporabniške izkušnje in varnosti do tehničnih omejitev in razvojnih procesov.

### Zahteve izdelka:

- Uporabnost:
    1. **Učinkovitost uporabe:** Sistem mora uporabnikom omogočati hitro doseganje njihovih ciljev. Povprečni uporabnik mora biti sposoben izvesti osnovne naloge, kot so dodajanje novega uporabnika objekta, nastavitev obvestil, dodajanje naprav in spreminjanje nastavitev varnostnega sistema, v manj kot 15 minutah.
    2. **Intuitivnost uporabniškega vmesnika:** Uporabniški vmesnik mora biti pregleden, logično zasnovan in enostaven za uporabo. Elementi, kot so gumbi, meniji in naslovi, morajo biti jasno označeni in umeščeni na pričakovana mesta. Uporabnik mora brez predhodnega usposabljanja razumeti osnovno delovanje sistema in biti sposoben samostojno upravljati osnovne funkcije v roku ene ure.
- Varnost:
    1. **Omejen dostop in nadzor sistema:** Poln nadzor nad delovanjem, konfiguracijo in nastavitvami sistema ima izključno administrator. Ostali uporabniki imajo dostop zgolj do izbranih funkcionalnosti.
    2. **Omejevanje dostopa:** Sistem mora omogočati ustrezno omejevanje nepooblaščenega dostopa do posameznih komponent, vključno s sistemom za detekcijo oseb in MQTT posrednikom.
    3. **Enkripcija zunanjih povezav v sistem**: Sistem mora omogočati varen dostop do sistema iz zunanjega (in notranjega omrežja), kar omogoča implementacija z obratnim posrednikom (reverse proxy) s TLS oz. SSL šifriranjem.
- Zanesljivost:
    1. **Persistenca dogodkov:** V primeru izpada sistema se mora zagotoviti, da bodo dogodki zaznave poslani v sistem ob prvi ponovni razpoložljivosti.
- Izvedba:
    1. **Zakasnitev zaznave:** Zakasnitev med zaznavo osebe s strani sistema za detekcijo oseb in prejetjem obvestila oziroma vklopom sistema za simulacijo prisotnosti mora biti maksimalno 10 sekund.
- Razpoložljivost:
    1. **Minimalna razpoložljivost:** Sistem mora v primeru pravilne konfiguracije zagotavljati najmanj 99% razpoložljivost storitev za ročno aktivacijo naprav in pošiljanje obvestil uporabnikom.
    2. **Avtomatska obnovitev sistema:** V primeru izpada sistema ali dela sistema, mora biti ta avtomatsko obnovljen v manj kot 5 minutah.
- Razširljivost:
    1. **Podpora za več uporabnikov:** Sistem mora podpirati hkratno uporabo s strani vsaj 5 uporabnikov brez upočasnitev ali napak v delovanju sistema.
    2. **Podpora za zunanje naprave:** Sistem mora podpirati vsaj eno zunanjo napravo za izvajanje simulacije prisotnosti.

### Organizacijske zahteve:

- **Upravljanje verzij in razvojni proces:** Vsa koda mora biti shranjena v GitHub repozitoriju, pri čemer morajo biti vse spremembe dokumentirane z jasnimi sporočili ob oddaji sprememb (*commit messages*) in izvedbami zahtev za združitev (*pull requests*), poleg tega pa morajo biti slednja pregledaa s strani vsaj enega drugega razvijalca pred združitvijo v glavno vejo. Zaradi preglednosti kode se mora izvajati tudi redno formatiranje kode z uporabo Black formatter, kar se izvaja preko uporabe Makefile.
- **Programski jezik in okolje:** Sistem mora biti razvit v Python 3.13 (ali novejšem). Docker vsebniki morajo uporabljati uradne Docker slike za vsako posamezno komponento. Za namen zagona se uporablja Docker Compose, pri čemer se uporablja ločena okolja za razvoj in produkcijsko verzijo.

### Zunanje zahteve:

- **Interoperabilnost:** Sistem mora delovati s kamerami, ki podpirajo RTSP in z zunanjimi napravami za simulacijo prisotnosti, ki komunicirajo preko MQTT ali specifične integracije (v primeru uporabe specifičnega produkta).

## 3.3 Predstavitev funkcionalnih zahtev

### 3.3.1 Diagram primerov uporabe

Spodnji diagram primerov uprabe grafično prikazuje glavne funkcionalnosti našega sistema ter interakcije z zunanjimi akterji, kot so uporabniki in zunanje naprave. V njem so vključene le funkcionalnosti s prioriteto ‘Must have’ in ‘Should have’.

<p align="center">
  <img src="gradivo/img/Osnutek%20sistema/diagram_primerov_uporabe.png" alt="Opis sistema" width="1000">
</p>

### 3.3.2 Specifikacije primerov uporabe

Sledeče funkcionalne zahteve opisujejo konkretne funkcionalnosti, ki jih mora sistem podpirati za uspešno delovanje in izpolnjevanje potreb uporabnikov. Razvrščene so po padajoči prioriteti, od ‘Must have’, ki označuje ključne in nujno potrebne funkcionalnosti, do ‘Would have’, ki se nanaša na funkcionalnosti, ki za trenutno verzijo rešitve niso ključne in bodo realizirane v prihodnosti.

Spodnja tabela prikazuje lestvico pogostosti uporabe, ki je bila uporabljena za določitev stopnje pogostosti uporabe v spodaj navedenih opisih funkcionalnih zahtev.

| Stopnja pogostosti uporabe | Opis |
| --- | --- |
| Redko | Funkcionalnost se uporablja le občasno. |
| Zmerno | Funkcionalnost se uporablja na tedenski ravni. |
| Pogosto | Funkcionalnost se uporablja skoraj vsakodnevno. |
| Zelo pogosto | Funkcionalnost se uporablja vsakodnevno. |

Omenjeni akterji v specificiranih primerih uporabe so:
- Administrator (vloga): Administrator sistema Home Assistant in posledično tudi naše integracije ima dostop do vseh nastavitev obeh sistemov.
- Uporabniki znotraj SUS (vloga): Član skupine uporabnikov objekta, ki ima določena pooblastila s strani administratorja. Integracija upošteva njegove akcije, do katerih lahko dostopa, in lokacijo za delovanje sistema.
- Kamera s podporo RTSP (zunanja naprava): Kamera, ki je sposobna video pretok kodirati v protokol RTSP in ga prepošiljati do sistema Frigate za nadaljnjo obdelavo.
- Sistemski števec (notranji sistem): Interni števec, ki ga sistem uporablja za avtomatski prehod iz stanja aktivnosti v stanje pripravljenosti. Dolžina števca je določena s strani administratorja sistema.

#### 1. Dodajanje pametne naprave
  
Akterji: administrator (vloga).

Povzetek: administrator lahko doda novo pametno napravo v sistem.

Osnovni tok: 

1. Administrator odpre nastavitve integracije sistema.
2. Med navedenimi storitvami sistema odpre akcijo dodajanja pametne naprave v sistem.
3. Ustrezno izpolni zahtevana polja in klikne na gumb za izvedbo akcije.
4. Pametna naprava je dodana v sistem.

Alternativni tok 1 - Nezadostna dovoljenja za dodajanje naprave:

1. Uporabnik brez administratorskih pravic odpre integracijo sistema.
2. Med navedenimi storitvami sistema odpre akcijo dodajanja pametne naprave v sistem.
3. Izpolni zahtevana polja in klikne na gumb za izvedbo akcije.
4. Pametna naprave se ne doda v sistem in prikaže se opozorilo o pomanjkanju administratorskih pravic.

(Pred)pogoji:

- Uporabnik sistema ima administratorske pravice.

Posledice/učinki uspešno izvedenega primera uporabe:

- V sistem je dodana nova naprava.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Število dodanih naprav ostane enako.

Posebne zahteve: 

- Uporabnik mora pravilno izpolniti zahtevana polja, saj v nasprotnem primeru naprava ne bo delovala.

Prioriteta: **Must have**

Pogostost uporabe: **Redko**
    
#### 2. Aktivacija pametne naprave

Akterji: administrator (vloga).

Povzetek: administrator lahko aktivira pametno napravo.

Osnovni tok:

1. Administrator odpre integracijo sistema
2. Med navedenimi storitvami sistema izvede akcijo aktiviranja določene pametne naprave.
3. Pametna naprava je aktivirana in prikaže se sporočilo o uspešni izvedbi akcije.

Alternativni tok 1 - Nezadostna dovoljenja za aktivacijo pametne naprave:

1. Uporabnik brez administratorskih pravic odpre integracijo sistema.
2. Med navedenimi storitvami sistema izvede akcijo aktiviranja določene pametne naprave.
3. Pametna naprave se ne aktivira in prikaže se sporočilo o pomanjkanju adminisitratorskih pravic.

Alternativni tok 2 - Naprava je že aktivirana:

1. Administrator odpre integracijo sistema.
2. Med navedenimi storitvami sistema izvede akcijo aktiviranja določene pametne naprave.
3. Naprava je bila predhodno že aktivirana, zato se uporabnika o tem obvesti.

(Pred)pogoji:

- Uporabnik sistema ima administratorske pravice

Posledice/učinki uspešno izvedenega primera uporabe:

- Naprava je aktivna v sistemu in jo sistem temu primerno uporablja

Posledice/učinki neuspešno izvedenega primera uporabe:

- Število aktivnih naprav se ne spremeni

Posebne zahteve:

- Posebnih zahtev ni

Prioriteta: **Must have**

Pogostost uporabe: **Redko**
    
#### 3. Deaktivacija pametne naprave

Akterji: administrator (vloga).

Povzetek: administrator lahko deaktivira pametno napravo.

Osnovni tok: 

1. Administrator odpre integracijo sistema.
2. Med navedenimi storitvami sistema izvede akcijo deaktiviranja določene pametne naprave.
3. Pametna naprava je deaktivirana in prikaže se sporočilo o uspešni izvedbi akcije.

Alternativni tok 1 - Nezadostna dovoljenja za deaktivacijo naprave:

1. Uporabnik brez administratorskih pravic odpre integracijo sistema.
2. Med navedenimi storitvami sistema izvede akcijo deaktiviranja določene pametne naprave.
3. Pametna naprave se ne deaktivira in prikaže se sporočilo o pomanjkanju adminisitratorskih pravic.

Alternativni tok 2 - Naprava je že deaktivirana:

1. Administrator odpre integracijo sistema.
2. Med navedenimi storitvami sistema izvede akcijo deaktiviranja določene pametne naprave.
3. Naprava je bila predhodno že deaktivirana, zato se uporabnika o tem obvesti.

(Pred)pogoji:

- Uporabnik sistema ima administratorske pravice.

Posledice/učinki uspešno izvedenega primera uporabe:

- Naprava je deaktivirana, zato sistem neha z njo upravljati.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Število deaktiviranih naprav se ne spremeni.

Posebne zahteve:

- Posebnih zahtev ni.

Prioriteta: **Must have**

Pogostost uporabe: **Redko**
    
#### 4. Odstranitev pametne naprave

Akterji: administrator (vloga).

Povzetek: Administrator lahko pametno napravo odstrani iz sistema.

Osnovni tok:

1. Administrator odpre integracijo sistema.
2. Med navedenimi napravami administrator izbere nastavitve željene naprave.
3. V nastavitvah napravo administrator odstrani napravo.
4. Naprava je odstranjena iz sistema in administrator je o akciji obveščen.

Alternativni tok 1 - Nezadostna dovoljenja za odstranitev pametne naprave:

1. Uporabnik brez administratorskih pravic odpre integracijo sistema.
2. Med navedenimi napravami izbere nastavitve željene naprave.
3. Naprave se ne da odstraniti ker nima administratorskih pravic.
4. Uporabnik zapre nastavitve brez sprememb.

(Pred)pogoji:

- Uporabnik sistema ima administratorske pravice

Posledice/učinki uspešno izvedenega primera uporabe:

- Naprava je odstranjena iz sistema

Posledice/učinki neuspešno izvedenega primera uporabe:

- Število naprav ostane enako

Posebne zahteve:

- Posebnih zahtev ni

Prioriteta: **Must have**

Pogostost uporabe: **Redko**
    
#### 5. Avtomatski prehod sistema iz stanja mirovanja v stanje pripravljenosti

Akterji: Uporabniki znotraj SUS (vloga).

Povzetek:  Uporabnik znotraj SUS lahko vpliva na spremembo stanja sistema s tem, ko zapusti določeno cono.

Osnovni tok:

1. Sistem je v stanju mirovanja.
2. Uporabnik znotraj SUS zapusti cono.
3. Če znotraj cone ni detektiranega nobenega uporabnika, ki je del SUS, sistem preide v stanje pripravljenosti. 

Alternativni tok 1 - Neupoštevan uporabnik zapusti cono:

1. Uporabnik, ki ni del SUS zapusti cono.
2. Stanje se ne spremeni.

Alternativni tok 2 - Uporabnik zapusti cono brez naprave:

1. Oseba, katere naprava je znotraj SUS zapusti cono, vendar brez fizične naprave ob sebi.
2. Stanje sistema se ne spremeni.

Alternativni tok 3 - Cono zapusti le del uporabnikov:

1. Cono zapusti del uporabnikov znotraj SUS.
2. Stanje sistema se ne spremeni.

(Pred)pogoji:

- Določena cona in skupina uporabnikov.

Posledice/učinki uspešno izvedenega primera uporabe:

- Sistem preide v stanje pripravljenosti.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Stanje sistema se ne spremeni.

Posebne zahteve:

- Osebe znotraj SUS morajo ob sebi imeti napravo z nameščeno Home Assistant aplikacijo, preko katere bo sistem imel dostop do lokacije uporabnikov.

Prioriteta: **Must have**

Pogostost uporabe: **Pogosto**
    
#### 6. Obdelava video pretoka in detekcija oseb

Akterji: Kamera s podporo RTSP (zunanja naprava).

Povzetek: Kamera s podporo RTSP omogoča dostop do video pretoka na določenem IP naslovu in vratih. Frigate dostopa do tega video pretoka in izvaja detekcijo oseb. 

Osnovni tok:

1. Kamera nenehno prenaša video tok preko RTSP, ne glede na stanje sistema.
2. Frigate dostopa do video toka in izvaja detekcijo oseb.
3. Razširitvena točka : zaznana oseba in poslano MQTT sporočilo v Home Assistant : avtomatski prehod sistema v aktivno stanje iz stanja pripravljenosti

Alternativni tok 1 - Ni zaznanih oseb:

1. Kamera nenehno prenaša video tok preko RTSP, ne glede na stanje sistema.
2. Frigate dostopa do video toka in izvaja detekcijo oseb.
3. V video toku ni prisotne osebe.
4.  Frigate ne zazna osebe in sporočilo o detekciji ni poslano.

Alternativni tok 2 - Oseba ni zaznana, kljub prisotnosti osebe:

1. Kamera nenehno prenaša video tok preko RTSP, ne glede na stanje sistema.
2. Frigate dostopa do video toka in izvaja detekcijo oseb.
3. V video toku je prisotna oseba.
4. Frigate osebe ne zazna zaradi nedelovanja funkcionalnosti za zaznavo oseb.

(Pred)pogoji:

- Uspešno povezan Frigate na kamero.

Posledice/učinki uspešno izvedenega primera uporabe:

- Oseba je zaznana in sporočilo o detekciji je poslano.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Oseba ni zaznana in sporočilo o detekciji ni poslano.

Posebne zahteve:

- Kamera je ustrezno nastavljena in izvaja pretok videa preko protokola RTSP.

Prioriteta: **Must have**

Pogostost uporabe: **Zelo** **pogosto** 

#### 7. Avtomatski prehod sistema v aktivno stanje iz stanja pripravljenosti

Akterji: /

Razširitvena točka za obdelavo video pretoka in detekcijo oseb.

Povzetek: Ob detektirani osebi, sistem preide v aktivno stanje.

Osnovni tok:

1. Sistem je v stanju pripravljenosti.
2. Sistem preko MQTT posluša za sporočila zaznave oseb.
3. Ob prejetem sporočilu o zaznavi osebe, sistem preide v aktivno stanje.

Alternativni tok 1 - Sporočilo ni prejeto:

1. Sistem je v stanju pripravljenosti.
2. Sistem preko MQTT posluša za sporočila zaznave oseb.
3. Sporočilo ni bilo prejeto, zato sistem ne spremeni stanja.

(Pred)pogoji:

- Sistem je v stanju pripravljenosti.

Posledice/učinki uspešno izvedenega primera uporabe:

- Sistem je v aktivnem stanju.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Sistem ostane v stanju pripravljenosti.

Posebne zahteve:

- Posebnih zahtev ni.

Prioriteta: **Must have**

Pogostost uporabe: **Zmerno**

#### 8. Izvajanje simulacije prisotnosti

Akterji: /

Povzetek: Sistem upravlja z aktiviranimi pametnimi napravami za simulacijo prisotnosti v objektu.

Osnovni tok:

1. Sistem je v aktivnem stanju.
2. Sistem začne z izvajanjem simulacije prisotnosti glede na uporabniške nastavitve - katere naprave so aktivirane, čas v dnevu.
3. Sistem ostane v aktivnem stanju, dokler ga administrator ročno ne deaktivira ali dokler gibanje ni več zaznano in od zadnje zaznave ne preteče določen čas, ki ga določi administrator.

Alternativni tok 1 - Motnje v delovanju pametnih naprav:

1. Sistem je v aktivnem stanju.
2. Med delovanjem sistema pride do motenj v delovanju pametnih naprav (izpad elektrike).
3. Naprave prenehajo delovati, čeprav je sistem v aktivnem stanju.

(Pred)pogoji:

- Sistem je v aktivnem stanju.

Posledice/učinki uspešno izvedenega primera uporabe:

- Sistem za določen čas izvaja simulacijo prisotnosti.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Simulacija prisotnosti je okrnjena.

Posebne zahteve:

- Posebnih zahtev ni.

Prioriteta: **Must have**

Pogostost uporabe: **Zmerno**
    
#### 9. Avtomatski prehod sistema iz aktivnega stanja v stanje pripravljenosti

Akterji: Sistemski števec (notranji sistem).

Povzetek: Ob poteku sistemskega števca sistem preide iz aktivnega stanja v stanje pripravljenosti.

Osnovni tok:

1. Sistem je v aktivnem stanju.
2. Od zadnje zaznave osebe je minilo več kot vnaprej določen časovni interval, ki ga določi administrator.
3. Sistem avtomatsko preide v stanje pripravljenosti.

Alternativni tok 1 - Zaznana oseba:

1. Sistem je v aktivnem stanju.
2. V vnaprej določenem časovnem intervalu je prišlo do zaznave osebe, sistemski števec se ponastavi.
3. Sistem ostane v aktivnem stanju.

(Pred)pogoji:

- Sistem je v aktivnem stanju.

Posledice/učinki uspešno izvedenega primera uporabe:

- Sistem preide v stanje pripravljenosti.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Sistem ostane v aktivnem stanju.

Posebne zahteve:

- Posebnih zahtev ni.

Prioriteta: **Must have**

Pogostost uporabe: **Zmerno**
    
#### 10. Avtomatski prehod sistema iz stanja pripravljenosti v stanje mirovanja

Akterji: Uporabniki znotraj SUS (vloga).

Povzetek: Uporabnik znotraj SUS lahko povzroči prehod sistema iz stanja pripravljenosti v stanje mirovanja.

Osnovni tok:

1. Sistem je v stanju pripravljenosti.
2. Uporabnik znotraj SUS pride v cono.
3. Sistem preide v stanje mirovanja.

Alternativni tok 1 - Uporabnik vstopi v cono brez naprave:

1. Oseba, katere naprava je znotraj SUS vstopi v cono, vendar brez fizične naprave ob sebi.
2. Stanje sistema se ne spremeni.

(Pred)pogoji:

- Določena cona in skupina uporabnikov.

Posledice/učinki uspešno izvedenega primera uporabe:

- Sistem preide v stanje mirovanja.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Stanje sistema se ne spremeni.

Posebne zahteve:

- Osebe znotraj SUS morajo ob sebi imeti napravo z nameščeno Home Assistant aplikacijo, preko katere bo sistem imel dostop do lokacije uporabnikov.

Prioriteta: **Must have**

Pogostost uporabe: **Pogosto**
    
#### 11. Določitev cone

Akterji: administrator (vloga).

Povzetek: administrator lahko določi cono deaktivacije sistema.

Osnovni tok:

1. Administrator odpre nastavitve integracije.
2. Privzeto je že izbrana cona, ki je bila določena ob nastavitvi Home Assistant sistema.
3. Med nastavljenimi conami izbere cono, glede na katero se bo sistem aktiviral in deaktiviral.
4. Prikaže se obvestilo, da je bila akcija uspešna.

Alternativni tok 1 - Nezadostna dovoljenja za nastavitev cone:

1. Uporabnik brez administratorskih pravic odpre nastavitve integracije.
2. Privzeto je že izbrana cona, ki je bila določena ob nastavitvi Home Assistant sistema.
3. Med nastavljenimi conami izbere cono, glede na katero se bo sistem aktiviral in deaktiviral.
4. Prikaže se opozorilo, da uporabnik nima administratorskih pravic in cona se ne določi.

(Pred)pogoji:

- Uporabnik sistema ima administratorske pravice.
- Nastavljena vsaj ena cona znotraj Home Assistant sistema.

Posledice/učinki uspešno izvedenega primera uporabe:

- Določena cona, glede na katero se sistem aktivira/deaktivira.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Cona ni določena, zato je sistem aktiven/neaktiven ne glede na lokacijo uporabnikov znotraj SUS.

Posebne zahteve:

- Posebnih zahtev ni

Prioriteta: **Should have**

Pogostost uporabe: **Redko**
    
#### 12. Upravljanje s skupino uporabnikov

Akterji: Administrator (vloga).

Povzetek: Administrator lahko izbere uporabnike sistema Home Assistant, ki bodo del SUS.

Osnovni tok:

1. Administrator odpre nastavitve integracije.
2. Med navedenimi storitvami sistema odpre akcijo za upravljanje SUS.
3. Med množico uporabnikov izbere osebe, ki bodo del SUS.
4. Izvede akcijo in prikaže se sporočilo o uspešni izvedbi akcije.

Alternativni tok 1 - Nezadostna dovoljenja za upravljanje s SUS:

1. Uporabnik brez administratorskih pravic odpre nastavitve integracije.
2. Med navedenimi storitvami sistema odpre akcijo za upravljanje SUS.
3. Med množico uporabnikov izbere osebe, ki bodo del SUS.
4. Akcija se ne izvede in pokaže se opozorilo o pomanjkanju administratorskih pravic.

(Pred)pogoji:

- Uporabnik sistema ima administratorske pravice.
- Vsaj ena dodatna oseba je prisotna v sistemu Home Assistant.

Posledice/učinki uspešno izvedenega primera uporabe:

- Dodani oziroma odstranjeni člani iz SUS.

Posledice/učinki neuspešno izvedenega primera uporabe:

- SUS ostane nespremenjena.

Posebne zahteve:

- Posebnih zahtev ni.

Prioriteta: **Should have**

Pogostost uporabe: **Redko**
    
#### 13. Pošiljanje obvestil

Akterji: /

Povzetek: Ob aktivaciji sistema se uporabnikom v SUS pošlje potisno obvestilo.

Osnovni tok:

1. Pošlje se potisno obvestilo uporabnikom v SUS, da je bilo zaznano gibanje.
2. Sporočilo je vidno na plošči za obvestila znotraj Home Assistant sistema in kot potisno obvestilo na obvestilni vrstici pametnega telefona oziroma naprave z nameščeno aplikacijo Home Assistant.

Alternativni tok 1 - Težave z internetno povezavo ali strežnikom:

1. Pošiljanje obvestila ne uspe zaradi težav z internetno povezavo ali strežnikom.
2. Sistem shrani neuspelo obvestilo in ga poskuša ponovno poslati ob prvi naslednji priložnosti.

(Pred)pogoji:

- Uporabnik ima vklopljena obvestila aplikacije v nastavitvah sistema.

Posledice/učinki uspešno izvedenega primera uporabe:

- Uporabnik iz SUS prejme obvestilo o aktivaciji sistema.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Uporabnik iz SUS z zamudo prejme obvestilo ali pa ga sploh ne prejme.

Posebne zahteve:

- Posebnih zahtev ni.

Prioriteta: **Should have**

Pogostost uporabe: **Zmerno**
    
#### 14. Ročni preklop sistema v aktivno stanje

Akterji: Administrator (vloga).

Povzetek: Administrator lahko ročno preklopi sistem v aktivno stanje.

Osnovni tok:

1. Administrator odpre integracijo sistema.
2. Med navedenimi akcijami izbere preklop sistema v aktivno stanje.
3. Sistem preide v aktivno stanje.

Alternativni tok 1 - Sistem je že v aktivnem stanju:

1. Administrator odpre integracijo sistema.
2. Med navedenimi akcijami izbere preklop sistema v aktivno stanje.
3. Sistem je že v aktivnem stanju zato se stanje ne spremeni.

Alternativni tok 2 - Nezadostna dovoljenja za ročni preklop stanja sistema:

1. Uporabnik brez administratorskih pravic odpre integracijo sistema.
2. Med navedenimi akcijami izbere preklop sistema v aktivno stanje.
3. Akcija se ne izvede in prikaže se opozorilo o pomanjkanju administratorskih pravic.

(Pred)pogoji:

- Uporabnik ima administratorske pravice.
- Sistem ni v aktivnem stanju.

Posledice/učinki uspešno izvedenega primera uporabe:

- Sistem preide v aktivno stanje.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Sistem ohrani trenutno stanje.

Posebne zahteve:

- Posebnih zahtev ni

Prioriteta: **Should have**

Pogostost uporabe: **Redko**
    
#### 15. Ročni preklop sistema v stanje mirovanja

Akterji: Administrator (vloga).

Povzetek: Administrator lahko ročno preklopi sistem v stanje mirovanja.

Osnovni tok:

1. Administrator odpre integracijo sistema.
2. Med navedenimi akcijami izbere preklop sistema v stanje mirovanja.
3. Sistem preide v mirovanje.

Alternativni tok 1 - Sistem je že v mirovanju:

1. Administrator odpre integracijo sistema.
2. Med navedenimi akcijami izbere preklop sistema v stanje mirovanja.
3. Sistem je že v mirovanju, zato se stanje ne spremeni.

Alternativni tok 2 - Nezadostna dovoljenja za ročni preklop stanja sistema:

1. Uporabnik brez administratorskih pravic odpre integracijo sistema.
2. Med navedenimi akcijami izbere preklop sistema v stanje mirovanja.
3. Akcija se ne izvede in prikaže se opozorilo o pomanjkanju administratorskih pravic.

(Pred)pogoji:

- Uporabnik ima administratorske pravice.
- Sistem je v aktivnem stanju.

Posledice/učinki uspešno izvedenega primera uporabe:

- Sistem preide v mirovanje.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Sistem ohrani trenutno stanje.

Posebne zahteve:

- Posebnih zahtev ni

Prioriteta: **Should have**

Pogostost uporabe: **Redko**
    
#### 16. Aktivacija shranjevanja slik

Akterji: administrator (vloga).

Povzetek: administrator lahko aktivira shranjevanje slik ob zaznavi osebe.

Osnovni tok:

1. Administrator odpre nastavitve integracije.
2. Med navedenimi storitvami sistema izvede akcijo aktivacije shranjevanja slik ter izbere lokacijo shranjevanja.
3. Akcija je izvedena in prikaže se sporočilo o uspešni izvedbi.

Alternativni tok 1 - Nezadostna dovoljenja za aktivacijo shranjevanja slik:

1. Uporabnik brez administratorskih pravic odpre nastavitve integracije sistema.
2. Med navedenimi storitvami sistema izvede akcijo aktivacije shranjevanja slik.
3. Akcija se ne izvede in prikaže se opozorilo o pomanjkanju administratorskih pravic.

(Pred)pogoji:

- Uporabnik sistema ima administrativne pravice.

Posledice/učinki uspešno izvedenega primera uporabe:

- V sklopu integracije se shranjujejo slike ob zaznavi osebe.

Posledice/učinki neuspešno izvedenega primera uporabe:

- V sklopu integracije se slike ob zaznavi osebe ne shranjujejo.

Posebne zahteve:

- Posebnih zahtev ni

Prioriteta: **Could have**

Pogostost uporabe: **Redko**
    
#### 17. Deaktivacija shranjevanja slik

Akterji: administrator (vloga).

Povzetek: administrator lahko deaktivira shranjevanje slik ob zaznavi osebe.

Osnovni tok:

1. Administrator odpre nastavitve integracije.
2. Med navedenimi storitvami sistema izvede akcijo deaktivacije shranjevanja slik.
3. Akcija je izvedena in prikaže se sporočilo o uspešni izvedbi.

Alternativni tok 1 - Nezadostna dovoljenja za deaktivacijo shranjevanja slik:

1. Uporabnik brez administratorskih pravic odpre nastavitve integracije sistema.
2. Med navedenimi storitvami sistema izvede akcijo deaktivacije shranjevanja slik.
3. Akcija se ne izvede in prikaže se opozorilo o pomanjkanju administratorskih pravic.

(Pred)pogoji:

- Uporabnik sistema ima administrativne pravice.

Posledice/učinki uspešno izvedenega primera uporabe:

- V sklopu integracije se slike ob zaznavi osebe ne shranjujejo.

Posledice/učinki neuspešno izvedenega primera uporabe:

- V sklopu integracije se shranjujejo slike ob zaznavi osebe.

Posebne zahteve:

- Posebnih zahtev ni

Prioriteta: **Could have**

Pogostost uporabe: **Redko**
    
#### 18. Upravljanje z nastavitvami shranjevanja videoposnetkov

Akterji: Administrator (vloga).

Povzetek: Administrator lahko določi, ali se bodo videoposnetki kamer ob zaznavi oseb shranjevali.

Osnovni tok:

1. Administrator odpre nastavitve integracije.
2. Med navedenimi storitvami sistema odpre akcijo za upravljanje z nastavitvami shranjevanja videoposnetkov.
3. Določi ali bo integracija shranjevala videoposnetke ob detekciji osebe.
4. Izvede akcijo in prikaže se sporočilo o uspešni izvedbi akcije.

Alternativni tok 1 - Nezadostna dovoljenja za upravljanje z nastavitvami shranjevanja videoposnetkov:

1. Uporabnik brez administratorskih pravic odpre nastavitve integracije.
2. Med navedenimi storitvami sistema odpre akcijo za upravljanje z nastavitvami shranjevanja videoposnetkov.
3. Določi ali bo integracija shranjevala videoposnetke ob detekciji osebe.
4. Akcija se ne izvede in prikaže se opozorilo o pomanjkanju administratorskih pravic.

(Pred)pogoji:

- Uporabnik ima administratorske pravice.

Posledice/učinki uspešno izvedenega primera uporabe:

- Spremenjene nastavitve shranjevanja videoposnetkov.

Posledice/učinki neuspešno izvedenega primera uporabe:

- Nastavitve ostanejo nespremenjene.

Posebne zahteve:

- Posebnih zahtev ni

Prioriteta: **Would have**

Pogostost uporabe: **Redko**

#### Sprejemni testi

| Primer uporabe | Funkcija, ki se testira | Začetno stanje sistema | Vhod | Pričakovan rezultat |
| --- | --- | --- | --- | --- |
| **1. Dodajanje pametne naprave** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Izvedba dodajanja pametne naprave v sistem. | Seznam že dodanih naprav je prazen ali pa že vsebuje določene naprave. | Administrator izpolni polja potrebna za konfiguracijo naprave in potrditev akcije. | Pametna naprava je bila dodana v sistem in sporočilo o uspešni izvedbi akcije. |
| Alternativni tok 1 - Nezadostna dovoljenja za dodajanje naprave | Onemogočeno dodajanje pametnih naprav uporabnikom brez administratorskih pravic.      | Seznam že dodanih naprav je prazen ali pa že vsebuje določene naprave. | Uporabnik brez administratorskih pravic izpolni polja potrebna za konfiguracijo naprave in potrditev akcije. | Pametna naprava ni bila dodana v sistem in opozorilo o pomanjkanju administratorskih pravic |
| **2. Aktivacija pametne naprave** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Izvedba aktivacije pametne naprave. | Pametna naprava ni aktivirana. | Administrator izbere napravo za aktivacijo in potrditev akcije. | Pametna naprava je bila aktivirana in sporočilo o izvedbi akcije. |
| Alternativni tok 1 - Nezadostna dovoljenja za aktivacijo pametne naprave | Onemogočeno aktiviranje pametne naprave uporabniku brez administratorskih pravic. | Pametna naprava ni aktivirana. | Uporabnik brez administratorskih pravic izbere napravo za aktivacijo in potrditev akcije. | Pametna naprava ni bila aktivirana in opozorilo o pomanjkanju administratorskih pravic. |
| Alternativni tok 2 - Naprava je že aktivirana | Onemogočeno aktiviranje pametne naprave, če je že aktivirana. | Pametna naprava je aktivirana. | Izbrana naprava za aktivacijo in potrditev akcije. | Akcija se ne izvede, opozorilo o že aktivirani napravi. |
| **3. Deaktivacija pametne naprave** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Izvedba deaktivacije pametne naprave. | Pametna naprava je aktivirana. | Administrator izbere napravo za deaktivacijo in potrditev akcije. | Pametna naprava je bila deaktivirana in sporočilo o uspešni izvedbi akcije. |
| Alternativni tok 1 - Nezadostna dovoljenja za deaktivacijo naprave | Onemogočeno deaktiviranje pametnih naprav uporabnikom brez administratorskih pravic. | Pametna naprava je aktivirana. | Uporabnik brez administratorskih pravic izbere napravo za deaktivacijo in potrditev akcije. | Pametna naprava ni bila deaktivirana in opozorilo o pomanjkanju administratorskih pravic. |
| Alternativni tok 2 - Naprava je že deaktivirana | Onemogočena izvedba deaktivacije pametne naprave, če je že deaktivirana. | Pametna naprava ni aktivirana. | Izbrana naprava za deaktivacijo in potrditev akcije. | Akcija se ne izvede, opozorilo o tem, da je ta pametna naprava že deaktivirana. |
| **4. Odstranitev pametne naprave** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Izvedba odstranitve pametne naprave. | Pametna naprava je dodana v sistem. | Administrator izbere napravo in potrditev akcije. | Pametna naprava je bila odstranjena, sporočilo o uspešni izvedbi akcije. |
| Alternativni tok 1 - Nezadostna dovoljenja za odstranitev pametne naprave | Onemogočeno odstranjanje naprav uporabnikom brez administratorskih pravic. | Pametna naprava je dodana v sistem. | Uporabnik brez administratorskih pravic izbere napravo in potrditev akcije. | Pametna naprava ni bila odstranjena, opozorilo o pomanjkanju administratorskih pravic. |
| **5.  Avtomatski prehod sistema iz stanja mirovanja v stanje pripravljenosti** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Prehod sistema iz stanja mirovanja v stanje pripravljenosti, ko še zadnji uporabnik iz SUS zapusti cono. | Sistem je v stanju mirovanja. | Uporabnik znotraj SUS zapusti cono. | Sistem preide iz stanja mirovanja v stanje pripravljenosti. |
| Alternativni tok 1 - Neupoštevan uporabnik zapusti cono | Sistem ne zamenja stanja, če cono zapusti uporabnik izven SUS. | Sistem je v stanju mirovanja. | Uporabnik izven SUS zapusti cono. | Sistem ne spremeni stanja. |
| Alternativni tok 2 - Uporabnik zapusti cono brez naprave | Sistem ne zamenja stanja, če uporabnik znotraj SUS zapusti cono brez fizične naprave ob sebi. | Sistem je v stanju mirovanja. | Uporabnik znotraj SUS zapusti cono brez fizične naprave ob sebi. | Sistem ne spremeni stanja. |
| Alternativni tok 3 - Cono zapusti le del uporabnikov | Sistem ne zamenja stanja, če cono zapusti le del uporabnikov znotraj SUS. | Sistem je v stanju mirovanja in znotraj cone je več kot en uporabnik iz SUS. | Uporabnik znotraj SUS zapusti cono. | Sistem ne spremeni stanja. |
| **6. Obdelava video pretoka in detekcija oseb** | ———————- | ——————— | ——————— | ——————— |
| Osnovni tok | Zaznana oseba in poslano MQTT sporočilo v Home Assistant. | Sistem je v kateremkoli stanju. | Video pretok. | Poslano MQTT sporočilo o zaznavi osebe. |
| Alternativni tok 1 - Ni zaznanih oseb | Na video prenosu ni zaznanih oseb in sporočilo zaznave ni poslano. | Sistem je v kateremkoli stanju. | Video pretok. | Sporočilo o zaznavi osebe ni poslano. |
| Alternativni tok 2 - Oseba ni zaznana, kljub prisotnosti osebe | Na video prenosu ni zaznanih oseb, čeprav so prisotne in sporočilo zaznave ni poslano. | Sistem je v kateremkoli stanju. | Video pretok. | Sporočilo o zaznavi osebe ni poslano. |
| **7. Avtomatski prehod sistema v aktivno stanje iz stanja pripravljenosti** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Prehod sistema v aktivno stanje, ob prejetem sporočilu o zaznavi osebe. | Sistem je v stanju pripravljenosti. | Sporočilo o zaznavi osebe je prejeto. | Sistem preide v aktivno stanje. |
| Alternativni tok 1 - Sporočilo ni prejeto | Sistem ne izvede prehoda v aktivno stanje, če ne prejme sporočila o zaznavi. | Sistem je v stanju pripravljenosti. | Sporočilo o zaznavi ni prejeto. | Sistem ne spremeni stanja. |
| **8. Izvajanje simulacije prisotnosti** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Uspešni zagon in izvajanje simulacije prisotnosti. | Sistem je v aktivnem stanju. | Uspešno izvedena funkcionalnost 7. | Sistem ostane v aktivnem stanju in izvaja simulacijo prisotnosti za predoločen čas po zaznavi gibanja in dokler gibanje ni več zaznano ali ga administrator ročno ne deaktivira. |
| Alternativni tok 1 - Motnje v delovanju pametnih naprav | Odziv sistema ob motnjah v delovanju pametnih naprav. | Sistem je v aktivnem stanju. | Uspešno izvedena funkcionalnost 7 in motnje v delovanju pametnih naprav (npr. izpad elektrike) | Sistem ostane v aktivnem stanju, vendar simulacija prisotnosti je okrnjena. |
| **9. Avtomatski prehod sistema iz aktivnega stanja v stanje pripravljenosti** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Sistem avtomatsko preide v stanje pripravljenosti, po izteku vnaprej določenega časovnega intervala. | Sistem je v aktivnem stanju. | Potek sistemskega števca. | Sistem preide v stanje pripravljenosti. |
| Alternativni tok 1 - Zaznana oseba | Sistem ostane v aktivnem stanju, v primeru ponovne zaznave osebe pred iztekom sistemskega števca. | Sistem je v aktivnem stanju. | Zaznana oseba pred iztekom sistemskega števca. | Sistem ostane v aktivnem stanju. |
| **10. Avtomatski prehod sistema iz stanja pripravljenosti v stanje mirovanja** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Prehod sistema iz stanja pripravljenosti v stanje mirovanja, ko prvi uporabnik znotraj SUS pride v cono. | Sistem je v stanju pripravljenosti. | Uporabnik znotraj SUS vstopi v cono. | Sistem preide iz stanja pripravljenosti v stanje mirovanja. |
| Alternativni tok 1 - Uporabnik vstopi v cono brez naprave | Sistem ne zamenja stanja, če uporabnik znotraj SUS pride v cono brez fizične naprave ob sebi. | Sistem je v stanju pripravljenosti. | Uporabnik znotraj SUS vstopi v cono brez fizične naprave ob sebi. | Sistem ne spremeni stanja. |
| **11. Določitev cone** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Izvedba akcije za nastavljanje cone. | Privzeto ali ročno nastavljena cona. | Administrator izbere cono izmed množice že predhodno nastavljenih con znotraj sistema Home Assistant in potrditev akcije. | Cona se nastavi in sporočilo o uspešni izvedbi akcije. |
| Alternativni tok 1 - Nezadostna dovoljenja za nastavitev cone | Onemogočeno nastavljanje cone za uporabnike brez administratorskih pravic. | Privzeto ali ročno nastavljena cona. | Uporabnik brez administratorskih pravic izbere cono izmed množice že predhodno nastavljenih con znotraj sistema Home Assistant in potrditev akcije. | Cona se ne nastavi in opozorilo o pomanjkanju administratorskih pravic. |
| **12. Upravljanje s ‘skupino uporabnikov’** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Izvedba akcije za izbor članov SUS. | Obstoječa SUS, ki vključuje administratorja in opcijsko ostale uporabnike. | Administrator izbere novo množico članov SUS. | SUS se ustrezno spremeni in prikazano obvestilo o uspešni izvedbi akcije. |
| Alternativni tok 1 - Nezadostna dovoljenja za upravljanje s SUS | Onemogočena izvedba akcije za izbor članov SUS uporabnikom brez administratorskih pravic. | Obstoječa SUS, ki vključuje administratorja in opcijsko ostale uporabnike. | Uporabnik brez administratorskih pravic izbere novo množico članov SUS. | SUS se ne spremeni in prikazano opozorilo o pomanjkanju administratorskih pravic. |
| **13. Pošiljanje obvestil** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Prejem potisnega obvestila ob prehodu sistema v aktivno stanje. | Sistem je v aktivnem stanju. | Uspešna izvedena funkcionalnost 7. | Uspešno poslano sporočilo, vidno na plošči za obvestila znotraj Home Assistant sistema in kot potisno obvestilo na obvestilni vrstici pametnega telefona. |
| Alternativni tok 1 - Težave z internetno povezavo ali strežnikom | Zapozneli prejem potisnega obvestila, zaradi težav z internetno povezavo ali strežnikom. | Sistem je v aktivnem stanju. | Uspešna izvedena funkcionalnost 7 in motnje v delovanju strežnika ali internetne povezave. | Neuspešno poslano sporočilo, ki ga sistem shrani in ponovno poskuša poslati ob prvi naslednji vzpostavitvi povezave ali odpravi težave s strežnikom. |
| **14. Ročni preklop sistema v aktivno stanje** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Ročni preklop sistema v aktivno stanje. | Sistem ni v aktivnem stanju. | Administrator ročno izbere prehod v aktivno stanje. | Sistem preide v aktivno stanje. |
| Alternativni tok 1 - Sistem je že v aktivnem stanju | Ročni preklop sistema v aktivno stanje, čeprav je sistem že v tem stanju. | Sistem je v aktivnem stanju. | Administrator ročno izbere prehod v aktivno stanje. | Stanje sistema se ne spremeni, obvestilo o že aktivnem stanju. |
| Alternativni tok 2 - Nezadostna dovoljenja za ročni preklop stanja sistema | Onemogočen ročni preklop sistema uporabnikom brez administratorskih pravic. | Sistem ni v aktivnem stanju. | Uporabnik brez administratorskih pravic ročno izbere prehod v aktivno stanje. | Stanje sistema se ne spremeni, obvestilo o pomanjkanju administratorskih pravic. |
| **15. Ročni preklop sistema v stanje mirovanja** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Ročni preklop sistema v stanje mirovanja. | Sistem ni v stanju mirovanja. | Administrator ročno izbere prehod sistema v stanje mirovanja. | Sistem preide v stanje mirovanja. |
| Alternativni tok 1 - Sistem je že v mirovanju | Ročni preklop sistema v stanje mirovanja, čeprav je sistem že v stanju mirovanja. | Sistem je v stanju mirovanja. | Administrator ročno izbere prehod sistema v stanje mirovanja. | Stanje sistema se ne spremeni, obvestilo, da je sistem že v stanju mirovanja. |
| Alternativni tok 2 - Nezadostna dovoljenja za ročni preklop stanja sistema | Onemogočen ročni preklop sistema uporabnikom brez administratorskih pravic. | Sistem ni v stanju mirovanja. | Uporabnik brez administratorskih pravic ročno izbere prehod sistema v stanje mirovanja. | Stanje sistema se ne spremeni, obvestilo o pomanjkanju administratorskih pravic. |
| **16. Aktivacija shranjevanja slik** | ———————- | ——————— | ——————— | ——————— |
| Osnovni tok | Izvedba akcije za aktivacijo shranjevanja slik. | Izklopljeno shranjevanje slik. | Administrator izbere opcijo aktivacije shranjevanja slik in lokacijo shranjevanja. | Shranjevanje slik je aktivirano. |
| Alternativni tok 1 - Nezadostna dovoljenja za aktivacijo shranjevanja slik | Onemogočena izvedba akcije aktivacije shranjevanja slik za uporabnike brez administratorskih pravic. | Izklopljeno shranjevanje slik. | Uporabnik brez administratorskih pravic izbere opcijo aktivacije shranjevanja slik lokacijo shranjevanja. | Shranjevanje slik ni aktivirano in sporočilo o pomanjkanju administratorskih pravic. |
| **17. Deaktivacija shranjevanja slik** | ———————- | ——————— | ——————— | ———————- |
| Osnovni tok | Izvedba akcije za deaktivacijo shranjevanja slik. | Vklopljeno shranjevanje slik. | Administrator izbere opcijo deaktivacije shranjevanja slik. | Shranjevanje slik je deaktivirano. |
| Alternativni tok 1 - Nezadostna dovoljenja za deaktivacijo shranjevanja slik | Onemogočena izvedba akcije deaktivacije shranjevanja slik za uporabnike brez administratorskih pravic. | Vklopljeno shranjevanje slik. | Uporabnik brez administratorskih pravic izbere opcijo deaktivacije shranjevanja slik. | Shranjevanje slik ni deaktivirano in sporočilo o pomanjkanju administratorskih pravic. |
| **18. Upravljanje z nastavitvami shranjevanja videoposnetkov** | ——————— | ——————— | ——————— | ——————— |
| Osnovni tok | Izvedba akcije za določitev, ali se bodo videoposnetki kamer ob zaznavi oseb shranjevali. | Obstoječe nastavitve za shranjevanje videoposnetkov. | Administrator določi nove nastavitve shranjevanja videoposnetkov. | Določene nove nastavitve shranjevanja videoposnetkov. |
| Alternativni tok 1 - Nezadostna dovoljenja za upravljanje z nastavitvami shranjevanja videoposnetkov | Onemogočena izvedba akcije za določitev, ali se bodo videoposnetki kamer ob zaznavi oseb shranjevali. | Obstoječe nastavitve za shranjevanje videoposnetkov. | Uporabnik brez administratorskih pravic določi nove nastavitve shranjevanja videoposnetkov. | Nastavitve shranjevanja videoposnetkov se ne spremenijo in sporočilo o pomanjkanju administratorskih pravic. |

## 3.4 Vrednotenje zahtev

Pri vrednotenju funkcionalnih zahtev se upoštevajo naslednji kriteriji: veljavnost zahteve napram uporabnikovim potrebam, skladnost z ostalimi zahtevami, celovitost funkcionalnosti napram uporabnikovim potrebam, realističnost izvedljivosti zahtev, in preverljivost zahtev s testiranji.

Vrednotenja zahtev so narejena po logičnih sklopih funkcionalnih zahtev delov končnega sistema.

### Upravljanje pametnih naprav

- Dodajanje pametne naprave
- Aktivacija pametne naprave
- Deaktivacija pametne naprave
- Odstranitev pametne naprave

Veljavnost: Sistem ob izpolnitvi zahtev omogoča administratorju nadzor nad upravljanjem integracij sistema s pametnimi napravami v objektu - dodajanje novih in odstranjevanje obstoječih naprav iz sistema, ter vključitev in izključitev možnosti aktivacije obstoječih pametnih naprav v primeru prehoda. Vse to predstavlja temeljne želene funkcionalnosti sistema.

Skladnost: Zahteve ne kažejo očitnih konfliktov z drugimi zahtevami, saj se osredotočajo na administracijo sistema, ne na dejansko delovanje sistema s podanimi nastavitvami.

Celovitost: Uporabnik (administrator) se zaveda, da sistem podpira le upravljanje določenih pametnih naprav. Prav tako ima zraven vsake akcije podan opis, kako dana akcija lahko vpliva na delovanje sistema.

Realističnost: Zahteve so glede na dani čas in omejitve izvedljive.

Preverljivost: Integracijski test in testi enot, ki preverjajo pravilnost stanj naprav po dodajanju ali odstranjevanju naprave.

### Upravljanje con aktivacij sistema

- Določitev cone

Veljavnost: Sistem omogoča izbiro določenih geolokacijskih con, pri katerih v primeru izstopa vseh uporabnikov iz njih sistem avtomatično izvede aktivacijo v fazo pripravljenosti. Funkcionalnost predstavlja temeljno želeno funkcionalnost sistema.

Skladnost: Zahteva ne povzroča konfliktov z drugimi funkcionalnostmi, saj se osredotoča na določitev geografske cone.

Celovitost: Uporabnik (administrator) se zaveda, da je potrebno definirati cono za pravilno oz. pričakovano delovanje sistema.

Realističnost: Zahteva je glede na dani čas in omejitve izvedljiva.

Preverljivost: Testi enote, ki preverjajo pravilnost nastavitve cone in prehodov sistema v stanje pripravljenosti.

### Shranjevanje videoposnetka/slik ob aktivaciji

- Aktivacija shranjevanja slik
- Deaktivacija shranjevanja slik
- Upravljanje z nastavitvami shranjevanja videoposnetkov

Veljavnost: Sistem naj bi omogočal vklop ali izklop shranjevanja videoposnetka in/ali slik dogajanja, ko sistem zazna gibanje v aktivnem stanju. Prav tako bi moral omogočati specifikacijo lokacije shranjevanja multimedijskih datotek za kasnejši pregled. Funkcionalnosti ne predstavljajo temeljne želene funkcionalnosti sistema, predstavlja pa želeno razširitev v prihodnosti.

Skladnost: Zahteve ne povzročajo konfliktov z drugimi funkcionalnostmi, saj se osredotočajo na hrambo videoposnetkov in slik kamere, kar ne vpliva na druge komponente sistema.

Celovitost: Uporabnik (administrator) se zaveda, da je v primeru želje hrambe videoposnetkov in/ali slik dogajanja potrebno vklopiti funkcionalnost shranjevanja videoposnetka in/ali slik dogajanja in lokacijo shranjevanja.

Realističnost: Zahteve glede na dani čas in omejitve verjetno niso izvedljive, so pa primerne kot ideje za razširitve v naslednjih iteracijah.

Preverljivost: Test enote, ki preveri pravilnost nastavitve shranjevanja videoposnetka in/ali slik in lokacije shranjevanja.

### Skupine uporabnikov

- Upravljanje s skupino uporabnikov

Veljavnost: Sistem omogoča določitev članov skupine uporabnikov (SUS), katerih lokacije sistem upošteva pri odločanju za aktivacijo faze pripravljenosti. Funkcionalnost predstavlja temeljni želeni funkcionalnosti sistema.

Skladnost: Zahteva ne povzroča konfliktov z drugimi funkcionalnostmi, saj se osredotoča na administracijo skupin uporabnikov, kar ne vpliva neposredno na druge komponente sistema.

Celovitost: Uporabnik (administrator) se zaveda, da je potrebno definirati SUS za pravilno oz. pričakovano delovanje sistema.

Realističnost: Zahteva je glede na dani čas in omejitve izvedljiva.

Preverljivost: Test enote, ki preveri pravilnost nastavitve članov skupine.

### Delovanje sistema

- Avtomatski prehod sistema iz stanja mirovanja v stanje pripravljenosti
- Obdelava video pretoka in detekcija oseb
- Avtomatski prehod sistema v aktivno stanje iz stanja pripravljenosti
- Izvajanje simulacije prisotnosti
- Avtomatski prehod sistema iz aktivnega stanja v stanje pripravljenosti
- Avtomatski prehod sistema iz stanja pripravljenosti v stanje mirovanja

Veljavnost: Sistem ob izpolnitvi zahtev prehaja med stanjem pripravljenosti, v katerem čaka na zaznavo gibanja ali na ponoven prihod uporabnikov v objekt, in stanjem aktivnosti, v katerem za določen čas oponaša prisotnost uporabnikov objekta. Vse to predstavlja temeljne želene funkcionalnosti sistema.

Skladnost: Zahteve ne kažejo očitnih konfliktov z drugimi zahtevami, vendar predstavljajo glaven del funkcionalnosti sistema, zato bo njegova skladnost z ostalimi deli sistema ključna za pravilno delovanje.

Celovitost: Uporabnik se zaveda, da sistem deluje v danih dveh stanjih. Za stanje aktivnosti (oponašanja prisotnosti) pričakuje, da bo po določenem času sistem prešel v stanje pripravljenosti zaradi energetske varčnosti s porabniki. Prav tako pričakuje avtomatično deaktivacijo sistema, ko pride on (ali kateri drugi uporabnik) v bližino objekta.

Realističnost: Zahteve so glede na dani čas in omejitve izvedljive.

Preverljivost: Integracijski testi, ki preverjajo komunikacijo z napravami in zunanjimi sistemi, in testi enot, ki preverjajo interno logiko prehajanja sistema med stanji.

### Obvestila

- Pošiljanje obvestil

Veljavnost: Sistem ob aktivaciji sistema omogoča pošiljanje obvestila vsem uporabnikom. Funkcionalnost predstavlja želeno funkcionalnost sistema.

Skladnost: Zahteva ne povzroča konfliktov z drugimi funkcionalnostmi, saj glavne funkcionalnosti sistema delujejo neodvisno od pošiljanja obvestil.

Celovitost: Uporabniki se zavedajo funkcionalnosti pošiljanja obvestil ob pomembnem dogodku, kot je aktivacija sistema.

Realističnost: Zahteva je glede na dani čas in omejitve izvedljiva.

Preverljivost: Test enote, ki preverja delovanje pošiljanja obvestil .

### Ročna aktivacija in deaktivacija sistema

- Ročni preklop sistema v aktivno stanje
- Ročni preklop sistema v stanje mirovanja

Veljavnost: Sistem omogoča ročno upravljanje s sistemom, ne le za potrebe testiranja ob namestitvi, temveč tudi za potrebe zasilne zaustavitve v primeru lažnega alarma. Funkcionalnosti predstavljata temeljni želeni funkcionalnosti sistema.

Skladnost: Zahteva ne povzroča konfliktov z drugimi funkcionalnostmi, saj je namenjena “zasilni” aktivaciji oz. deaktivaciji sistema.

Celovitost: Uporabnik (administrator) se zaveda, da je potrebno s tema funkcionalnostima delovati previdno, saj vplivajo ne le na delovanje sistema zanje, temveč za vse uporabnike objekta.

Realističnost: Zahtevi sta glede na dani čas in omejitve izvedljivi.

Preverljivost: Testi enot, ki preverijo pravilnost delovanja funkcionalnosti ne glede na trenutno stanje sistema.

## 3.5 Merila uspeha

Integracija omogoča vse želene koristi, saj je bila preizkušena nasproti vsem danim uporabniškim zahtevam, po katerih smo snovali implementacijo končnega sistema. Ta je po naši oceni skladen s pričakovanji, kar lahko potrdimo tudi z naborom testov posameznih delov sistema, ki se skladajo v končno celoto.

# 4 Opis sistema

## 4.1 Pregled sistema

### Predstavitev sistema

Integracija Varko povezuje mnoge komponente v enovit varnostni sistem. Spodaj je prikazan splošen kontekstni (blokovni) diagram sistema.

<p align="center">
  <img src="gradivo/img/Osnutek%20sistema/opis_sistema.png" alt="Opis sistema">
</p>

Sistem Frigate je namenjen prepoznavi ljudi v video prenosu, ki ga zagotavljajo nameščene kamere preko RTSP protokola. V primeru zaznave ljudi to preko MQTT protokola javi sistemu Mosquitto.

Sistem Mosquitto je posrednik sporočil protokola MQTT, po katerem poteka večina komunnikacije med sistemi znotraj naše rešitve. V primeru prejetja sporočila o zaznavi ljudi s strani sistema Frigate to sporoči sistemu Home Assistant.

Poslovna logika razvite integracije se ob prejetju sporočila o zaznavi ljudi odloči o ukrepanju, kar naredi na podlagi uporabniških nastavitev integracije ter lokacij uporabnikov, ki jih priskrbi sistem Home Assistant preko mobilne aplikacije. V primeru pravih pogojev integracija zažene varnostni odziv - simulacijo prisotnosti uporabnikov objekta preko aktivacije integriranih pametnih naprav, za kar se uporabi protokol MQTT (sporočila se posredujejo preko sistema Mosquitto).

Stanje sistema lahko administrator sistema kadarkoli nastavi tudi ročno iz uporabniškega vmesnika.

### Načrtovalski vzorci
[//]: # (TODO: DODAJ ŠE VSAJ 2 NAČRTOVALSKA VZORCA)

Pri trenutni implementaciji smo se poslužili nekaterih načrtovalski vzorcev, saj so omogočili ne le ponovno uporabo določenih delov kode, temveč tudi večjo preglednost implementacije. Izbrani vzorci so:

**Decorator**

Vzorec `decorator` smo uporabili za lažje [upravljanje z dodajanjem in odstranjevanjem Home Assistant storitev](https://github.com/TPO-2024-2025/Projekt-20/blob/b093a67c51fdb78dc1214e81a0a3696de97a1773/src/custom_components/varko/decorators.py#L9-L11) ter za [preverjanje avtorizacije](https://github.com/TPO-2024-2025/Projekt-20/blob/b093a67c51fdb78dc1214e81a0a3696de97a1773/src/custom_components/varko/decorators.py#L14-L34). Implementacije Home Assistant storitev smo ovili z dekoratorjem, ki je poskrbel, da se servis avtomatsko doda in odstrani z Home Assistant instance. Prav tako smo določene storitve ovili z dekoratorjem, ki je poskrbel, da to storitev lahko kličejo samo administratorji.

**Singleton**

Vzorec `singleton` smo uporabili pri [implementaciji posameznih managerjev](https://github.com/TPO-2024-2025/Projekt-20/blob/b093a67c51fdb78dc1214e81a0a3696de97a1773/src/custom_components/varko/services/device_manager.py#L19-L30). Te so odgovorni za svoje področje (recimo za upravljanje z skupinami, napravami, …). Z vzorcem singleton smo poskrbeli, da je vedno ustvarjena največ ena instanca posameznega managerja. S tem smo omogočili avtomatsko dodajanje in odstranjevanje storitev s pomočjo zgoraj omenjenega `decorator` vzorca.

**State**

Vzorec `state` smo uporabili za [prehajanje med stanji](https://github.com/TPO-2024-2025/Projekt-20/blob/b093a67c51fdb78dc1214e81a0a3696de97a1773/src/custom_components/varko/services/state_manager.py#L20-L93) znotraj naše integracije. Z njim smo zagotovili pravilno prehajanje med stanji sistema in ob enem ohranili kodo pregledno in enostavno.

**Entity**

Vzorec `entity` smo uporabili za [upravljanje luči](https://github.com/TPO-2024-2025/Projekt-20/blob/2aafe714672bde674a891a6cbfaddf502ba297c7/src/custom_components/varko/light.py#L46-L99). Z vzorcem smo poskrbeli za enostavnejše upravljanje z entitetami pametnih naprav.

### Izzivi implementacije

Izzivi, ki so se med razvojem razvojem sistema pojavili, so bili redki.

Eden izmed izzivov, s katerimi smo se soočili pri implementaciji logike za upravljanje s conami, je bila zahteva, da mora biti sledena naprava uporabnika sistema SUS priključena na isto omrežje kot strežnik, na katerem deluje Home Assistant. Ta pogoj je razvoj in testiranje nekoliko otežil. Rešitev omenjene težave v tej razvojni fazi še ni bila izvedena, je pa načrtovana za eno izmed prihodnjih različic sistema.

Nekaj težav se je pojavilo tudi zaradi neintuitivnega življenjskega cikla integracije sistema Home Assistant, natančneje njenih metapodatkov.

## 4.2 Osrednji arhiterkturni pogledi

### Namestitveni diagram

Na spodnji sliki je predstavljen namestitveni diagram sistema.

Glavni koordinator izvajanja sistema je `Docker Compose`, ki se sam izvaja v okolju `Docker Host`. `Docker Compose` koordinira posamezne vsebnike, vsak predstavlja svojo funkcijo - `Frigate` kot sistem za prepoznavo ljudi na video posnetku v primeru zaznave subjekta pošlje sporočilo v protokolu MQTT, ki se preko `MQTT posrednika` prepošlje sistemu `Home Assistant`, ki pa vsebuje integracijo Varko. Tako `Frigate` kot `MQTT posrednik` potrebujeta konfiguracijsko datoteko. `Brskalnik` in `Telefon` nista ovita v posebno okolje saj delujeta na večini operacijskih sistemov; oba komunicirata z glavnino sistema preko protokola HTTP(S). `Telefon` se uporablja za zaznavanje lokacije uporabnika.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_namestitveni.png" alt="Namestitveni diagram">
</p>

### Paketni diagram

Na spodnji sliki je predstavljen paketni diagram, ki prikazuje poenostavljen logični pregled sistema.

Paket `VarkoPlošča` predstavlja naš lasten uporabniški vmesnik, ki komunicira z naslednjimi paketi:
- `UpravljanjeStanj` skrbi za ustrezno prehajanje stanj našega sistema,
- `UpravljanjeSUS` skrbi za dodajanje / odstranitev članov SUS (skupina uporabnikov sistema),
- `UpravljanjeCon` skrbi za logiko med uporabniki, ki so del SUS in izbrano cono,
- `UpravljanjeNaprav` skrbi za logiko povezano s pametnimi napravami (dodajanje / odstranjevanje, aktivacija / deaktivacija).
- `UpravljanjeRadioPostaje` skrbi za logiko povezave do API-ja z radio postajami, ki se uporablja za upravljanje zvočnih integriranih naprav.
- `Store` in `Entitete` so abstrakcije, zagotovljene s strani sistema Home Assistant, ki jih integracija uporablja za delovanje - shrambo in dostop do "entitet" (npr. uporabniki, naprave, ...) definiranih v sistemu Home Assistant.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_paketni.png" alt="Paketni diagram">
</p>

### Komponentni diagram

Na spodnji sliki je predstavljen komponentni diagram sistema.

Komponenti `Frigate` in `MQTT posrednik` se preko vmesnikov povezujeta v dejansko integracijo. Ta ima podobno notranjo zgradbo, kot je opisana pri paketnem diagramu. `Device manager` in `State manager` se preko vmesnika povezujeta na `Entitete`, ki predstavljajo logične celote, integrirane v sistem Home Assistant. `Base manager` se preko vmesnika povezuje na `Shrambo`, ki predstavlja interno shrambo, ki jo sistem Home Assistant ponuja vsem integracijam. `UpravljanjeRadioPostaje` priskrbi radijske postaje - avdio prenos, ki naj se predvaja na napravah.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_komponentni.png" alt="Komponentni diagram">
</p>

### Diagram prehodov stanj

Spodnji diagram prikazuje diagram prehodov stanj, kjer so označena tri glavna (in tudi edina potrebna) stanja sistema Varko (`ACTIVE`, `READY`, `IDLE`) in ustrezni prehodi med njimi. Za uporabo tovrstnega diagrama smo se odločili zaradi narave našega sistema. Celotno delovanje in interakcije z zunanjimi napravami so namreč odvisne od trenutnega stanja, poleg tega pa smo v implementaciji uporabili načrtovalski vzorec State.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_stanj.png" alt="Diagram prehodov stanj">
</p>

### Diagram zaporedja

Spodnji diagram prikazuje splošen diagram zaporedja delovanja integracije. Sledeči akterji ostajajo enaki kot v zgornjih diagramih. Zgornji del diagrama prikazuje prehod in delovanje v stanje READY, spodaj še za stanje READY in na koncu prehod v osnovno stanje IDLE. Pomen stanj je opisan v diagramu prehodov stanj.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_zaporedja.png" alt="Diagram zaporedja">
</p>

### Razredni diagram

Spodnji diagram prikazuje razredno strukturo implementiranega sistema.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/diagram_razredni.png" alt="Razredni diagram">
</p>

# 5 Končno stanje

## 5.1 Osnutek delovanja

Sistem na podlagi lokacije uporabnikov določi, kdaj se mora aktivirati. Lokacija uporabnikov se pridobiva s pomočjo v Home Assistant že vgrajene podpore za sledenje lokacije uporabnikov preko, s strani uporabnika določenih, lokacijskih con, ki bodo sužile kot meje za določanje prisotnosti uprabnikov.

V primeru odsotnosti vseh uporabnikov objekta (glede na določeno lokacijsko cono) bo sistem prešel v način "samodejnega varnostnega načina" - stanje "READY". Varnostna kamera v tem primeru spremlja okolico in preko RTSP protokola prenaša video prenos v živo, do katerega lahko dostopa sistem Frigate. Ta izvaja detekcijo oseb na danem prenosu, ter ob zaznavi proži dogodek preko MQTT protokola.

Če je v času do vrnitve vsaj enega uporabnika objekta v takem stanju sistema zaznano gibanje, sistem Frigate pošlje zahtevo preko MQTT posrednika na sistem Varko, ki poskrbi za samodejno proženje ustreznih ukrepov v obliki upravljanja naprav, povezanih z integracijo, s čimer ustvari vtis prisotnosti ljudi v objektu. Prav tako sistem uporabnikom pošlje obvestilo o prožitvi sistema.

## 5.2 Uporabljene komponente sistema, namestitev in testiranje

### Uporabljene platforme, knjižnice in orodja

Za razvoj sistema bomo uporabili različne platforme, orodja in knjižnice, ki omogočajo enostavno integracijo, obdelavo videa in avtomatizacijo procesov:

- **Home Assistant**: Centralna platforma, ki bo povezovala uporabniško lokacijo, integracije z napravami in izvajala avtomatizirano simulacijo prisotnosti prebivajočih glede na MQTT dogodke. Uporabili smo jo, ker je razširjena platforma za upravljanje s pametnimi domovi.
- **Zone detection** (vgrajen v Home Assistant): Mehanizem za določanje prisotnosti uporabnikov na podlagi geolokacije in vnaprej določenih območij, ki bo omogočal preklapljanje sistema med aktivnim nadzorom doma (ob odsotnosti prebivajočih) in izklopljenim nadzorom (ob prisotnosti prebivajočih). Uporabili smo jo, ker je to primarni način upravljanja integracij na podlagi uporabniške lokacije v ekosistemu Home Assistant.

- **Frigate**: Odprtokodna rešitev za analizo videoposnetkov v realnem času, ki bo omogočala zaznavanje oseb na podlagi video toka s kamer. Uporabili smo jo zaradi velike količine dokumentacije in splošne primernosti za to nalogo.
- **Docker in Docker Compose**: Okolje za enostavno namestitev in upravljanje komponent sistema v izoliranih vsebnikih. Uporabili smo ju zaradi optimizacije procesa razvoja ter lažje prenosljivosti do končnih uporabnikov.
- **RTSP**: Protokol za prenos video toka s kamer v sistem za obdelavo slik in zaznavanje oseb (uporablja ga Frigate).
- **MQTT**: Protokol za sporočanje dogodkov, ki bo omogočal komunikacijo med Frigate in Home Assistant za sprožitev avtomatizacij (uporabljajo ga vsi sistemi).

Za implementacijo integracije Varko smo uporabili tudi zunanje knjižnice:
- **black formatter**: Razširitev razvojnega okolja, ki skrbi za konsistentno formatiranje kode. Uporabili smo jo zaradi splošne razširjenosti.
- **unittest**: Python knjižnica za olajšanje implementacije testov enot. Uporabili smo jo zaradi splošne razširjenosti.

Razvoj smo večinoma opravljali v razvojnem okolju **Visual Studio Code** in **Pycharm**. Uporabili smo jih zaradi predhodnega poznavanja ter primernosti za urejanje Python kode.
Pisanje dokumentacije večinoma delamo v spletnem urejevalniku **Notion**, končne popravke pa delamo kar v okolju **GitHub**, ki ga uporabljamo tudi za kontrolo verzij implementacije sistema. Uporabili smo ju zaradi lažjega procesa razvoja.

Nenazadnje smo za zagotovitev delovanja sistema potrebovali naslednje naprave in zahteve zanje:

- naprava za izvedbo Docker Compose (npr. osebni računalnik),
- dostop do omrežja,
- kamera s podporo RTSP,
- mobilni telefon z nameščeno aplikacijo Companion App (Home Assistant),
- pametne naprave, ki so podprte v sklopu našega sistema (pametne luči in televizija).

## 5.3 Namestitev
[//]: # (TODO: STANJE KJE JE APLIKACIJA KONČNO NAMEŠČENA)

Za uspešno namestitev sistema je potrebno vzpostaviti in skonfigurirati naslednje komponente:

- **Home Assistant**: uporabi se uradna slika Docker za platformo Home Assistant. Potrebna konfiguracija vključuje definicijo poti do konfiguracijske mape, nastavitve ustreznih vrat za dostop do platforme ter druge sistemske nastavitve.
- **Frigate**: uporabi se uradna slika Docker za sistem procesiranja video vsebin Frigate. Potrebna konfiguracija vključuje določanje poti za video tok (IP kamere, ki prenaša video preko RTSP protokola), nastavitev vrat za dostop do uporabniškega vmesnika, ter omogočenje dostopa do omrežja obdelovanje video vsebin v realnem času.
- **MQTT Broker**: uporabi se ločen vsebnik Docker za posrednika MQTT, saj vsebniška različica sistema Home Assistant nima podpore posredništva MQTT sporočil. Potrebna konfiguracija vključuje nastavitev ustreznih vrat za povezovanje z drugimi napravami, določitev poti do konfiguracijskih datotek, ter omogočenje dostopa do omrežja za komunikacijo med sistemom Home Assistant, sistemom Frigate in drugimi napravami v objektu.
- **Mobilna aplikacija**: za pridobivanje uporabniške lokacije in uprabljanje z nastavitvami sistema se uporablja mobilno aplikacijo Home Assistant, ki je dostopna za mobilna operacijska sistema iOS in Android.

Za enostavno upravljanje glavnih komponent sistema (Home Assistant, Frigate, posrednik MQTT) se uporabi Docker Compose, ki omogoča enostaven zagon in povezovanje večih vsebnikov. Vse ustrezne nastavitve, vključno z vrati, potmi do konfiguracijskih datotek in parametri za posamezne komponente, so tako definirane v .yaml datoteki, kar bo omogočilo enostavnejšo konfiguracijo, tako med razvojem kot za končne uporabnike.

## 5.4 Delovanje sistema
[//]: # (TODO: POPRAVI OPIS IN SLIKE ZA UI)

Uporabniški vmesnik je izdelan kot ločena plošča v sistemu Home Assistant, kjer uporabnik dostopa do nastavitev integracije. Do nje lahko dostopa uporabnik sistema Home Assistant preko glavnega menija na levi strani kontrolne plošče.

Na spodnjih slikah je prikazana kontrolna plošča integracije, ki omogoča:
- upravljanje z integriranimi napravami - dodajanje in odvzemanje naprav iz uporabe
- upravljanje z lokacijskimi conami - določitev lokacijske cone za uporabo pri delovanju sistema
- upravljanje s skupino uporabnikov - dodajanje in odvzemanje uporabnikov sistema Home Assistant iz uporabe pri delovanju sistema
- upravljanje s stanji sistema - ročna nastavitev stanja sistema

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/ui_general.png" alt="Kontrolna plošča">
</p>

Spodnja slika predstavlja pojavno okno z menijem, ki se pojavi ob kliku na opcijo "Add device". Vsebuje vnosna polja, ki jih je potrebno pred potrditvijo izpolniti.

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/ui_detail.png" alt="Odprt meni kontrolne plošče">
</p>

Do določenih nastavitev lahko dostopa le administrator sitema Home Assistant, do ostalih pa tudi drugi avtenticirani uporabniki. Ob poskusu nedovoljenega dostopa do funkcionalnosti se uporabniku prikaže obvestilo o premajhnih pooblastilih.

Na dani [povezavi](https://drive.google.com/file/d/1jkdYJKgqECaB8Iw7G31vEh_gptoYXKOg/view) je dostopen video, na katerem je ravidno delovanje ročne aktivacije/deaktivacije sistema (stanja ACTIVE/READY), in s tem posledično tudi vklopa/izklopa simulacije prisotnosti (ta v danem primeru prižge luč).
Iz videa je razvidno, da se v primeru ročne aktivacije sistema (nastavitev v stanje ACTIVE) luč v sklopu simulacije prisotnosti prižge, in ob ročni deaktivaciji sistema (nastavitev v stanje IDLE) ugasne.

Na dani [povezavi](https://drive.google.com/file/d/19v6aEoE9l4VhLSqn-DFdoqN5If0By1lX/view) je dostopen video, na katerem je razvidno delovanje avtomatske aktivacije/deaktivacije sistema (stanja READY/IDLE) na podlagi lokacije uporabnika ter določene lokacijske cone, s pomočjo česar sistem določi pravilne ukrepe.
Iz videa je razvidno, kako sprememba velikosti in pozicije cone vpliva na stanje sistema, odvisno če se v novonastavljeni coni še vedno nahaja uporabnik.

Na dani [povezavi](https://drive.google.com/file/d/1FJD9dj0E-LkcjZEMBeXM4hx7w_e-NBLt/view) je dostopen video, na katerem je razvidno delovanje avtomatske aktivacije/deaktivacije sistema (stanja ACTIVE/READY) na podlagi lokacije uporabnika, določene lokacijske cone ter video prenosa, na katerem sistem zaznava/ne zaznava človeka.
Iz videa je razvidno, kako, kot v prejšnjem videu, nastavitev lokacijske cone vpliva na stanje sistema. V stanju pripravljenosti (stanje READY) se nato sistem na podlagi prepoznave osebe odloči za aktivacijo sistema, ob umiku osebe iz kadra pa se deaktivira.

Na dani [povezavi](https://drive.google.com/file/d/1o_g5KD_7A9K8NYkgzexKum-Ds1HNtw0z/view) je dostopen video, na katerem je razvidno delovanje dodajanja in odstranjevanja uporabnikov iz uporabniške skupine.
Iz videa je razvidno, kako po tem, ko dodamo novo osebo oz. njen telefon med uporabnike, sistem začne tej osebi slediti. Ko osebo odstranimo, ji sistem ne sledi več.

Diagrami sestave razvitega sistema in izzivi pri razvoju so vidni v 4. poglavju (opis sistema).

### Testiranje

V času razvojnega procesa smo testirali posamezne gradnike prototipa sistema Prav tako smo pripravili zbirko testov enot, s katerimi bi lažje zagotavljali kakovost produkta in sebi olajšali proces razvoja.

Sistem mora biti testiran v čimbolj realnih pogojih, da se zagotovi zanesljivo delovanje (na primer testiranje zaznavanja oseb mora delovati tudi v primeru da je v okviru kamere viden le del človeka).

Testiranje s testi enot se izvaja avtomatično preko Github Actions, ki se poženejo na vsakem Pull Requestu. Tako se še pred združitvijo kode na glavno vejo preverja novo-napisano kodo.

Skupno je bilo napisanih 78 testov enot, ki testirajo funkcionalnosti sistema.

[//]: # (TODO: POSODOBI ŠTEVILKE)

Ustreznost testne strategije bomo ovrednostili s pokritostjo kode:

[//]: # (TODO: POKRITOST KODE S TESTI)

### Statistika končne implementacije prototipa sistema

Do končne implementacije prototipa sistema smo napisali 4025 vrstic kode, od tega 82% v Pythonu, 6% v JavaScriptu, 2% v HTML, 4% v CSS, ostalo pa so konfiguracijske datoteke, potrebne za delovanje sistemov. Razlika med številoma vrstic kode prototipa in razvite implementacije tako znaša 3245 vrstic kode.

[//]: # (TODO: POSODOBI ŠTEVILKE)

# 6 Vodenje projekta

Projektno vodenje bo potekalo z inspiracijo [Scrum-ov](https://www.scrum.org/resources/what-scrum-module). Sprinti se bodo v veliki meri ujemali z roki oddaje posamezne iteracije. Na ta način bomo poskrbeli, da bo delo ekipe znotraj sprinta čim bolj usklajeno sprotnimi zahtevami projekta.
Za organizacijo bomo uporabljali [GitHub Issues](https://github.com/TPO-2024-2025/Projekt-20/issues?q=is%3Aissue), ki bodo služili tudi kot **backlog**.

Najprej smo razvili prototip, ki je predstavljal minimalno delujoč sistem in je zajemal naslednje funkcionalnosti:

- Ročna aktivacija sistema preko mobilne naprave
- Integracija z eno pametno napravo

Po konsolidaciji pomislekov in predlogov, ki so se pojavili med in po razvitju prototipa, smo začeli z implementacijo končnega produkta.

[//]: # (TODO: DOPOLNI KONEC IMPLEMENTACIJE)
Ključni dogodki, ki so se zgodili med implementacijo:
- Vzpostavitev razvojnega okolja - 24.3.2025 ([PR](https://github.com/TPO-2024-2025/Projekt-20/pull/32))
- Začetek dela na prototipu - 27.3.2025 ([PR](https://github.com/TPO-2024-2025/Projekt-20/pull/34))
- Implementiran prototip - 6.4.2025 ([PR](https://github.com/TPO-2024-2025/Projekt-20/pull/44))
- Izboljšave kontinuirane integracije (CI) - 6.4.2025 ([PR](https://github.com/TPO-2024-2025/Projekt-20/pull/45))
- Začetek implementacije končnega produkta - 21.4.2025 ([PR](https://github.com/TPO-2024-2025/Projekt-20/pull/53))
- Dodan CI na GitHub Actions - 4.5.2025 ([PR](https://github.com/TPO-2024-2025/Projekt-20/pull/74))
- Konec implementacije končnega produkta -

## 6.1 Usklajevanje ekipe

### Sestanki ekipe

Ekipa se bo vedo sestajala enkrat na teden proti koncu tedna.

Sestanki se bodo odvijali pred koncem vsakega sprinta za pregled dela, ki ga je še potrebno dokončati, in ob začetku vsakega sprinta za pregled možnih izboljšav glede na prejšnjem sprintu, ter pregled izzivov, ki jih bomo v danem sprintu poizkusili rešiti.

Po potrebi se lahko posamezni člani v primerih nejasnosti ali potrebe po pomoči drugih članov med seboj domenijo za dodatne termine sestankov.

### Cilj sestankov

Cilj tedenskih sestankov je usklajevanje do sedaj opravljenih nalog z ekipo. Po sestankih je jasno, kaj je bilo do sedaj narejeno, in kaj nas še čaka v tekočem sprintu.
Cilj sestankov ob koncu sprinta je, da z ekipo skupaj pogledamo izdelek ob koncu sprinta in drug drugemu izpostavimo morebitne pomankljivosti in s tem zagotovimo boljšo kvaliteto izdelka ob koncu sprinta.

Cilj sestankov ob začetku sprinta je, da imamo jasno določene cilje novega sprinta. Poleg tega je cilj tudi, da lahko vsi člani ekipe pred vsemi predstavijo svoje predloge za izboljšave dela v prihajajočih sprintih.

Cilji sestankov so bili doseženi, saj smo se lahko iz iteracije v iteracijo prilagajali izkušnjam prejšnjih iteracij, kar nam je omogočilo agilen pristop k problemom, na katere smo naleteli. Izvedli smo vse zastavljene sestanke ob koncih in začetkih iteracij, prav tako smo redno sklicevali izredne sestanke za hitro izmenjavo znanj in informacij o poteku dela.

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

Kritična pot je označena s simbolom :blue_square:, torej zaporedna opravila s tem simbolom predstavljajo kritično pot.

| OPRAVILA | sprint | začetek | konec | trajanje (delovni dnevi) | drsni čas (delovni dnevi) | odvisen od |  rezultat aktivnosti |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **1 Predlog projekta** | —————— | —————— | —————— | —————— | —————— | —————— | —————— |
| :blue_square: 1.1 Projektna ideja | 1 | 24.2 | 25.2 | 2  | 2 | / | Zasnovana projektna ideja - dokumentacija |
| 1.2 Zajem zahtev | 1 | 24.2 | 25.2 | 2 | 13 | / | Zajete zahteve - dokumentacija |
| 1.3 Tehnični načrt projekta | 1 | 26.2 | 3.3 | 4 | 9 | 1.1, 1.2 | Zasnovan tehnični načrt izvedbe projekta - dokumentacija |
| :blue_square: 1.4 Razdelitev vlog članov skupine | 1 | 26.2 | 26.2 | 1 | 2 | 1.1 | Razdelitev predvidenih vlog članov ekipe - dokumentacija |
| :blue_square: 1.5 Finančni in časovni načrt projekta | 1 | 27.2 | 12.3 | 10 | 2 | 1.1, 1.4 | Dokončan COCOMO-2 finančni načrt ter časovni načrt projekta - dokumentacija |
| 1.6 Opredelitev tveganj | 1 | 26.2 | 4.3 | 5 | 8 | 1.1 | Opredeljene možnosti tveganj projekta - dokumentacija |
| **2 Osnutek sistema** | —————— | —————— | —————— | —————— | —————— | —————— | —————— |
| 2.1 Vzpostavitev okolja | 2 | 17.3 | 18.3 | 2 | 1 | 1.5 | Vzpostavljeno razvojno okolje |
| :blue_square: 2.2 Retrospektiva in načrt iteracije | 2 | 17.3 | 17.3 | 1 | 1 | 1.3, 1.5, 1.6 | Zasnovan načrt iteracje - dokumentacija |
| :blue_square: 2.3 Izdelava osnovnega delujočega sistema (prototipa) | 2 | 19.3 | 1.4 | 10 | 1 | 2.1, 2.2 | Izdelan prototip sistema |
| :blue_square: 2.4 Izdelava poročila o stanju | 2 | 2.4 | 3.4 | 2 | 1 | 2.3 | Dokumentacija |
| **3 Izvedljiv sistem** | —————— | —————— | —————— | —————— | —————— | —————— | —————— |
| :blue_square: 3.1 Retrospektiva in načrt iteracije | 3 | 7.4 | 7.4 | 1 | 0 | 2.4 | Zasnovan načrt iteracje - dokumentacija |
| :blue_square: 3.2 Izdelava arhitekturnega načrta | 3 | 8.4 | 10.4 | 3 | 0 | 3.1 | Zasnovan arhitekturni načrt implementacije sistema |
| :blue_square: 3.3 Izdelava poročila o stanju | 4 | 30.4 | 30.4 | 1 | 0 | 3.5, 3.6 | Dokumentacija |
| :blue_square: 3.4 Zaledni sistem in njegovo testiranje | 3 | 11.4 | 18.4 | 6 | 0 | 3.2 | Implementiran zaledni sistem in njegovi testi enot |
| 3.5 Uporabniški vmesnik (frontend) in njegovo testiranje | 4 | 22.4 | 29.4 | 6 | 0 | 3.4 | Implementiran uporabniški vmesnik in njegovo razvojno testiranje |
| :blue_square: 3.6 Integracija pametnih naprav in njihovo testiranje | 4 | 22.4 | 29.4 | 6 | 0 | 3.4 | Integracija vsaj ene pametne naprave |
| **4 Končna izdaja** | —————— | —————— | —————— | —————— | —————— | —————— | —————— |
| :blue_square: 4.1 Retrospektiva in načrt iteracije | 5 | 5.5 | 5.5 | 1 | 4 | 3.3 | Zasnovan načrt iteracje - dokumentacija |
| 4.2 Izdelava končnega poročila | 5 | 13.5 | 15.5 | 3 | 6 | 4.4 | Dokumentacija |
| :blue_square: 4.3 Izdelava končne dokumentacije | 5 | 13.5 | 19.5 | 5 | 4 | 4.4 | Dokumentacija |
| :blue_square: 4.4 Uporabniško testiranje | 5 | 6.5 | 12.5 | 5 | 4 | 4.1 | Uporabniško testiran končni izdelek |
| **Vodenje projektne ekipe** | / | 24.2 | 19.5 | 59  | / | / | Uspešno izveden projekt |

Aktivnosti na kritični poti so označene z modro oznako.

Vseskupaj $54$ dni iz kritične poti * $5$ študentov = $270$ ŠČD oz. ŠČU dela.
Glede na razporeditev dela pride $223$ ŠČD oz. ŠČU dela na kritični poti.

Po dnevih natančno:

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/gannt_dnevi.png" alt="Dnevni Ganntov diagram">
</p>

Po tednih natančno:

<p align="center">
  <img src="gradivo/img/Izvedljiv sistem/gannt_tedni.png" alt="Tedenski Ganntov diagram">
</p>

### Diagram PERT

<p align="center">
  <img src="gradivo/img/Osnutek sistema/pert.png" alt="Pertov diagram">
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
  <img src="gradivo/img/Predlog%20projekta/cocomo_1.png" alt="COCOMO 2 - Ocena obsega">
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

Podrobnejša delitev nalog je bila definirana v 6. poglavju poročila.

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

# 9 Refleksija

Projekt nam je ponudil dragoceno priložnost za poglobljeno spoznavanje ekosistema pametnih domov, zlasti platforme Home Assistant, in razvijanje praktičnih veščin na področju načrtovanja, implementacije in testiranja programskih rešitev v agilnem okolju. Skozi iterativni proces razvoja sistema smo se spoznali s pristopi k definiciji uporabniških zahtev, časovnih in finančnih načrtov za agilne pristope k razvoju, učinkovito smo implementirali razvojne vzorce in skalabilno arhitekturo sistema, ter se nenazadnje pobližje spoznali z agilnimi pristopi k vodenju in sodelovanju pri projektu.

Spodaj delimo ključne izkušnje, spoznanja in priporočila, ki smo jih pridobili med delom na projektu.

### Uspehi

Med projektom smo zabeležili več uspehov, ki so potrdili učinkovitost našega pristopa in izboljšali kakovost končnega izdelka:

- Agilni razvojni pristop: Uporaba širših načel metodologije Scrum in rednih retrospektivnih sestankov se je izkazala za zelo učinkovito. Omogočilo nam je hitro prilagajanje novim spoznanjem in izzivom ter sprotno izboljševanje delovnih procesov.
- Uspešna integracija komponent: Kljub začetnemu pomanjkanju izkušenj z nekaterimi orodji (Home Assistant, Frigate, MQTT) smo uspeli uspešno integrirati vse ključne komponente sistema (Home Assistant, Frigate, MQTT Broker, mobilna aplikacija) v enovit, delujoč varnostni sistem.
- Razvoj robustne poslovne logike: Implementirana poslovna logika je zasnovana za zanesljivo delovanje, kar potrjujejo tudi zasnovani in izvedeni testi.
- Avtomatizacija testiranja in CI: Vzpostavitev avtomatskega izvajanja testov enot preko GitHub Actions je pomembno prispevala k ohranjanju kakovosti kode in hitrejšemu iterativnemu razvojemu pristopu.
- Učinkovito reševanje težav z vzpostavitvijo razvojnega okolja: Kljub nekaterim začetnim težavam pri vzpostavitvi razvojnega in testnega okolja (omejitve Frigate, povezava kamere preko RTSP), smo te izzive uspešno rešili in si tako zagotovili stabilno delovno okolje.
- Dobra timska dinamika: Kljub občasnim nepričakovanim zamudam in izzivom je ekipa ohranila dobro komunikacijo, sodelovanje in motivacijo, kar je ključno prispevalo k uspešnemu zaključku projekta.

Našo najboljšo prakso bi opredelili kot kombinacijo agilnega pristopa z rednimi retrospektivami in hitre implementacije avtomatiziranih testov in procesa CI. Ta kombinacija nam je omogočila, da smo hitro identificirali in reševali probleme, kar je tudi eden glavnih ciljev vsake izvedbe projektov.

### Izzivi in rešitve

Skozi iteracije smo se s pomočjo retrospektivnih sestankov ocenjevali in izboljševali prakse, kar je prisostvovalo k uspešnemu agilnemu pristopu k problemu. Spodaj je naštetih nekaj izzivov, s katerimi smo se spopadali skozi projektno delo, in pristop ter rezultat reševanja le-teh.

Ekipa se je z ekosistemom Home Asistant srečala prvič, kar je vplivalo na daljša obdobja raziskovanja in načrtovanja strategij implementacij. Skozi iteracije projekta smo se vse bolj spoznali z zmogljivostmi in priporočljivimi praksami implementacije integracije za dani sistem, kar je vplivalo na vse hitrejše razvojne cikle posameznih funkcionalnosti, in večje zanesljivost razvite rešitve.

Začetne težave pri vzpostavitvi okolja, kot so omejitve glede uporabe okoljskih spremenljivk v sistemu Frigate, in testirnega okolja, kot je povezava spletne kamere preko RTSP protokola na implementiran sistem, smo prav tako zaradi tega hitro odpravili.

V začetnih iteracijah še nismo imeli vzpostavljenega učinkovitega procesa kontinuirane integracije (CI), ki bi olajšala iterativen razvoj in testiranje. Zato smo kar se da hitro razvili skripto, ki vzpostavljanje Docker vsebnikov avtomatizira, in tako razbremeni razvijalce.

Med drugim se je ekipa neprestano spopadala z izzivi dobavnih rokov pametnih naprav, na katerih bi razvito integracijo lahko testirali. Tako smo npr. morali izvedbo integracije zvočnika prestaviti med delovne naloge kasnejše iteracije, vendar v tej nadaljnjih težav zaradi tega ni bilo.

Nenazadnje so se skozi vse iteracije pojavljale nepričakovane zamude (npr. pri implementaciji prototipa, implementaciji končnega produkta, itd.), zaradi česar smo istočasno zaključevali razvojni proces in že izdelovali poročila. Ta smo morali zaradi sprotnih sprememb implementacije naknadno popravljati. Izziv smo reševali z rednimi sestanki ob začetkih in koncih iteracij, kjer smo čim prej opredelili natančen plan naslednje iteracije, v katerem smo upoštevali vse na novo zaznane vire zamud in nejasnosti.

# 9.1 Priporočila

Na podlagi naših izkušenj med projektom bi priporočili naslednje:

Za prihodnje projekte s podobnim obsegom in novimi tehnologijami bi namenili več časa in truda časa za poglobljeno raziskavo vseh ključnih tehnologij in orodij že v zgodnji fazi projekta. Temeljito razumevanje ekosistema, s katerim smo v vseh nadaljnjih iteracijah delali, bi lahko bistveno zmanjšalo nepričakovane težave in še bolj pospešilo razvojne cikle.

Ostalim ekipam bi priporočali čimprejšnjo vzpostavitev procesa kontinuirane integracije (CI) in drugih praks za pospešitev razvojenga procesa in odstranitev blokerjev, ki bi razvoj zavirali. Dobra implementacija naštetih procesov omogoča hitrejše in bolj samozavestno iterativno razvijanje. Tudi agilni pristop z rednimi retrospektivami se je izkazal za zelo koristnega pri sprotnem prilagajanju in reševanju težav.
