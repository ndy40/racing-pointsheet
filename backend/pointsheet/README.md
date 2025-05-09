Production Mode DB settings:

DATABASE=sqlite:///${instance_path}/{DB_NAME}?PRAGMA journal_mode=WAL&PRAGMA busy_timeout=5000&PRAGMA synchronous=NORMAL&cache=shared
