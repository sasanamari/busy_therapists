# Finding a Therapist in Germany — Step by Step

Finding a free spot for therapy in Germany is tricky, and it can be even more difficult if you have public health insurance or need therapy in a language other than German. This tool not only helps you find and email therapists in your area, it can also help you in a process that gives you access to more therapists through your public health insurace. If you can showcase that there are no therapists available to you within the next three months, you may demand that your public health insurance pays for a licensed therapist out of their network. This tool guides and helps you in the bureaucratic process.


---

## How this works
- Copy `my_data.csv.example`, then rename the copy `my_data.csv`. Fill in your details and filters in `my_data.csv`
   - In case you're on a Windows computer and unfamiliar with csv files, you can open them with Excel for easier readability.
   - At different stages of the process, you may update this file accordingly.
- Run the main file and pick a numbered option from the menu
  - **Python users:** `python main.py` in the project folder
  - **Everyone else:** double-click the app
- The tool either searches for therapists and opens an HTML file with ready-to-send emails, or generates a letter for your insurance
- Option 1 uses your filters freely, while other options ignore certain filters because the process requires it (e.g. option 4 always looks for busy therapists regardless of your availability setting)

---

## The big picture

In Germany, public health insurance (gesetzliche Krankenversicherung) covers psychotherapy — but the number of publicly funded therapists hasn't kept up with demand. Waiting times of 3+ months are common, and many people can't find anyone available at all.

If that happens to you, there is a legal workaround: **Kostenerstattung** (cost reimbursement). Under §13 Abs. 3 SGB V, your insurer is legally required to pay for a private therapist if you can prove that the public system failed to provide timely care.

To qualify, you need to show:
1. **You need therapy** — documented by an initial evaluation with a public therapist (PTV11 form)
2. **You couldn't find a public therapist** — a contact list of 20+ therapists who had no availability
3. **You found a private therapist** who is qualified and can start soon
4. **A doctor confirms** the medical necessity

This tool helps you with steps 2 and 3. The rest of this guide walks you through the full process.

---

## Step 1: Try the straightforward route first

Use this tool to search for therapists near you who accept your insurance and have availability soon. You can filter by language, therapy method, gender, and more.

- In `my_data.csv` set **Availability** to `available now` or `up to 3 months`
- Run the tool and send the emails it generates either by clicking on the email link or copy and pasting the email content.
- If a therapist replies and it feels like a good match — you're done. Congrats! 

Contacts are saved to `output/busy_therapists.csv`. If you want to start from scratch, delete that file before running again.

If this doesn't work out (long waiting lists, no replies), continue below.

---

## Step 2: Find a private therapist

Start looking for a private therapist you actually want to work with. They need to meet two criteria:

1. **Licensed in one of these approved methods** (Richtlinienverfahren):
   - Behavioural therapy (Verhaltenstherapie)
   - Depth psychology (Tiefenpsychologisch fundierte Psychotherapie)
   - Psychoanalysis (Analytische Psychotherapie)

2. **Willing to handle the Kostenerstattung paperwork** — not all private therapists are, so ask explicitly

To search, run the main file and choose **option 2: Find a private therapist (Kostenerstattung)**.

- This option searches therapie.de for therapists who accept Kostenerstattung and have availability soon, near the zip code you set in `my_data.csv`
- It uses the **private therapist inquiry email template**, which asks the therapist to confirm both criteria above in writing
- Your other filters (language, gender, therapy method) are respected — this is someone you'll actually be working with, so finding a good fit matters

Note that therapie.de's Kostenerstattung filter is not exhaustive — not all willing therapists are listed there. If you don't find someone suitable, try searching on [complicated.life](https://complicated.life), Google, or other directories, and use the same email template to ask them directly whether they're willing to work with Kostenerstattung.

Contacts are saved to `output/private_therapists.csv`. To start fresh, delete that file before running again.

Once you've found someone promising, see them for 1–2 sessions to make sure it feels right. Note: these initial sessions may or may not be reimbursed later — you may need to pay for them out of pocket for now.

**Ask your private therapist** what forms your GP will need to fill in — they may have specific forms for you to bring to the GP appointment.

---

## Step 3: Get your PTV11 form

This is the most important document for your reimbursement application. It comes from a **probationary session** (Probatorische Sitzung) with a public insurance therapist — just 1–3 sessions, much easier to get an appointment for than full therapy.

To find a therapist for this step, run the main file and choose **option 3: Request probationary sessions (to get PTV11 + urgency note)**.

- This option searches for therapists with **public insurance**, without filtering for availability — availability filters apply to ongoing therapy slots, not probationary sessions
- It uses the **probationary session email template**, which explicitly states that you need the PTV11 form with an urgency sticker for a Kostenerstattung application

Contacts are saved to `output/probationary_therapists.csv`. To start fresh, delete that file before running again.

The therapist will assess you and fill in the PTV11 with a pre-diagnosis, and an urgency sticker. **Hold on to this form — you'll need it for your insurance application.**

**Ask the therapist:**
- Whether you also need to contact **116 117** (available by phone, app, or website) to get a referral number — some insurers require it, some don't. The therapist should know.

> **On 116 117 referrals:** A referral creates a useful paper trail. The downside is you might lose control over which therapist you're assigned to in the initial assessment. You might be sent to a German-only therapist or a group therapy session.
>
> - **Language:** Frustratingly, not speaking German isn't a legally accepted reason to turn down a therapist. However, if you show up and the therapist cannot provide adequate care in your language, they can decline to treat you — which is a valid outcome. Bring a short written note in German explaining the situation if needed.
> - **Group therapy:** If you're assigned to group therapy and your symptoms make it genuinely unsuitable (for example, social anxiety that prevents you from participating), you can decline on the grounds that it is not compatible with your clinical needs.

---

## Step 4: Build your rejection list

You need to show your insurer that you contacted at least 20 public therapists and none could see you within a reasonable time. **Do this last among steps 2–4** — you want the waiting times to be as recent as possible when you apply.

Run the main file and choose **option 4: Contact public therapists for insurance documentation**.

- This option always searches for therapists with **public insurance** and long wait times, near the zip code you set in `my_data.csv`. The other filters (language, gender, therapy method) are ignored to maximise the number of contacts. The number of therapists to contact is also set in `my_data.csv` — 20–30 is recommended.
- It uses the same **therapy request email template** as option 1, and appends results to `output/busy_therapists.csv` — so your contact list from step 1 carries over. To start from scratch, delete that file before running.

You don't need to filter by language, gender, or therapy method — legally, availability is what matters, not whether the therapist would have been a perfect match.

- Contact at least **20 therapists** — more is better if you want to move faster
- No reply is also valid, but give it 1–2 weeks before counting it
- Contact a few extra upfront if you'd rather not wait on stragglers
- If therapists already turned you down in step 1, they count too — they're already in `output/busy_therapists.csv`

Track responses manually in `output/responses.csv` as replies come in. When you run option 5, the tool converts this into a formatted PDF (`output/contact_log.pdf`) ready to attach to your insurance application.

---

## Step 5: Get a note from your GP

Ask your GP (or psychiatrist, if you're already seeing one) for:
- A **medical certificate of necessity** (Ärztliche Notwendigkeitsbescheinigung)
- A **consultation report** (Konsiliarbericht)

This is straightforward — tell them you've been struggling (depression, anxiety etc which has caused difficulty functioning at work, school, or in daily life) and need documentation to support a therapy application. Bring any forms your private therapist gave you. Don't stress about this appointment — it's mostly filling out forms, not a deep medical examination.

---

## Step 6: Submit your application

Run **option 5: Apply for reimbursement** to generate the insurance application email and `output/contact_log.pdf` automatically.

Before running, make sure `my_data.csv` has your **Insurance email** filled in — the letter will be addressed there. The tool will then ask you to select your private therapist from the list built in step 2, or enter their name and email manually if you found them outside the tool.

Once you have everything, attach the following to the email before sending:

- ✅ Contact log (`output/contact_log.pdf`)
- ✅ PTV11 form with urgency sticker
- ✅ Confirmation from your private therapist (licensed method + willingness to do paperwork)
- ✅ Ärztliche Notwendigkeitsbescheinigung + Konsiliarbericht from your GP

**How to submit:**
- Email is a good first step
- If there's a branch office near you, a **personal visit** is worth it — harder to ignore than an email, and perhaps less stressful than a phone call. Although, an email is technically sufficient. 

---

## Step 7: Wait — then follow up if needed

Your insurer should respond within about a month. If they don't:

1. **~4 weeks with no reply:** Run **option 6: Follow up** — make sure **Application date** is filled in `my_data.csv` (the date you sent your application)
2. **~5 weeks, still nothing:** Run **option 8: Legal threat** — requires both **Application date** and **Follow-up date** in `my_data.csv`
3. **Application rejected:** Run **option 7: Appeal a rejection** — requires **Rejection date** in `my_data.csv` (the date on the rejection letter). The tool will also ask you to confirm your private therapist, same as in step 6.

> You don't need a lawyer. Silence and rejection are standard tactics insurers use to discourage costly claims. A firm, formal response is almost always enough when your paperwork is complete.
