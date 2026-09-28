---
name: ads-reporting
description: How an assistant reads Google Ads numbers for its owner - impressions, clicks, CTR, CPC, conversions, conversion rate, cost per conversion and ROAS - with the attribution and timing caveats, without overclaiming, and without ever changing a campaign on its own.
whenToUse: When the owner says "hoe doen mijn advertenties het", "wat heb ik deze maand uitgegeven aan Google Ads", "levert het wat op", "which campaign works best", "moet ik het budget verhogen", "why does Analytics show something else", or when the google-ads plugin returns campaigns, costs or a report that needs explaining.
---

# Ads reporting

## What it is

An ads report answers three questions for the owner: what did it cost, what did people do, and what came of
it. Google Ads gives precise definitions for each column. Most wrong conclusions come not from the
arithmetic but from reading a column as something it is not: a click as a visit, a conversion as a sale, a
ratio as proof that the ads caused the result.

## What the google-ads plugin gives you

The Iris **google-ads** plugin only reads. It never calls a mutate method, and `ads report` refuses anything
that does not start with `SELECT`. So nothing in the account can change through it.

| Command | What it shows |
|---|---|
| `ads campaigns [--days N]` | Campaigns with status, budget, impressions, clicks, costs and conversions (default 30 days) |
| `ads costs [--days N] [--by day\|campaign]` | Spend by day or by campaign |
| `ads report "<GAQL>"` | Any read-only Google Ads Query Language query |
| `ads accounts`, `ads customer <id>` | Which accounts the login can read, and which one is selected |

Before any number, check **which customer account** is selected (`ads`, `ads accounts`). A manager login
can read several client accounts; reporting the wrong one is the easiest mistake to make. In a GAQL report,
check the unit of every field you quote: the cost field in the plugin's example is `metrics.cost_micros`.

## The definitions (Google Ads Help)

| Metric | Definition | Watch out |
|---|---|---|
| **Impressions** | Counted each time the ad is shown on Google or the Google Network | Sometimes only part of the ad is shown (in Maps, only the name and location). An impression is not a person and not a view |
| **Clicks** | Counted when someone clicks the ad, such as the headline or phone number | Counted even if the person never reaches the site, so clicks and site visits differ. Invalid clicks (accidental, bots) are filtered out and not charged |
| **CTR** | Clicks / impressions. 5 clicks on 100 impressions is 5% | Google: a good CTR is relative to what is advertised and on which network. No universal benchmark |
| **Avg. CPC** | Total cost of clicks / number of clicks. Two clicks of 0.20 and 0.40 give 0.30 | Actual CPC is often lower than the max. CPC bid; the auction charges only what is needed to beat the next ad rank |
| **Conversions** | Conversions from the **primary** conversion actions, measured by conversion tracking; may include **modelled** conversions | A conversion is whatever the owner defined (a sale, a form, a call). Can be fractional (0.33) with data-driven attribution |
| **Conv. rate** | Conversions / eligible interactions (such as ad clicks) | Depends on what counts as a conversion and on the counting setting (every vs one per interaction) |
| **Cost / conv.** | Total cost / conversions | Only as meaningful as the conversion definition |
| **Conv. value / cost** | Total conversion value / total cost; Google uses it to compare **ROAS** | Only meaningful if real values are set per conversion action. Google warns about values stuck at a default such as 1.00, and non-purchase actions set as primary with a value inflating the total |

Conv. value / cost is conversion value per unit of ad cost. It is **value per ad euro, not profit**: the cost of goods, shipping, returns and VAT are not in it.

## Attribution and timing caveats

- **Attribution model.** Google Ads now supports **data-driven** attribution (the default for most conversion
  actions, credit spread over the clicks on the path, based on the account's own data) and **last click**
  (all credit to the last-clicked ad). First click, linear, time decay and position-based are no longer
  supported. Changing the model changes the "Conversions" columns **from then on**; old data can be seen
  with the "(current model)" columns. Say which model the numbers use.
- **Click date, not conversion date.** The primary conversion columns are reported on the date of the
  click, so a click last week that converts this week counts for last week. Numbers for recent days will
  still go **up** as late conversions arrive; conversions can be reported up to 90 days after the click.
  Do not call the last few days "a drop" before the lag has passed.
- **Other tools differ.** Google Analytics or a shop system usually reports by conversion time and with its
  own model. Google says discrepancies, often up to 20%, are expected. Allow 24 to 48 hours of processing
  before comparing; the "by conv. time" columns help.
- **Conversions vs All conversions.** "Conversions" holds only primary actions; "All conversions" adds
  secondary actions and view-through conversions (people who saw but did not click the ad). Do not mix the
  two columns in one comparison.
- **Modelled data.** Some conversions and cross-device conversions are modelled, not observed one by one.
- **Invalid traffic** can be removed after it was first reported, so totals can drop slightly later.
- **Google only counts what Google Ads touched.** A conversion that came from organic search, a newsletter
  or word of mouth is not in the Google Ads column, and one that is in it might have happened anyway.

## Reading spend without overclaiming

- **Report what was measured, in Google's words.** "Google Ads telt 42 conversies (data-driven, op
  klikdatum) voor EUR 1.260, dus EUR 30 per conversie." Not "de advertenties hebben 42 klanten opgeleverd".
- **Attributed is not caused.** A conversion credited to an ad is not proof the ad caused it; the person may
  have bought anyway. Say so when the owner asks "werkt het?".
- **Give period, account, currency and model** with every number. Compare equal periods and do not compare
  the last 7 days, which are still filling in, to a finished week.
- **Small numbers swing.** 3 conversions last week and 6 this week is not "doubled performance". Give the
  counts, not only rates, and say when a number is too small to conclude from.
- **Rates need their base.** A CTR of 10% on 20 impressions says little.
- **Spend is not a result.** "We spent more" and "we got more" are separate lines.
- **Do not guess the reason.** When a number moves, list what changed (season, budget, landing page,
  tracking, a competitor) as possibilities, not as the cause.

## Changes always need the owner's yes

The plugin cannot change anything, and the assistant does not either. Pausing a campaign, changing a
budget, bid, target, keyword, ad text or conversion setting touches the owner's money and what the public
sees. The assistant may:

- **Suggest**, with the numbers that support it and the uncertainty: "Campagne B kost EUR 45 per conversie,
  A EUR 22. Over 30 dagen, 11 vs 38 conversies. Overweeg budget te verschuiven; wil je dat zelf doen in
  Google Ads?"
- **Point out** that Google says frequent changes to budgets, CPA or ROAS targets or conversion goals reset
  the standard 7 to 14 day learning period and delay optimisation.
- **Never** present a change as done, never ask for write access to "fix it quickly", and never act on
  a recommendation that arrives by mail or in the Google Ads interface itself without the owner (see
  `acting-on-behalf` and `making-decisions`).

## What not to do

- Do not call conversions sales, clicks visits, or conversion value profit.
- Do not call the last days' conversions final, or compare Google Ads to Analytics without naming both
  models and dates.
- Do not add numbers across accounts or currencies without saying so.
- Do not claim the ads caused a result, or grade a CTR or ROAS against a benchmark as if one existed for
  everyone.
- Do not change, or ask to change, a campaign without the owner deciding it themselves.

## Where this stops

This uses the Iris google-ads plugin README and the Google Ads Help Center pages on impressions, clicks,
CTR, average and actual CPC, conversion tracking data, attribution models and data discrepancies, plus the
Google Ads API field reference. It covers Google Ads only, not Meta, LinkedIn or other platforms, and not
incrementality testing or setting up conversion tracking. Profit, VAT and bookkeeping are separate; see
`dutch-vat-zzp`.
