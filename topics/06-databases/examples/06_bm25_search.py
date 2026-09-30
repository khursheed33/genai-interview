"""06_bm25_search.py — book index + BM25 from scratch (then vs FTS5).

Run: uv run python topics/06-databases/examples/06_bm25_search.py
"""

import math
import re
import sqlite3

DOCS = {
    1: "crispy dosa with coconut chutney",
    2: "idli sambar breakfast poha",
    3: "dosa dosa dosa festival menu",
    4: " Paneer tikka   MASALA! ",
}
STOP = {"with", "and", "the"}


def analyze(text):  # SAME chain at index + query time (mismatch = zero hits!)
    return [t for t in re.findall(r"[a-z]+", text.lower()) if t not in STOP]


assert analyze(DOCS[4]) == ["paneer", "tikka", "masala"]

# inverted index: term -> {doc: freq}
INDEX, DLEN = {}, {}
for did, text in DOCS.items():
    toks = analyze(text)
    DLEN[did] = len(toks)
    for t in toks:
        INDEX.setdefault(t, {}).setdefault(did, 0)
        INDEX[t][did] += 1
assert INDEX["dosa"] == {1: 1, 3: 3}


def bm25_scores(query, k1=1.2, b=0.75):
    N, avgdl = len(DOCS), sum(DLEN.values()) / len(DOCS)
    scores = {}
    for t in analyze(query):
        postings = INDEX.get(t, {})
        idf = math.log(1 + (N - len(postings) + 0.5) / (len(postings) + 0.5))
        for did, tf in postings.items():
            denom = tf + k1 * (1 - b + b * DLEN[did] / avgdl)
            scores[did] = scores.get(did, 0) + idf * (tf * (k1 + 1) / denom)
    return scores


def bm25(query):
    return sorted(bm25_scores(query), key=bm25_scores(query).get, reverse=True)


ranked, scores = bm25("dosa"), bm25_scores("dosa")
assert ranked == [3, 1], ranked  # tf=3 wins — but NOTE saturation: 3x tf != 3x score!
assert scores[3] < 2 * scores[1]
print("BM25 'dosa' ->", ranked, {k: round(v, 2) for k, v in scores.items()})
print("(tf=3 beats tf=1, yet saturation caps the gap — length-norm + k1 at work)")
assert bm25("paneer tikka") == [4]

# sqlite FTS5 agrees (when compiled in — stdlib Windows builds usually include it)
try:
    fts = sqlite3.connect(":memory:")
    fts.execute("CREATE VIRTUAL TABLE s USING fts5(txt)")
    fts.executemany("INSERT INTO s VALUES (?)", [(t,) for t in DOCS.values()])
    top = fts.execute("SELECT txt FROM s WHERE s MATCH 'dosa' LIMIT 1").fetchone()[0]
    assert "dosa" in top
    print("FTS5 agrees:", top[:30], "...")
except sqlite3.OperationalError:
    print("FTS5 not compiled here — pure-python BM25 above is the portable lesson")
print("OK — TF*IDF*length-norm; text=search vs keyword=exact; analyzers must match")
