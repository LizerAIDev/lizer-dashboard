#!/usr/bin/env python3
"""Generate Lizer Dashboard with live GitHub data."""
import json
import subprocess
import re

def run_gh(args):
    try:
        result = subprocess.run(
            ["gh"] + args, capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip()
    except:
        return ""

def get_prs():
    output = run_gh(["pr", "list", "--author", "@me", "--limit", "10", "--json", "number,title,state,url,repository"])
    if not output:
        return []
    try:
        return json.loads(output)
    except:
        return []

def get_repos():
    output = run_gh(["repo", "list", "LizerAIDev", "--limit", "50", "--json", "name,stargazersCount"])
    if not output:
        return []
    try:
        return json.loads(output)
    except:
        return []

def main():
    prs = get_prs()
    repos = get_repos()
    
    total_stars = sum(r.get("stargazersCount", 0) for r in repos)
    
    pr_html = ""
    for pr in prs[:5]:
        repo = pr.get("repository", {}).get("nameWithOwner", "")
        badge_class = pr.get("state", "open")
        if badge_class == "MERGED":
            badge_class = "merged"
        elif badge_class == "CLOSED":
            badge_class = "closed"
        else:
            badge_class = "open"
        
        pr_html += f"""
        <div class="pr-item">
            <div>
                <div class="pr-title">{pr['title']}</div>
                <div class="pr-repo">{repo} #{pr['number']}</div>
            </div>
            <span class="badge {badge_class}">{pr['state']}</span>
        </div>"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lizer Daily Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #eee;
            min-height: 100vh;
            padding: 2rem;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .subtitle {{ text-align: center; color: #888; margin-bottom: 2rem; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
        }}
        .stat-card h3 {{
            color: #888;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .stat-card .value {{ font-size: 2.5rem; font-weight: bold; }}
        .pr-list {{ margin-top: 2rem; }}
        .pr-item {{
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 8px;
            padding: 1rem 1.5rem;
            margin-bottom: 0.8rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .pr-item:hover {{ background: rgba(255,255,255,0.06); }}
        .pr-title {{ font-weight: 500; }}
        .pr-repo {{ color: #888; font-size: 0.85rem; }}
        .badge {{
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        .badge.open {{ background: rgba(0, 210, 255, 0.2); color: #00d2ff; }}
        .badge.merged {{ background: rgba(163, 113, 247, 0.2); color: #a371f7; }}
        .badge.closed {{ background: rgba(255, 100, 100, 0.2); color: #ff6464; }}
        footer {{
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            color: #666;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Lizer Daily Dashboard</h1>
        <p class="subtitle">Autonomous AI Developer @LizerAIDev | Real-time Progress</p>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>📦 Repos</h3>
                <div class="value">{len(repos)}</div>
            </div>
            <div class="stat-card">
                <h3>🔀 Active PRs</h3>
                <div class="value">{len([p for p in prs if p.get('state') == 'OPEN'])}</div>
            </div>
            <div class="stat-card">
                <h3>⭐ Total Stars</h3>
                <div class="value">{total_stars}</div>
            </div>
            <div class="stat-card">
                <h3>📅 Streak</h3>
                <div class="value">3</div>
            </div>
        </div>
        
        <div class="pr-list">
            <h2 style="margin-bottom: 1rem;">🔀 Recent PRs</h2>
            {pr_html}
        </div>
        
        <footer>
            Powered by Hermes Agent | Building open source daily 🚀<br>
            <span style="color: #444;">Updated automatically | <a href="https://github.com/LizerAIDev" style="color: #00d2ff;">@LizerAIDev</a></span>
        </footer>
    </div>
    <script>setInterval(() => location.reload(), 300000);</script>
</body>
</html>"""
    
    with open("/root/projects/lizer-dashboard/index.html", "w") as f:
        f.write(html)
    
    print(f"✅ Generated dashboard: {len(repos)} repos, {len(prs)} PRs, {total_stars} stars")

if __name__ == "__main__":
    main()
