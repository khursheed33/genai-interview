# 04 — Classic Designs II: Talk, Scroll & Watch (chat/feed/streaming/storage/crawler)

## 1. Chat (rooms that feel instant!)

```
client -WS-> gateway (sticky room!) -> router -> [room: pub/sub fan-out!] + [history: DB!]
presence (heartbeat + TTL!) | typing (ephemeral!) | receipts (per-msg ACK!)
```

- 1:1 = queue-ish; group = fan-out per message (100 members = 100 writes OR 1 write + 100 reads? **write-fan-out** for small groups (fast reads!), **read-fan-out** for celebrities (1 write, followers pull — the 10M-follower problem!)). History: per-room ordered log (partition = room!). Media → S3 + thumb workers. E2E: Signal protocol (server sees ciphertext!). Demo fan-out math: `../examples/06_fanout_cost.py`.

## 2. News feed (scroll that never ends!)

Same fan-out choice! Regulars: push to followers' timelines (Redis lists, TRIMM!). Celebrities: pull on read (followers fetch author's recent). Rank: chronological → score (recency×affinity×freshness, precomputed by workers!). Pagination: cursor on `(score, id)` (no offset skips!).

## 3. Video/files (bytes that never buffer!)

Upload → **multipart direct-to-S3** (presigned!) → transcode workers (1080/720/480 ladder!) → **HLS/DASH chunks** on CDN (10s segments, adaptive bitrate!) → signed URLs (expiry!). Metadata DB tiny (pointers!). Live: RTMP in → chunker → 5s-delay edge. Storage math: 1M videos × 500MB × ladder 3 = petabytes (S3 + lifecycle to Glacier!).

## 4. Crawler + autocomplete + search box (the web eaters!)

- Crawler: **frontier (priority queue!)** → fetcher (politeness: 1 req/s/host + robots!) → dedupe (SimHash/bloom — topic 07!) → parser → index. Scale: 1B pages/mo = 400 RPS fetch (DNS cache + keep-alive!). Dark side: traps (calendar infinite!), duplicates (canonical!), freshness (PageRank-ish revisit!).
- Autocomplete: **trie** (prefix tree, top-k per node, updated hourly!) + personal layer. Search box: ES/OpenSearch (BM25 — topic 06!) + click-signal rerank.

One-liner: **"Chat/feed = push normals, pull celebrities; video = S3 ladder + HLS CDN; crawl polite + dedupe, complete via trie."**
Ride/payment/scheduler/gateway variants reuse the same blocks (state machine + idempotency + DLQ + audit — say the pattern!).
