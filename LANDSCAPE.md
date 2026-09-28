# The skill landscape

What other agent systems install most, what that means for this registry, and where the gap is. Measured on
**28 September 2026** from the public skills.sh leaderboard (1,435,285 skills listed) and its search API.
Install counts move daily; use them for order of magnitude, not as exact numbers.

## Read these numbers with care

- **Some counts look inflated.** Every skill of `lllllllama/rigorpilot-skills` sits at about 450K, and the
  Lark/Feishu packs total over 16M. Round, identical numbers across a whole pack suggest automated installs.
- **Many top entries are bound to one product** (Lark, Azure, HeyGen HyperFrames, RunComfy). They teach that
  product's CLI and are of no use without it.
- **Many popular "skills" carry code.** Examples are `webapp-testing` (Python scripts) and `agent-browser`
  (a CLI). In this registry those would be a plugin or an MCP server, not a skill.
- **We do not copy them.** Each has its own license. Where a topic is worth having, we write our own version
  from the primary sources (the standard, the vendor's documentation, the research) and name those sources.

## The top 25, by field

Chosen from the leaderboard for general usefulness: product-bound packs are left out, and a family is
counted once.

| # | Skill (source) | Installs | Field | What it is | Text only? |
|---|---|---|---|---|---|
| 1 | find-skills (vercel-labs/skills) | 3.6M | Meta | Finds and installs other skills | Tool |
| 2 | grill-me (mattpocock/skills) | 1.2M | Thinking | Questions a plan branch by branch until there is shared understanding | Yes |
| 3 | frontend-design (anthropics/skills) | 930K | Design | Distinctive interfaces: choose an aesthetic first, then type, colour, motion, layout | Yes |
| 4 | vercel-react-best-practices (vercel-labs) | 749K | Frontend | 70 React/Next.js performance rules in 8 priority groups | Yes |
| 5 | teach (mattpocock/skills) | 720K | Learning | Lessons tied to why the learner wants it, with a record of progress over sessions | Yes |
| 6 | domain-modeling (mattpocock/skills) | 710K | Backend | Naming and modelling the domain before code | Yes |
| 7 | web-design-guidelines (vercel-labs) | 674K | Design | Audits UI against Vercel's interface and accessibility guidelines | Yes |
| 8 | diagnosing-bugs (mattpocock) / systematic-debugging (obra) | 673K / 274K | Engineering | Root cause before any fix; stop and rethink after three failed fixes | Yes |
| 9 | hyperframes / motion-graphics (heygen-com) | 672K / 310K | Motion | Motion graphics and video from HTML, with a brief and a director step | Product-bound |
| 10 | code-review (mattpocock) / requesting-code-review (obra) | 626K / 240K | Engineering | Reviewing a change, and asking for review well | Yes |
| 11 | remotion-best-practices (remotion-dev) | 549K | Motion | Video in React: animation, audio, captions, transitions, 30+ rule files | Yes |
| 12 | design-taste-frontend (leonxlnx/taste-skill) | 529K | Design | Taste rules against generic AI-looking UI | Yes |
| 13 | supabase-postgres-best-practices (supabase) | 420K | Backend | Postgres performance, RLS, schema and locking in 8 priority groups | Yes |
| 14 | skill-creator (anthropics/skills) | 393K | Meta | Writing, testing and tuning skills | Mixed |
| 15 | brainstorming (obra/superpowers) | 378K | Thinking | Turning a rough idea into a design by questions before any work | Yes |
| 16 | ui-ux-pro-max (nextlevelbuilder) | 374K | Design | Styles, palettes, type pairings and UX rules as a searchable set | Mixed |
| 17 | to-prd / to-spec (mattpocock) | 368K / 571K | Product | From conversation to a spec or requirements document | Yes |
| 18 | vercel-composition-patterns (vercel-labs) | 360K | Frontend | Component composition patterns in React | Yes |
| 19 | prisma-database-setup (prisma) | 319K | Backend | Setting up Prisma with a database | Product-bound |
| 20 | emil-design-eng (emilkowalski) | 303K | Motion/design | Interface animation and polish | Yes |
| 21 | impeccable (pbakaus) | 298K | Design | Design review and refinement commands | Yes |
| 22 | shadcn (shadcn/ui) | 272K | Frontend | Using the shadcn/ui components correctly | Product-bound |
| 23 | test-driven-development (obra/superpowers) | 238K | Engineering | Red, green, refactor, and no code without a failing test | Yes |
| 24 | pptx, pdf, docx, xlsx (anthropics/skills) | 228K-174K | Documents | Reading and making office files | Code |
| 25 | seo-audit, copywriting (coreyhaines31/marketingskills) | 216K / 210K | Marketing | Auditing a site for search, and writing copy that converts | Yes |

The OpenAI catalogue (openai/skills) is much smaller in installs (its top is `pdf` at 12.8K). Its themes
are the same: CI fixing, Playwright, security reviews, Figma to code, deploys.

## What this means for us

1. **Most of what is popular is text.** Design taste, React rules, Postgres rules and debugging method are
   knowledge. They fit this registry, provided we write them from primary sources.
2. **Tool-heavy skills are plugins here.** Browser automation, office files and video rendering need code.
   `web-fetch` already covers reading pages, and office files would be a plugin.
3. **Product-bound skills belong with the product.** A Lark or Azure skill only makes sense next to that
   product's plugin.

## The gap: personal and soft skills

Everything above is for building software. Searching the same directory for coaching, learning, planning,
wellbeing, triage and personal assistance finds almost nothing with any use:

| Skill (source) | Installs |
|---|---|
| dbs-learning (dontbesilent2025/dbskill) | 20K |
| continuous-learning (affaan-m/ecc) | 10K |
| mentoring-juniors (github/awesome-copilot) | 7K |
| personal-productivity (refoundai/lenny-skills) | 5.6K |
| personal-assistant (ailabs-393) | 2.7K |
| energy-management (refoundai/lenny-skills) | 1.6K |
| daily-prep (github/awesome-copilot) | 1.4K |
| productivity-gtd, adhd-productivity, time-management | under 400 each |

The ones that come closest are the thinking tools from software (`grill-me`, `brainstorming`, `teach`,
`to-questionnaire`), each with hundreds of thousands of installs. People clearly want an assistant that
asks good questions and teaches well; nobody has written those skills for a person's life instead of their
code.

That is the gap Iris is built for: a personal assistant, living with one owner. The soft skills in the
roadmap come from this.
