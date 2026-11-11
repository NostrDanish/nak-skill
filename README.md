# nak-skill

Portable Agent Skill for the [NAK CLI](https://github.com/fiatjaf/nak) (Nostr Army Knife).

## Scope

The skill focuses on read-only Nostr queries, public identifier encoding/decoding, unsigned event preparation, relay diagnostics and carefully approved publication/migration workflows.

It deliberately does not teach agents to generate, decode or handle raw private keys. NAK may fall back to a machine default key when signing is requested without a configured signer; the skill therefore requires `--no-sign` for event drafts and only publishes events already signed by a trusted signer.

## Coverage

1. **Query & discovery** — fetch by event/author/kind/tag, NIP-05 resolution, live streams.
2. **Broadcast & migration** — plan backups, inspect relay data, prepare controlled migrations.
3. **Public identity & encoding** — npub/note/nevent/naddr/nprofile; no nsec decoding or key generation.
4. **Event preparation & publishing** — unsigned event drafts, inspect-before-sign, publish pre-signed events after approval.
5. **Development & testing** — local relay inspection, diagnostics, Git-over-Nostr queries and performance checks.
6. **Analytics & monitoring** — counts, engagement queries, relay comparisons and search diagnostics.

## Install

The command reference is based on NAK v0.22.3. Install it with Go from the pinned tag:

~~~bash
go install github.com/fiatjaf/nak@v0.22.3
~~~

Clone this skill into a folder named `nak` (the folder name must match the skill frontmatter):

~~~bash
git clone https://github.com/NostrDanish/nak-skill <skills-root>/nak
~~~

## Security

- Do not use `--sec`, `--prompt-sec`, environment variables or shell substitution in agent-run commands.
- Never let an agent use NAK's default machine key.
- Prepare unsigned events with `--no-sign --author <pubkey>`; pass events to a trusted signer.
- Publish only a pre-signed event after explicit approval of exact relay targets.
- Never ask an agent to generate or display real account secrets.

## Verification

The repository includes upstream Agent Skills format CI. CLI examples should be smoke-tested against the pinned release before changing the version baseline.

## Source and license

Extracted from the [nostr-skills](https://github.com/NostrDanish/nostr-skills-registry) collection. License: CC-BY-SA-4.0.
