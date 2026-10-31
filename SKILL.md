---
name: nak
description: "Use the nak CLI (Nostr Army Knife) to query relays, fetch by nevent/naddr/nip05, encode or decode NIP-19, and sign or publish events. Triggers on nak, nostr army knife, and CLI req/fetch/encode of Nostr events. Not the live spec (nostr-nips skill) and not application code (nostr skill)."
license: CC-BY-SA-4.0
---

# nak

`nak` is fiatjaf's Nostr CLI: https://github.com/fiatjaf/nak

When a flag is unclear, run `nak <command> --help`. Do not invent subcommands.

## Install

Prefer a package manager or Go. Both build the same upstream binary:

```bash
go install github.com/fiatjaf/nak@latest
# or: brew install nak
```

Upstream also documents `curl -sSL https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh | sh`. That runs a remote script. Use it only when Go and Homebrew are unavailable, and read the script first.

## Secrets

nak reads `NOSTR_SECRET_KEY` (hex, nsec, or ncryptsec) from the environment. Use that, `--prompt-sec`, or a `bunker://` URI.

Do not pass a raw nsec to `--sec`. It shows up in the process list and in shell history. Do not print the key. Generating a key may print it once; stop there and move it to the environment.

## Task routing

| Task | Command |
|---|---|
| Event or profile from an nevent, naddr, nprofile, npub, or nip05 | `nak fetch <code>` (uses hints inside the code). Add `-r wss://relay` to add relays. |
| Filter you write yourself | `nak req` with an explicit relay. No relay prints the filter and does not connect. |
| Author's outbox relays | `nak req --outbox -a <hex-pubkey> ...` |
| One event by id | `nak req -i <hex-id> wss://relay` |
| Author / kind / tag | `nak req -a <hex> -k 1 -t t=bitcoin -l 20 wss://relay` |
| Keep the subscription open | `nak req -l 0 --stream wss://relay` |
| Page past a relay's limit | `nak req -k 1 --limit 5000 --paginate --paginate-interval 2s wss://relay` |
| Copy events | `nak req -i <id> wss://source \| nak event wss://dest` (dests are extra arguments) |
| Sync two relays | `nak sync wss://a wss://b` |
| Note, profile, or other event | `nak event -k 1 -c "hello" wss://relay`. No relay prints the event and does not publish. |
| Kind 0 | content is JSON: `nak event -k 0 -c '{"name":"Alice"}'` |
| Deletion request | `nak event -k 5 -e <event-id>` (relays may ignore it) |
| Verify | `nak verify` on event JSON from stdin |
| Keys | `nak key generate`, `nak key public`, `nak encode npub <hex>` |
| Decode any NIP-19 or nip05 | `nak decode npub1...` |
| nevent / naddr with hints | `nak encode nevent <id> -r wss://relay`, `nak encode naddr -k 30023 -a <author> -d <slug> -r wss://relay` |
| NIP-42 | `nak req --auth ...` and `nak event --auth ...` |
| NIP-49 | `nak key encrypt` / `nak key decrypt` |
| Gift wrap | `nak gift wrap` / `nak gift unwrap` (see `--help` for the current flags) |
| Blossom via nak | `nak blossom --server <host> upload <file>` — the blossom skill has the protocol rules |
| Git over Nostr | `nak git clone\|init\|fetch\|pull\|push\|sync` |
| Local relay | `nak serve` (`--negentropy`, `--grasp`, `--blossom` exist; check `--help`) |
| Relay admin (NIP-86) | `nak admin --help`. Do not guess method names. |

`sort:hot` and `popular:24h` are NIP-50 search strings some relays implement. nak just forwards `--search`. They are not nak features.

## Rules that match the protocol

- `nak fetch` follows hints. `nak req` does not, unless you pass `--outbox` or name the relays.
- Publish to the author's write relays and read from their read relays. One big relay is not the outbox model.
- The first `d` tag is the address identifier.
- Kind 5 is a deletion request, not a guarantee.
- Tag letters and kind ranges are specified by NIPs. This skill does not override the nostr-nips skill.

Edge cases (stdin versus flags, `@file` content, multi-value tags, `--bare`, `--pow`, `--ts`) are in [references/command-shapes.md](references/command-shapes.md).
