---
name: saas-metrics
description: How an assistant reads subscription numbers from Stripe for its owner - MRR, ARR, customer and revenue churn, net and gross revenue retention, refunds and failed payments - and says what the numbers do and do not show, without overclaiming.
whenToUse: When the owner says "hoeveel MRR hebben we", "wat is onze churn", "hoe ging september", "is het goed of slecht", "wat zeg ik tegen investeerders", "why did revenue drop", "hoeveel betalingen zijn mislukt", or when the stripe plugin returns revenue, subscriptions or invoices that need explaining.
---

# SaaS metrics

## What it is

A subscription business is judged on a few numbers: how much recurring revenue it has (MRR, ARR), how much
of it leaves (churn), and how much it keeps and grows from existing customers (revenue retention). Each has
a precise definition. The most common mistake is not arithmetic but mixing them up: calling cash received
"MRR", or a good month "growth".

This skill uses Stripe's own definitions, because the owner's numbers come from Stripe. Other tools define
some of these differently; always say which definition you used.

## What the stripe plugin gives you

The Iris **stripe** plugin is **read-only**: it never creates, changes, refunds or deletes anything. With a
restricted read-only key it shows:

| Command | What it is | What it is not |
|---|---|---|
| `stripe revenue [--month YYYY-MM]` | The **successful payments** of one calendar month in UTC, per currency, with gross, refunded and net | Not MRR. It is cash collected, including one-off payments and annual plans paid in that month |
| `stripe subscriptions --status active` (and `past_due`, `unpaid`, `canceled`, `trialing`, `all`) | The subscriptions, from which MRR can be worked out | Without `--status`, Stripe leaves out canceled ones |
| `stripe invoices --status open` (and `paid`, `uncollectible`, `void`, `draft`) | Invoices by status, for failed and unpaid money | |
| `stripe payments`, `stripe customers`, `stripe balance` | Recent charges, customers, the balance, and whether the key is `live` or `test` | |

Stripe sends amounts in the smallest unit; the plugin prints them properly (`EUR 1,234.56`). Check live or
test mode before reporting any number: test data is not the business.

The Stripe Dashboard's Billing analytics computes MRR, churn and cohort retention itself, with settings the
owner chose. When the owner has it, its numbers are the reference; say when yours are a manual estimate.

## The definitions

### MRR (monthly recurring revenue)

Stripe: the sum of the **monthly-normalised value of all `active` and `past_due` subscriptions**.

- A yearly plan counts as one twelfth per month. Stripe's example: 100 subscribers at USD 100 a month plus
  50 at USD 600 a year gives 10,000 + 2,500 = **USD 12,500 MRR**.
- Excluded: taxes, free plans, metered (usage-based) products, and subscription items in a trial.
- A subscription that is canceled or marked `unpaid` counts as churn and leaves MRR.
- One-off refunds and one-off payments do not change MRR (Stripe support), unless the plan's price changes.
- Discounts: permanent recurring discounts are always subtracted; one-time and recurring coupons depend on
  the owner's Dashboard setting. Stripe calls subtracting them the more conservative choice.

### ARR (annual recurring revenue)

Stripe: **ARR = MRR x 12**. It is recurring revenue extrapolated over a year, not a forecast and not
this year's turnover. A business with MRR of EUR 8,000 has ARR of EUR 96,000 whatever it actually billed
this year.

### MRR movements

Stripe's MRR growth starts from MRR at the beginning of the period, adds **new**, **reactivation** and
**expansion** MRR, subtracts **contraction** and **churned** MRR, and adjusts for currency (FX) effects.
Report these parts, not only the net change: +EUR 500 net can be +EUR 2,000 new and -EUR 1,500 lost.

### Churn

| Metric | Stripe's definition |
|---|---|
| **Subscriber (customer) churn rate** | Subscribers who churned in the past 30 days, divided by (active subscribers 30 days ago + new subscribers in the past 30 days). Example: start 1,000, +100 new, -100 churned: 100 / 1,100 = **9.1%** |
| **Churned revenue** | Churned MRR plus contraction MRR in the period (so downgrades count) |
| **Gross revenue churn** | Churned MRR / MRR at the end of the previous month x 100 |
| **Net revenue churn** | (Churned MRR - expansion MRR) / MRR at the end of the previous month x 100. Negative means existing customers grow faster than they leave |

A subscriber counts as churned when all their subscriptions are canceled or `unpaid`, or their MRR drops to
zero (for example a 100% coupon when discounts are subtracted). **Customer churn and revenue churn can move
in opposite directions**: losing ten small customers and keeping one large one that upgrades is high
customer churn and negative net revenue churn. Report both.

### Revenue retention

- **NRR (net revenue retention)** = (starting recurring revenue - MRR lost to churn - MRR lost to downgrades +
  revenue from upgrades) / starting recurring revenue x 100, for the **same existing customers**. Stripe's
  example: 100,000 - 5,000 - 2,000 + 8,000 = **101%**. It can exceed 100%.
- **GRR (gross revenue retention)** is the same without upgrades. It **cannot exceed 100%**, which is why
  Stripe calls it the most honest indicator of long-term sustainability.
- New customers do not belong in either. If they are in, it is growth, not retention.
- Stripe's **cohort** view groups subscribers by when they first started generating positive MRR, and shows for each month how
  many subscribers and how much MRR remain.

### ARPU and lifetime value

- **ARPU** = total MRR / active subscribers. Example: USD 50,000 / 100 = USD 500.
- Stripe estimates **subscriber lifetime value** as ARPU / subscriber churn rate (USD 500 / 9% is about
  USD 5,555). It is an estimate from a single point in time: a small change in churn moves it a lot. Say so.

## Refunds and failed payments

- **Refunds**: `stripe revenue` shows gross, refunded and net for the month. One-off refunds do not change
  MRR, so a month with many refunds can have steady MRR and lower cash. Report both, and look at the
  reasons for the refunds before calling it a trend.
- **Failed payments**: a subscription whose latest invoice failed goes `past_due`. It **still counts in MRR**
  while past due. Depending on the owner's settings it later becomes `unpaid` (leaves MRR, invoices keep
  coming as drafts, no payment is attempted) or is canceled. Stripe can retry failed payments with Smart
  Retries; its recommended default is 8 tries within 2 weeks.
- So a high `past_due` count makes MRR look better than the cash is. Report it next to MRR:
  "MRR EUR 12.400, waarvan EUR 900 bij abonnementen met een mislukte betaling."
- In the first 23 hours after a subscription with automatic charging is created, it is `incomplete` until
  the first invoice is paid. It is not yet a customer.

## Reading the numbers without overclaiming

- **Name the metric and the definition.** "Omzet september" (cash, `stripe revenue`) is not "MRR".
- **Give the period, the currency and the mode.** Stripe's `revenue` month is in UTC, so a payment just
  after midnight on the 1st in the Netherlands still falls in the previous month. Do not add currencies together without
  saying how they were converted.
- **One month is not a trend.** Say "hoger dan augustus", not "we groeien", until several months point the
  same way. Seasonality, annual renewals and one large customer can each make a month look special.
- **Small numbers swing.** With 40 subscribers, 2 cancellations is 5% churn. Give the counts next to the
  percentages.
- **Correlation is not cause.** A price change and a churn rise in the same month are not proof that one
  caused the other. Say what else happened.
- **Benchmarks are context, not verdicts.** Stripe describes NRR above 100% as generally healthy; whether it
  is good for this business depends on stage and market. Do not grade the owner.
- **For investors, the bank or the tax office**, give definitions with every number, and let the owner (and
  their accountant) check before anything is sent (`acting-on-behalf`). Revenue for VAT or income tax is a
  different thing; see `dutch-vat-zzp`.

## What not to do

- Do not call cash collected MRR, or MRR x 12 "this year's revenue".
- Do not include new customers in NRR or GRR, or leave downgrades out of revenue churn.
- Do not report a number from a test key as if it were the business.
- Do not refund, cancel, retry, email customers or change a price: the plugin cannot, and any such action
  touches money and other people. Draft and ask.
- Do not share customer names or amounts outside the conversation with the owner (`gdpr-basics`).

## Where this stops

This uses the Iris stripe plugin README; Stripe's Billing analytics documentation (MRR, MRR growth,
subscribers, ARPU, lifetime value, churn and cohort retention); Stripe's documentation on subscription
statuses and payment retries; a Stripe support article on MRR and ARR; and Stripe's guides on ARR, revenue
churn and net revenue retention. Other tools and investors may use other definitions. This is not
accounting or tax advice: recognised revenue for the books follows accounting rules, not these metrics.
