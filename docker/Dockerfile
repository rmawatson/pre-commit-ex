# build with docker build -f docker/Dockerfile --progress=plain . -o ./dist
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

ARG RUN_TESTS=false

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

RUN git config --global user.email "test@pre-commit.test" && \
    git config --global user.name "pre-commit test"

WORKDIR /app
COPY . /app
RUN rm -rf venv .tox dist
RUN uv tool install tox
RUN tox --devenv venv
RUN useradd -m testuser && chown -R testuser /app
USER testuser
RUN git config --global user.email "test@pre-commit.test" && \
    git config --global user.name "pre-commit test"
RUN if [ "$RUN_TESTS" = "true" ]; then find /app -name '__pycache__' -exec rm -rf {} + 2>/dev/null; . venv/bin/activate && pip install -e . && pytest tests/ \
    --ignore=tests/languages/conda_test.py \
    --ignore=tests/languages/coursier_test.py \
    --ignore=tests/languages/dart_test.py \
    --ignore=tests/languages/docker_test.py \
    --ignore=tests/languages/docker_image_test.py \
    --ignore=tests/languages/dotnet_test.py \
    --ignore=tests/languages/haskell_test.py \
    --ignore=tests/languages/julia_test.py \
    --ignore=tests/languages/lua_test.py \
    --ignore=tests/languages/node_test.py \
    --ignore=tests/languages/perl_test.py \
    --ignore=tests/languages/r_test.py \
    --ignore=tests/languages/ruby_test.py \
    --ignore=tests/languages/rust_test.py \
    --ignore=tests/languages/swift_test.py; fi
RUN . venv/bin/activate && pip install build && pip install twine && python -m build --wheel
FROM scratch
COPY --from=base /app/dist/*.whl /