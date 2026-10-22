## 🛠️ Setup

To run the project locally, follow the steps below. We recommend using a virtual environment to avoid version conflicts.

**1. Clone the repository:**
```bash
git clone [https://github.com/mxrtaaa/fotoszop_app.git](https://github.com/mxrtaaa/fotoszop_app.git)
cd fotoszop_app
```

**2. Create a virtual environment:**
To avoid conflicts with other projects, create a virtual environment (`venv`) in the main application folder:
```bash
python -m venv venv
```

**3. Activate the environment:**
Before downloading dependencies and running the application, activate the virtual environment.

* **Windows (PowerShell):**
  ```bash
  .\venv\Scripts\activate
  ```
* **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```
*(Once activated correctly, `(venv)` will appear at the beginning of your terminal prompt).*

**4. Install dependencies:**
With the environment active, install all necessary packages with a single command:
```bash
pip install -r requirements.txt
```

**5. Run the application:**
Once the libraries are installed, launch the main GUI application:
```bash
python frontend/main_window.py
```
