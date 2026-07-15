#!/usr/bin/env python3
"""
GitHub profile README auto-updater.
Pulls writing articles from feed.xml and recent GitHub repo updates.
Also injects GitHub stats badges into the dynamic section.
"""
import json, os, re, textwrap, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

README_PATH        = os.environ.get("README_PATH", "README.md")
START_MARKER       = "<!-- dynamic:activity:start -->"
END_MARKER         = "<!-- dynamic:activity:end -->"
MAX_ITEMS          = int(os.environ.get("MAX_ITEMS", "5"))
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")
BLOG_FEED_URL      = os.environ.get("BLOG_FEED_URL", "https://akkireddy-challa.github.io/feed.xml").strip()
GITHUB_USERNAME    = (GITHUB_REPOSITORY.split("/")[0] if GITHUB_REPOSITORY else "akkireddy-challa")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "github-profile-readme-bot/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def clean(text):
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()

def parse_date(value):
    if not value:
        return None
    for v in [value.replace("Z", "+00:00"), value]:
        try:
            return datetime.fromisoformat(v)
        except Exception:
            pass
    try:
        return parsedate_to_datetime(value)
    except Exception:
        return None

def fmt(dt):
    if not dt:
        return "date unavailable"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d")

def parse_rss(url):
    try:
        root = ET.fromstring(fetch(url))
    except Exception:
        return []
    items = []
    ch = root.find("channel") or root
    for item in ch.findall("item"):
        items.append({
            "title": clean(item.findtext("title", "")),
            "link": clean(item.findtext("link", "")),
            "published": parse_date(item.findtext("pubDate", "")),
            "summary": clean(item.findtext("description", "")),
        })
    items = [x for x in items if x["title"] and x["link"]]
    items.sort(key=lambda x: x.get("published") or datetime(1970,1,1,tzinfo=timezone.utc), reverse=True)
    return items[:MAX_ITEMS]

def github_repo_updates(limit=5):
    if not GITHUB_USERNAME:
        return []
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    req = urllib.request.Request(
        f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page={limit*3}",
        headers={"User-Agent": "github-profile-readme-bot/1.0"},
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            repos = json.loads(r.read().decode())
    except Exception:
        return []
    out = []
    for repo in repos:
        if repo.get("fork") or repo["name"] == GITHUB_USERNAME:
            continue
        out.append({
            "name": repo["name"],
            "url": repo["html_url"],
            "description": clean(repo.get("description") or "No description yet."),
            "stars": repo.get("stargazers_count", 0),
            "updated_at": parse_date(repo.get("updated_at","")),
        })
        if len(out) >= limit:
            break
    return out

def stats_badges():
    u = GITHUB_USERNAME
    return (
        f"[![GitHub Stats](https://github-readme-stats.vercel.app/api?username={u}&show_icons=true&theme=dark&hide_border=true&count_private=true)](https://github.com/{u})\n"
        f"[![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={u}&layout=compact&theme=dark&hide_border=true)](https://github.com/{u})\n"
        f"[![GitHub Streak](https://streak-stats.demolab.com?user={u}&theme=dark&hide_border=true)](https://github.com/{u})\n"
        f"\n"
        f"![Profile views](https://komarev.com/ghpvc/?username={u}&color=0e75b6&style=flat)"
    )

def build_block():
    articles = parse_rss(BLOG_FEED_URL)
    repos    = github_repo_updates(MAX_ITEMS)
    lines = [
        "## \ud83d\udce1 Current output", "",
        "_Updated automatically every day via GitHub Actions._", "",
        "### \u270d\ufe0f Latest writing",
    ]
    if articles:
        for a in articles:
            s = (" \u2014 " + textwrap.shorten(a["summary"], 100, placeholder="\u2026")) if a.get("summary") else ""
            lines.append(f"- [{a['title']}]({a['link']}) ({fmt(a.get('published'))}){s}")
    else:
        lines.append("- No articles yet.")
    lines += ["", "### \ud83d\udee0 Recent project activity"]
    for r in repos:
        stars = f" \u2b50 {r['stars']}" if r["stars"] else ""
        lines.append(f"- [{r['name']}]({r['url']}){stars} \u2014 {r['description']} _(updated {fmt(r.get('updated_at'))})_")
    lines += ["", "### \ud83d\udcca GitHub stats", ""]
    lines.append(stats_badges())
    lines += ["", f"_Last refreshed: {fmt(datetime.now(timezone.utc))} UTC_"]
    return "\n".join(lines)

def run():
    with open(README_PATH, encoding="utf-8") as f:
        original = f.read()
    replacement = START_MARKER + "\n" + build_block() + "\n" + END_MARKER
    updated = re.sub(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        replacement, original, flags=re.S
    )
    if updated == original:
        updated = original.rstrip() + "\n\n" + replacement + "\n"
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
    print("README updated.")

if __name__ == "__main__":
    run()
