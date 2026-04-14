# my_data.csv Field Reference

All fields are in the **Your data** column of `my_data.csv`. Fields marked *optional* can be left blank — if they appear in a template, they'll stay as visible placeholders so you can fill them in before sending.

---

## Your details

| Field | Required | Notes |
|---|---|---|
| Name | Yes | Your full name. Used to sign emails. |
| City | Yes | Your city. Appears in email body. |
| Zip code | Yes | Used to search for therapists near you. |
| Your insurance | Yes | `public` or `private` or `self-pay`. Used in email text. |
| Insurance company | Yes | E.g. `TK (Techniker Krankenkasse)`. |
| Symptoms | Yes | Brief description (e.g. `depression and anxiety`). Appears in email body. |
| Previous diagnosis | Optional | E.g. `ADHD`, `Generalized Anxiety Disorder`. Leave blank if none. |
| Your email | Optional | Only used in the contact log — never sent automatically. |
| Number of therapists | Yes | How many therapists to contact. 20–30 recommended. |
| Email language | Optional | `German` or `English`. Defaults to German if left blank. |

---

## Search filters

These filters apply when the tool searches for therapists (options 1–4).

| Field | Notes |
|---|---|
| Availability | `yes` = cascade from available-now to 3 months (recommended for options 1/2/4). `no` = busy therapists for documentation (option 3). Or a specific value — see below. Leave blank for no filter. |
| Therapist insurance | Used in option 1. `public`, `private`, `kostenerstattung`, or `self-pay`. Leave blank to search all. Options 2–4 override this automatically. |
| Foreign therapy language | Only needed if you want therapy in a language other than German. E.g. `English`, `Persian`. |
| Therapy format | `individual`, `group`, `family`, `couples`, or `children`. Leave blank for no filter. |
| Focus / topic | E.g. `depression`, `anxiety`, `trauma`, `ADHD`, `burnout`. Leave blank for no filter. |
| Therapist gender | `female`, `male`, or `non-binary`. Leave blank for no preference. |

For the full list of valid values for language, focus, and format filters, see [therapie_de_filter_params.md](therapie_de_filter_params.md).

---

## Insurance letter fields

These fields are used in the insurance application and appeal emails (options 5–8). All optional — leave blank to keep the placeholder visible in the email so you can fill it in before sending.

| Field | Used in | Notes |
|---|---|---|
| Insurance number | Options 5, 6, 7, 8 | Your Versichertennummer (e.g. `A123456789`). |
| Insurance email | Options 5, 6, 7, 8 | Email address of your Krankenkasse. |
| Application date | Options 6, 8 | Date you sent the Kostenerstattung application (e.g. `2026-04-01`). |
| Follow-up date | Option 8 | Date you sent the follow-up email. |
| Rejection date | Option 7 | Date on the rejection letter from your Krankenkasse. |
