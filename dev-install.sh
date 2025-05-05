# Create a virtual environment (if not already done)
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt