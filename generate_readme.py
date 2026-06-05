#!/usr/bin/env python3
"""
GitHub profile README auto-updater.
Pulls blog posts, vlogs, and recent GitHub repo updates
into the dynamic section of README.md.

Env vars (set as GitHub Actions repo variables):
  BLOG_FEED_URL        RSS or Atom feed URL for blog posts
  VLOG_FEED_URL        RSS or Atom feed URL for vlogs (YouTube channel feed works)
  MAX_ITEMS            items per section (default 5)
  README_PATH          path to README (default README.md)
  GITHUB_REPOSITORY    set automatically by GitHub Actions
"""
import json, os, re, textwrap, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

README_PATH       = os.environ.get("README_PATH", "README.md")
START_MARKER      = "<!-- dynamic:activity:start -->"
END_MARKER        = "<!-- dynamic:activity:end -->"
MAX_ITEMS         = int(os.environ.get("MAX_ITEMS", "5"))
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")
BLOG_FEED_URL     = os.environ.get("BLOG_FEED_URL", "").strip()
VLOG_FEED_URL     = os.environ.get("VLOG_FEED_URL", "").strip()


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


def parse_feed(url):
    root = ET.fromstring(fetch(url))
    items = []
    ns = "http://www.w3.org/2005/Atom"
    tag = root.tag.lower()
    if "rss" in tag:
        ch = root.find("channel") or root
        for item in ch.findall("item"):
            items.append({
                "title":     clean(item.findtext("title", "")),
                "link":      clean(item.findtext("link", "")),
                "published": parse_date(item.findtext("pubDate", "")),
                "summary":   clean(item.findtext("description", "")),
            })
    else:
        for entry in root.findall(f"{{{ns}}}entry") or root.findall("entry"):
            link = ""
            for node in entry.findall(f"{{{ns}}}link"):
                href, rel = node.attrib.get("href",""), node.attrib.get("rel","alternate")
                if href and rel == "alternate":
                    link = href; break
                if href and not link:
                    link = href
            items.append({
                "title":     clean(entry.findtext(f"{{{ns}}}title","")),
                "link":      link,
                "published": parse_date(entry.findtext(f"{{{ns}}}updated","") or entry.findtext(f"{{{ns}}}published","")),
                "summary":   clean(entry.findtext(f"{{{ns}}}summary","") or entry.findtext(f"{{{ns}}}content","")),
            })
    items = [x for x in items if x["title"] and x["link"]]
    items.sort(key=lambda x: x.get("published") or datetime(1970,1,1,tzinfo=timezone.utc), reverse=True)
    return items[:MAX_ITEMS]


def github_repo_updates(limit=5):
    if not GITHUB_REPOSITORY:
        return []
    owner = GITHUB_REPOSITORY.split("/")[0]
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    req   = urllib.request.Request(
        f"https://api.github.com/users/{owner}/repos?sort=updated&per_page={limit*3}",
        headers={"User-Agent": "github-profile-readme-bot/1.0"},
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        repos = json.loads(r.read().decode())
    out = []
    for repo in repos:
        if repo.get("fork"):
            continue
        out.append({
            "name":        repo["name"],
            "url":         repo["html_url"],
            "description": clean(repo.get("description") or "No description yet."),
            "updated_at":  parse_date(repo.get("updated_at","")),
        })
        if len(out) >= limit:
            break
    return out


def fmt(dt):
    if not dt:
        return "date unavailable"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d")


def feed_section(heading, items, empty):
    lines = [f"### {heading}"]
    if not items:
        lines.append(f"- {empty}")
        return lines
    for x in items:
        s = (" — " + textwrap.shorten(x["summary"], 100, placeholder="…")) if x.get("summary") else ""
        lines.append(f"- [{x['title']}]({x['link']}) ({fmt(x.get('published'))}){s}")
    return lines


def project_section(items):
    lines = ["### Recent project updates"]
    if not items:
        lines.append("- No recent project updates found.")
        return lines
    for x in items:
        lines.append(f"- [{x['name']}]({x['url']}) — {x['description']} (updated {fmt(x.get('updated_at'))})")
    return lines


def build_block():
    blog     = parse_feed(BLOG_FEED_URL)     if BLOG_FEED_URL  else []
    vlog     = parse_feed(VLOG_FEED_URL)     if VLOG_FEED_URL  else []
    projects = github_repo_updates(MAX_ITEMS)
    lines = [
        "## 📡 Current output", "",
        "This section refreshes automatically every day via GitHub Actions.", "",
        *feed_section("Latest blog posts", blog,
            "No blog feed configured yet — add `BLOG_FEED_URL` in Actions variables to enable."), "",
        *feed_section("Latest vlogs", vlog,
            "No vlog feed configured yet — add `VLOG_FEED_URL` in Actions variables to enable."), "",
        *project_section(projects), "",
        f"_Last refreshed: {fmt(datetime.now(timezone.utc))} UTC_",
    ]
    return "\n".join(lines)


def run():
    with open(README_PATH, encoding="utf-8") as f:
        original = f.read()
    replacement = START_MARKER + "\n" + build_block() + "\n" + END_MARKER
    updated = re.sub(re.escape(START_MARKER)+r".*?"+re.escape(END_MARKER), replacement, original, flags=re.S)
    if updated == original:
        updated = original.rstrip() + "\n\n" + replacement + "\n"
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
    print("README updated.")


if __name__ == "__main__":
    run()
