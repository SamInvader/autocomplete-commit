# Auto-Commit

A **human-friendly Git commit message generator**.  
It scans your repository, detects changes, and produces clear commit messages that are easy to read.  
Perfect for developers who want to speed up their commit workflow.

---

## ✨ Features
- Detects **added, modified, deleted, renamed** files
- Shows **exact lines** changed (optional)
- **Human-readable messages** (no cryptic logs)
- Works as a **command-line tool**
- Multiple options to customize output

---

## 🚀 Installation
```bash
pip install autocommit
```

---

🔧 Usage

After installing, run:
```bash
autocommit --help
```
Example
```bash
autocommit --verbose --show-lines --flavor
```
Output:
```
Created file main.py
Changes in main.py:
  + print("Hello world")

Modified file cli.py
Changes in cli.py:
  - print("old")
  + print("new")

🚀 Let's go!
```

---

⚙️ Arguments

Flag / Option	Description

--verbose	Show detailed file list
--show-lines	Show exact added/removed lines
--flavor	Add a fun ending (🚀, ✅, 🔥, etc.)
--short	Shorten messages for quick commits
--no-color	Disable colored output



---

📌 Example Workflow
```
git add .
autocommit --verbose --show-lines
git commit -m "$(autocommit --short)"
```

---

📝 License

This project is licensed under the MIT License.


---

⚡ Coming Soon

An NPM version of Autocomplete Commit for JavaScript/Node.js developers.
