# Launch links

Use the channel-specific URL when publishing:

- Reddit: <https://garda.s1st.de/go/reddit>
- Discord: <https://garda.simon-stieber.de/go/discord>
- LinkedIn: <https://garda.simon-stieber.de/go/linkedin>
- Windinfo: <https://garda.simon-stieber.de/go/windinfo>

All three paths render the regular forecast directly. The Reddit link uses the
pseudonymous `s1st.de` face; it suppresses the personal credit and keeps links
to the Walchensee project's pseudonymous host. Cloudflare Web Analytics
therefore records the path without relying on query parameters, which its RUM
dataset does not expose. The private stats dashboard labels these paths as
Reddit, Discord and LinkedIn. Cloudflare figures can arrive with roughly a
24-hour delay.
