#!/bin/bash

cat > .git/hooks/pre-commit <<EOF
#!/bin/bash
uv run mypy .
uv run ruff format .
uv run ruff check --select I,RUF022 --fix .
EOF

chmod +x .git/hooks/pre-commit

echo 'Pre-commit hook is set!'