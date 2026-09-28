---
name: seo-basics
description: What search engines actually document about being found - crawling and indexing, titles and snippets, helpful people-first content, structured data, sitemaps, robots.txt, noindex, canonical URLs, Core Web Vitals, and the spam policies to stay clear of.
whenToUse: When the owner says "waarom staat mijn site niet in Google", "hoe kom ik hoger in Google", "kun je de SEO checken", "moet ik een sitemap hebben", "iemand biedt me backlinks aan", "should I write 50 blog posts with AI for SEO", "why is this page not indexed", when you build or review a website, write page titles or meta descriptions, or when someone promises top rankings for money.
---

# SEO basics

## What it is

Search engine optimisation is helping search engines understand a site, and helping people decide from a
search result whether to visit it. Google says it plainly in its own starter guide: there are no secrets
that automatically rank a site first. This skill keeps to what Google Search Central documents, so the
assistant can separate real work from folklore and from offers that break the rules.

Google documents three stages, and not every page gets through each one:

| Stage | What happens | What stops it |
|---|---|---|
| Crawling | Googlebot finds URLs, mostly through links, fetches the page and renders it with a recent Chrome, running JavaScript | Server or network errors, robots.txt rules, pages behind a login |
| Indexing | Google works out what the page is about, groups duplicates and picks one canonical URL | Low quality content, a `noindex` rule, a design that makes indexing hard |
| Serving | For a query, Google returns what it judges most relevant and useful | The page does not match what people search for, or quality is low |

Google does not accept payment to crawl a site more often or to rank it higher, and it guarantees nothing,
even for sites that follow its rules. Anyone who promises "nummer 1 in Google" is selling something else.

## First: is the site in the index at all?

1. Search `site:voorbeeld.nl` (the owner's domain). Results mean the site is indexed.
2. If not, check that the page is reachable without a login, not blocked in robots.txt, and has no
   `noindex`. Search Console's URL Inspection tool shows how Google sees a page.
3. Google finds most pages through links. A new site with no links to it may take time; telling people
   about the site is the first step, a sitemap the second.

Changes take time to show: Google says a few hours to several months, and suggests waiting a few weeks
before judging an effect.

## What to work on

**Content people want.** Google's own starter guide says compelling, useful content will likely matter
more than anything else in it. Its self-check for helpful, reliable, people-first content asks, among
other things:

- Does it give original information, analysis or first-hand experience, not a rewrite of others?
- Does the title describe the content without exaggerating?
- Would someone leave feeling they learned enough to reach their goal?
- Is it clear who made it, and how (bylines, an about page, how a review was tested)?

Warning signs in the same guidance: writing mainly to attract search visits, covering many unrelated
topics hoping something ranks, heavy automation, writing to a word count (Google says it has no preferred
word count), and changing dates to look fresh when nothing changed.

**Titles.** Every page gets a `<title>`. Make it unique, descriptive and concise; not "Home". Do not repeat
keywords. A site name can go at the start or end, with a separator like a hyphen, colon or pipe. Make the
main heading on the page clearly the most prominent. Google builds the title link from several sources
(the `<title>`, the main visible title, headings, `og:title`, link text) and may rewrite it when the title
is empty, outdated, inaccurate or the same on many pages.

**Meta descriptions.** Snippets come mostly from the page content; Google sometimes uses the meta
description. A good one is short, unique to the page, and states the most relevant points. For example:
"Fietsenmaker in Utrecht-Oost. Reparatie klaar terwijl u wacht, di-za 9-18 uur." rather than a list of
keywords.

**URLs, links and images.** Use descriptive words in URLs (`/fietsen/reparatie`) rather than random IDs.
Write link text that says where the link goes. Put `nofollow` or a similar annotation on links you do not
vouch for, and on links in comments or forum posts from users. Give images descriptive `alt` text and
place them near related text.

**Headings.** Break long text into sections with headings, for readers. Google says the order and number
of headings do not matter for its ranking; semantic order does matter for screen reader users (see
`web-interface-guidelines`).

**Page experience.** Google's core ranking systems look at many aspects, not one score. Its self-check:
good Core Web Vitals, HTTPS, works on mobile, not too many ads, no intrusive interstitials, main content
easy to tell apart. Core Web Vitals are used by the ranking systems; the other aspects do not directly
raise rankings but make the site better to use. The current Core Web Vitals, with web.dev's thresholds for
a good experience at the 75th percentile of page loads:

| Metric | Measures | Good |
|---|---|---|
| Largest Contentful Paint (LCP) | Loading | within 2.5 seconds |
| Interaction to Next Paint (INP) | Responsiveness | 200 milliseconds or less |
| Cumulative Layout Shift (CLS) | Visual stability | 0.1 or less |

Good scores do not guarantee top positions: Google still shows the most relevant content even when its
page experience is poor.

## Technical files, and what each one does not do

| Tool | Use it for | It does not |
|---|---|---|
| `sitemap.xml` | Listing the URLs you care about, helpful for large or new sites with few links, or much video, image or news content | Guarantee crawling or indexing. Google says small, well-linked sites (about 500 pages or fewer) may not need one; many CMSes make one automatically |
| `robots.txt` | Managing crawler traffic, keeping crawlers off unimportant or duplicate pages | Keep a page out of Google. A blocked URL can still be indexed if others link to it, and not every crawler obeys |
| `noindex` (meta tag or `X-Robots-Tag` header) | Keeping a page out of search results | Work if robots.txt blocks the page, because then Google never sees the rule. Google does not support `noindex` inside robots.txt |
| `rel="canonical"` | Telling Google which of several duplicate URLs to show | Need to be perfect: Google picks a canonical itself if you do not. Redirects are a strong signal, canonical links strong, sitemap inclusion weak |
| Structured data (JSON-LD recommended) | Making a page eligible for rich results, such as recipes or events | Guarantee rich results. Mark up only what is visible on that page, and check it with the Rich Results Test |

Truly private content belongs behind a password, not behind robots.txt. Duplicate content is not a
violation of the spam policies; it is only inefficient. Do not use robots.txt or `noindex` to choose a
canonical within a site.

## What not to do: Google's spam policies

Sites that break these can rank lower or disappear from results, by automated systems or a manual action.
Say no, and explain why, when the owner is offered any of them:

| Practice | In short |
|---|---|
| Cloaking | Showing search engines different content than people |
| Doorway abuse | Many near-identical pages or domains per city or query that funnel to one page |
| Expired domain abuse | Buying an old domain to rank low-value content on its reputation |
| Hidden text and links | White text on white, text behind images, meant only for search engines |
| Keyword stuffing | Lists of cities, keywords or phone numbers repeated to rank |
| Link spam | Buying or selling links that pass ranking credit, excessive link swaps, automated links, keyword-rich links in widgets, footers or forum signatures. Paid links are fine with `rel="nofollow"` or `rel="sponsored"` |
| Scaled content abuse | Many pages made mainly to rank, however they are made, including generative AI without added value |
| Scraping | Republishing others' content, or lightly reworded copies, without adding value |
| Site reputation policy | Third-party content published on a strong site mainly to borrow that site's rankings |
| Sneaky redirects | Sending people somewhere other than what search engines saw |
| Thin affiliation | Affiliate pages that copy the merchant's descriptions without original value |

Also not worth the owner's money, per Google: the keywords meta tag (Google does not use it), keywords in
the domain name (hardly any effect), a set content length, and treating E-E-A-T as a ranking factor
(Google says it is not one, though its systems look for signals of experience, expertise, authority and
trust).

## How the assistant works with this

- Check facts on the live site before advising: the `<title>`, meta description, robots.txt, `noindex`,
  canonical, sitemap. Report what you found, with the URL.
- Write titles and descriptions for the owner's review; they publish. Contacting link sellers, agencies or
  other sites waits for the owner's yes (`acting-on-behalf`).
- When the owner wants AI help with content, help them add what only they know: their experience, photos,
  prices, opening hours. That is what the helpful content guidance asks for.

## What not to claim

- Never promise a ranking, a position or a date. Google guarantees neither indexing nor ranking.
- Do not present ranking factors, weights or "the algorithm" as known. Google documents principles, not a
  formula.
- Do not state other search engines work the same. This skill follows Google's documentation; Bing and
  others publish their own guidelines.

## Where this stops

This follows Google Search Central documentation (SEO Starter Guide, How Search Works, helpful content,
spam policies, title links, structured data, sitemaps, robots.txt, `noindex`, canonical URLs, page
experience) and web.dev on Core Web Vitals, as read in September 2026. Policies and metrics change; check
the current pages before a big decision. It does not cover paid search ads, local business listings,
international sites (`hreflang`), or a site move. For a large or commercial site, a professional who
follows these same guidelines is worth the money; one who promises guaranteed rankings is not.
