"""06_fanout_cost.py — push normals, pull celebrities (the 10M-follower math!).

Run: uv run python topics/09-system-design/examples/06_fanout_cost.py
"""


def push_cost(followers):
    return followers  # 1 write per follower timeline!


def pull_cost(followed_celebrities):
    return followed_celebrities  # 1 read per followed celeb on refresh!


normal, celeb = 200, 10_000_000
print(f"post by normal ({normal} followers): push {push_cost(normal)} writes")
print(f"post by celeb ({celeb} followers): push {push_cost(celeb):,} writes (MELT!)")
assert push_cost(celeb) == 10_000_000

# hybrid: push if followers < threshold, else pull (read-fan-out!)
THRESH = 10_000


def strategy(followers):
    return "push" if followers < THRESH else "pull"


assert strategy(normal) == "push" and strategy(celeb) == "pull"
refresh_reads = 50  # user follows 50 celebs: 50 reads per refresh (cached 30s!)
print(f"celeb reader pays {pull_cost(refresh_reads)} cached reads (cheap vs 10M writes!)")
print("OK — push small (fast reads!), pull stars (surviving writes!), threshold ~10k!")
