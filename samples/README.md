# Sample Email Templates

This directory contains example emails generated from the templates with fake data for documentation purposes.

## File Overview

### German Emails

- **`sample_therapy_request_de.txt`** - Therapy inquiry in German (without previous diagnosis)
- **`sample_therapy_request_de_with_diagnosis.txt`** - Therapy inquiry in German (with previous diagnosis)

### English Emails

- **`sample_therapy_request_en.txt`** - Therapy inquiry in English (without previous diagnosis)
- **`sample_therapy_request_en_with_diagnosis.txt`** - Therapy inquiry in English (with previous diagnosis)

## About the Template

Simple, direct inquiry asking about therapy availability and waiting times. The email is designed to be straightforward and personal, increasing the likelihood that therapists will respond.

## Test Data Used

All samples use fake data:
- **Therapist**: Dr. Anna Schmidt (a.schmidt@example.com)
- **German Patient**: Max Mustermann, Berlin, TK insurance
- **English Patient**: John Doe, Berlin, Allianz insurance

## Regenerating Samples

To regenerate these samples (if templates change):

```bash
python generate_samples.py
```
