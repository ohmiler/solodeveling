# Production customer identifier migration

Target: the primary production database.

Proposed procedure:

1. Run `python migrate.py --production` from an operator workstation.
2. Replace `customer_id` values in place using the new generated identifiers.
3. Drop the legacy `customer_id_backup` column immediately after the update.

The document does not name an approver, backup or restore point, staging rehearsal,
validation query, rollback or roll-forward procedure, or post-migration observation
window.
