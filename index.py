#!/usr/bin/env python3
"""
BlackRoad OS Repository Index
Central catalog and discovery service for BlackRoad-OS organization repositories.

Copyright © 2024-2026 BlackRoad OS, Inc. All rights reserved.
"""

import os
import sys
import json
import argparse
import requests
from typing import List, Dict, Optional
from datetime import datetime
from collections import defaultdict


class RepositoryIndex:
    """Main repository indexing class for BlackRoad-OS."""
    
    def __init__(self, organization: str = "BlackRoad-OS"):
        self.organization = organization
        self.github_api = "https://api.github.com"
        self.cache_file = ".repo_cache.json"
        self.repositories = []
        
    def fetch_all_repositories(self) -> List[Dict]:
        """Fetch all repositories from the GitHub organization."""
        print(f"🔍 Fetching repositories from {self.organization}...")
        
        repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{self.github_api}/orgs/{self.organization}/repos"
            params = {
                "page": page,
                "per_page": per_page,
                "sort": "updated",
                "direction": "desc"
            }
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    break
                    
                repos.extend(data)
                print(f"  📦 Fetched {len(data)} repositories (page {page})")
                
                if len(data) < per_page:
                    break
                    
                page += 1
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Error fetching repositories: {e}")
                break
        
        self.repositories = repos
        print(f"✅ Total repositories found: {len(repos)}")
        return repos
    
    def categorize_repositories(self) -> Dict[str, List[Dict]]:
        """Categorize repositories based on topics, names, and descriptions."""
        categories = defaultdict(list)
        
        for repo in self.repositories:
            name = repo.get("name", "").lower()
            topics = [t.lower() for t in repo.get("topics", [])]
            description = (repo.get("description") or "").lower()
            
            # Categorization logic
            if any(x in topics or x in name for x in ["core", "infrastructure", "scheduler", "socket"]):
                categories["infrastructure"].append(repo)
            
            if any(x in topics or x in name for x in ["ai", "ml", "inference", "machine-learning"]):
                categories["ai"].append(repo)
            
            if any(x in topics or x in name for x in ["cicd", "jenkins", "devops", "quality"]):
                categories["devops"].append(repo)
            
            if any(x in topics or x in name or x in description for x in ["editor", "debug", "branch", "athena", "review"]):
                categories["development-tools"].append(repo)
            
            if any(x in topics or x in name for x in ["portal", "legal", "store", "status"]) or name.endswith("-io"):
                categories["web-portals"].append(repo)
            
            if any(x in topics or x in name for x in ["subtitle", "watermark", "content", "media"]):
                categories["media"].append(repo)
            
            if any(x in topics or x in name for x in ["translate", "i18n", "localization"]):
                categories["translation"].append(repo)
            
            if any(x in topics or x in name for x in ["crm", "seo", "knowledge", "business"]):
                categories["business"].append(repo)
            
            if any(x in topics or x in name for x in ["quantum", "robot", "atmospheric", "simulator"]):
                categories["specialized"].append(repo)
            
            if any(x in topics or x in name for x in ["synapse", "matrix", "chat", "messaging"]):
                categories["communication"].append(repo)
            
            if any(x in topics or x in name for x in ["blockchain", "chain", "bridge"]):
                categories["blockchain"].append(repo)
            
            if any(x in topics or x in name for x in ["pulse", "health", "monitor"]):
                categories["monitoring"].append(repo)
        
        return dict(categories)
    
    def generate_statistics(self) -> Dict:
        """Generate statistics about the repositories."""
        stats = {
            "total_repositories": len(self.repositories),
            "languages": defaultdict(int),
            "topics": defaultdict(int),
            "by_category": {},
            "updated_recently": 0,
            "total_stars": 0,
            "total_forks": 0,
            "archived": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        for repo in self.repositories:
            # Language stats
            lang = repo.get("language")
            if lang:
                stats["languages"][lang] += 1
            
            # Topic stats
            for topic in repo.get("topics", []):
                stats["topics"][topic] += 1
            
            # Overall stats
            stats["total_stars"] += repo.get("stargazers_count", 0)
            stats["total_forks"] += repo.get("forks_count", 0)
            
            if repo.get("archived", False):
                stats["archived"] += 1
            
            # Recently updated (within last 30 days)
            updated_at = repo.get("updated_at", "")
            if updated_at:
                try:
                    updated_date = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
                    days_ago = (datetime.now() - updated_date).days
                    if days_ago <= 30:
                        stats["updated_recently"] += 1
                except ValueError:
                    pass
        
        # Category statistics
        categories = self.categorize_repositories()
        for category, repos in categories.items():
            stats["by_category"][category] = len(repos)
        
        return stats
    
    def export_json(self, output_file: str = "repositories.json"):
        """Export repository data as JSON."""
        data = {
            "organization": self.organization,
            "total_count": len(self.repositories),
            "generated_at": datetime.now().isoformat(),
            "repositories": self.repositories,
            "categories": self.categorize_repositories(),
            "statistics": self.generate_statistics()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported to {output_file}")
    
    def export_markdown(self, output_file: str = "REPOSITORIES.md"):
        """Export repository data as Markdown."""
        categories = self.categorize_repositories()
        stats = self.generate_statistics()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# BlackRoad OS Repository Index\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
            
            # Statistics
            f.write("## Statistics\n\n")
            f.write(f"- **Total Repositories:** {stats['total_repositories']}\n")
            f.write(f"- **Total Stars:** {stats['total_stars']}\n")
            f.write(f"- **Total Forks:** {stats['total_forks']}\n")
            f.write(f"- **Updated Recently (30 days):** {stats['updated_recently']}\n")
            f.write(f"- **Archived:** {stats['archived']}\n\n")
            
            # Top languages
            f.write("### Top Languages\n\n")
            top_languages = sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True)[:10]
            for lang, count in top_languages:
                f.write(f"- **{lang}**: {count} repositories\n")
            f.write("\n")
            
            # Categories
            f.write("## Repositories by Category\n\n")
            for category, repos in sorted(categories.items()):
                f.write(f"### {category.replace('-', ' ').title()} ({len(repos)})\n\n")
                for repo in sorted(repos, key=lambda x: x['name']):
                    name = repo['name']
                    url = repo['html_url']
                    desc = repo.get('description', 'No description')
                    lang = repo.get('language', 'N/A')
                    stars = repo.get('stargazers_count', 0)
                    f.write(f"- **[{name}]({url})**")
                    if desc:
                        f.write(f" - {desc}")
                    f.write(f" `{lang}` ⭐ {stars}\n")
                f.write("\n")
            
            # Uncategorized
            categorized_names = set()
            for repos in categories.values():
                categorized_names.update(r['name'] for r in repos)
            
            uncategorized = [r for r in self.repositories if r['name'] not in categorized_names]
            if uncategorized:
                f.write(f"### Other Repositories ({len(uncategorized)})\n\n")
                for repo in sorted(uncategorized, key=lambda x: x['name']):
                    name = repo['name']
                    url = repo['html_url']
                    desc = repo.get('description', 'No description')
                    lang = repo.get('language', 'N/A')
                    f.write(f"- **[{name}]({url})** - {desc} `{lang}`\n")
        
        print(f"✅ Exported to {output_file}")
    
    def export_html(self, output_file: str = "catalog.html"):
        """Export repository data as HTML."""
        categories = self.categorize_repositories()
        stats = self.generate_statistics()
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BlackRoad OS Repository Catalog</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #e0e0e0;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            padding: 2rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
        }
        h1 {
            color: #FF1D6C;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: rgba(255, 29, 108, 0.1);
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #FF1D6C;
        }
        .stat-number { font-size: 2rem; font-weight: bold; color: #FF1D6C; }
        .stat-label { color: #999; }
        .category {
            background: rgba(0,0,0,0.3);
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 10px;
        }
        .category h2 {
            color: #FF1D6C;
            margin-bottom: 1rem;
            border-bottom: 2px solid #FF1D6C;
            padding-bottom: 0.5rem;
        }
        .repo-card {
            background: rgba(255,255,255,0.05);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
            border-left: 3px solid #FF1D6C;
        }
        .repo-card:hover {
            background: rgba(255,255,255,0.1);
            transform: translateX(5px);
            transition: all 0.3s;
        }
        .repo-name {
            color: #FF1D6C;
            font-weight: bold;
            text-decoration: none;
            font-size: 1.1rem;
        }
        .repo-name:hover { text-decoration: underline; }
        .repo-desc { color: #ccc; margin: 0.5rem 0; }
        .repo-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.9rem;
            color: #999;
        }
        .badge {
            background: rgba(255, 29, 108, 0.2);
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🖤 BlackRoad OS Repository Catalog</h1>
            <p>The Road to AI Sovereignty</p>
            <p style="color: #999;">Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + """</p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">""" + str(stats['total_repositories']) + """</div>
                <div class="stat-label">Total Repositories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">""" + str(stats['total_stars']) + """</div>
                <div class="stat-label">Total Stars</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">""" + str(stats['updated_recently']) + """</div>
                <div class="stat-label">Updated Recently</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">""" + str(len(stats['languages'])) + """</div>
                <div class="stat-label">Languages</div>
            </div>
        </div>
"""
        
        for category, repos in sorted(categories.items()):
            category_name = category.replace('-', ' ').title()
            html += f"""
        <div class="category">
            <h2>{category_name} ({len(repos)})</h2>
"""
            for repo in sorted(repos, key=lambda x: x['name']):
                name = repo['name']
                url = repo['html_url']
                desc = repo.get('description', 'No description available')
                lang = repo.get('language', 'N/A')
                stars = repo.get('stargazers_count', 0)
                
                html += f"""
            <div class="repo-card">
                <a href="{url}" class="repo-name" target="_blank">{name}</a>
                <div class="repo-desc">{desc}</div>
                <div class="repo-meta">
                    <span class="badge">{lang}</span>
                    <span>⭐ {stars}</span>
                </div>
            </div>
"""
            html += """
        </div>
"""
        
        html += """
    </div>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Exported to {output_file}")
    
    def list_repositories(self, category: Optional[str] = None, language: Optional[str] = None):
        """List repositories with optional filtering."""
        repos = self.repositories
        
        if category:
            categories = self.categorize_repositories()
            repos = categories.get(category, [])
            print(f"\n📚 Repositories in category '{category}': {len(repos)}\n")
        elif language:
            repos = [r for r in repos if r.get('language', '').lower() == language.lower()]
            print(f"\n📚 Repositories with language '{language}': {len(repos)}\n")
        else:
            print(f"\n📚 All Repositories: {len(repos)}\n")
        
        for repo in sorted(repos, key=lambda x: x['name']):
            name = repo['name']
            desc = repo.get('description', 'No description')
            lang = repo.get('language', 'N/A')
            stars = repo.get('stargazers_count', 0)
            url = repo['html_url']
            print(f"  🖤 {name}")
            print(f"     {desc}")
            print(f"     Language: {lang} | Stars: ⭐ {stars}")
            print(f"     {url}")
            print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BlackRoad OS Repository Index - Central catalog and discovery service"
    )
    parser.add_argument("--list", action="store_true", help="List all repositories")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--language", type=str, help="Filter by programming language")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--export", type=str, help="Export to JSON file")
    parser.add_argument("--markdown", type=str, help="Export to Markdown file")
    parser.add_argument("--html", type=str, help="Export to HTML file")
    parser.add_argument("--catalog", action="store_true", help="Generate all catalog formats")
    parser.add_argument("--update", action="store_true", help="Force update from GitHub")
    
    args = parser.parse_args()
    
    # Initialize index
    index = RepositoryIndex()
    
    # Fetch repositories
    index.fetch_all_repositories()
    
    if not index.repositories:
        print("❌ No repositories found or failed to fetch.")
        return 1
    
    # Handle commands
    if args.stats:
        stats = index.generate_statistics()
        print("\n📊 Repository Statistics\n")
        print(f"Total Repositories: {stats['total_repositories']}")
        print(f"Total Stars: {stats['total_stars']}")
        print(f"Total Forks: {stats['total_forks']}")
        print(f"Updated Recently: {stats['updated_recently']}")
        print(f"Archived: {stats['archived']}")
        print(f"\nTop Languages:")
        for lang, count in sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {lang}: {count}")
        print(f"\nCategories:")
        for cat, count in sorted(stats['by_category'].items()):
            print(f"  {cat}: {count}")
    
    elif args.list or args.category or args.language:
        index.list_repositories(category=args.category, language=args.language)
    
    elif args.export:
        index.export_json(args.export)
    
    elif args.markdown:
        index.export_markdown(args.markdown)
    
    elif args.html:
        index.export_html(args.html)
    
    elif args.catalog:
        index.export_json("repositories.json")
        index.export_markdown("REPOSITORIES.md")
        index.export_html("catalog.html")
        print("\n✅ Generated all catalog formats!")
    
    else:
        # Default: show summary
        print(f"\n🖤 BlackRoad OS Repository Index")
        print(f"📦 Total Repositories: {len(index.repositories)}")
        print(f"\nUse --help for available commands")
        print(f"Example: python index.py --list")
        print(f"Example: python index.py --stats")
        print(f"Example: python index.py --catalog")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
