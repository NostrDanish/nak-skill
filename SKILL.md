---
name: nak
description: Interact with Nostr using the nak CLI (Nostr Army Knife). Use when nak is installed or should be installed for keys, encode/decode, fetch, req, publish, relay sync, NIP-42 auth, bunker signing, POW, or git-over-Nostr. For protocol rules and stdlib Python tools, also load the `nostr` skill. For live NIP text, load `nostr-nips`.
license: CC-BY-SA-4.0
nak_version: "check with `nak --version` before relying on flags"
---

# nak — Nostr Army Knife

GitHub: https://github.com/fiatjaf/nak

Use nak when you want a **real CLI** against relays. Use `nostr` skill scripts
when you need stdlib-only sign/verify or the user does not have Go/nak.

## Install

```bash
curl -sSL https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh | sh
# or: brew install nak
# or: go install github.com/fiatjaf/nak@latest
nak --version
```

## Safety

- The nsec **is** the account. Prefer `$NOSTR_SECRET_KEY` in the environment
  over `--sec` on the command line (argv is visible in `ps`).
- Never paste an nsec into chat, logs, or a committed file.
- Interactive / user-key signing: `--connect bunker://…` (NIP-46). Bots may
  hold an nsec in env; humans should not.
- `nak key generate` output is a secret. Treat the file like an nsec.

## Task routing

| Job | Start with |
|---|---|
| Find events / NIP-05 / live stream | `nak fetch` (hints in the id) or `nak req` (explicit relays) |
| Copy or backup between relays | `nak req … \| nak event dest` or `nak sync` |
| Encode / decode / new keys | `nak decode`, `nak encode`, `nak key generate` |
| Sign and publish | `nak event` (omit relays to print unsigned-looking signed JSON) |
| Auth-required relay | `nak req --auth` / `nak event --auth` |
| Git over Nostr | `nak git clone nostr://…` |
| Flag edge cases | [references/command-guide.md](references/command-guide.md) |

Mental models and copy-paste commands:
[references/command-guide.md](references/command-guide.md).
