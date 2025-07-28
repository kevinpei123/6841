# HTTP Exfiltration - Personalised Write‑up


**Category:** Forensics – 400 pts  
**Flag:** `flag{http:forensics}`

---

## Challenge Flow



1. A PCAP containing HTTP traffic is given. 
2. You can export the embedded files of http traffic with tshark
tshark -r network.pcap --export-objects http,http_objs
3. inside the embedded files you can find a secret.zip that can be unzipped
unzip secret.zip -d extracted
4. Inside theres an image `payload.png`
5. read its exif comment to find the solution
exiftool extracted/payload.png | grep -i 'comment'
6. Submit **flag{http:forensics}**.

---

## How Difficulty Was Increased and Defense Mechanisms

I initially got the idea for this CTF because I am concurrently doing COMP3331 which is network security and wanted to mirror and imitate the layered protocol analysis. As a result, I used a multi-stage pupeline of using http export, archive unpacking and also metadata extration instead of more simple steps. I also increased the difficulty by using a stealth transfer where unless you are using the correct reader, you would not be able to understand what the files are, but in vscode you can see the secret.zip. The solvers must locate the .zip and the .png files so generic filenames won't work. Once unzipped, the PNG has no visible clues, as the flag lives in the EXIF comment

---




### Build Section

This challenge is a compact network‑forensics pivot chain that starts from a single capture file `network.pcap` and drives an export→unzip→metadata path to a final image whose EXIF comment contains the flag.
It implements the following artifacts and breadcrumbs:
an **HTTP/1.1 transfer** of a ZIP `secret.zip` inside the PCAP, a **ZIP entry** `payload.png`, and an **EXIF Comment** on that PNG that holds the final flag. Because raw HTTP can be segmented, chunked, or compressed in transit, I validated that object reassembly works end‑to‑end and that the exported ZIP is byte‑accurate and unzip‑able.

Because the first artifact is the captured HTTP objects, solvers must export the objects. The file bytes ride in TCP segments and need reassembly. The ZIP layer is extremely light so the focus stays on packet→object workflow, and the second layer (image metadata) requires a tools pivot (EXIF) so accidental guesses fail. The major issues I accounted for were TCP/HTTP reassembly and potential content‑encoding.
I used TCPdump to make the pcap file as it captured the network packets are they were transmited. I used EXIF in this case to store a **Comment** on `payload.png` that yields the flag after object export and unzip.

---

## Solution Section

1. First I confirm the PCAP contains HTTP flows and locate candidate objects.

```bash
tshark -r network.pcap -Y http -T fields -e http.request.method -e http.host -e http.request.uri -e http.response.code | head
```

where `-Y http` filters HTTP packets, and the `-T fields ...` view shows requests/responses that imply downloadable content.

2. Export the HTTP objects

Use `tshark`’s object export to a directory:
Tshark is the command‑line version of Wireshark. It captures and analyzes packets, applies the same display filters as Wireshark and can be used in this install to get the file from network.pcap

```bash
mkdir -p http_objs
tshark -r network.pcap \
  -o tcp.desegment_tcp_streams:TRUE \
  -o http.desegment_body:TRUE \
  -o http.reassemble_body:TRUE \
  --export-objects http,http_objs
```

This writes each reassembled HTTP body to `http_objs/` with filenames.

3. Locate and verify the embedded ZIP

List the directory and check integrity:

```bash
ls -l http_objs
unzip -t http_objs/secret.zip
```

This confirms `secret.zip` exists.

4. Unzip and inspect the PNG

Extract the archive to a working folder:

```bash
unzip -o http_objs/secret.zip -d extracted
ls -l extracted
```

Inside there’s an image `payload.png`.

5. Read EXIF from the final image to get the flag of **flag{http\:forensics}**

```bash
exiftool extracted/payload.png | grep -i 'comment'
```

and it gave me the results of

```
Comment                         : flag{http:forensics}
```

6. Submit **flag{http\:forensics}**.

---






---

## Related & Future Forensics Variants

- HTTP header exfiltration via custom fields embedding flag fragments in requests.
- Steganography in HTTP‑transferred media requiring both metadata and pixel analysis.
- Chunked Transfer‑Encoding reassembly to reconstruct split payloads across multiple segments.



---

### Sources

- **ExifTool** https://exiftool.org/
- **tshark HTTP object export**: https://www.wireshark.org/docs/man-pages/tshark.html
- **Wireshark User’s Guide**: https://www.wireshark.org/docs/wsug_html_chunked/
- **COMP3331 materials**


