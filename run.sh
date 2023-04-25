clear

python3 tests.py -b 2>&1

echo "Running main.py" && python3 main.py > /dev/null 2>&1

echo "Clearing cache" && find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete