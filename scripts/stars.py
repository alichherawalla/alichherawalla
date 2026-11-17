"""Write stars.svg: lifetime GitHub stars across Off Grid AI, Wednesday Solutions and alichherawalla."""
import json, os, subprocess, sys

ORGS = ["off-grid-ai", "wednesday-solutions"]

def total():
    n = 0
    for path in [f"orgs/{o}/repos?per_page=100&type=public" for o in ORGS] + ["users/alichherawalla/repos?per_page=100&type=owner"]:
        out = subprocess.run(["gh", "api", "--paginate", path,
                              "--jq", ".[] | .stargazers_count"],
                             check=True, capture_output=True, text=True).stdout
        n += sum(int(x) for x in out.split())
    return n

def short(n):
    if n < 1000: return str(n)
    return f"{n/1000:.1f}k"

def svg(value):
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
  <path d="M34 21.5 L36.9 28.6 L44.5 29.2 L38.7 34.1 L40.5 41.5 L34 37.5 L27.5 41.5 L29.3 34.1 L23.5 29.2 L31.1 28.6 Z" fill="#c5cbd3"/>
  <g font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif">
    <text x="66" y="25" font-size="8.5" letter-spacing="1.2" fill="#9aa1ab" font-weight="600">LIFETIME STARS</text>
    <text x="66" y="45" font-size="16" fill="#f0f2f5" font-weight="500">{value}</text>
  </g>
  <path d="M213 1 H244 V44 L228.5 37 L213 44 Z" fill="url(#r)"/>
  <path d="M228.5 12.5 L230.6 17.6 L236 18 L231.9 21.5 L233.2 26.8 L228.5 23.9 L223.8 26.8 L225.1 21.5 L221 18 L226.4 17.6 Z" fill="#fff"/>
</svg>
'''

n = int(sys.argv[1]) if len(sys.argv) > 1 else total()
open(os.path.join(os.path.dirname(__file__), "..", "stars.svg"), "w").write(svg(short(n)))
print(n, short(n))
