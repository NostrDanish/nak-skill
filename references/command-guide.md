# nak command guide

Six mental models. Run `nak --help` / `nak <cmd> --help` if a flag looks stale.

## 1. Query & Discovery

```bash
nak fetch nevent1...                    # uses embedded relay hints
nak fetch alex@gleasonator.dev          # NIP-05
nak fetch naddr1...
nak fetch -r relay.primal.net naddr1... # override relays
nak req -i <event_id> <relay>
nak req -k 1 -a <pubkey> <relay>
nak req --tag t=bitcoin <relay>
nak req --search "sort:hot" <relay>     # relay-dependent
nak req --stream <relay>
```

`nak fetch` uses hints inside the identifier. `nak req` needs explicit relays.

## 2. Broadcast & Migration

```bash
cat event.json | nak event <relay>
nak req -i <id> relay1 | nak event relay2
nak req -k 1 source_relay | nak event dest_relay
nak req --paginate source_relay | nak event backup_relay
cat event.json | nak event relay1 relay2 relay3
nak sync source_relay dest_relay
```

## 3. Identity & Encoding

```bash
nak decode npub1...
nak decode user@domain.com
nak encode npub <hex_pubkey>
nak key generate
nak key generate | nak key public | nak encode npub
nak encode nevent <event_id> --relay <relay>
nak encode naddr -k 30023 -a <author> -d <identifier> -r <relay>
nak encode nprofile <pubkey> -r relay1 -r relay2
```

## 4. Event Creation & Publishing

```bash
nak event --prompt-sec <relay>
nak event -k 1 -c "Hello Nostr" <relay>
nak event -k 1 -t t=bitcoin -t t=nostr <relay>
nak event -k 5 -e <event_id> --prompt-sec <relay>
nak event --connect "bunker://..." <relay>
# No relays = print signed JSON, do not publish
nak event -c "test" --sec "$NOSTR_SECRET_KEY"
```

Prefer `export NOSTR_SECRET_KEY=…` over `--sec` on the command line.

## 5. Development & Testing

```bash
nak req localhost:8000
nak req -i <id> <relay> | jq .
nak admin --prompt-sec banevent --id <id> <relay>
nak git clone nostr://...
nak req -k 30617 <git-relay>
time nak req -k 0 -a <pubkey> <relay>
```

## 6. Analytics & Monitoring

```bash
nak req -k 1 <relay> | wc -l
nak count -k 7 -e <event_id> <relay>
nak req -l 0 --stream relay1 relay2
nak req --tag client=<app> <relay>
```

## Edge cases

**Content from file:** `-c @content.txt`

**Multi-value tag:** `-t custom="value1;value2;value3"` → `["custom","value1","value2","value3"]`

**Bare filter:** `nak req -k 1 -l 5 --bare` prints the filter JSON only.

**Stdin filter + flags:** `echo '{"kinds":[1]}' | nak req -l 5 -k 3 --bare`

**Relay schemes:** `localhost:8000`, `ws://127.0.0.1:7777`, `relay.example.com` (assumes `wss://`).

**Encode from JSON stdin:** `echo '{"pubkey":"<hex>","relays":["wss://…"]}' | nak encode`

**Verify:** `nak event -c "test" | nak verify`

**First `d` tag wins** on addressable events.

**Timestamps:** `nak event --ts 1700000000 -c "backdated"`

**Kind 0 content is JSON:** `nak event -k 0 -c '{"name":"Alice"}'`

**POW:** `nak event --pow 20 -c "mined"`

**NIP-42:** `nak req --auth -k 1 wss://…` and `nak event --auth …`

**Stdin overrides flags** for `nak event` JSON input.
