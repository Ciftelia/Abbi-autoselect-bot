## How to Run

### On Assigned Laptop (Windows)

1. Open **Git Bash**
2. Run:

   ```bash
   cd /path/to/folder/
   python auto-upload-abii-questions.py
   ```

---

### On Other Computers

### 1. Install ChromeDriver

Download the appropriate version of ChromeDriver from:  
[https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)

---

### 2. Running the Script

#### On Bash

```bash
cd /path/to/folder/
chmod +x ./intro.bash
./intro.bash
```

---

#### Other
```
cd /path/to/folder/
pip install -r requirements.txt
python auto-upload-abii-questions.py
```

---

### Troubleshooting

- Make sure you have Python 3 and pip installed.
- Ensure ChromeDriver is in your system PATH or in the project folder.
- If you see errors about missing packages, run:  
  ```bash
  pip install -r requirements.txt
  ```
- For environment variables, create a `.env` file with your credentials:
  ```
  EMAIL=your_email@example.com
  PASS=your_password
  ```
- If you encounter issues, try running the script in a clean virtual environment.

