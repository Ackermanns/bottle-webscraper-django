from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.getcwd()
DB_LOCATION = os.path.join(BASE_DIR,"base\\scripts\\database\\booze.db")

print(DB_LOCATION)