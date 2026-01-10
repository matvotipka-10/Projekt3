# Elections Scraper
### Závěrečný projket (Python část) v rámci kurzu Datový analytik s Pythonem od ENGETO.
---
### Popis: 
Cílem projektu je vytvořit **webový scraper**, který automaticky stáhne a zpracuje
**výsledky voleb do Poslanecké sněmovny ČR z roku 2017** přímo z webu volby.cz.

Program:
- přijme URL územního celku,
- projde všechny obce v daném celku,
- stáhne volební data pro každou obec,
- uloží výsledky do jednoho přehledného CSV souboru.

---

### Instalace:
Doporučeno spouštět projekt ve virtuálním prostředí.
Nejprve nainstaluj potřebné knihovny ze souboru requirements.txt:
```bash
pip3 install -r requirements.txt
```
---

### Spouštění programu:
Soubor `main.py` se spouští z příkazového řádku a vyžaduje **dva povinné argumenty**:
1. **URL adresa** územního celku z webu volby.cz
2. **Název výstupního CSV souboru**

```bash
python main.py "URL adresa" "nazev CSV"
```

---

### Ukázka:
**Vstupní parametry**:
1. https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3203
2. plzen_results

**Soupštění programu**:
```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3203" "plzen_results"
```
**Výstup**:
CSV soubor obsahující:
- kód obce,
- název obce,
- počet registrovaných voličů,
- počet vydaných obálek,
- počet platných hlasů,
- počet hlasů pro jednotlivé politické strany.





