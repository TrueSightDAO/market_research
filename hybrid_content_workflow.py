#!/usr/bin/env python3
"""
Hybrid Content Workflow: Systematic Planning + Creative Ideation
Combines our structured approach with Grok's creative content generation
"""

import pandas as pd
import json
from datetime import datetime, timedelta
from grok_content_generator import GrokContentGenerator

class HybridContentWorkflow:
    def __init__(self, grok_api_key):
        self.grok = GrokContentGenerator(grok_api_key)
        self.content_schedule = pd.read_csv('agroverse_schedule_till_easter.csv')
        self.hashtags_db = pd.read_csv('instagram_hashtags.csv')
        
        # Define our systematic themes and patterns
        self.core_themes = [
            'Behind-the-Scenes',
            'Community Impact', 
            'Regenerative Farming',
            'Cacao Education',
            'Recipes & Rituals'
        ]
        
        self.post_types = ['Reel', 'Carousel']
        
    def analyze_content_gaps(self, weeks_ahead=4):
        """Identify content gaps where we need fresh ideas"""
        print("🔍 Analyzing content gaps...")
        
        # Find content with empty or generic descriptions
        gaps = self.content_schedule[
            (self.content_schedule['Description'].str.len() < 50) |
            (self.content_schedule['Description'].str.contains('Engaging', na=False)) |
            (self.content_schedule['status'].isna())
        ].copy()
        
        print(f"Found {len(gaps)} content entries that need creative enhancement")
        return gaps
    
    def generate_creative_enhancements(self, content_gaps):
        """Use Grok to enhance content that needs creative improvement"""
        print("🎨 Generating creative enhancements with Grok...")
        
        enhanced_content = []
        
        for idx, row in content_gaps.head(10).iterrows():  # Process first 10 for testing
            print(f"\n📝 Enhancing content for {row['Post Day']} - {row['Theme']}")
            
            # Prepare context for Grok
            context = f"""
            Date: {row['Post Day']}
            Theme: {row['Theme']}
            Post Type: {row['Post Type']}
            Current Description: {row['Description']}
            Week: {row['Week']}
            """
            
            # Get creative enhancement from Grok
            enhancement = self.grok.enhance_existing_content(context)
            
            if enhancement:
                enhanced_content.append({
                    'original_row': idx,
                    'enhancement': enhancement,
                    'post_day': row['Post Day'],
                    'theme': row['Theme']
                })
                print(f"✅ Enhanced content for {row['Post Day']}")
            else:
                print(f"❌ Failed to enhance content for {row['Post Day']}")
        
        return enhanced_content
    
    def generate_trending_ideas(self, current_trends=""):
        """Generate trending content ideas using Grok"""
        print("🔥 Generating trending content ideas...")
        
        trending_ideas = self.grok.generate_trending_content(current_trends)
        
        if trending_ideas:
            print("✅ Generated trending content ideas")
            return trending_ideas
        else:
            print("❌ Failed to generate trending ideas")
            return None
    
    def generate_weekly_themes(self, week_number, season="fall"):
        """Generate creative weekly themes using Grok"""
        print(f"📅 Generating creative themes for Week {week_number}...")
        
        weekly_themes = self.grok.generate_week_themes(week_number, season)
        
        if weekly_themes:
            print(f"✅ Generated themes for Week {week_number}")
            return weekly_themes
        else:
            print(f"❌ Failed to generate themes for Week {week_number}")
            return None
    
    def systematic_content_planning(self, start_week=1, num_weeks=4):
        """Our systematic approach to content planning"""
        print(f"📊 Systematic content planning for weeks {start_week}-{start_week + num_weeks - 1}")
        
        planned_content = []
        
        for week in range(start_week, start_week + num_weeks):
            week_content = self.content_schedule[
                self.content_schedule['Week'] == f'Week {week}'
            ].copy()
            
            if len(week_content) > 0:
                planned_content.append({
                    'week': week,
                    'content': week_content,
                    'themes': week_content['Theme'].tolist(),
                    'post_types': week_content['Post Type'].tolist()
                })
        
        return planned_content
    
    def hybrid_content_strategy(self, weeks_ahead=4, include_trending=True):
        """Main hybrid workflow combining systematic planning with creative ideation"""
        print("🚀 Starting Hybrid Content Strategy")
        print("=" * 60)
        
        # Step 1: Systematic Analysis
        print("\n📊 Step 1: Systematic Content Analysis")
        content_gaps = self.analyze_content_gaps(weeks_ahead)
        systematic_plan = self.systematic_content_planning(1, weeks_ahead)
        
        # Step 2: Creative Enhancement
        print("\n🎨 Step 2: Creative Enhancement with Grok")
        enhanced_content = self.generate_creative_enhancements(content_gaps)
        
        # Step 3: Trending Content (if requested)
        trending_ideas = None
        if include_trending:
            print("\n🔥 Step 3: Trending Content Generation")
            trending_ideas = self.generate_trending_ideas(
                "sustainability, farm-to-table, authentic storytelling, regenerative agriculture"
            )
        
        # Step 4: Weekly Theme Generation
        print("\n📅 Step 4: Creative Weekly Themes")
        weekly_themes = {}
        for week in range(1, min(weeks_ahead + 1, 5)):  # Generate themes for first 4 weeks
            themes = self.generate_weekly_themes(week, "fall")
            if themes:
                weekly_themes[f'Week {week}'] = themes
        
        # Compile results
        results = {
            'systematic_analysis': {
                'content_gaps': len(content_gaps),
                'weeks_planned': len(systematic_plan),
                'total_posts': sum(len(week['content']) for week in systematic_plan)
            },
            'creative_enhancements': enhanced_content,
            'trending_ideas': trending_ideas,
            'weekly_themes': weekly_themes,
            'recommendations': self.generate_recommendations(enhanced_content, trending_ideas)
        }
        
        return results
    
    def generate_recommendations(self, enhanced_content, trending_ideas):
        """Generate actionable recommendations based on hybrid analysis"""
        recommendations = []
        
        if enhanced_content:
            recommendations.append({
                'type': 'content_enhancement',
                'priority': 'high',
                'action': f'Review and implement {len(enhanced_content)} creative enhancements',
                'impact': 'Improved engagement and authenticity'
            })
        
        if trending_ideas:
            recommendations.append({
                'type': 'trending_content',
                'priority': 'medium',
                'action': 'Integrate trending content ideas into upcoming schedule',
                'impact': 'Increased reach and viral potential'
            })
        
        recommendations.append({
            'type': 'workflow_optimization',
            'priority': 'low',
            'action': 'Run hybrid workflow weekly for continuous improvement',
            'impact': 'Consistent content quality and innovation'
        })
        
        return recommendations
    
    def save_results(self, results, filename="hybrid_content_results.json"):
        """Save hybrid workflow results"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"💾 Results saved to {filename}")

def main():
    """Test the hybrid workflow"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("GROK_API_KEY")
    
    if not api_key:
        print("❌ Error: GROK_API_KEY not found in environment variables.")
        print("Please set GROK_API_KEY in your .env file.")
        return
    
    workflow = HybridContentWorkflow(api_key)
    
    print("🚀 Testing Hybrid Content Workflow")
    print("=" * 50)
    
    # Run hybrid strategy
    results = workflow.hybrid_content_strategy(weeks_ahead=2, include_trending=True)
    
    # Display results
    print("\n📊 HYBRID WORKFLOW RESULTS")
    print("=" * 50)
    
    print(f"Systematic Analysis:")
    print(f"  - Content gaps found: {results['systematic_analysis']['content_gaps']}")
    print(f"  - Weeks planned: {results['systematic_analysis']['weeks_planned']}")
    print(f"  - Total posts: {results['systematic_analysis']['total_posts']}")
    
    print(f"\nCreative Enhancements: {len(results['creative_enhancements'])} generated")
    print(f"Weekly Themes: {len(results['weekly_themes'])} weeks planned")
    print(f"Recommendations: {len(results['recommendations'])} actionable items")
    
    # Save results
    workflow.save_results(results)
    
    print("\n✅ Hybrid workflow test completed!")

if __name__ == "__main__":
    main()
