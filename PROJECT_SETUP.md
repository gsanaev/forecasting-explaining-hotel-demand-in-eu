
# Data Science Projekt Template 🚀

Willkommen zu deinem Data Science Projekt! Dieses Template hilft dir dabei, dein Projekt professionell zu organisieren und transparent zu dokumentieren.

## 📋 Schnellstart: Dein Projekt in 5 Schritten

### 1. Template verwenden
- Klicke auf **"Use this template"** → **"Create a new repository"**
- Wähle einen passenden Repository-Namen für dein Projekt
- Stelle sicher, dass das Repository **public** ist (für Kurszwecke)

### 2. Repository anpassen
- [ ] `README.md` mit deinem Projektthema aktualisieren
- [ ] `PROJECT_SETUP.md` durchlesen
- [ ] Issues für dein spezifisches Projekt anpassen

### 3. Kanban-Board erstellen
- [ ] Gehe zu **"Projects"** → **"New project"**
- [ ] Wähle das **"Board"** Template
- [ ] Folge der detaillierten Anleitung unten

### 4. Issues verknüpfen
- [ ] Bestehende Issues mit deinem Board verknüpfen
- [ ] Neue projektspezifische Issues erstellen

### 5. Wöchentliche Planung einrichten
- [ ] Milestone für Projektphasen erstellen
- [ ] Labels für Kategorien anpassen

---

## 🎯 Über dieses Template

Dieses Template ist speziell für Data Science Projekte in Kursen entwickelt und bietet dir:

- **Strukturierte Projektorganisation** mit Kanban-Boards
- **Vordefinierte Aufgabenvorlagen** für typische Data Science Workflows
- **Dokumentations-Standards** für transparente Projektverfolgung
- **Flexible Anpassung** an verschiedene Projektthemen

---

## 📊 Kanban-Board Setup (Schritt-für-Schritt)

### Board erstellen
1. **Repository öffnen** → Reiter **"Projects"**
2. **"New project"** klicken
3. **"Board"** auswählen (nicht "Table" oder "Roadmap")
4. **Projektnamen eingeben**: z.B. "[Dein Name] - Data Science Projekt"
5. **"Create"** klicken

### Spalten konfigurieren
Dein Board sollte diese Spalten haben (Standard + Ergänzungen):

| Spalte | Zweck | Automatisierung |
|--------|-------|-----------------|
| **📝 Backlog** | Alle Aufgaben sammeln | Neue Issues hier |
| **🎯 This Week** | Wochenplanung | Manuell verschieben |
| **🔄 In Progress** | Aktuelle Arbeit | Auto bei Issue-Assignment |
| **👀 Review/Test** | Qualitätskontrolle | Manuell |
| **✅ Done** | Abgeschlossene Tasks | Auto bei Issue-Close |

### Spalten hinzufügen/anpassen:
1. **"+ Add column"** rechts im Board
2. **Spaltenname eingeben**
3. **Automatisierung konfigurieren** (siehe unten)

---

## 🔧 Board-Automatisierung einrichten

### Automatische Regeln konfigurieren:
1. **Board öffnen** → **"..." (drei Punkte)** → **"Settings"**
2. **"Manage access"** → **"Built-in automation"**
3. **Folgende Regeln aktivieren:**

```
✅ Neue Issues → "Backlog"
✅ Assigned Issues → "In Progress" 
✅ Geschlossene Issues → "Done"
✅ Wiedereröffnete Issues → "In Progress"
```

---

## 📋 Issue-Vorlagen nutzen

In diesem Repository findest du vordefinierte Issue-Templates:

### 1. 📊 Data Collection & Exploration
**Typische Aufgaben:**
- Datenquellen identifizieren
- Datensatz beschaffen und laden
- Erste Datenexploration (EDA)
- Datenqualität bewerten

### 2. 🧹 Data Preprocessing
**Typische Aufgaben:**
- Missing Values behandeln
- Ausreißer identifizieren
- Feature Engineering
- Daten normalisieren/skalieren

### 3. 🤖 Modeling & Analysis
**Typische Aufgaben:**
- Baseline-Modell entwickeln
- Verschiedene Algorithmen testen
- Hyperparameter-Tuning
- Model Evaluation

### 4. 📈 Visualization & Reporting
**Typische Aufgaben:**
- Ergebnisse visualisieren
- Präsentation vorbereiten
- Dokumentation vervollständigen
- Code Review

### Neue Issues erstellen:
1. **"Issues"** Tab → **"New issue"**
2. **Template auswählen** oder **"Open a blank issue"**
3. **Titel, Beschreibung, Labels** hinzufügen
4. **Milestone und Assignee** setzen (dich selbst)

---

## 🏷️ Labels und Kategorien

Nutze diese Label-Struktur für bessere Organisation:

### Priorität
- 🔴 `priority: high` - Kritische Aufgaben
- 🟡 `priority: medium` - Wichtige Aufgaben  
- 🟢 `priority: low` - Nice-to-have

### Typ
- 📊 `type: data` - Datenarbeit
- 🤖 `type: modeling` - Machine Learning
- 📝 `type: docs` - Dokumentation
- 🐛 `type: bug` - Fehlerbehebung

### Status
- 💭 `status: planning` - In Planung
- 🔄 `status: blocked` - Blockiert
- ❓ `status: question` - Frage/Unterstützung nötig

---

## 📅 Wöchentliche Arbeitsorganisation

### Milestone-Planung
1. **"Issues" → "Milestones" → "New milestone"**
2. **Beispiel-Milestones:**
   - 📊 Woche 1: Datensammlung & EDA
   - 🧹 Woche 2: Data Preprocessing  
   - 🤖 Woche 3: Erste Modelle
   - 📈 Woche 4: Optimierung & Dokumentation

### Wochenplanung-Routine
**Jeden Montag:**
1. **Issues für die Woche** von "Backlog" → "This Week"
2. **Prioritäten setzen** (max. 3-5 Issues pro Woche)
3. **Zeitschätzungen** in Issue-Beschreibungen ergänzen

**Jeden Freitag:**
1. **Fortschritt reviewen** – was ist in "Done"?
2. **Blockierte Issues** identifizieren und lösen
3. **Nächste Woche vorbereiten**

---

## 🔍 Best Practices

### Issue-Beschreibungen
**Gute Issues enthalten:**
```markdown
## Ziel
Was soll erreicht werden?

## Akzeptanzkriterien
- [ ] Kriterium 1
- [ ] Kriterium 2

## Notizen
Wichtige Hinweise, Links, etc.

## Definition of Done
Wann ist diese Aufgabe wirklich fertig?
```

### Commit-Messages
**Verknüpfe deine Commits mit Issues:**
```bash
git commit -m "Add data cleaning pipeline - closes #3"
git commit -m "Fix missing value handling - refs #3"
```

### Code-Organisation
```
├── data/
│   ├── raw/          # Originaldaten
│   ├── processed/    # Bereinigte Daten
│   └── external/     # Externe Datenquellen
├── notebooks/        # Jupyter Notebooks
├── src/             # Python/R Code
├── docs/            # Dokumentation
└── reports/         # Berichte und Präsentationen
```

---

## 🆘 Hilfe und Tipps

### Häufige Probleme

**❓ "Ich sehe mein Board nicht"**
- Das Board muss mit deinem Repository verknüpft sein
- Prüfe die Repository-Settings → Projects

**❓ "Issues erscheinen nicht im Board"**  
- Issues manuell zum Board hinzufügen
- Automatisierung prüfen und aktivieren

**❓ "Spalten-Automatisierung funktioniert nicht"**
- Board-Settings → Built-in automation
- Regeln einzeln aktivieren/deaktivieren

### Weitere Ressourcen
- [GitHub Projects Dokumentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Issue Templates Guide](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
- [GitHub Flow Workflow](https://guides.github.com/introduction/flow/)

---

## 📞 Support

Bei Fragen zum Template oder Board-Setup:
1. **Issue in diesem Repository erstellen** mit Label `question`
2. **Kursleiter kontaktieren**
3. **GitHub Community Discussions** nutzen

---

## ✨ Template Updates

Dieses Template wird regelmäßig verbessert. Um Updates zu erhalten:
1. **Watch** dieses Repository
2. **Releases** verfolgen für neue Versionen
3. **Feedback** über Issues willkommen!

---

**Viel Erfolg bei deinem Data Science Projekt! 🚀**

> Erstellt mit ❤️ für strukturierte, transparente Projektarbeit