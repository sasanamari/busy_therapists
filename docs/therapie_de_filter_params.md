# therapie.de Search Filter Parameters

Discovered 2026-04-01 by fetching the search results page HTML.
Base URL: `https://www.therapie.de/therapeutensuche/ergebnisse/`

---

## Parameters

### `ort` — Location (required)
German postal code, e.g. `10117`

### `search_radius` — Search radius in km (optional)
Default is ~10km. Use `25` as fallback when default yields too few results.

### `sprache` — Therapy language
Note: German is the implicit default and does not appear as an option here.
Only additional (non-German) languages are listed.

| Value | Deutsch | English |
|---|---|---|
| 1 | Arabisch | Arabic |
| 2 | Dänisch | Danish |
| 3 | Englisch | English |
| 4 | Finnisch | Finnish |
| 5 | Französisch | French |
| 6 | Griechisch | Greek |
| 7 | Hebräisch | Hebrew |
| 8 | Italienisch | Italian |
| 9 | Japanisch | Japanese |
| 10 | Kroatisch | Croatian |
| 11 | Chinesisch | Chinese |
| 12 | Niederländisch | Dutch |
| 13 | Norwegisch | Norwegian |
| 14 | Polnisch | Polish |
| 15 | Portugiesisch | Portuguese |
| 16 | Russisch | Russian |
| 17 | Schwedisch | Swedish |
| 18 | Serbokroatisch | Serbo-Croatian |
| 19 | Spanisch | Spanish |
| 20 | Tschechisch | Czech |
| 21 | Türkisch | Turkish |
| 22 | Ungarisch | Hungarian |
| 24 | Bulgarisch | Bulgarian |
| 25 | Gebärdensprache | Sign language |
| 26 | Persisch | Persian (Farsi) |
| 27 | Rumänisch | Romanian |
| 28 | Slowakisch | Slovak |
| 29 | Ukrainisch | Ukrainian |
| 30 | Albanisch | Albanian |

### `arbeitsschwerpunkt` — Focus / Topic
| Value | Deutsch | English |
|---|---|---|
| 1 | allg. psych. Problem - Lebensberatung | General psychological issues / life counselling |
| 2 | Angst - Phobie | Anxiety / phobia |
| 3 | Essstörung | Eating disorder |
| 4 | Persönlichkeitsstörung | Personality disorder |
| 6 | Notfall - Krise | Emergency / crisis |
| 7 | Psychose - Schizophrenie | Psychosis / schizophrenia |
| 8 | Zwang | OCD |
| 9 | Psychosomatik | Psychosomatics |
| 10 | Depression | Depression |
| 12 | Sexualität | Sexuality |
| 13 | Trauma - Gewalt - Missbrauch | Trauma / violence / abuse |
| 14 | Neurologie | Neurology |
| 15 | Sucht | Addiction |
| 16 | Supervision | Supervision |
| 17 | Coaching | Coaching |
| 18 | Stress - Burnout - Mobbing | Stress / burnout / workplace bullying |
| 19 | Psychoonkologie | Psycho-oncology |
| 20 | Schmerzen | Chronic pain |
| 21 | Trauer | Grief |
| 30 | ADHS | ADHD |
| 31 | Autismus | Autism |

### `verfahren` — Therapy method
| Value | Deutsch | English |
|---|---|---|
| 1 | Tiefenpsychologisches Verfahren | Depth psychology |
| 2 | Verhaltenstherapie | Cognitive behavioural therapy (CBT) |
| 3 | Systemische Therapie | Systemic therapy |
| 4 | Gestalttherapie | Gestalt therapy |
| 5 | Gesprächstherapie | Person-centred therapy |
| 6 | Integrative Therapie | Integrative therapy |
| 7 | Humanistische Verfahren | Humanistic approaches |
| 8 | Hypnose | Hypnotherapy |
| 9 | Kunsttherapie | Art therapy |
| 10 | Musiktherapie | Music therapy |
| 11 | Tanztherapie | Dance/movement therapy |
| 12 | Alternative Verfahren | Alternative approaches |
| 13 | Körperorientierte Verfahren | Body-oriented therapy |
| 14 | Psychoanalyse | Psychoanalysis |
| 29 | Kurzzeittherapie | Brief therapy |
| 30 | Traumatherapie | Trauma therapy |
| 31 | NLP | NLP (Neuro-linguistic programming) |
| 32 | Entspannungsverfahren | Relaxation techniques |
| 36 | EMDR | EMDR |
| 37 | Online-Beratung | Online counselling |
| 38 | Schematherapie | Schema therapy |
| 40 | Neuropsycholog. Psychotherapie | Neuropsychological psychotherapy |

### `abrechnungsverfahren` — Insurance / Payment
| Value | Deutsch | English |
|---|---|---|
| 1 | GKV: Kassenleistung | Public insurance (statutory, GKV) |
| 2 | Private Krankenversicherung | Private insurance (PKV) |
| 3 | Selbstzahler | Self-pay |
| 6 | Kostenerstattungsverfahren | Kostenerstattung (reimbursement route) |
| 7 | Kassenleistung oder Kostenerstattung | Public insurance or Kostenerstattung |
| 8 | Heilfürsorge | Civil servant healthcare (Heilfürsorge) |
| 9 | Beihilfe | Civil servant subsidy (Beihilfe) |

### `terminzeitraum` — Availability / Wait time
| Value | Deutsch | English |
|---|---|---|
| 1 | Freie Plätze vorhanden | Available now |
| 2 | Wartezeit bis drei Monate | Wait up to 3 months |
| 3 | Wartezeit über drei Monate | Wait over 3 months |
| 4 | Wartezeit über zwölf Monate | Wait over 12 months |
| krisen | Bei Krisen freie Plätze | Crisis slots available |

⚠️ Note: We previously hardcoded `terminzeitraum=4` thinking it meant "available now" — it actually means "wait over 12 months". Available now is `terminzeitraum=1`.

### `therapieangebot` — Target group / Format
| Value | Deutsch | English |
|---|---|---|
| 1 | Einzeltherapie | Individual therapy |
| 2 | Familientherapie | Family therapy |
| 3 | Gruppentherapie | Group therapy |
| 4 | Therapie für Kinder und Jugendliche | Therapy for children and adolescents |
| 5 | Paartherapie | Couples therapy |

### `geschlecht` — Therapist gender
| Value | Deutsch | English |
|---|---|---|
| 1 | Männlich | Male |
| 2 | Weiblich | Female |
| 4 | Divers | Non-binary / diverse |
| 5 | Kein Eintrag | Not specified |
