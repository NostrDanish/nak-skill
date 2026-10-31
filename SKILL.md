---
name: nak
description: "Use the nak CLI (Nostr Army Knife, verified against v0.21) to generate keys, encode or decode npub/nsec/note/nevent/naddr, fetch by nevent or NIP-05, query and count and sync relays, sign and publish events, gift-wrap, upload to Blossom, run a bunker, administer a relay, and use git-over-nostr. Triggers on nak, nostr CLI, nak req, nak event, nak fetch, encode npub. Not the NIP spec (nostr-nips) and not a library (nostr)."
license: CC-BY-SA-4.0
---

# nak

`nak` is the Nostr CLI. Flag names below were checked against **v0.21.2**. Before you invent a flag, run `nak <command> --help`. If that flag is not listed, it does not exist.

`nak --version` first. A much older binary will not match this skill.

## Install

Prefer a pinned install:

```bash
go install github.com/fiatjaf/nak@v0.21.2
```

Also fine: a release binary from https://github.com/fiatjaf/nak/releases, `brew install nak` on macOS. The upstream `curl | sh` installer tracks master; use it only when you mean to track master.

## Secrets

- A raw nsec or hex secret goes in the environment: `export NOSTR_SECRET_KEY=...` for that process only. nak reads it. Do not pass it as `--sec`. The process list and the shell history keep `--sec` arguments.
- `bunker://` URLs and `ncryptsec1` strings are also secrets. Put those in `NOSTR_SECRET_KEY` too. ncryptsec prompts for the password.
- Do not run `nak key default` in a chat or a log. It prints the machine's default secret.
- `nak key generate` prints a new secret. Store it in a mode-0600 file outside any repo. Do not commit it, and do not paste it back into the chat.
- Publishing with no relays prints the event and does not send it. That is the safe way to inspect a signed event.

## Which command

| Job | Command |
|---|---|
| Events from relays you name | `nak req` |
| One event or profile from hints inside a nevent, naddr, nprofile, or NIP-05 | `nak fetch` |
| How many | `nak count` (NIP-45; the relay must support it) |
| Build, sign, and optionally publish | `nak event` |
| Copy one event between relays | `nak req -i <id> <src> \| nak event <dst>...` |
| Negentropy sync | `nak sync <source> <dest>` |
| Decode / encode | `nak decode`, `nak encode` |
| Keys | `nak key generate`, `nak key public`, `nak key encrypt`, `nak key decrypt` |
| What is kind N | `nak kind <n>` |
| One-line NIP summary | `nak nip <id>` |
| Relay info doc | `nak relay <url>` |
| Someone's read/write relays | `nak relays <pubkey-or-nip05>` |
| Profile card | `nak profile <npub-or-nip05>` |
| Gift wrap (NIP-59) | `nak gift wrap` / `nak gift unwrap` |
| Blossom file | `nak blossom upload\|download\|list\|mirror\|check` |
| Remote signer | `nak event` with `NOSTR_SECRET_KEY=bunker://...` |
| Be a signer | `nak bunker` |
| Relay admin (NIP-86) | `nak admin <method> <relay>` |
| Git over Nostr (NIP-34) | `nak git` |
| Check a signature | `nak verify` (event on stdin or as the argument) |

Outbox publish and read: `nak event --outbox` publishes to the author's write relays and to the read relays of `p`-tagged people. `nak req --outbox` reads from the authors' write relays. Both need network and are off unless you pass the flag.

## Recipes that are easy to get wrong

Query:

```bash
nak req -k 1 -a <pubkey-hex> -l 20 wss://relay.example.com
nak req --stream -k 1 wss://relay.example.com          # stays open after EOSE
nak req -k 1 --limit 50000 --paginate wss://nos.lol    # walks until, past the relay's page cap
nak fetch nevent1...                                   # uses hints inside the code
nak fetch -r wss://relay.example.com naddr1...         # extra relay, hints still apply
```

`-l 0` is the default and means no limit. `--search` is a NIP-50 string passed through; the relay defines what it means (`sort:hot` is not a nak feature). `--auth` answers a NIP-42 challenge and retries.

Build:

```bash
nak event -k 1 -c "hello" wss://relay.example.com
nak event -k 0 -c '{"name":"alice"}'                   # kind 0 content is JSON
nak event -k 1 -t t=bitcoin -t t=nostr                 # repeated single-letter tags
nak event -t custom="value1;value2;value3"            # one tag, many values, split on ';'
nak event -c @content.txt                              # leading @ reads a file
nak event -k 30023 -d my-slug                          # first -d is the addressable identifier
nak event --ts 1700000000 -c "backdated"
nak event --pow 16 -c "mined"
echo '{"content":"from stdin"}' | nak event -c "ignored"   # stdin wins over the flags it replaces
```

No `--prompt-sec`. No `--connect`. A bunker signs when the secret **is** the bunker URL in `NOSTR_SECRET_KEY`.

Identity:

```bash
nak key generate | nak key public | nak encode npub    # public half only; the secret was on the pipe, do not log it
nak decode npub1...
nak decode name@domain.com                             # NIP-05
nak encode nevent <event-id-hex> -r wss://relay.example.com
nak encode naddr -k 30023 -a <author-hex> -d <identifier> -r wss://relay.example.com
echo '{"pubkey":"<hex>","relays":["wss://relay.example.com"]}' | nak encode
```

Admin and git:

```bash
nak admin banevent wss://relay.example.com --id <event-id>
nak git clone 'nostr://...'
```

`nak admin` methods are subcommands (`allowpubkey`, `banpubkey`, `banevent`, ...). The relay URL is the argument, not a flag.

## Local relay URL shapes

`nak req localhost:8000`, `nak req ws://127.0.0.1:7777`, and `nak req relay.example.com` (no scheme means `wss://`). `nak serve` starts an in-memory relay for tests.
