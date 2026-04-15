# DON'T PANIC — your Hitchhiker's Guide to finding a therapist in Germany

> The German healthcare bureaucracy is, if not exactly friendly, mostly traversable. The is a tool to help people in Germany find therapists and build the documentation needed to apply for cost reimbursement (Kostenerstattung) from their public health insurance. You don't need a lawyer, you don't need to speak German, and you don't need to figure it all out at once. Just follow the steps.

---

## What this tool does

Finding a therapist in Germany is hard — waiting times of 3+ months are common, and navigating the system when you're already struggling is exhausting. This tool helps you search for therapists near you based on your needs (insurance type, language, therapy method, and more) and generates personalized emails to send to them directly.

If you have public health insurance and can't find a therapist with availability, there's a legal route to get your insurer to cover a private therapist instead. This tool also guides you through that process: it helps you build the required contact documentation, and generates the formal letters you'll need to submit your application — and appeal if needed.

---

## The legal basis

This is a well-established legal right. Under **§13 Abs. 3 SGB V**, your public health insurer is required to cover private therapy costs if you can demonstrate that the public system couldn't provide timely care. The process is officially recommended by the **Bundespsychotherapeutenkammer (BPtK)** — the federal chamber of psychotherapists. For the full background, see the [BPtK guide (PDF)](docs/BPtK_Ratgeber_Kostenerstattung.pdf).

---

## Getting started

Choose the setup path that fits you:

| I have Python installed | I don't have Python. I just want to run the program. |
|---|---|
| [Technical install →](docs/install_technical.md) | [Non-technical install →](docs/install_nontechnical.md) |

---

## Using the tool

Once installed, read the [step-by-step guide](docs/guide.md) — it walks you through the full Kostenerstattung process and explains which tool option to use at each stage.

For a full reference of every field in `my_data.csv`, see [my_data.csv reference](docs/my_data_reference.md).

---

## Responsible use

- **Rate limiting is built in** — the tool waits between requests automatically. Don't modify this.
- **Emails are genuine requests** — even when documenting unavailability, you're sending real inquiries, not spam.
- **Personal use only** — this tool is for your own therapy search, not for bulk or commercial use.

---

## License

MIT
