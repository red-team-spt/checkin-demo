# Security rules

1. No SQL built by string concatenation or formatting. Use parameterized queries.
2. No shell command built from user input. Never use os.system or shell=True; pass an argument list.
3. No secret, token or password in the code.
4. No eval or exec on external data.
5. Validate and encode all external input before use.
