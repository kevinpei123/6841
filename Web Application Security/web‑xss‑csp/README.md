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



## How Difficulty Was Increased

I increased the difficulty that blocked the obvious script injections by using manual html escaping, this forces the solver to actually look at the website precisely. I also increased the difficulty by adding a chain of different elements that forced solvers to use string‑break → CSP bypass → same‑origin script instead of using a one-liner.


---

## Defence Mechanisms

- I implemented a basic character escape of `& < > "` to stop HTML injection directly
- I implemented a Content-Security-Policy to remove the use of inline scripts
- I stored the flag in a secure cookie requiring javascript execution on the same origin for exfiltration


---

## Related & Future Variants

- Stored XSS where the script is permanently stored on the vulnerable web server, often in a database, this can combine with sqli
- DOM-based XSS where the attack occurs entirely within the client-side code.


---

### Sources

* **MDN – Content Security Policy** https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
* **PortSwigger – DOM‑based XSS** https://portswigger.net/web-security/cross-site-scripting/dom-based
* **PayloadsAllTheThings – XSS** https://github.com/swisskyrepo/PayloadsAllTheThings#xss-cross-site-scripting
