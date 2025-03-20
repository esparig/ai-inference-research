mkdir mlserver-test
cd mlserver-test/
uv init --python=python3.11
uv add pip mlserver spacy wikipedia-api
uv run python -m spacy download en_core_web_lg

mkdir -p similarity_model
uv run python check.py 

uv run python app.py





