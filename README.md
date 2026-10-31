# nak-skill

Agent skill for the [`nak` CLI](https://github.com/fiatjaf/nak) (Nostr Army Knife).

`SKILL.md` is the install + safety + routing layer. Copy-paste commands and
edge cases live in `references/command-guide.md`.

Use with [nostr-skill](https://github.com/NostrDanish/nostr-skill) for protocol
rules and stdlib sign/verify, and [nostr-nips](https://github.com/NostrDanish/nostr-nips-skill)
for live spec text.

## Install

Copy or symlink into the agent's skills directory. The skill does not vendor
`nak`; the agent installs the CLI when needed (`nak --version` to confirm).

## License

CC-BY-SA-4.0
