#!/usr/bin/env python3
"""
Content Creator Interface - Easy access to hybrid content generation
Combines systematic planning with Grok's creative ideation
"""

import sys
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from grok_content_generator import GrokContentGenerator
from hybrid_content_workflow import HybridContentWorkflow

# Load environment variables
load_dotenv()

class ContentCreator:
    def __init__(self):
        self.api_key = os.getenv("GROK_API_KEY")
        if not self.api_key:
            raise ValueError("GROK_API_KEY not found in environment variables. Please set it in your .env file.")
        self.grok = GrokContentGenerator(self.api_key)
        self.workflow = HybridContentWorkflow(self.api_key)
    
    def show_menu(self):
        """Display the main menu"""
        print("\n🚀 AGROVERSE CONTENT CREATOR")
        print("=" * 50)
        print("Hybrid Approach: Systematic Planning + Creative Ideation")
        print("=" * 50)
        print("1. 🎨 Generate Creative Content Ideas")
        print("2. 🔥 Generate Trending Content Ideas")
        print("3. ✨ Enhance Existing Content")
        print("4. 📅 Generate Weekly Themes")
        print("5. 🚀 Run Full Hybrid Workflow")
        print("6. 📊 Analyze Content Gaps")
        print("7. 💡 Quick Content Ideas")
        print("8. ❌ Exit")
        print("=" * 50)
    
    def generate_creative_ideas(self):
        """Generate creative content ideas for a specific theme"""
        print("\n🎨 CREATIVE CONTENT IDEAS")
        print("=" * 30)
        
        themes = [
            "Behind-the-Scenes",
            "Community Impact", 
            "Regenerative Farming",
            "Cacao Education",
            "Recipes & Rituals"
        ]
        
        print("Available themes:")
        for i, theme in enumerate(themes, 1):
            print(f"{i}. {theme}")
        
        try:
            choice = int(input("\nSelect theme (1-5): ")) - 1
            if 0 <= choice < len(themes):
                theme = themes[choice]
                post_type = input("Post type (Reel/Carousel): ").strip() or "Reel"
                context = input("Additional context (optional): ").strip()
                
                print(f"\n🤖 Generating creative ideas for '{theme}' {post_type}...")
                ideas = self.grok.generate_content_ideas(theme, post_type, context)
                
                if ideas:
                    print("\n✅ CREATIVE IDEAS GENERATED:")
                    print("=" * 40)
                    print(ideas)
                    
                    # Save to file
                    filename = f"creative_ideas_{theme.lower().replace('-', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                    with open(filename, 'w') as f:
                        f.write(f"Creative Ideas for {theme} {post_type}\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(ideas)
                    print(f"\n💾 Ideas saved to: {filename}")
                else:
                    print("❌ Failed to generate ideas")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def generate_trending_ideas(self):
        """Generate trending content ideas"""
        print("\n🔥 TRENDING CONTENT IDEAS")
        print("=" * 30)
        
        trends = input("Current trends to consider (optional): ").strip()
        if not trends:
            trends = "sustainability, farm-to-table, authentic storytelling, regenerative agriculture"
        
        print(f"\n🤖 Generating trending content ideas...")
        trending = self.grok.generate_trending_content(trends)
        
        if trending:
            print("\n✅ TRENDING IDEAS GENERATED:")
            print("=" * 40)
            print(trending)
            
            # Save to file
            filename = f"trending_ideas_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(filename, 'w') as f:
                f.write("Trending Content Ideas\n")
                f.write("=" * 30 + "\n\n")
                f.write(trending)
            print(f"\n💾 Ideas saved to: {filename}")
        else:
            print("❌ Failed to generate trending ideas")
    
    def enhance_existing_content(self):
        """Enhance existing content"""
        print("\n✨ ENHANCE EXISTING CONTENT")
        print("=" * 30)
        
        print("Paste your existing content below (press Enter twice when done):")
        content_lines = []
        while True:
            line = input()
            if line == "" and content_lines and content_lines[-1] == "":
                break
            content_lines.append(line)
        
        content = "\n".join(content_lines[:-1])  # Remove the last empty line
        
        if content.strip():
            print(f"\n🤖 Enhancing content with Grok...")
            enhancement = self.grok.enhance_existing_content(content)
            
            if enhancement:
                print("\n✅ CONTENT ENHANCEMENT:")
                print("=" * 40)
                print(enhancement)
                
                # Save to file
                filename = f"content_enhancement_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                with open(filename, 'w') as f:
                    f.write("Content Enhancement\n")
                    f.write("=" * 25 + "\n\n")
                    f.write("Original Content:\n")
                    f.write("-" * 20 + "\n")
                    f.write(content + "\n\n")
                    f.write("Enhanced Content:\n")
                    f.write("-" * 20 + "\n")
                    f.write(enhancement)
                print(f"\n💾 Enhancement saved to: {filename}")
            else:
                print("❌ Failed to enhance content")
        else:
            print("❌ No content provided")
    
    def generate_weekly_themes(self):
        """Generate weekly themes"""
        print("\n📅 WEEKLY THEMES")
        print("=" * 20)
        
        try:
            week = int(input("Week number: "))
            season = input("Season (fall/spring/summer/winter): ").strip() or "fall"
            
            print(f"\n🤖 Generating themes for Week {week}...")
            themes = self.grok.generate_week_themes(week, season)
            
            if themes:
                print(f"\n✅ WEEK {week} THEMES:")
                print("=" * 40)
                print(themes)
                
                # Save to file
                filename = f"weekly_themes_week_{week}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                with open(filename, 'w') as f:
                    f.write(f"Week {week} Themes ({season.title()})\n")
                    f.write("=" * 40 + "\n\n")
                    f.write(themes)
                print(f"\n💾 Themes saved to: {filename}")
            else:
                print("❌ Failed to generate themes")
        except ValueError:
            print("❌ Please enter a valid week number")
    
    def run_hybrid_workflow(self):
        """Run the full hybrid workflow"""
        print("\n🚀 HYBRID WORKFLOW")
        print("=" * 25)
        
        try:
            weeks = int(input("Number of weeks to analyze (1-8): ") or "2")
            include_trending = input("Include trending content? (y/n): ").strip().lower() != 'n'
            
            print(f"\n🤖 Running hybrid workflow for {weeks} weeks...")
            results = self.workflow.hybrid_content_strategy(weeks, include_trending)
            
            print("\n✅ HYBRID WORKFLOW RESULTS:")
            print("=" * 40)
            print(f"Content gaps found: {results['systematic_analysis']['content_gaps']}")
            print(f"Weeks planned: {results['systematic_analysis']['weeks_planned']}")
            print(f"Total posts: {results['systematic_analysis']['total_posts']}")
            print(f"Creative enhancements: {len(results['creative_enhancements'])}")
            print(f"Weekly themes: {len(results['weekly_themes'])}")
            print(f"Recommendations: {len(results['recommendations'])}")
            
            # Save results
            filename = f"hybrid_workflow_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            self.workflow.save_results(results, filename)
            print(f"\n💾 Full results saved to: {filename}")
            
        except ValueError:
            print("❌ Please enter a valid number")
    
    def analyze_content_gaps(self):
        """Analyze content gaps in the schedule"""
        print("\n📊 CONTENT GAP ANALYSIS")
        print("=" * 30)
        
        gaps = self.workflow.analyze_content_gaps(4)
        print(f"Found {len(gaps)} content entries that need enhancement")
        
        if len(gaps) > 0:
            print("\nSample gaps:")
            for i, (idx, row) in enumerate(gaps.head(5).iterrows()):
                print(f"{i+1}. {row['Post Day']} - {row['Theme']} - {row['Description'][:50]}...")
        
        return gaps
    
    def quick_content_ideas(self):
        """Generate quick content ideas for immediate use"""
        print("\n💡 QUICK CONTENT IDEAS")
        print("=" * 25)
        
        # Generate ideas for each core theme
        themes = ["Behind-the-Scenes", "Community Impact", "Regenerative Farming", "Cacao Education"]
        
        all_ideas = []
        for theme in themes:
            print(f"\n🤖 Generating quick ideas for {theme}...")
            ideas = self.grok.generate_content_ideas(theme, "Reel", "Quick, engaging content")
            if ideas:
                all_ideas.append(f"\n=== {theme.upper()} ===\n{ideas}")
        
        if all_ideas:
            combined_ideas = "\n".join(all_ideas)
            print("\n✅ QUICK CONTENT IDEAS:")
            print("=" * 40)
            print(combined_ideas)
            
            # Save to file
            filename = f"quick_ideas_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(filename, 'w') as f:
                f.write("Quick Content Ideas\n")
                f.write("=" * 25 + "\n\n")
                f.write(combined_ideas)
            print(f"\n💾 Ideas saved to: {filename}")
        else:
            print("❌ Failed to generate quick ideas")
    
    def run(self):
        """Main application loop"""
        while True:
            self.show_menu()
            
            try:
                choice = input("\nSelect option (1-8): ").strip()
                
                if choice == "1":
                    self.generate_creative_ideas()
                elif choice == "2":
                    self.generate_trending_ideas()
                elif choice == "3":
                    self.enhance_existing_content()
                elif choice == "4":
                    self.generate_weekly_themes()
                elif choice == "5":
                    self.run_hybrid_workflow()
                elif choice == "6":
                    self.analyze_content_gaps()
                elif choice == "7":
                    self.quick_content_ideas()
                elif choice == "8":
                    print("\n👋 Goodbye! Happy content creating!")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-8.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Happy content creating!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")

def main():
    """Main function"""
    creator = ContentCreator()
    creator.run()

if __name__ == "__main__":
    main()
