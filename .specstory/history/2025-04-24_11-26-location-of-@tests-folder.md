<!-- Generated by SpecStory -->

# Location of @tests Folder (2025-04-24 13:26:14)

_**User**_

should the@tests folder be where it is?  

---

_**Assistant**_



---

Let me check the current project structure and determine the proper location for the tests folder.

---

Read file: pyproject.toml

---

Let me examine how the source code is organized:

---

<details>
            <summary>Listed directory src/mimearchivefs • **6** results</summary>
        
| Name |
|-------|
| 📄 `ziplike.py` |
| 📄 `exceptions.py` |
| 📄 `filesystem.py` |
| 📄 `core.py` |
| 📄 `__init__.py` |
| 📄 `utils.py` |

</details>

---

Now I'll check if there's a top-level tests directory:

---

Could not resolve URI: Error: Unable to resolve nonexistent file '/Users/adam/Developer/vcs/github.twardoch/MimeArchiveFS-py/tests'

---

Based on the project structure and the content of `pyproject.toml`, I can see:

1. The main source code is in `src/mimearchivefs/` directory
2. There are test files in `mimearchivefs/tests/`
3. The `pyproject.toml` configuration shows:
   - `testpaths = ["tests"]` (in pytest configuration)
   - The sdist build includes `"tests"` at the top level

No, the tests folder should not be where it currently is. According to the project configuration:

1. Tests should be in a top-level `tests/` folder (at the same level as `src/`), not inside the `mimearchivefs/` package
2. The `pyproject.toml` is configured to look for tests in `tests/` at the project root

You should move the tests from `mimearchivefs/tests/` to a top-level `tests/` directory to match the configuration in your `pyproject.toml`.

---



---

