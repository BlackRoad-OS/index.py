#!/usr/bin/env python3
"""
Example usage of the BlackRoad OS Repository Index.
Demonstrates how to use the index programmatically.
"""

import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_static_data():
    """Load the static repository data."""
    static_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "repositories-static.json"
    )
    
    with open(static_file, 'r') as f:
        return json.load(f)


def example_list_all_repositories():
    """Example: List all repositories."""
    print("📚 Example 1: List All Repositories\n")
    
    data = load_static_data()
    
    print(f"Organization: {data['organization']}")
    print(f"Total Repositories: {data['total_count']}")
    print(f"\nCategories: {len(data['categories'])}")
    
    for category, repos in data['categories'].items():
        print(f"  - {category}: {len(repos)} repositories")
    
    print("\n" + "="*60 + "\n")


def example_list_by_category():
    """Example: List repositories in a specific category."""
    print("🤖 Example 2: AI & Machine Learning Repositories\n")
    
    data = load_static_data()
    ai_repos = data['categories'].get('ai', [])
    
    for repo in ai_repos:
        print(f"  🖤 {repo['name']}")
        print(f"     {repo['description']}")
        print(f"     {repo['html_url']}")
        print()
    
    print("="*60 + "\n")


def example_search_by_keyword():
    """Example: Search repositories by keyword."""
    keyword = "scheduler"
    print(f"🔍 Example 3: Search for '{keyword}'\n")
    
    data = load_static_data()
    results = []
    
    for category, repos in data['categories'].items():
        for repo in repos:
            if keyword.lower() in repo['name'].lower() or \
               keyword.lower() in repo['description'].lower():
                results.append((category, repo))
    
    print(f"Found {len(results)} repositories:\n")
    
    for category, repo in results:
        print(f"  🖤 {repo['name']} ({category})")
        print(f"     {repo['description']}")
        print(f"     {repo['html_url']}")
        print()
    
    print("="*60 + "\n")


def example_generate_report():
    """Example: Generate a simple report."""
    print("📊 Example 4: Repository Report\n")
    
    data = load_static_data()
    
    print(f"BlackRoad OS Repository Report")
    print(f"{'='*60}")
    print(f"Organization: {data['organization']}")
    print(f"Total Repositories: {data['total_count']}")
    print(f"Generated: {data['generated_at']}")
    print()
    
    print("Category Breakdown:")
    print(f"{'-'*60}")
    
    categories = data['categories']
    sorted_categories = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
    
    for category, repos in sorted_categories:
        bar = "█" * (len(repos) // 2)
        print(f"{category:20} | {bar} {len(repos)}")
    
    print()
    print("="*60 + "\n")


def example_get_links():
    """Example: Extract all repository URLs."""
    print("🔗 Example 5: Extract All Repository URLs\n")
    
    data = load_static_data()
    all_urls = []
    
    for category, repos in data['categories'].items():
        for repo in repos:
            all_urls.append(repo['html_url'])
    
    print(f"Total URLs: {len(all_urls)}\n")
    print("First 10 URLs:")
    for url in all_urls[:10]:
        print(f"  - {url}")
    
    print(f"\n... and {len(all_urls) - 10} more")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    print("\n🖤 BlackRoad OS Repository Index - Usage Examples\n")
    print("="*60 + "\n")
    
    example_list_all_repositories()
    example_list_by_category()
    example_search_by_keyword()
    example_generate_report()
    example_get_links()
    
    print("✅ All examples completed!")
    print("\n💡 Tip: Modify these examples for your own use cases!")
    print("📖 See README.md for more information.\n")
