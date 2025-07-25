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


