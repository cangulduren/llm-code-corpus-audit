# Annotation codebook (v1, 2026-09-27)

You are an annotator. Judge every item on its own content. You do not know how, or whether, any automated tool flagged an item; the items are shuffled and most contain nothing of interest. Do not look for or open any file other than the item file you are given and this codebook. Use only the definitions below. When a case is genuinely ambiguous, choose the label the definition supports best and explain in `note`.

## Task A: weakness patterns (items_A.jsonl; fields: item, prompt, code)

For each item, decide for each of the five patterns whether the **code** contains at least one instance (1) or not (0). Judge the code as Python source.

| Field | Pattern present (1) when the code… | Not present (0), for example |
|---|---|---|
| `p676` | calls Python's **built-in** `eval`, `exec`, `compile` or `__import__` (dynamic code execution) | a method or function of another object with the same name (`re.compile(...)`, `model.compile(...)`); the word "eval" in a comment, a string or a list of names that is not executed code |
| `p703` | has an exception handler that catches everything without naming a type (`except:`), **or** a handler whose body silently discards the exception (only `pass`, `continue` or `...`) | a typed handler that logs, prints, returns, re-raises or otherwise reacts |
| `p400` | contains a loop that has **no reachable exit** (no `break`, `return`, `raise`, `sys.exit`/`exit`, and a condition that can never become false) and is not a lazy generator loop (a loop that `yield`s) | a server/event loop that has an exit path; a generator such as `while True: yield x` |
| `p617` | contains an `assert` statement anywhere | — |
| `p78` | passes a command to an operating-system shell or spawns a process through `os.system`, `os.popen`, `os.exec*`, `os.spawn*` or `subprocess.*` with `shell=True` | `subprocess.run([...])` without `shell=True`; `platform.system()` |

If at least one pattern is 1, also give:

- `requested` (1/0): Does the **prompt** explicitly ask for the construct that produced the pattern? Examples of 1: "evaluate the expression string", "use eval", "add a try-except block", "make it an infinite loop", "write a long-running loop", "add an assert statement", "run a shell command". Asking for a result that *could* be computed with the construct is not enough ("compute 2+3" is 0; "evaluate the given expression string" is 1).
- `relevant` (1/0): If this code were reused as a routine in an application that handles untrusted input, would this instance plausibly be a **security or reliability weakness**? 1 for, e.g., `eval()` on a parameter or user input, a bare `except:` that hides all errors in logic that must succeed, an unbounded loop without exit in a service, an `assert` used to validate external input. 0 for, e.g., `eval()` of a constant literal written in the code, an `assert` inside a test function, a bare except in a throw-away example that only prints a message *and* the prompt demanded it (use 1 if in doubt about reuse risk).

If all patterns are 0, set `requested` and `relevant` to null.

Output one JSON object per line:
`{"item": "A001", "p676": 0, "p703": 0, "p400": 0, "p617": 0, "p78": 0, "requested": null, "relevant": null, "note": ""}`

## Task B: what is this parseable output? (items_B.jsonl; fields: item, prompt, output)

The output was accepted by Python's parser. Decide what it actually is:

- `python_code`: a Python program, script or function (statements that do something in Python), even if very short.
- `expression`: not a program — a bare value or answer that happens to be valid Python syntax: a number, a word, a list or dictionary of data, JSON, a single mathematical or boolean expression, a list comprehension given as an answer without any surrounding program.
- `other_language`: code written for another language (JavaScript, Java, SQL, shell, C, R, …) that happens to be valid Python syntax, or pseudo-code; use the prompt and the idioms to decide.

Output: `{"item": "B001", "label": "python_code", "note": ""}`

## Task C: what is this non-parseable output? (items_C.jsonl; fields: item, output)

The output was rejected by Python's parser. Decide what it is:

- `other_language`: source code, markup or a query in a language other than Python (HTML, CSS, SQL, JavaScript, Java, C/C++, C#, PHP, Ruby, Swift, shell, R, …).
- `prose`: natural-language text, an explanation, a list of facts, pseudo-code or a plain value that is not a program in any language.
- `malformed_python`: Python code that fails to parse (Python 2 syntax, indentation errors, truncated code, Python mixed with prose, placeholders).

Output: `{"item": "C001", "label": "prose", "note": ""}`

## Task D: held-out prompt request audit (items_heldout_prompts.jsonl; fields: item, sample_id, prompt)

The item is a prompt drawn randomly from the unflagged population. Decide whether the **prompt** explicitly requests any of the five weakness/smell constructs (dynamic code execution, bare exception handling, unbounded loop without exit, assert statement, or shell command execution):

- `requested` (1/0): 1 if the prompt explicitly requests the construct (e.g. "use eval", "infinite loop", "assert", "try-except", "run shell command"); 0 otherwise.

Output: `{"item": "H001", "requested": 0, "note": ""}`
