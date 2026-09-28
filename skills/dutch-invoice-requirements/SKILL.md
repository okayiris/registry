---
name: dutch-invoice-requirements
description: What a Dutch invoice must show and how long to keep it, for a zzp'er or small business - the art. 35a Wet OB list, simplified invoices up to EUR 100, credit notes, foreign currency, e-invoicing, the deadline to send, payment terms, statutory interest and collection costs.
whenToUse: When the owner says "wat moet er op mijn factuur", "mag ik deze factuur nog aanpassen", "creditnota maken", "factuur in dollars", "hoe lang moet ik facturen bewaren", "de klant betaalt niet", "mag ik incassokosten rekenen", "wat is de betaaltermijn", "moet ik e-factureren", or when you draft, check or chase an invoice in their bookkeeping (Moneybird, Stripe).
---

# Dutch invoice requirements

## What it is

The rules for invoices sent by a business established in the Netherlands. The **content** of an invoice
comes from the Wet op de omzetbelasting 1968 (Wet OB, art. 34c to 35c). **Payment terms, interest and
collection costs** come from the Burgerlijk Wetboek Boek 6 and the Besluit vergoeding voor buitengerechtelijke
incassokosten. **Keeping** records comes from the Algemene wet inzake rijksbelastingen (art. 52). Figures are
as of 2026.

This skill does not cover VAT rates, the KOR or filing returns. For those use `dutch-vat-zzp`; for EU
customers also `eu-vat-for-freelancers`.

## Who must get an invoice

- Every **business** customer, and legal entities that are not businesses (associations, foundations),
  including foreign ones.
- Advance payments from such customers also need an invoice.
- **Private customers**: no invoice is required, apart from a few exceptions (like a new vehicle to another EU
  country). Sending one anyway is fine.
- Businesses that only make exempt supplies, and KOR participants, do not have to meet all invoice
  requirements.

## Deadline to send

Send the invoice **by the 15th day of the month after the month of supply**. A periodic invoice may cover
several separate supplies, for a period of at most one calendar month (art. 35 Wet OB).

## What must be on it (art. 35a Wet OB)

| Item | Note |
|---|---|
| Invoice date | the date it is issued |
| Invoice number | consecutive, in one or more series; each number used once |
| Your **btw-id** (NL...B..) | never the omzetbelastingnummer, see `dutch-vat-zzp` |
| Your KVK number | when registered in the Handelsregister |
| Full name and address of you and the customer | legal name, or the trade name if registered at KVK with address; the actual address, not only a PO box |
| Customer's btw-id | when the customer owes the VAT (reverse charge) |
| What was supplied | quantity and kind of goods, or kind and extent of the service ("1 massage of 1 hour") |
| Date of supply or advance payment | when fixed and different from the invoice date |
| Amount excluding VAT per rate or exemption | plus unit price, and discounts not in the unit price |
| VAT rate and VAT amount | the rate itself is in `dutch-vat-zzp` |

Extra wording when it applies:

- **"btw verlegd"** when the customer owes the VAT;
- a mention of the **exemption** when a supply is exempt;
- **"factuur uitgereikt door afnemer"** when the customer makes the invoice (self-billing, only when agreed
  beforehand and each invoice is accepted by the supplier);
- "bijzondere regeling" wording for travel agencies and second-hand goods, and the fiscal representative's
  details when one pays the VAT.

Wrongly numbered invoices must be corrected; otherwise the customer has no right to deduct the VAT.

## Simplified invoice (vereenvoudigde factuur)

Allowed when:

- the invoice amount is **at most €100 including VAT**;
- the document changes an earlier invoice (a credit note or correction);
- the business uses the KOR.

It shows at least: the date, your name and address, what was supplied, the VAT or the data to calculate it,
and for a change, a reference to the original invoice.

**Not allowed** for intra-community supplies of goods, distance sales, and supplies in another EU country
where you are not established and the VAT is reverse-charged to the customer.

## Credit notes and corrections

Any document that changes an earlier invoice and refers to it specifically and unambiguously **counts as an
invoice** (art. 34f Wet OB). The law also requires that an invoice's content stays unchanged from issue to the
end of the retention period (art. 35b).

In practice this means: do not edit or delete an invoice that has been sent. Issue a **credit note** that
refers to the original invoice number and says what changes, give it its own number, and if needed send a new
invoice. A credit note may be a simplified invoice. How the VAT correction goes into the return is in
`dutch-vat-zzp`.

## Foreign currency and language

- Amounts may be in **any currency**, as long as the **VAT amount is stated in euros**, converted with the
  exchange rate mechanism of the EU VAT directive (art. 35a lid 4 Wet OB).
- The tax inspector may require a Dutch translation of an invoice when needed for an audit (art. 35a lid 5).

## Paper, PDF and e-invoicing

- You choose paper or digital. A **PDF by e-mail** is a digital invoice. An **e-invoice** goes from your
  system into the customer's system. Both must meet the same requirements.
- The customer must **agree** to electronic invoicing (art. 35b). You must be able to guarantee the origin,
  the integrity of the content and the readability, in a way you choose yourself.
- Selling to the **Rijksoverheid** (central government)? It must be an e-invoice, not a PDF: via your own
  bookkeeping software or the government's Leveranciersportaal.
- **Coming, not yet law:** on 11 September 2026 the cabinet announced it wants mandatory e-invoicing for
  business-to-business transactions, domestic and international, from **1 July 2030**, and reporting from
  1 July 2031. KOR businesses would be exempt. The bill is expected before summer 2027. Mention it as a plan;
  nothing changes in 2026.

## How long to keep invoices

- All invoices **sent and received**: **7 years** (art. 52 AWR). Invoices about real estate: 10 years. Under
  the OSS Union or Import scheme: 10 years for those supplies.
- Keep them in the form they were sent or received: a digital invoice stays digital. Paper may be scanned and
  the original discarded if the scan is a correct and complete copy and authenticity data is kept.
- Invoices contain personal data. Do not keep them longer than the retention period without a good reason
  (see `gdpr-basics`).

## Payment terms (art. 6:119a BW)

| Customer | Term |
|---|---|
| Business, no term agreed | **30 days** after receiving the invoice |
| Business, term agreed | at most **60 days**, longer only if expressly agreed and not grossly unfair to the supplier |
| Large company paying an SME or zzp'er | at most **30 days**; a longer term is void |
| Government | 30 days after receipt, rarely 60 |
| Consumer | no statutory term; set a reasonable one in the contract or terms |

A company is "large" here if it meets at least two of three on two consecutive balance sheet dates: 250
employees or more, net turnover over €50 million, balance sheet total over €25 million.

## When the customer pays late

**Statutory interest (wettelijke rente):**

- Business or government customer: **wettelijke handelsrente**, **10.4% since 1 July 2026**, owed from the
  day after the payment deadline without a reminder. The rate is set per half year; check the current rate.
- Consumer: wettelijke rente for non-commercial transactions, **4% since 1 January 2026**, over the time the
  customer is in default.
- Let the customer know you will charge it, for example on the invoice or in the reminder.

**Collection costs (incassokosten, WIK):**

- **Business customer:** at least **€40**, owed without a reminder from the day after the deadline
  (art. 6:96 lid 4 BW). A contract may set other collection costs.
- **Consumer:** first a **free reminder** (aanmaning) giving **14 days** to pay, stating the costs that will
  follow. Only after that may costs be charged, and never more than the scale (art. 6:96 lid 5 and 6 BW).
  Several invoices go in one reminder.
- The scale (Besluit art. 2): 15% of the first €2,500; 10% of the next €2,500; 5% of the next €5,000; 1% of
  the next €190,000; 0.5% above that. Minimum €40, maximum €6,775.

**Limitation (verjaring):** a business customer's invoice lapses 5 years after the payment term ends; a
consumer's invoice for goods after 2 years, for services 5 years. A (registered) reminder restarts the period.

## How to work with it

1. Drafting or checking an invoice: go through the table above, then the extra wording. Check the btw-id,
   the number series and the 15th-of-next-month deadline.
2. A mistake in a sent invoice: propose a credit note plus a new invoice, never an edit.
3. Chasing payment: a friendly reminder first, then for a consumer the free 14-day aanmaning. Draft; the owner
   approves and sends (`acting-on-behalf`, `difficult-conversations`).
4. Calculate interest and collection costs with the date and the scale, and show the calculation.

## What not to claim

- Do not name a VAT rate or decide an exemption here; use `dutch-vat-zzp`.
- Do not charge collection costs to a consumer before the free 14-day reminder has run out.
- Do not present mandatory e-invoicing in 2030 as law; it is a plan.
- Do not give an interest rate for another period without checking the current one.
- Do not send reminders, credit notes or invoices without the owner's yes.

## Where this stops

Based on the Wet OB 1968 (art. 34c to 35c), the Burgerlijk Wetboek Boek 6 (art. 96, 119, 119a), the Besluit
vergoeding voor buitengerechtelijke incassokosten, art. 52 AWR, the Belastingdienst's pages on invoices,
Ondernemersplein on invoicing and payment terms, and Rijksoverheid on the statutory interest and the
e-invoicing plan. Special regimes (margin goods, travel agencies, OSS, real estate) and debt collection in
court are out of scope; refer to a tax adviser or a lawyer.
