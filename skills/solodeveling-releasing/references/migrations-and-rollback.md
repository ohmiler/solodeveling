# Migrations and recovery

Treat destructive, irreversible, or production migration work as Critical.

## Prove the transition

- Identify source and target schema or data versions, invariants, volume, concurrency,
  compatibility with old and new application versions, and irreversible operations.
- Exercise the forward transition on representative and edge data. Check nulls,
  duplicates, maximum sizes, ordering, partial records, encoding, and interrupted
  execution where relevant.
- Verify integrity with counts, constraints, checksums, business invariants, and
  application reads and writes. Test idempotency or document why it is impossible.
- Validate backup creation and restoration, not merely backup existence. Redact data
  and credentials from evidence.

## Choose recovery before execution

Define rollback and roll-forward procedures, decision owner, trigger, time limit, and
data-loss or compatibility consequences. Some data changes cannot be safely rolled
back; prefer expand/migrate/contract or another staged transition and name the point
of no return.

Never execute a destructive migration without explicit user authority for the exact
environment and a credible recovery decision. On unexpected behavior, stop further
mutation when safe, preserve timestamps and evidence, assess integrity, and follow
the predefined rollback or roll-forward path.
