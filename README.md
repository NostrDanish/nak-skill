# nak-skill

Agent skill for the [`nak`](https://github.com/fiatjaf/nak) CLI (Nostr Army Knife). Commands and flags were checked against nak **v0.21.2**. The skill tells the agent to run `nak <command> --help` before using a flag this file does not list.

Pairs with [nostr-skill](https://github.com/NostrDanish/nostr-skill) (libraries and scripts) and [nostr-nips-skill](https://github.com/NostrDanish/nostr-nips-skill) (the spec text).

## Install

Copy or symlink the directory that contains `SKILL.md` into the agent's skills path. Install the binary separately (`go install github.com/fiatjaf/nak@v0.21.2`, a release binary, or Homebrew).

## License

CC-BY-SA-4.0
