# :orange_square: Osnutek sistema (1. poročilo o stanju)

| [:arrow_backward:](01_Predlog_projekta.md) Prejšnji dokument |                       Trenutni dokument                       | Naslednji dokument [:arrow_forward:](03_Izvedljiv_sistem_2_porocilo_o_stanju.md) |
| :----------------------------------------------------------- | :-----------------------------------------------------------: | -------------------------------------------------------------------------------: |
| :yellow_square: **Predlog projekta**                         | :orange_square: **Osnutek sistema**<br>(1. poročilo o stanju) |                    :green_square: **Izvedljiv sistem**<br>(2. poročilo o stanju) |

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

Vzpostavitev razvojnega okolja vključuje nastavitev Docker vsebnikov za:

- sistem Frigate, namenjen prepoznavi subjektov vhodnem v video prenosu iz varnostnih kamer,
- sistem MQTT posrednika, namenjenega povezavi sistemov in naprav preko protokola MQTT,
- sistem Home Assistant, ki je glavni gradnik sistema, ki povezuje vse ostale

To predstavlja potreben korak za nadaljevanje dela na naslednji določeni delovni nalogi - izdelava osnovnega delujočega sistema - prototipa. Prototip naj bi ključeval osnovne postopke delovanja Docker vsebnikov ter dejanskega prototipa izdelovanega sistema (integracije).

V okviru načrtovanja ni bilo predvideno, da bi prototip vključeval integracijo pametnih naprav, saj ni bilo jasno, kdaj lahko pričakujemo pridobitev dobavljenih komponent.

Za zaključek iteracije smo načrtovali izdelavo poročila o osnutku sistema, v katerem obrazložimo narejeno delo te iteracije.

### Doseženi cilji iteracije

Ekipa je dosegla vse zastavljene cilje, torej končni produkt te iteracije vsebuje prototip, ki vsebuje delujoče zunanje dele sistema, ter prototip integracije. Ta kljub dvomih o časovnem roku dobave testirne pametne naprave v fazi načrtovanja nam je vseeno uspelo implementirati in testirati tudi integracijo s pametno žarnico, saj smo le-to pridobili še pred zaključkom razvojne faze iteracije.

## 1.2 Spremembe

Večjih sprememb načrta implementacije sistema iz prve iteracije (predloga projekta) nismo zaznali, kar pripisujemo dobri predstavitvi osnutka sistema iz prve iteracije.

V drugi iteraciji se je le spremenil načrt glede prototipa integracije s pametno napravo, ki je zaradi ugodnih okoliščin dobave materiala vseeno prišel pred pričakovanim rokom.

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

Uporabniški vmesnik je izdelan kot ločena plošča v sistemu Home Assistant, kjer uporabnik dostopa do nastavitev integracije. V prototipu vmesnika je na plošči za vsako storitev implementiran:

- Naslov storitve
- Vnosna polja za vhod storitve
- Gumb za aktivacijo

<p align="center">
  <img src="gradivo/img/Osnutek%20sistema/zaslonska_maska_1.png" alt="Opis sistema" width="1000">
</p>

<p align="center">
  <img src="gradivo/img/Osnutek%20sistema/zaslonska_maska_2.png" alt="Opis sistema" width="500">
</p>

#### Vmesniki do zunanjih sistemov

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

- **Upravljanje verzij in razvojni proces:** Vsa koda mora biti shranjena v GitHub repozitoriju, pri čemer morajo biti vse spremembe dokumentirane z jasnimi sporočili ob oddaji sprememb (*commit messages*) in izvedbami zahtev za združitev (*pull requests*), poleg tega pa morajo biti slednja pregledana s strani vsaj enega drugega razvijalca pred združitvijo v glavno vejo. Zaradi preglednosti kode se mora izvajati tudi redno formatiranje kode z uporabo Black formatter, kar se izvaja preko uporabe Makefile.
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

## 3.5 Slovar terminov

Slovar terminov vsebuje izraz, ki se v poročil nahaja, in njegov pomen.

| Têrmin | Opis |
| --- | --- |
| SUS | Skupina uporabnikov sistema; uporabniki, ki so s strani administratorja dodani v integracijo. |
| Potisno obvestilo (ang. push notification) | Obvestilo, ki se samodejno prikaže uporabniku na napravi, brez potrebe po odprtju aplikacije. |
| IoT (ang. Internet of Things) | Koncept, kjer so naprave in objekti povezani v omrežje, omogočajo izmenjavo podatkov ter omogočajo daljinsko spremljanje, upravljanje ali avtomatizacijo nalog. IoT naprave so pogosto opremljene s senzorji, aktuatorji in povezljivostjo za omrežje. |
| MQTT | Protokol za prenos sporočil, ki se pogosto uporablja za IoT naprave. |
| MQTT tema (ang. topic) | Naslov v protokolu MQTT, preko katerega se pošiljajo in prejemajo sporočila med napravami ali strežniki. Teme omogočajo kategorizacijo sporočil. |
| Mosquitto | Mosquitto je odprtokodni MQTT strežnik (broker), ki omogoča prenos sporočil med napravami v IoT sistemu. Implementira MQTT protokol in omogoča napravam in sistemom, da komunicirajo s pošiljanjem in prejemanjem sporočil preko tem. Pogosto se uporablja v IoT aplikacijah za obvladovanje podatkovnih tokov v realnem času. |
| Frigate | Frigate je odprtokodna programska oprema za video nadzor v realnem času z zaznavanjem objektov, ki se pogosto uporablja z IP kamerami. Omogoča integracijo z različnimi sistemi za avtomatizacijo doma in je sposobna izvajati naloge, kot so zaznavanje gibanja in sledenje objektom z uporabo modelov strojnega učenja. |
| RTSP (Real-Time Streaming Protocol) | Protokol, ki omogoča prenos video in avdio podatkov preko omrežja v realnem času. Pogosto se uporablja za video nadzor (kamere). |
| Integracija Varko | Razvita integracija v Home Assistant. |
| Stanje mirovanja sistema | Stanje sistema Varko, ko je v izbrani lokacijski coni prisoten vsaj en uporabnik z nameščeno Home Assistant aplikacijo in je ta uporabnik del SUS. V tem stanju sistem ne spremlja zaznav oseb in ne komunicira z zunanjimi napravami. |
| Stanje pripravljenosti sistema | Stanje sistema Varko, ko se vsi uporabniki skupine SUS nahajajo izven izbrane lokacijske cone. V tem stanju sistem spremlja okolico s pomočjo kamere in je pripravljen na aktivacijo varnostnih ukrepov ob zaznavi potencialnih oseb v bližini objekta. |
| Stanje aktivnega sistema | Stanje sistema Varko, ko se vsi uporabniki skupine SUS nahajajo izven izbrane lokacijske cone in ob zaznavi osebe na posnetku izvaja simulacijo prisotnosti uporabnikov objekta. |

# 4 Opis sistema

<p align="center">
  <img src="gradivo/img/Osnutek%20sistema/opis_sistema.png" alt="Opis sistema" width="1000">
</p>

#### Predstavitev sistema

Sistem Frigate je namenjen prepoznavi ljudi v video prenosu, ki ga zagotavljajo nameščene kamere preko RTSP protokola. V primeru zaznave ljudi to preko MQTT protokola javi sistemu Mosquitto.

Sistem Mosquitto je posrednik sporočil protokola MQTT, po katerem poteka večina komunnikacije med sistemi znotraj naše rešitve. V primeru prejetja sporočila o zaznavi ljudi s strani sistema Frigate to sporoči sistemu Home Assistant.

Poslovna logika razvite integracije se ob prejetju sporočila o zaznavi ljudi odloči o ukrepanju, kar naredi na podlagi uporabniških nastavitev integracije ter lokacij uporabnikov, ki jih priskrbi sistem Home Assistant preko mobilne aplikacije. V primeru pravih pogojev integracija zažene varnostni odziv - simulacija prisotnosti uporabnikov objekta preko aktivacije integriranih pametnih naprav, za kar se uporabi protokol MQTT (sporočila se posredujejo preko sistema Mosquitto).

Simulacijo prisotnosti lahko uporabnik kadarkoli aktivira in deaktivira tudi ročno iz uporabniškega vmesnika.

#### Izzivi

Izzivi z vzpostavitvijo sistema Frigate:

- Sistem v YAML konfiguraciji podpira le dve specifični okoljski spremenljivki, uporabljeni za enkripcijo komunikacije z ostalimi deli sistema. Zaradi te omejitve uporabnik ne more nastaviti IP naslova in vrat RTSP kamere preko okoljskih spremenljivk, temveč mora po vsaki spremembi slednjih nastavitev ponovno zgraditi Docker vsebnik. Gre za privzeto omejitev delovanja sistema Frigate, na katero nimamo vpliva, a pomeni dodatno delo za uporabnika.
- Testiranje videoprenosa je brez fizične RTSP kamere nekoliko zahtevnejše. Zato smo pripravili skripto, ki omogoča uporabo spletne kamere kot RTSP vira, kar nam je omogočilo uspešno preverjanje delovanja sistema Frigate.

Izzivi z vzpostavitvijo sistema Mosquitto (MQTT Broker):

- Večjih izzivov ni bilo.

Izzivi z vzpostavitvijo sistema Home Assistant in razvite integracije:

- Sistem smo zaradi boljše prenosljivosti vzpostavili v okolju Docker. Zaradi omejitev pri vključitvi izvorne kode razvite integracije je bilo skozi velik del časa razvoja prototipa potrebno po vsaki spremembi poslovne logike v razvojnem okolju potrebno ročno ponovno zgraditi Docker vsebnike. To je predstavljalo upočasnitev razvojnega procesa. To smo z uporabo orodja `make` premostili, tako da je potreben le ponoven zagon Docker vsebnikov, zaradi česar bo razvojni proces v prihodnje deloval še toliko učinkovitejše.

Izzivi z integracijo pametnih naprav:

- Večjih izzivov ni bilo.

Izzivi pri izdelavi prototipa uporabniškega vmesnika:

- Večjih izzivov ni bilo.

# 5 Trenutno stanje

#### Delovanje sistema

Cilji iteracije so večinoma ostali isti kot v procesu načrtovanja iteracije. Kot že opisano v uvodu, se je skozi razvojni proces zaradi spremenjenih pogojev dobave uvedel še dodaten cilj razvoja prototipa integracije pametne naprave, natančneje pametne žarnice.

Trenutno delujoče stanje je razvidno iz opisov in slik vmesnikov v 3. poglavju.

Diagram sestave razvitega sistema in izzivi, ki so se med razvojem razvojem sistema pojavili, so opisani v 4. poglavju (opis sistema).

#### Testiranje

V času razvojenga procesa smo testirali vse gradnike prototipa sistema.

Pri sistemu Frigate smo testirali zmožnost prepoznave ljudi na posnetku in zmožnosti komunikacije preko protokolov RTSP (s kamerami) in MQTT (z MQTT posrednikom).

Pri sistemu Mosquitto smo predvsem testirali zmožnosti komunikacije preko protokola MQTT.

Pri sami integraciji smo med razvojnim procesom ročno testirali pravilnost vključevanja integracije v sistem Home Assistant, pravilnost povezovanja sistema Home Assistant z mobilno aplikacijo za pridobitev lokacije uporabnika, pravilnost delovanja zaslonskih mask, ter zahtevane primere uporabe, implementirane v okviru izdelave prototipa (kot so povezava in komunikacija z MQTT posrednikom za upravljanje pametnih naprav).

Zaradi narave razvojnega procesa prototipov testov enot nismo pisali, saj se je implementacija sistema hitro spreminjala.

#### Statistika končne implementacije prototipa sistema

Do končne implementacije prototipa sistema smo napisali 780 vrstic kode, od tega 52% v Pythonu, 18% v JavaScriptu, ostalo pa so konfiguracijske datoteke, potrebne za delovanje sistemov.

# 6 Vodenje projekta

Glavni cilj za nasledno iteracijo je preiti iz implementiranega prototipa z omejenimi funkcionalnostmi do implementirane in testirane Home Assistant integracije, ki je skladna z zastavljenimi zahtevami, navedenimi v 3. poglavju.

Poleg tega je (kratkoročna) želja tudi, da se čim prej vzpostavi [CI cevovod](https://en.wikipedia.org/wiki/CI/CD), ki bo skrbel za kvaliteto kode in stabilnost glavne razvojne veje na GitHub-u.

Dnevnik sprememb smo vodili v sklopu funkcije [GitHub Issues](https://github.com/TPO-2024-2025/Projekt-20/issues), kjer smo zapisovali potrebne informacije o delovnih nalogah, kot so opis, dodeljeni razvijalec, čas dodelitve in dokončanja naloge, prioritete, itd.

### 6.1 Projektni načrt

#### Ganttov diagram

Časovni načrt po dnevih natančno:

<p align="center">
  <img src="gradivo/img/Osnutek%20sistema/gannt_1.png" alt="Dnevni Ganntov diagram">
</p>

Časovni načrt po tednih natančno:

<p align="center">
  <img src="gradivo/img/Osnutek%20sistema/gannt_2.png" alt="Tedenski Ganntov diagram" width="600">
</p>

#### Diagram PERT

<p align="center">
  <img src="gradivo/img/Osnutek%20sistema/pert.png" alt="Pertov diagram">
</p>

### 6.2 Projektni načrt

- Posodobljen Ganttov diagram in graf PERT.

# 7 Ekipa

**Vsi člani so sodelovali pri**:

- retrospektivi in načrtu iteracije
- razdelitvi vlog dela
- izdelavi poročila o stanju

Natančenjši procentualni deleži so navedeni v [predlogu projekta](01_Predlog_projekta.md), natančenej v poglavju 6.2.

#### Miha Vintar

**Projektni vodja, scrum master in vodja zalednega sistema**:

- vodenje projekta
- vzpostavitev okolja Home Assistant
- definicija funkcionalnih zahtev
- izdelava dokumentacije

#### Klemen Remec

**Vodja dokumentacije in načrtovanja**:

- vzpostavitev osnutka integracije
- definicija aplikacijskega programskega vmesnika integracije
- izdelava in pregled dokumentacije

#### Tara Majkič

**Sistemski analitik**:

- časovni načrt projekta
- implementacija prototipa poslovne logike
- predstavitev funkcionalnih zahtev
- izdelava dokumentacije

#### Jaka Pelko

**Vodja ekipe za integracijo z zunanjimi napravami**:

- vzpostavitev okolja Frigate
- vzpostavitev okolja MQTT posrednika
- definicija nefunkcionalnih zahtev sistema
- predstavitev funkcionalnih zahtev
- izdelava dokumentacije

#### Jaka Čelik

**Vodja ekipe za uporabniški vmesnik**:

- izdelava prototipa uporabniškega vmesnika
- predstavitev funkcionalnih zahtev
- izdelava dokumentacije

# 8 Refleksija

#### Izzivi

V prvem delu smo morali razvijalci neučinkovito po vsaki spremembi ponovno zgraditi Docker vsebnike, kar je povzročilo počasnejši cikel od pisanja do preverjanja implementacije. Izziv smo proti koncu razrešili z uporabo orodij za avtomatizacijo upravljanja vsebnikov.

Zaradi nepričakovanih zamud pri implementaciji prototipa smo istočasno zaključevali razvojni proces in že izdelovali poročilo. Ko se je prototip v tem času spreminjal, smo neaktualne dele poročil morali popravljati, kar nam je vzelo še dodaten čas. Ob začetku naslednje iteracije bomo zato čim prej opredelili natančen plan arhitekture sistema, ki ga mislimo v dani iteraciji implementirati, kar bo tudi omejilo nesporazume glede predvidenih funkcionalnosti.

#### Uspehi

Kljub izzivom smo iteracijo zaključili uspešno še pred zaključnim rokom. Implementiran prototip vsebuje vse zamišljene funkcionalnosti, prav tako smo dosegli višjo raven razumevanja možnosti dejanske implementacije celotnega sistema.
