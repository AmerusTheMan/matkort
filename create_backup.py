import sqlite3
from pathlib import Path
from datetime import date, datetime, timedelta

backup_dir = Path("database_backup")

source = sqlite3.connect("data.db")
backup = sqlite3.connect(backup_dir / f"backup_{date.today()}.db")

with backup:
    source.backup(backup)

backup.close()
source.close()


cutoff = datetime.now() - timedelta(days=10)

for file in backup_dir.iterdir():
    if file.is_file():
        modified = datetime.fromtimestamp(file.stat().st_mtime)

        if modified < cutoff:
            file.unlink()
            print(f"Deleted: {file}")

