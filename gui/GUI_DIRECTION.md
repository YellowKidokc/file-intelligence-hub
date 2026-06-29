# GUI Direction

The GUI should become the primary operator console.

## It should handle

- file rename approval
- folder summary review
- tag review
- search by extension / tag / folder / confidence
- move / copy / archive actions
- threshold confirmations
- low-confidence queue

## It should not be responsible for

- being the only source of truth
- holding the durable ledger
- doing all heavy parsing itself

That belongs to SQLite + parser/API workers.

## Excel still matters

Excel remains useful for:

- exports
- comparison sheets
- summaries
- manual audit slices

But the "daily driving" should happen in the GUI.
