# SafeGuard

A Python GUI application for managing insurance-related data.

## Installation

1. Clone the repository:
   ```powershell
   git clone https://github.com/luisraulfranco2007-bot/SafeGuard.git
   cd SafeGuard
   ```
2. Create a virtual environment:
   ```powershell
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Run

```powershell
python main.py
```

## Notes

- The `build/` and `dist/` folders are generated artifacts and are not included in this repository.
- If you add new dependencies, update `requirements.txt` using:
  ```powershell
  pip freeze > requirements.txt
  ```
