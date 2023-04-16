clear

echo "Running main.py" && python3 main.py 2>&1

echo "Clearing cache" && find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete