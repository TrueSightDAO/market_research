#!/usr/bin/env python3
"""
Generate HTML from Markdown for easy copy-paste into Wix
This is more reliable than fighting with Ricos JSON format
"""

import markdown
from datetime import datetime

def generate_blog_html(markdown_file, output_file=None):
    """Convert Markdown blog post to HTML for Wix"""
    
    print(f"\n{'='*80}")
    print("GENERATING HTML FOR WIX")
    print(f"{'='*80}\n")
    
    # Read markdown content
    with open(markdown_file, 'r') as f:
        content = f.read()
    
    # Remove metadata section
    content_lines = content.split('\n')
    clean_content = []
    skip_metadata = True
    metadata = {}
    
    for line in content_lines:
        if skip_metadata and line.startswith('**') and ':' in line:
            # Extract metadata
            key = line.split(':')[0].replace('**', '').strip()
            value = ':'.join(line.split(':')[1:]).strip()
            metadata[key] = value
            continue
        if skip_metadata and line.startswith('---'):
            skip_metadata = False
            continue
        if not skip_metadata or line.startswith('# '):
            skip_metadata = False
            clean_content.append(line)
    
    clean_markdown = '\n'.join(clean_content)
    
    # Convert to HTML
    html = markdown.markdown(
        clean_markdown,
        extensions=['extra', 'nl2br', 'sane_lists']
    )
    
    # Extract title from first H1
    import re
    title_match = re.search(r'<h1>(.*?)</h1>', html)
    title = title_match.group(1) if title_match else "Untitled Post"
    
    # Generate output filename if not provided
    if not output_file:
        slug = metadata.get('URL Slug', 'blog-post')
        output_file = f'agroverse_blog_posts/{slug}_html.html'
    
    # Create formatted HTML with instructions
    full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>

<!-- 
================================================================
INSTRUCTIONS FOR POSTING TO WIX:
================================================================

1. Go to Wix Dashboard: https://www.wix.com/dashboard
2. Navigate to: Blog > Posts > + New Post
3. Copy the HTML below (starting from <h1>)
4. In Wix Editor:
   - Click the "..." menu > "Add HTML/Code"
   - OR switch to HTML mode and paste
   - OR copy-paste directly into rich text editor (Wix will convert)
5. Add these settings manually:
   - Title: {title}
   - URL Slug: {metadata.get('URL Slug', 'auto')}
   - SEO Title: {metadata.get('SEO Title', title)}
   - Meta Description: {metadata.get('Meta Description', '')}
   - Schedule Date: October 14, 2025, 9:00 AM UTC
6. Add featured image (1200 x 628px recommended)
7. Add Instagram embeds where noted
8. Review and click "Schedule"

SEO Keywords: {metadata.get('SEO Keywords', 'N/A')}
Target Word Count: {metadata.get('Word Count Target', 'N/A')}

================================================================
-->

{html}

<!-- 
================================================================
POST-PUBLISHING CHECKLIST:
================================================================
- [ ] Update Instagram bio link to this post
- [ ] Share on Instagram Stories
- [ ] Send email newsletter
- [ ] Create Pinterest pins
- [ ] Post to Facebook/LinkedIn
- [ ] Update Google Sheets status to "SCHEDULED"
================================================================
-->

</body>
</html>
"""
    
    # Save to file
    with open(output_file, 'w') as f:
        f.write(full_html)
    
    print(f"✅ HTML generated successfully!")
    print(f"   Output file: {output_file}")
    print(f"   Title: {title}")
    print(f"   Word count: ~{len(clean_markdown.split())} words")
    
    if metadata:
        print(f"\n📋 SEO Metadata:")
        for key, value in metadata.items():
            print(f"   {key}: {value[:80] if len(value) > 80 else value}...")
    
    print(f"\n📝 Next Steps:")
    print(f"   1. Open file: {output_file}")
    print(f"   2. Copy the HTML content")
    print(f"   3. Paste into Wix blog editor")
    print(f"   4. Add images and Instagram embeds manually")
    print(f"   5. Schedule for October 14, 2025, 9:00 AM")
    
    return output_file


if __name__ == "__main__":
    # Generate HTML for Okanogan post
    output = generate_blog_html('agroverse_blog_posts/okanogan_journey.md')
    print(f"\n🎉 Done! Open {output} to view the HTML")

