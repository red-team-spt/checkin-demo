# Security rules

1. No SQL built by string concatenation or formatting. Use parameterized queries.
2. No shell command built from user input. Never use os.system or shell=True; pass an argument list.
3. No secret, token or password in the code.
4. No eval or exec on external data.
5. Validate and encode all external input before use.
6. GDPR: never log, print or store personal data (names, emails, phone numbers, IP addresses, identifiers, health or payment data) in clear text. Collect only what is needed and encrypt or pseudonymise what is stored.
7. Dependencies: do not add or upgrade a package to a version with a known vulnerability. Pin exact versions. Do not add unmaintained or suspicious packages or packages from untrusted sources.
