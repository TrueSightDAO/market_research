# Truesight DAO Blog Post Management

Complete guide for managing blog content scheduling and publishing for Truesight DAO.

## 📁 Directory Structure

```
online_content/truesight_dao/blog_post/
├── README.md                          # This file (consolidated documentation)
├── sync_truesight_blog_schedule.py   # Sync blog schedule to Google Sheets
├── truesight_blog_schedule.csv       # Blog content schedule
├── truesight_recent_activity.csv      # Recent activity tracking
└── truesight_blog_posts/             # Markdown blog post content
    ├── 20251013_cacao_sourcing_expansion.md
    └── 20251022_f6160186_operational_framework_2026.md
```

## 🎯 Overview

This directory manages blog content publishing for Truesight DAO, including:
- Blog schedule management and synchronization
- Blog post content storage
- Recent activity tracking

## 🔧 Key Scripts

### `sync_truesight_blog_schedule.py`
Sync blog schedule from CSV to Google Sheets:
```bash
python3 sync_truesight_blog_schedule.py
```

**What it does:**
- Reads `truesight_blog_schedule.csv`
- Syncs to Google Sheets
- Preserves manual status updates

## 📋 Blog Schedule Structure

**CSV File:** `truesight_blog_schedule.csv`

Similar structure to Agroverse blog schedule, but tailored for Truesight DAO content.

## 📚 Blog Posts

**Directory:** `truesight_blog_posts/`

Contains markdown files for blog post content:
- `20251013_cacao_sourcing_expansion.md` - Cacao sourcing expansion content
- `20251022_f6160186_operational_framework_2026.md` - Operational framework for 2026

## 📊 Recent Activity Tracking

**File:** `truesight_recent_activity.csv`

Tracks recent blog activity and publishing status.

## 💡 Best Practices

1. **Consistency** - Maintain regular publishing schedule
2. **Quality** - Focus on DAO-specific content and values
3. **Integration** - Coordinate with other Truesight DAO content channels

---

*Last updated: November 2025*
*This README consolidates all Truesight DAO blog post documentation for easy reference by Cursor AI*

