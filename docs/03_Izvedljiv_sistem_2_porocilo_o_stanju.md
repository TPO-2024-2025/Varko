# :green_square: Izvedljiv sistem (2. poročilo o stanju)

| [:arrow_backward:](02_Osnutek_sistema_1_porocilo_o_stanju.md) Prejšnji dokument |                       Trenutni dokument                       | Naslednji dokument [:arrow_forward:](04_Koncna_izdaja_celovito_koncno_porocilo.md) |
| :------------------------------------------------------------------------------ | :-----------------------------------------------------------: | ---------------------------------------------------------------------------------: |
| :orange_square: **Osnutek sistema**<br>(1. poročilo o stanju)                   | :green_square: **Izvedljiv sistem**<br>(2. poročilo o stanju) |                      :blue_square: **Končna izdaja**<br>(celovito končno poročilo) |

![Terminski načrt](https://teaching.lavbic.net/plantuml/svg/dPRFRk8m4CRlVehHza0NAPGOabOhL5LjjrArAxLQxQceXu6Or2JOA3PqOTL7w5lrmNOSGigVb5GhV831ytqpFu-ZN1YBcOrHMGjVVeji8fL992XyUyti5yPwnYvISSxo7TSIummdy9S1M3aHgLGY_m7maxvUwLHdS3JYxfD7RxIogoZbBIZquZBH94NM9GwJEDCp5HMvucmKZA9TnU3cykpxLP6EMQQVzrstzanaAepLPNN_upDCjH7HHmALJQOoVh9bfo-iTrBGOyHKJT6n6-mesGoLeR-4igpn92C18wtjGFzXAQfuXh40ax9f9fKrGqm5F0kHf0kIH3lB8bmG454Komp9RaTucmTUk-jn7wJP3jAg3FAD86kimXtFFyt3hcQY8XKSHMs1ey5wHzThVxIZL0uEImGU3p_OmUupFHP32_cu6bWbSAgAiNulJ_XMqZz_eEaLLYGWbtCSeneZJ4bm8Yp2CM-tUEjhxoHFEd-49vnEXJA0TakriQTQOTHi_i9bHFV0YZdCmIIpAKrJimd7FbWH2RNXWmRwr_uZf6YeWG3ee4obvEro83EasfToZWUq-9OMe8hMTAWLPzKm81ITeUU1tmAgCSEX91QUHz2QpNj2akgOq13Qn3ghefgyaEEEirLorxQpjlLNFUmPSsUS1rZ_Begme4zMM7fjE_cdhSx18t7Zn_eF6EivNPazjLLb3pjmzmhhR1BX5KJkZ9gviJ7IM37vB92W1DAjyLtZeDEOwao_lSeKGRkzQZpRzZfjTGyISTVjdKYbO465rr09DgbqAgZSBkV4Uopd1PTTBDrgB669vQp6U8s5rsC9Mi51B6wzO-47i7Hgi8IRMBeLM7vezVQgt3rrnNzoLdnUTtl2NIf9xYFSk9UzR5dni1OA3z-XLEWLIBerI7nUCjb_RX4ECQnyu8Qjy61v8It6BaWtVydu1m00 "Terminski načrt")

Do 11. tedna naj bi bila implementirana osnovna funkcionalnost sistema v obliki demo prototipa. 2. poročilo o stanju je osredotočeno na razdelka [**4 Opis sistema**](#4-opis-sistema) in [**5 Trenutno stanje**](#5-trenutno-stanje). Pri opisu sistema se je treba osredotočiti predvsem na opis arhitekture sistema.

Izogibajte se nepotrebnemu podvajanju pri opisovanju sistema. Vključite ostale informacije na najbolj ustrezna mesta, med [uvodom](#1-uvod) in [opisom sistema](#4-opis-sistema).

Za izdelavo diagramov uporabite orodje [**PlantUML**](https://plantuml.com/) in v poročilo vključite izvorno kodo diagrama v jeziku PlantUML (v mapi [`gradivo`](gradivo)), sliko diagrama pa vključite s povezavo (in ne preko neposredne vključitve binarne datoteke) preko storitve <https://teaching.lavbic.net/plantuml>, kot prikazujejo primeri vključenih diagram v tej predlogi poročila.

## :page_with_curl: Naslov projekta

## :information_desk_person: Ime ekipe: Člani ekipe

## 1 Uvod

### 1.2 Poudarki

- Kakšen je bil načrt za to iteracijo?
  - Kaj je ekipa dosegla?

### 1.3 Spremembe

- Povzemite vse večje spremembe predloga projekta.
- Vključite datum, motivacijo, opis in posledice vsake spremembe.
- Če sprememb ni bilo, samo navedite, da jih ni bilo.

## 2 Potrebe naročnika

- Na kratko opišite želeno splošno izkušnjo naročnika.

## 3 Cilji projekta

- Povzamite naročnikove težave, ki jih projekt naslavlja.
- Kakšne koristi bo prinesel projekt?

## 4 Opis sistema

### 4.1 Pregled sistema

- Predstavite sistem in glavne izzive.
  - Povzemite utemeljitve izbranih načrtovalskih odločitev.
  - Narišite kontekstni diagram, ki prikazuje, kako sistem sodeluje z zunanjimi storitvami, podatkovnimi bazami ipd. Jasno označite meje sistema.
- Na kratko pojasnite zunanje interakcije sistema.

### 4.2 Osrednji arhitekturni pogledi

- Za vsak pogled zagotovite osrednji diagram (npr. postavitveni ([deployment](https://plantuml.com/deployment-diagram)), paketni ([class](https://plantuml.com/class-diagram)) diagram oz. komponentni ([component](https://plantuml.com/component-diagram)) diagram).

  - Pri predlogu upoštevajte arhitekturne in načrtovalske vzorce.
  - Priporoča se uporaba naslednjih diagramskih tehnik (ne nujno vseh):

    - **Razredni diagram** ([Class Diagram](https://plantuml.com/class-diagram), izvorna koda :bar_chart: [PlantUML](./gradivo/plantuml/RD.puml))

      ![RD](https://teaching.lavbic.net/plantuml/svg/TPDDRi8m48NtFiN8tK2heEOFQ1O8bRO7oBeR4xlWujYLROf4sxjtY0KaG3RHwFbblZVnPEuyitvRAoXVYDj8_SKigw5Ip3du8G1BLcrMrcmrNnXbBEpMqek3RYmNDcXt-Tlpz7M1AhFMx8AuLFWc-MirFRUg6eUtJ3iy4jgJjUG2Acah9GXPD7HQihqL768Ap44PDt4YvgrSRdrSm8Sop2FWmfu4UzAn9mKuhFIgfQLjBSB7GosyuImUD76H8BKV5ZYfKOBfQr8QI6c7b1N0cHTUrgAbvZsi9B1EyOR7iKwET33i7JKB0R9EWF6vnL6QzD2pmJKl3udIynZz_3pmymv_Uir_wk6FR_0dDxHfo9JTk17y-ZG62YQAi1YDxh4kqKZ12LpjR_KfzBkMUvXHWZj17uEbSH-iES75YgBV6TxZmN0ioLneZh_5Fm00)

    - **Diagram zaporedja** ([Sequence Diagram](https://plantuml.com/sequence-diagram), izvorna koda :bar_chart: [PlantUML](./gradivo/plantuml/DZ.puml))

      ![DZ](https://teaching.lavbic.net/plantuml/svg/bPDFRvj04CNlyob6xiKvL14OgYfAhVnhJvLQkN4EKIu3Z9EjOOSk2qvTzRjt5YU69kwX1v1sv_VUl9s5iyQJysrLujKjm8Cf65SYFfD7W6PjR4sEAimeNzyxQMsHIoaElIFRQ8cj7r45hwWj_JK_-lFItDjAovZhYzs8ejoBkn1NiBlipR9ItLy1-uuxQFDWF8yXvsGpqYEEYWt_QDdc_DcizB4yxlOc_NJn_kFb0Vgh3iBafYRh_rzmC2xqHy79iXP7cJLhZ2Pu_WsN4PwUzhNv7A0UR72oeAtZ0jC9KeEBLBaik9BxgUWXCjwHiPAvME-a_0UOxC14GRqIuuDX26WwygoHG5EzdMlF4wmZFFc05NifwDtqQA0MAMYcGCLAnGCLJQFPc8i1If4QjuHTGsl1JYDOQJnWo1eS4dMO3Gw9za4S79909dio6SXqQcKpFJgCFsSBwuB_hhzSFmLH_FWOhzJvE_wgPq7y-yxgLgStlRLK0Ti28D1Fyz7QJSFxCvcUbgpWaYp3k4tSpqjbowYNVSawLW6spry40PoflVw0Vm00)

    - **Diagram aktivnosti** ([Activity Diagram](https://plantuml.com/activity-diagram-beta), izvorna koda :bar_chart: [PlantUML](./gradivo/plantuml/DA.puml))

      ![DA](https://teaching.lavbic.net/plantuml/svg/VL5DJyCm3BtxLqJY0gTfV4Y8JcDbWpCI_06lyRhGrAaIbpAX_NVSRaWH1mwnvFTU_9wJLHACqhVUR4g0r3ZkC69hBEsmz_9ENr9wLtDBBARIGZ5JRR5gwXXwjbNm8Hg9o4afrMMgj4SR1iUrsQ5Fb35LOEl41NwJWoTZ7RQA02pIs2y1At6VJWuRX_Me_mQJUQudps7lX1JtZkc4NDozFDq_hnN36CCmtShvhTSHYXtrd2t_qHnXCJl7WUcn029rX68UoaRZSKXYveLgi_xwJtzJm9Xxm6WpzBRu7QLBwFwNhw4E7sR-U3LQXGvWHMprStu0)

    - **Diagram stanj** ([State Diagram](https://plantuml.com/state-diagram), izvorna koda :bar_chart: [PlantUML](./gradivo/plantuml/DS.puml))

      ![DS](https://teaching.lavbic.net/plantuml/svg/NP91Ri8m44NtFiK8TfMG6Zkqm09HABs0kwkw66ANXYHsvJYYKjMxTuABIRoneZVFyx-bR5gFpdTD3S-IiROgpHSwRE20HNLqjZEgiBLru1sQbaRQ-86bz0TsjN_Lt_wfBe-ceJ4KT6WtiD0vUzvTrXngsZiOKRhNyCC0jZ4mcEVFqkkUMwUq2smwVzakzZkYic-TmltrxXNzqeik0HFopKb3DW5iGMPCPYjGTWLO5UK98Kj57aJE91-98XL540MJOYJEKp4FOivaFewcxBUxTvYj-rvK36Rz9uy2Zqn4Hbj4wZrGrzHxZDwDBIBB8rjIgz3WrkkU_KDgnzX66qL_oHy0)

    - **Psevdokoda**

      > **assume** vrednost1 &subseteq; C, vrednost2 &subseteq; C  
      > **let** maxVrednost1 = max {r | (s,r) &in; vrednost1}  
      > **for** (s, r) **in** vrednost2:  
      > &nbsp;&nbsp;&nbsp;&nbsp;**if** r &le; maxVrednost1 **return false**  
      > **return true**

- Za arhitekturne elemente v diagramu dodajte katalog elementov z imenom in namenom vsakega elementa.
- Za vsak element določite enega člana ekipe (tudi, če je več članov ekipe prispevalo k elementu), ki bo njen skrbnik.

## 5 Trenutno stanje

- Kakšni dodatni cilji te iteracije, poleg tega, kar je že navedeno v [uvodu](#1-uvod)?
  - Kaj deluje? Vključite posnetke zaslona.
  - Kakšni izzivi?
  - Uporabite blokovni diagram za razlago trenutnega sistema.
- Katere teste ste izvedli?
- Koliko vrstic kode ste napisali (skupno do tega trenutka)?

## 6 Vodenje projekta

_Nadaljujte z vzdrževanjem **dnevnika sprememb**. Dodaje vse nove spremembe v projektu, kjer vključite datum, opis, motivacijo in posledico vsake spremembe._

- Prikažite dnevnik sprememb do tega trenutka.
  - Kakšni so cilji za naslednjo iteracijo?
  - Kakšen je načrt za preostanek semestra?

### 6.2 Projektni načrt

- Posodobljen Ganttov diagram in graf PERT.

## 7 Ekipa

- Kakšne so bile vloge v ekipi za to iteracijo?
  - Kaj je prispeval vsak član ekipe?
  - Navedite grobo oceno prispevka posameznega člana ekipe v odstotkih.

## 9 Refleksija

- Kaj je šlo po pričakovanjih?
  - Kaj ni šlo po pričakovanjih?
  - Kakšne težave so se pojavile pri ciljih, ki jih niste dosegli?
  - Kako nameravate premagati te težave?
  - Kaj boste naredili drugače v naslednji iteraciji?
