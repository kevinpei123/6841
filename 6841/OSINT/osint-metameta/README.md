# Simple_osint – Personalised Write‑up

**Category:** OSINT – 150 pts  
**Flag:** `flag{simple_osint}`

---

## Challenge Flow


1. This challege began with the screenshot.png that displayed a clear error string of “Fatal build‑kite 9d2e12b7”
2. This PNG then had an EXIF "Comment" tag of `KU5Y48zX`
3. Using what looks like the end of an url, append this to `https://pastebin.com/` to fetch the paste
4. the Paste contains a ROT13‑obfuscated Imgur link
5. decode the paste and fetch an imgur url that can be donwloaded `https://imgur.com/gallery/you-are-on-right-track-d2q5etf`
6. find the flag using the EXIF "Comment" tag which gives the flag of flag{simple_osint}




---

## How Difficulty Was Increased and Defense Mechanisms


I inreased the difficulty by using layered obfuscation as the on-screen text is a diversion that would make many people confused. However, the pasteid is actually in an EXIF comment and not in related to the screenshot at all. I also increased the difficulty by requiring the player to have a layer of undestanding about the endings of urls and for the player to test many websites to find where the clue is. Furthermore, I used a cipher as I thought that it could be extremely easy if the user just got the solution from there and added the rot13 decode to the imgur url into the exif read. 


I also increased the difficulty by adding a large number of layers to the ctf where a layered “access → decode → access → decode” pattern echoes multi‑stage pivots, teaching that real‑world hunts often chain distinct extraction and decoding steps. I took inspiration from ssh related systems to overcome the challenge of increasing the difficulty of the challenge. For example, ssh uses "encrypt → access → decrypt". I flipped it on its head to make solving the ctf easier by making it sort of a reverse ssh, where it it access, decrypt, access, to get the solution. 


---

## Related & Future Variants


- Social‑media pivot: error ID leads to an Twitter post where the flag is hidden in the post’s image EXIF metadata
- Archive retrieval: original Pastebin entry is deleted, forcing use of the Wayback Machine to recover the ROT13 payload
- DNS TXT lookup: clue encoded in a DNS TXT record on a stealth subdomain, requiring dig to extract the paste ID and proceed



---

### Sources

- **ExifTool** https://exiftool.org/  
- **Pastebin FAQ**: https://pastebin.com/faq  
- **Imgur** https://imgur.com/  
- **OSINT Techniques** https://github.com/lockfale/osint-techniques  
- **OSINT Framework** https://osintframework.com/  
- **OSINT Tools by Open Source Intelligence Techniques** https://www.osintprinciples.com/tools/  



