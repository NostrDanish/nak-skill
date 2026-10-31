# nak command shapes

Checked against nak's own README and `req` flags (nak 0.21.x). Re-check with `nak <command> --help` if a flag is rejected.

## Keys

```bash
export NOSTR_SECRET_KEY   # hex, nsec, or ncryptsec. nak picks this up.
nak event -c "hello"       # no --sec
```

`--prompt-sec` prompts. A bunker URI may be passed to `--sec` because it is not the nsec itself. A raw nsec on `--sec` leaks via the process list.

## Content and tags

```bash
nak event -c @content.txt
nak event -t t=bitcoin -t t=nostr
nak event -t 'e=<id>;wss://relay.example;root'
# semicolon splits one tag into extra values: ["e", "<id>", "wss://relay.example", "root"]
```

The flag is `-t` or `--tag`.

## Filters

```bash
nak req -k 1 -l 5 --bare          # prints the filter JSON only
echo '{"kinds":[1]}' | nak req -l 5 -k 3 --bare
nak req -l 0 --stream wss://relay.example.com
```

Stdin wins over flags when both set the same field. An event piped into `nak event` keeps the stdin content even if `-c` is also set.

## Relays

```bash
nak req localhost:8000
nak req ws://127.0.0.1:7777
nak req relay.example.com          # bare host is treated as wss://
```

## Encode from JSON

```bash
echo '{"pubkey":"<hex>","relays":["wss://relay.example.com"]}' | nak encode
```

## Time and proof of work

```bash
nak event --ts 1700000000 -c "backdated"
nak event --pow 20 -c "mined event"
```

## Auth

```bash
nak req --auth -k 1 wss://relay.example.com
nak event --auth -c "test" wss://relay.example.com
```
