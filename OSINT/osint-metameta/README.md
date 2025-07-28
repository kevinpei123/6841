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




## Indepth Build and Solution Notes

### Build Section

This challenge is a compact OSINT pivot chain that starts from a single file `screenshot.png` and drives a four‑step access→decode→access→decode path to a final image whose metadata contains the flag.
It implements the following artifacts and breadcrumbs:
the on‑image distraction text `Fatal build‑kite 9d2e12b7`, the EXIF Comment tag `KU5Y48zX` (a Pastebin‑looking ID), a Pastebin paste whose content is ROT13 of an Imgur or other hosted URL, and a downloadable image whose EXIF Comment holds the final flag. Because many hosts strip metadata in previews, I validated that the direct file still retains EXIF. 

Because the first breadcrumb lives in image metadata, solvers must check EXIF rather than chase the visible string on the pixels; the visible text is a deliberate red herring. The ROT13 layer is intentionally light‑weight so the focus stays on pivot discipline. The major issue I accounted for was metadata stripping by image hosts; I tested the direct download path (or self‑hosted file) to ensure the EXIF `Comment` with the flag persists. I initially considered making the paste discoverable from the on‑screen text, but because that risks guessability, EXIF is preferred for evidence and controlled difficulty. 


EXIF is the Exchangeable Image File Format which is a standard for storing metadata inside image files, it is usually used to describe how/where a photo was taken or processed and lets software organize/search photos without changing pixels. I used it in this case to write comments for each of the photos. 



---

## Solution Section

1. First I extract the initial breadcrumb from the PNG using EXIF tooling.
   It is a straightforward step to confirm whether the image contains a metadata hint; as a result, it can be used to recover the Pastebin‑style ID so that the users can progress with the challenge.
   The command I used was:

```bash
exiftool screenshot.png | grep -i 'comment'
```

where `exiftool` prints the metadata and `grep -i 'comment'` narrows to the EXIF Comment field.

and it gave me the results of

```
Comment                         : KU5Y48zX
```

2. Fetch the Paste by ID (pivot to web)

Open in a browser:

```bash
curl -s https://pastebin.com/raw/KU5Y48zX
```

This returns a URL‑shaped string but **ROT13**‑obfuscated (starts with `uggc://`).

3. Decode the ROT13 to recover the actual URL

Use a simple shell transform:

```bash
curl -s https://pastebin.com/raw/KU5Y48zX | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

This yields:

```
https://imgur.com/gallery/you-are-on-right-track-d2q5etf
```

4. Download the image file

Open the gallery and copy the direct image link or construct the direct host path, then download:

```bash
curl -L -o clue.png "https://imgur.com/gallery/you-are-on-right-track-d2q5etf"
```


5. Read EXIF from the final image to get the flag of flag{simple\_osint}

```bash
exiftool clue.png | grep -i 'comment'
```

and it gave me the results of

```
Comment                         : flag{simple_osint}
```

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



