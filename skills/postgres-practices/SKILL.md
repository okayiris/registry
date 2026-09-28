---
name: postgres-practices
description: Working well with PostgreSQL - reading EXPLAIN ANALYZE, choosing indexes and when not to, avoiding N+1 queries, pooling connections, transactions and isolation, migrations that do not lock out users, row-level security and vacuum - from the PostgreSQL and PgBouncer documentation.
whenToUse: When the owner says "deze query is traag", "waarom gebruikt hij mijn index niet", "can you add an index", "the app runs out of connections", "the migration locked the table", "hoe zet ik row level security aan", "do I need to run VACUUM", when you write or review SQL, a schema change or a migration for PostgreSQL, or before you run anything against a production database.
---

# PostgreSQL practices

## What it is

Practical rules for PostgreSQL, each taken from the official documentation. On 28 September 2026 the
current documentation is for **PostgreSQL 18**; 19 is in development. Ask which version the owner runs
(`SELECT version();`) before relying on details.

**Production is the owner's.** Reading plans is safe. Anything that changes data or schema on a shared or
production database waits for the owner's yes (see `acting-on-behalf`), and `EXPLAIN ANALYZE` counts as
running the query.

## 1. Read the plan before changing anything

`EXPLAIN` shows the plan the planner chose: a tree of nodes, scans at the bottom, joins and sorts above.
`EXPLAIN ANALYZE` also **runs** the query and shows what really happened.

| In the output | What it means |
|---|---|
| `cost=0.00..445.00` | Estimated start-up and total cost, in arbitrary units (not milliseconds). A parent's cost includes its children. |
| `rows=` (estimate) | Rows the node is expected to **emit**, not rows it scans |
| `actual time=... rows=... loops=` | Real milliseconds and rows, **averaged per loop**; multiply by `loops` for the total |
| `Rows Removed by Filter` | Rows read and thrown away: a sign the condition is not used as an index condition |
| `Index Cond` vs `Filter` | An index condition narrows what is read; a filter checks each row after reading |
| `Buffers: shared hit=... read=...` | Pages found in cache (hit) and pages read |

What to look for first, in the docs' words: **whether the estimated row counts are reasonably close to
reality**. Estimates come from statistics that `ANALYZE` gathers from a sample of the table; when they are
far off, check that the table has been analyzed recently.

Cautions from the documentation:

- `EXPLAIN ANALYZE` has side effects: an `UPDATE` or `DELETE` really happens. To look at one safely, wrap it:
  `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`
- Its timing leaves out network transfer and adds measurement overhead.
- **Do not extrapolate from a small table.** The planner's costs are not linear; on a table of one page it
  nearly always chooses a sequential scan, index or not. Test on realistic data sizes.

## 2. Indexes: which, and when not

- `CREATE INDEX` makes a **B-tree** by default, which fits the common cases. Other methods (`hash`,
  `gist`, `spgist`, `gin`, `brin`) exist for other kinds of data and queries.
- An index on a column used in a **join condition** can speed up joins a lot; indexes also help `UPDATE` and
  `DELETE` with a `WHERE`.
- **Composite (multicolumn) order matters.** A B-tree on `(a, b)` works best with conditions on the leading
  column. Equality on leading columns plus a range on the next one limits what is scanned; conditions on
  later columns are checked in the index but may not shrink the scan. The current version can sometimes skip-scan
  when the leading column has few distinct values, but do not design around that. The docs advise using
  multicolumn indexes **sparingly**; more than three columns rarely helps.
- **Partial indexes** (`CREATE INDEX ... WHERE billed IS NOT TRUE`) index only the rows queries look for,
  which keeps the index small and cheaper to maintain. The query's `WHERE` must imply the index predicate.
  Do **not** make one partial index per category value; one index on `(category, data)` is better, and
  partitioning is the tool for truly huge tables.
- **When not to add one.** Every index must be kept in step with the table, which slows writes and can
  prevent heap-only tuple (HOT) updates. Remove indexes that are seldom or never used. A query that returns
  a large share of the table will not use an index anyway.

## 3. Avoid N+1 queries

This is practice advice, not a PostgreSQL term: code fetches a list (1 query), then runs one more query per
row (N queries). Each round trip costs time even when each query is fast.

- Fetch the related rows in one go: a `JOIN`, or one query with `WHERE id = ANY($1)` for a list of ids.
- In an ORM, use its eager-loading option for the relation.
- Spot it in logs: the same statement repeated many times per request.

## 4. Connections and pooling

When many clients (several app instances, serverless functions) each open their own connections, a
pooler such as **PgBouncer** shares a smaller set of server connections among them. How many connections
the server and pool should have depends on the setup; that is a measurement, not a rule.

| PgBouncer mode | A server connection belongs to a client | Notes |
|---|---|---|
| Session | For the whole client connection | Supports all PostgreSQL features |
| Transaction | Only during a transaction | Breaks some session features; the application must cooperate |
| Statement | Only for one statement | Multi-statement transactions are not allowed |

In **transaction pooling** these never work: `SET`/`RESET`, `LISTEN`, `WITH HOLD` cursors, SQL-level
`PREPARE`/`DEALLOCATE`, temp tables that keep rows across transactions, `LOAD`, and session-level advisory
locks. Protocol-level prepared statements work only when `max_prepared_statements` is non-zero. Check the
application for these before switching modes.

## 5. Transactions and isolation

| Level | What it gives | What the app must do |
|---|---|---|
| Read Committed (default) | Each statement sees data committed before **that statement** began | Two `SELECT`s in one transaction can see different data |
| Repeatable Read | One stable snapshot for the whole transaction | Retry on serialization failure |
| Serializable | Result is as if transactions ran one at a time | Retry on serialization failure (SQLSTATE `40001`) |

Read Uncommitted behaves like Read Committed in PostgreSQL. With Repeatable Read or Serializable, the
application needs a general way to **retry the whole transaction** from the start.

Also from the documentation:

- Keep transactions as small as integrity needs.
- Do not leave connections "idle in transaction". An open transaction holds its locks and stops vacuum from
  removing dead rows; `idle_in_transaction_session_timeout` can end such sessions.
- Take locks on several objects in the **same order** everywhere to avoid deadlocks. PostgreSQL detects a
  deadlock and aborts one transaction; which one cannot be predicted, so be ready to retry.

## 6. Migrations without locking out users

Without a deadlock, a transaction waiting for a lock **waits indefinitely**. Know what each step locks.

| Step | Lock and effect | Safer way |
|---|---|---|
| `CREATE INDEX` | Blocks writes (not reads) until done; hours on a very large table | `CREATE INDEX CONCURRENTLY` |
| Most `ALTER TABLE` forms | `ACCESS EXCLUSIVE`: blocks even `SELECT` | Keep it short; set `lock_timeout` |
| `ADD COLUMN` with a volatile default (such as `clock_timestamp()`) | Rewrites the whole table and its indexes | A non-volatile default or no default is fast, with no rewrite |
| Changing a column's type | Usually rewrites the table and indexes | Plan it, or add a new column and backfill |
| Adding a foreign key or `CHECK` | Scans the whole table | `ADD CONSTRAINT ... NOT VALID`, then `VALIDATE CONSTRAINT` (takes only `SHARE UPDATE EXCLUSIVE`) |

About `CREATE INDEX CONCURRENTLY`:

- It scans the table twice and waits for older transactions, so it takes longer and adds load.
- It **cannot run inside a transaction block**, which matters for migration tools that wrap every
  migration in one.
- If it fails, it leaves an **`INVALID`** index that is not used for queries but still costs on every write.
  Drop it and try again, or `REINDEX INDEX CONCURRENTLY`.
- Only one concurrent build per table at a time.

Set `lock_timeout` for the migration session only (the docs advise against setting it server-wide), so a
step that cannot get its lock fails quickly instead of waiting. Then retry at a quieter moment.

## 7. Row-level security (RLS)

- `ALTER TABLE t ENABLE ROW LEVEL SECURITY;` then `CREATE POLICY`. With RLS on and **no policy, nothing is
  visible**: the default is deny.
- **Superusers and roles with `BYPASSRLS` always bypass it, and so does the table owner** unless you run
  `ALTER TABLE t FORCE ROW LEVEL SECURITY`. Test as the role the application really uses.
- `USING` filters existing rows; `WITH CHECK` controls rows being inserted or updated. A policy for all
  commands with only `USING` uses that same expression as its `WITH CHECK`.
- Several permissive policies combine with `OR`; restrictive policies combine with `AND`.
- Unique, primary key and foreign key checks bypass RLS, which can leak whether a row exists. Design keys
  with that in mind.
- `TRUNCATE` is not subject to RLS.

## 8. VACUUM and autovacuum

`VACUUM` reclaims space from updated and deleted rows, updates planner statistics, updates the visibility
map (which speeds up index-only scans), and protects against **transaction ID wraparound**, which the docs
call catastrophic data loss if ignored.

- Let the **autovacuum daemon** do it. The docs call disabling it unwise unless the workload is extremely
  predictable.
- Plain `VACUUM` runs alongside normal work. **`VACUUM FULL`** takes an `ACCESS EXCLUSIVE` lock and needs
  extra disk space; avoid it in normal operation.
- For a table emptied regularly, `TRUNCATE` beats `DELETE` plus `VACUUM`.
- Long-open transactions stop vacuum from cleaning up. Find them in `pg_stat_activity`.
- Autovacuum does not analyze partitioned parent tables; run `ANALYZE` on them yourself.

## What not to claim

- Do not promise an index will be used. Show the plan before and after, on realistic data.
- Do not read `cost` as milliseconds.
- Do not call a migration safe without naming the locks it takes.
- Do not present N+1 or pool sizing numbers as PostgreSQL rules; they are practice.

## Where this stops

Based on the PostgreSQL 18 documentation (Using EXPLAIN; Indexes: introduction, multicolumn, partial;
CREATE INDEX; ALTER TABLE; Explicit Locking; Transaction Isolation; Client Connection Defaults; Row
Security Policies; Routine Vacuuming) and PgBouncer's feature page, read on 28 September 2026. Managed
services (cloud databases, Supabase and others) add their own roles, poolers and limits: read their
documentation too. Replication, backups, tuning server memory and partitioning design are outside this
skill.
