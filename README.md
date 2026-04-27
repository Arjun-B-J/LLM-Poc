# LLM-Poc

A proof-of-concept natural-language-to-SQL application ("Lumen.AI") that lets a
user ask questions in plain English, generates a MySQL query with a local LLM,
runs the query against a MySQL database, and renders the results in a Streamlit
UI.

## How it works

1. The user types a question in the Streamlit app.
2. `sqlcoder` (via Ollama) is prompted with the question plus the live database
   schema (dumped to `output.sql` by `getSchema.py`) and produces a SQL query.
3. `llama3` (via Ollama) is used as a clean-up pass to strip any prose and
   force the output into valid MySQL syntax (e.g. removing Postgres-isms like
   `NULLS LAST`).
4. The cleaned query is executed via `mysql-connector-python`, the rows are
   loaded into a pandas DataFrame, and the result is shown in the UI alongside
   the generated SQL. There is also experimental `pandasai` charting code.

## Tech stack

- Python
- [Ollama](https://ollama.com/) running `sqlcoder` and `llama3` locally
- LangChain (`langchain_community.llms.Ollama`) as the LLM client
- Streamlit for the UI
- MySQL via `mysql-connector-python`
- pandas + pandasai (for chart generation)
- Hugging Face `transformers` with `defog/sqlcoder2` (alternative path in
  `app.py`, not used by the Streamlit app)

## Files

- `streamlitApp.py` — main Streamlit app (Lumen.AI).
- `pipeline.py` — CLI version of the same NL-to-SQL flow.
- `langchainOllama.py` — minimal Ollama smoke test.
- `app.py` — alternative path using Hugging Face `defog/sqlcoder2` directly.
- `getSchema.py` — dumps `SHOW CREATE TABLE` for every table in the configured
  database into `output.sql`, which is then injected into the LLM prompt.
- `runSQL.py` — small standalone script for running a hand-written query.
- `schema.txt` / `output.sql` — example / generated schema dumps.
- `demo/`, `Demo Sped Up/`, `Latest/` — demo recordings / assets.

## Running it

Prerequisites:

- Python 3.10+
- A running MySQL server with a database you want to query
- [Ollama](https://ollama.com/) installed locally, with the models pulled:
  ```
  ollama pull sqlcoder
  ollama pull llama3
  ```

Setup:

```bash
pip install -r requirements.txt
# the requirements file does not currently pin streamlit / langchain /
# mysql-connector-python / pandasai / ollama — install those as needed:
pip install streamlit langchain langchain-community mysql-connector-python pandas pandasai
```

## Configuration

MySQL connection details are read from environment variables. Copy
`.env.example` to `.env` and fill in your values, or export them in your
shell before running the scripts:

```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password_here
export MYSQL_DATABASE=your_db_here
```

On Windows PowerShell, use `$env:MYSQL_PASSWORD = "..."` etc.

Then:

```bash
# 1. Dump the schema the LLM will see
python getSchema.py

# 2. Launch the UI
streamlit run streamlitApp.py
```

## Status

This is an exploratory proof of concept. Database credentials are hard-coded,
there is no input sanitization on the LLM-generated SQL, and the chart path in
`streamlitApp.py` is a hard-coded absolute path — none of this is intended for
production use.
