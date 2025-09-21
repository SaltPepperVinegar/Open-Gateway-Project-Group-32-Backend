run:
\tuvicorn app.main:app --reload
lint:
\truff check .
fmt:
\tblack .
type:
\tmypy app
test:
\tpytest -q
