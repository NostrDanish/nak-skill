# nak-skill

Kimi/Claude-style agent skill for the [`nak` CLI](https://github.com/fiatjaf/nak) (Nostr Army Knife).

Covers the 6 core mental models of working with Nostr via nak:

1. **Query & Discovery** — fetch events by id/author/kind/tag, NIP-05 resolution, live streaming
2. **Broadcast & Migration** — publish, copy events between relays, paginated backups, relay sync
3. **Identity & Encoding** — npub/nsec/note/nevent/naddr/nprofile encode/decode, key generation
4. **Event Creation & Publishing** — notes, tags, deletion, replaceable events, bunker remote signing
5. **Development & Testing** — local relays, admin ops, git-over-Nostr, performance benchmarking
6. **Analytics & Monitoring** — counts, engagement chains, client analytics, content ranking

Plus command shapes and edge-cases: signing methods, `@file` content, multi-value tags, bare filters, POW, NIP-42 AUTH, timestamp overrides.

If `NOSTR_SECRET_KEY` is unset and you do not pass a key, nak signs as the public default key `01`. That key is not yours. NIP-86 admin is `nak admin <method> <relay>`, not a flag in front of the method name.

## Install

Upload `SKILL.md` as a `.skill` package to your agent's skill library, or clone this repo into your skills directory.

## Source

Extracted from the [nostr-skills](https://github.com/NostrDanish/nostr-skills-registry) collection.

## License

CC-BY-SA-4.0
