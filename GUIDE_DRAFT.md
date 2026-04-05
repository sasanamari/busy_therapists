# Finding a Therapist in Germany — Step by Step

Finding a free spot for therapy in Germany is tricky, and it can be even more difficult if you have public health insurance or need therapy in a language other than German. This tool not only helps you find and email therapists in your area, it can also help you in a process that gives you access to more therapists through your public health insurace. If you can showcase that there are no therapists available to you within the next three months, you may demand that your public health insurance pays for a licensed therapist out of their network. This tool guides and helps you in the bureaucratic process.


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

- Copy `my_data.csv.example`, then rename the copy `my_data.csv`. Fill in your details in `my_data.csv`
   - In case you're on a Windows computer and unfamiliar with csv files, you can open them with Excel for easier readability.
- Set **Availability** to `available now` or `up to 3 months`
- Run the tool and send the emails it generates either by clicking on the email link or copy and pasting the email content.
- If a therapist replies and it feels like a good match — you're done. Congrats! 

If this doesn't work out (long waiting lists, no replies), continue below.

---

## Step 2: Get your PTV11 form

This is the most important document for your reimbursement application. It comes from a **probationary session** (Probatorische Sitzung) with a public insurance therapist — just 1–3 sessions, much easier to get an appointment for than full therapy.

**How to find someone:**
- Run the tool with **Insurance filter** set to `public`, and no availability filter
- Use the probationary session email template. It mentions explicitly in your email that you need the PTV11 form with an urgency sticker for a Kostenerstattung application

The therapist will assess you and fill in the PTV11 with a pre-diagnosis, and an urgency sticker. **Hold on to this form — you'll need it for your insurance application.**

**Ask the therapist:**
- Whether you also need to contact **116 117** (available by phone, app, or website) to get a referral number — some insurers require it, some don't. The therapist should know.

> **On 116 117 referrals:** A referral creates a useful paper trail. The downside is you might lose control over which therapist you're assigned to in the initial assessment. You might be sent to a German-only therapist or a group therapy session.
>
> - **Language:** Frustratingly, not speaking German isn't a legally accepted reason to turn down a therapist. However, if you show up and the therapist cannot provide adequate care in your language, they can decline to treat you — which is a valid outcome. Bring a short written note in German explaining the situation if needed.
> - **Group therapy:** If you're assigned to group therapy and your symptoms make it genuinely unsuitable (for example, social anxiety that prevents you from participating), you can decline on the grounds that it is not compatible with your clinical needs.

---

## Step 3: Build your rejection list

You need to show your insurer that you contacted at least 20 public therapists and none could see you within a reasonable time. **This runs in parallel with Steps 2 and 4** — start as early as possible.

For this step, keep the filters simple. You only need:
- Your **zip code** (for proximity)
- **Insurance filter**: `public`
- **Availability**: `over 3 months` or `over 12 months`

You don't need to filter by language, gender, or therapy method — legally, availability is what matters here, not whether the therapist would have been a perfect match.

- Contact at least **20 therapists** — more is better if you want to move faster
- Track all responses in the `responses.csv` file the tool generates: dates, replies, waiting times
- No reply is also valid, but give it 1–2 weeks before counting it
- Contact a few extra upfront if you'd rather not wait on stragglers
- If you already kept a log from therapists that turned you down in step 1, you may add them to `responses.csv`

The tool automatically keeps `responses.csv` up to date as you run it. When you're ready to apply, attach it to your insurance application email.

---

## Step 4: Find a private therapist

Start looking for a private therapist you actually want to work with. They need to meet two criteria:

1. **Licensed in one of these approved methods** (Richtlinienverfahren):
   - Behavioural therapy (Verhaltenstherapie)
   - Depth psychology (Tiefenpsychologisch fundierte Psychotherapie)
   - Psychoanalysis (Analytische Psychotherapie)

2. **Willing to handle the Kostenerstattung paperwork** — not all private therapists are, so ask explicitly

**How to search:**
- Set **Insurance filter** to `kostenerstattung` in `my_data.csv` — therapie.de has a filter for this (not always up to date, but a good starting point). If you don't find a good therapist, you may also reach out to therapists who work with private health insurance and ask them in your email whether they are willing to work with `kostenerstattung`.
- Use the private therapist inquiry email template, which covers both criteria above

Once you've found someone promising, see them for 1–2 sessions to make sure it feels right. Note: these initial sessions may or may not be reimbursed later — you may need to pay for them out of pocket for now.

**Ask your private therapist** what forms your GP will need to fill in — they may have specific forms for you to bring to the GP appointment.

---

## Step 5: Get a note from your GP

Ask your GP (or psychiatrist, if you're already seeing one) for:
- A **medical certificate of necessity** (Ärztliche Notwendigkeitsbescheinigung)
- A **consultation report** (Konsiliarbericht)

This is straightforward — tell them you've been struggling (depression, anxiety etc which has caused difficulty functioning at work, school, or in daily life) and need documentation to support a therapy application. Bring any forms your private therapist gave you. Don't stress about this appointment — it's mostly filling out forms, not a deep medical examination.

---

## Step 6: Submit your application

Once you have everything, send it to your health insurance (Krankenkasse):

- ✅ PTV11 form with urgency sticker
- ✅ Contact list of 20+ unavailable public therapists (generated by this tool)
- ✅ Confirmation from your private therapist (licensed method + willingness to do paperwork)
- ✅ Ärztliche Notwendigkeitsbescheinigung + Konsiliarbericht from your GP

Use the insurance application letter template (template 4) as your cover letter.

**How to submit:**
- Email is a good first step
- If there's a branch office near you, a **personal visit** is worth it — harder to ignore than an email, and less stressful than a phone call

---

## Step 7: Wait — then follow up if needed

Your insurer should respond within about a month. If they don't:

1. **~4 weeks with no reply:** Send the follow-up email template asking for a status update
2. **~5 weeks, still nothing:** Send the legal threat template
3. **Application rejected:** Send the Widerspruch (formal objection) template

> You don't need a lawyer. Silence and rejection are standard tactics insurers use to discourage costly claims. A firm, formal response is almost always enough when your paperwork is complete.
