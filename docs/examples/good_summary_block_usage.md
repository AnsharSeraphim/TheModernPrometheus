# Good Summary Block Usage Example

## Correct pattern

1. Run the required wrappers:
   - `python scripts/run_precommit_suite.py`
   - `python scripts/run_tests.py`
2. Copy only the final summary blocks from:
   - `build/automation_contract/precommit_summary_block.txt`
   - `build/automation_contract/test_summary_block.txt`
3. Paste those blocks in PR notes and final session summaries.

## Why this is good

- Preserves canonical evidence formatting.
- Avoids ambiguous progress logs or clipped output.
- Makes pass/fail status and command provenance auditable.
