# GaonBooks-Web

가온북스 책검색 웹사이트

- python 3.12

## pre-commit run

```bash
pipenv run pre-commit run --all-files
```

## run - backend

```bash
pipenv run gunicorn app.main:app \
    --name gaonbooks-dev \
    -w 2 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile ./gunicorn-access.log \
    --error-logfile ./gunicorn-error.log \
    --capture-output \
    --log-level info \
    --daemon
```

```bash
pipenv run uvicorn app.main:app --reload
```

## run - frontend

```bash
npm run dev -- --port 5555
```
