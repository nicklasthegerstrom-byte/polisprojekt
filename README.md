# Polisens Händelsebevakning

Ett Python-projekt som hämtar och filtrerar händelser från **Polisens öppna API**.  
Användaren kan välja tidsintervall, söka efter nyckelord (t.ex. "mord", "skottlossning"), sortera händelser per ort samt öppna länkar till polisens webbplats.  

## 🚀 Funktioner
- Hämta senaste händelser (max 500) från polisens API.
- Filtrera efter tidsperiod (3h, 6h, 12h, 24h eller alla).
- Sökfunktion för att hitta specifika händelser i listan.
- Sortera händelser per ort.
- Visa klickbara länkar direkt till polisens webbplats.
- Planerade funktioner:
  - Larmfunktion (t.ex. SMS eller notiser).
  - GUI med dropdown-menyer och klickbara länkar.

## 📦 Installation

1. Klona projektet:
   ```bash
   git clone https://github.com/nicklasthegerstrom-byte/polisprojekt.git
   cd polisprojekt


   
GUI Layout (Planned)

Top Frame – Filters

Time Filter Buttons: 3h | 6h | 12h | 24h | All

Refresh Button: to manually check for new events

Middle Frame – Search

Keyword Search: input box + search button

Location Search: input box + search button

Main Frame – Event Display

Scrollable Text widget or Listbox to show events

Each event formatted nicely like in your terminal version

Bottom Frame – Exit

Quit button