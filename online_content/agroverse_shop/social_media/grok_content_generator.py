#!/usr/bin/env python3
"""
Grok Content Generator for Agroverse Instagram Content
Hybrid approach combining systematic planning with creative ideation
"""

import requests
import json
import pandas as pd
from datetime import datetime
import hashlib

class GrokContentGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Load existing content patterns for context
        self.content_schedule = pd.read_csv('agroverse_schedule_till_easter.csv')
        self.hashtags_db = pd.read_csv('instagram_hashtags.csv')
        
    def get_system_prompt(self):
        """System prompt that defines Grok's role in our hybrid approach"""
        return """You are Grok, the creative content ideation specialist for Agroverse.shop, a sustainable cacao brand. 

Your role in our hybrid approach:
- Generate creative, engaging content ideas that align with our brand voice
- Suggest trending angles and fresh perspectives on cacao/sustainability topics
- Create compelling captions with strong CTAs
- Recommend relevant hashtags from our curated database
- Maintain authenticity while being creative and engaging

Brand Context:
- Focus: Sustainable cacao from Pará & Bahia, Brazil
- Themes: Regenerative Farming, Community Impact, Cacao Education, Recipes & Rituals, Behind-the-Scenes
- Tone: Authentic, educational, community-focused, inspiring
- Target: Conscious consumers, chocolate lovers, sustainability advocates

Content Types: Reels, Carousels, Stories
Posting Schedule: 4 posts per week (Mon-Thu)
Current Date: September 2025

Your creative ideas should complement our systematic content planning while adding fresh, engaging angles."""

    def generate_content_ideas(self, theme, post_type, context=""):
        """Generate creative content ideas using Grok"""
        
        prompt = f"""
        Generate 3 creative content ideas for Agroverse.shop Instagram {post_type} focusing on "{theme}".
        
        Context: {context}
        
        For each idea, provide:
        1. Creative Hook/Title
        2. Detailed Description (2-3 sentences)
        3. Engaging Caption (with emojis, line breaks, and strong CTA)
        4. 15-20 relevant hashtags (mix of general and targeted)
        5. Suggested CTA
        6. Why this idea is engaging/unique
        
        Make it authentic, educational, and community-focused. Think about what would make someone stop scrolling and engage.
        """
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "grok-3",
                    "messages": [
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.8
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Grok API: {e}")
            return None

    def generate_trending_content(self, current_trends=""):
        """Generate content ideas based on current trends"""
        
        prompt = f"""
        Generate 5 trending content ideas for Agroverse.shop that could go viral on Instagram.
        
        Current trends to consider: {current_trends}
        
        Focus on:
        - Sustainable cacao farming
        - Brazilian culture and farming practices
        - Educational content about chocolate making
        - Community impact stories
        - Behind-the-scenes farm life
        
        For each idea, provide:
        1. Trend-based Hook
        2. Why it's trending/viral potential
        3. Content Description
        4. Caption with trending elements
        5. Relevant hashtags including trending ones
        6. Engagement strategy
        
        Make it authentic to our brand while leveraging trending formats and topics.
        """
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "grok-3",
                    "messages": [
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 2500,
                    "temperature": 0.9
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Grok API: {e}")
            return None

    def enhance_existing_content(self, current_content):
        """Enhance existing content with creative improvements"""
        
        prompt = f"""
        Review and enhance this existing Instagram content for Agroverse.shop:
        
        Current Content:
        {current_content}
        
        Please provide:
        1. Creative improvements to the caption
        2. Better CTA suggestions
        3. Additional relevant hashtags
        4. Engagement-boosting elements
        5. Alternative creative angles for the same content
        
        Maintain the authentic, educational tone while making it more engaging and shareable.
        """
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "grok-3",
                    "messages": [
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 1500,
                    "temperature": 0.7
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Grok API: {e}")
            return None

    def generate_week_themes(self, week_number, season="fall"):
        """Generate creative themes for a specific week"""
        
        prompt = f"""
        Generate creative weekly themes for Week {week_number} of Agroverse.shop's Instagram content (Fall 2025).
        
        Season: {season}
        Week: {week_number}
        
        Provide 4 creative themes (one for each post day: Mon, Tue, Wed, Thu) that:
        1. Connect to seasonal elements
        2. Align with our brand values (sustainability, community, education)
        3. Offer fresh angles on cacao/sustainable farming
        4. Include specific content ideas for each theme
        5. Suggest optimal posting times/strategies
        
        Make each theme unique but cohesive with our overall brand narrative.
        """
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "grok-3",
                    "messages": [
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.8
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Grok API: {e}")
            return None

def main():
    """Test the Grok integration"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("GROK_API_KEY")
    
    if not api_key:
        print("❌ Error: GROK_API_KEY not found in environment variables.")
        print("Please set GROK_API_KEY in your .env file.")
        return
    
    generator = GrokContentGenerator(api_key)
    
    print("🤖 Testing Grok Content Generator")
    print("=" * 50)
    
    # Test 1: Generate content ideas for a specific theme
    print("\n📝 Test 1: Generating content ideas for 'Behind-the-Scenes' theme")
    ideas = generator.generate_content_ideas(
        theme="Behind-the-Scenes",
        post_type="Reel",
        context="Farm life, daily routines, authentic moments"
    )
    
    if ideas:
        print("✅ Grok generated content ideas:")
        print(ideas)
    else:
        print("❌ Failed to generate content ideas")
    
    # Test 2: Generate trending content
    print("\n🔥 Test 2: Generating trending content ideas")
    trending = generator.generate_trending_content(
        current_trends="sustainability, farm-to-table, authentic storytelling"
    )
    
    if trending:
        print("✅ Grok generated trending content:")
        print(trending)
    else:
        print("❌ Failed to generate trending content")

if __name__ == "__main__":
    main()
