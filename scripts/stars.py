"""Write the profile stat cards (stars.svg, contributions.svg, npm.svg), styled like the Top Committer badge."""
import datetime, json, os, subprocess, sys, urllib.parse, urllib.request

USER = "alichherawalla"
ORGS = ["off-grid-ai", "wednesday-solutions"]
NPM = ["react-screentype-hook", "react-floki", "jsonapi-redux-data", "@ogai/llama.rn"]
OUT = os.path.join(os.path.dirname(__file__), "..")
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def stars():
    paths = [f"orgs/{o}/repos?per_page=100&type=public" for o in ORGS] + [f"users/{USER}/repos?per_page=100&type=owner"]
    return sum(int(x) for p in paths for x in gh("api", "--paginate", p, "--jq", ".[] | .stargazers_count").split())


def contributions():
    total = 0
    for y in range(2013, datetime.date.today().year + 1):
        q = f'{{user(login:"{USER}"){{contributionsCollection(from:"{y}-01-01T00:00:00Z",to:"{y}-12-31T23:59:59Z"){{contributionCalendar{{totalContributions}}}}}}}}'
        total += int(gh("api", "graphql", "-f", f"query={q}", "--jq", ".data.user.contributionsCollection.contributionCalendar.totalContributions"))
    return total


def npm_downloads():
    total, end = 0, datetime.date.today()
    for pkg in NPM:
        start = datetime.date(2015, 1, 10)
        while start < end:
            stop = min(start + datetime.timedelta(days=540), end)
            url = f"https://api.npmjs.org/downloads/point/{start}:{stop}/{urllib.parse.quote(pkg, safe='@')}"
            try:
                total += json.load(urllib.request.urlopen(url, timeout=30)).get("downloads", 0)
            except Exception:
                pass
            start = stop + datetime.timedelta(days=1)
    return total


def short(n):
    if n < 1000:
        return str(n)
    return f"{n / 1000:.1f}k" if n < 100_000 else f"{round(n / 1000)}k"


STAR = "M{x} {y} l2.9 7.1 7.6 .6 -5.8 4.9 1.8 7.4 -6.5 -4 -6.5 4 1.8 -7.4 -5.8 -4.9 7.6 -.6 Z"
ICONS = {
    "star": f'<path d="{STAR.format(x=34, y=21.5)}" fill="#c5cbd3"/>',
    "commit": '<circle cx="34" cy="32" r="5.5" stroke="#c5cbd3" stroke-width="2.4"/><path d="M21 32h7.5M39.5 32H47" stroke="#c5cbd3" stroke-width="2.4" stroke-linecap="round"/>',
    "package": '<path d="M34 22.5 43 27v10l-9 4.5L25 37V27Z" stroke="#c5cbd3" stroke-width="2" stroke-linejoin="round"/><path d="M25 27l9 4.5 9-4.5M34 31.5v10" stroke="#c5cbd3" stroke-width="2" stroke-linejoin="round"/>',
}


def card(label, value, icon):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 259 64" width="259" height="64" fill="none">
  <defs>
    <linearGradient id="c" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#2e3136"/><stop offset="45%" stop-color="#1a1c20"/><stop offset="100%" stop-color="#0d0e10"/></linearGradient>
    <linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#fff" stop-opacity="0.07"/><stop offset="100%" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="r" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#2fa35f"/><stop offset="100%" stop-color="#1f7a44"/></linearGradient>
  </defs>
  <rect x="1" y="1" width="257" height="62" rx="8" fill="url(#c)" stroke="#565c66"/>
  <rect x="1" y="1" width="257" height="32" rx="8" fill="url(#s)"/>
  <rect x="5" y="5" width="249" height="54" rx="4" stroke="#7f8792" stroke-width="0.6"/>
  <circle cx="34" cy="32" r="17" stroke="#9aa1ab" stroke-width="0.8"/>
  {ICONS[icon]}
  <g font-family="{FONT}">
    <text x="66" y="25" font-size="8.5" letter-spacing="1.2" fill="#9aa1ab" font-weight="600">{label}</text>
    <text x="66" y="45" font-size="16" fill="#f0f2f5" font-weight="500">{value}</text>
  </g>
</svg>
'''


if __name__ == "__main__":
    cards = {
        "stars.svg": ("LIFETIME STARS", stars, "star"),
        "contributions.svg": ("LIFETIME CONTRIBUTIONS", contributions, "commit"),
        "npm.svg": ("NPM DOWNLOADS", npm_downloads, "package"),
    }
    only = sys.argv[1:]
    for name, (label, fn, icon) in cards.items():
        if only and name not in only:
            continue
        n = fn()
        open(os.path.join(OUT, name), "w").write(card(label, short(n), icon))
        print(name, n, short(n))
