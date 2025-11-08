#!/usr/bin/env python3
"""
Consolidated Hit List - All shop targets organized by region
Unified list combining Bay Area, Central CA, Coastal CA, SoCal, and Arizona routes
"""

import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
import time
import requests

# Google Sheets configuration
SPREADSHEET_ID = "1eiqZr3LW-qEI6Hmy0Vrur_8flbRwxwA7jXVrbUnHbvc"
SERVICE_ACCOUNT_EMAIL = "agroverse-market-research@get-data-io.iam.gserviceaccount.com"

# Scope for Google Sheets API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

DAPP_REMARKS_SHEET = "DApp Remarks"

# ============================================================================
# CONSOLIDATED HIT LIST - Organized by Region for Easy Daily Planning
# ============================================================================
SHOPS = [
    # ========================================================================
    # EXISTING PARTNERS (Reference Only)
    # ========================================================================
    {
        "name": "The Love of Ganesha",
        "address": "1700 Haight St",
        "city": "San Francisco",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "ACCEPTED - Bought outright (no consignment). Successful model - prefer outright purchase over consignment.",
        "priority": "Existing Partner",
        "status": "Partnered",
        "outcome": "Accepted - outright purchase"
    },
    {
        "name": "Kiki's Cocoa",
        "address": "1423 Hayes St",
        "city": "San Francisco",
        "state": "CA",
        "type": "Boutique Chocolate",
        "notes": "Already a partner - ethically-sourced, single-origin",
        "priority": "Existing Partner",
        "status": "Partnered"
    },
    {
        "name": "Green Gulch Zen Monastery",
        "address": "1601 Shoreline Highway",
        "city": "Muir Beach",
        "state": "CA",
        "type": "Spiritual/Zen Center",
        "notes": "Partner - Buddhist practice center with organic farm and gardens",
        "priority": "Existing Partner",
        "status": "Partnered"
    },
    {
        "name": "HackerDojo",
        "address": "855 Maude Ave",
        "city": "Mountain View",
        "state": "CA",
        "type": "Tech Community / Coworking",
        "notes": "Partner - Collaborative hackerspace and tech community center",
        "priority": "Existing Partner",
        "status": "Partnered"
    },
    {
        "name": "Miss Tomato Sandwiches and liquor",
        "address": "199 87th St",
        "city": "Daly City",
        "state": "CA",
        "type": "Restaurant/Liquor",
        "notes": "Partner - Sandwiches and liquor",
        "priority": "Existing Partner",
        "status": "Partnered"
    },
    {
        "name": "The Ponderosa",
        "address": "Slab City",
        "city": "Niland",
        "state": "CA",
        "type": "Unique/Lifestyle",
        "notes": "Already a partner - off-grid, sustainability focus. Check if they want additional products.",
        "priority": "Existing Partner",
        "status": "Partnered"
    },
    # ========================================================================
    # REJECTED (Reference Only)
    # ========================================================================
    {
        "name": "East West Bookshop",
        "address": "324 Castro St",
        "city": "Mountain View",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "REJECTED - Doesn't like consignment + needs 100% markup. Issue is pricing structure, not venue fit. Need to offer outright purchase + calculate wholesale price that allows 100% markup.",
        "priority": "High",
        "status": "Rejected",
        "outcome": "Rejected - pricing/markup issue"
    },
    # ========================================================================
    # BAY AREA - San Francisco
    # ========================================================================
    {
        "name": "Infinity Coven",
        "address": "447 Stockton St",
        "city": "San Francisco",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(650) 420-5932",
        "email": "admin@InfinityCoven.com",
        "notes": "Witchy boutique with spells, herbs, books, and community workshops near Union Square. Strong magic/empowerment focus—excellent prospect for ceremonial cacao placement.",
        "priority": "High",
        "status": "Shortlisted"
    },
    {
        "name": "Paxton Gate",
        "address": "824 Valencia St",
        "city": "San Francisco",
        "state": "CA",
        "type": "Curiosity Shop",
        "notes": "Curiosity shop blending natural history with metaphysical items (minerals, taxidermy, oddities). Eclectic bohemian vibe. Potential for cacao as unique regenerative addition.",
        "priority": "Medium",
        "status": "Research"
    },
    # ========================================================================
    # BAY AREA - South Bay (Mountain View, Palo Alto, San Jose)
    # ========================================================================
    {
        "name": "7 Rays Holistic Center",
        "address": "3035 El Camino Real",
        "city": "Palo Alto",
        "state": "CA",
        "type": "Wellness Center",
        "notes": "Offers reiki, crystal healing, metaphysical products (tarot, sacred geometry). Focus on energy work and personal growth. Suitable for cacao as ceremonial enhancement.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "iChakras Smart Healing Center",
        "address": "398 Main St",
        "city": "Los Altos",
        "state": "CA",
        "type": "Wellness Center",
        "phone": "(650) 797-8077",
        "website": "https://www.ichakras.com/",
        "email": "meditate@ichakras.com",
        "notes": "Smart meditation center with metaphysical shop, wellness services, chakra balancing, holistic healing, sound baths, and meditation classes. Open Tue-Sat 12pm-7pm.",
        "priority": "High",
        "status": "Contacted",
        "contact_date": "2025-11-07",
        "contact_method": "Drop-off",
        "visit_date": "2025-11-07",
        "contact_person": "Chloe (staff)",
        "owner_name": "Crystal",
        "product_interest": "Retail cacao display (5 bags on consignment)",
        "sales_notes": "Dropped off five sample bags with Chloe (staff). Crystal was busy; Chloe will check if they can display the cacao. If not a fit, plan to retrieve the bags. Assume-close approach seemed welcome."
    },
    {
        "name": "Ancient Ways",
        "address": "4075 Telegraph Ave",
        "city": "Oakland",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(510) 653-3244",
        "website": "https://www.ancientways.com/",
        "notes": "Pagan and metaphysical store with herbs, candles, books, ritual supplies, bulk herbs, oils, stones, incense, and readings. Serving Oakland's spiritual community for over 30 years. Community-oriented events and ancient traditions. Open 11am-7pm daily (closed Christmas and New Year's Day).",
        "priority": "High",
        "status": "Manager Follow-up",
        "contact_date": "2025-11-05",
        "contact_method": "In-person",
        "follow_up_date": "2025-11-12 11:30-12:00",
        "contact_person": "Don (staff)",
        "owner_name": "Sue",
        "referral": "Don",
        "sales_notes": "Met with Don (staff). Buyer Sue unavailable; call next Wednesday between 11:30am-12pm."
    },
    {
        "name": "Amethyst House",
        "address": "1639 Meridian Ave",
        "city": "San Jose",
        "state": "CA",
        "type": "Wellness Center",
        "phone": "(408) 933-9181",
        "website": "https://www.amethysthousehealing.com/",
        "notes": "Boutique wellness studio with healing services (Reiki, Coaching, Sound Therapy), boutique with curated tools and gifts. Open Tue-Thu 10am-5pm, Fri 10am-7pm, by appointment other days. Focus on complementary and preventative care.",
        "priority": "High",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Contact form",
        "sales_notes": ""
    },
    {
        "name": "Saia Holistic",
        "address": "1645 S Bascom Ave #9",
        "city": "Campbell",
        "state": "CA",
        "type": "Wellness Center",
        "phone": "(669) 223-8955",
        "website": "https://saiawholistic.com/",
        "email": "monnaa@saiawholistic.com",
        "notes": "Holistic wellness center. Check website for services and retail offerings.",
        "priority": "High",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    {
        "name": "Mystic Flora Apothecary",
        "address": "1501 El Camino Real Suite F",
        "city": "San Mateo",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(650) 622-4264",
        "website": "https://www.mysticflora.com/",
        "instagram": "https://www.instagram.com/mysticflora_apothecary/",
        "notes": "Animistic, transcultural apothecary offering teas, ritual tools, community practitioner services, and a self-service tea house. Confirm cacao wholesale fit and scheduling interests.",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "Tokenz",
        "address": "530 Main St",
        "city": "Half Moon Bay",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(650) 712-8457",
        "website": "https://www.tokenzhmb.com/",
        "notes": "Long-running Half Moon Bay boutique (est. 1982) with global imports: masks, statuary, gemstones, incense, bells, gongs, sarongs. Confirm cacao alignment and wholesale interest.",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "Garden Apothecary",
        "address": "601 Main St",
        "city": "Half Moon Bay",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "website": "https://gardenapothecary.com/",
        "email": "shop@gardenapothecary.com",
        "notes": "Botanist-formulated skincare/tea apothecary in downtown Half Moon Bay. Organic, small-batch wellness products with in-store workshops and teas. Confirm ceremonial cacao alignment and wholesale options.",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "Go Ask Alice",
        "address": "1125 Pacific Ave",
        "city": "Santa Cruz",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(831) 469-4372",
        "website": "https://www.goaskalicesantacruz.com/",
        "email": "info@goaskalice.org",
        "notes": "Herbal apothecary and ritual boutique (teas, elixirs, tarot/oracle, decor) open daily 11am-8pm. In-store services include tarot and astrology readings (schedule via practitioners). Verify interest in ceremonial cacao and wholesale options.",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "Moonstone Metaphysical",
        "address": "130 N Santa Cruz Ave",
        "city": "Los Gatos",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(408) 313-4744",
        "website": "https://moonstone-metaphysical.business.site",
        "instagram": "https://www.instagram.com/moonstonemetaphysical/",
        "notes": "Metaphysical shop offering crystals, candles, incense, and spiritual products. Sister store of Moon Kissed in Santa Cruz.",
        "priority": "High",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Instagram",
        "sales_notes": ""
    },
    {
        "name": "Celestial Trading",
        "address": "85 5th St",
        "city": "Gilroy",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "website": "https://www.celestialtrading.us/",
        "notes": "Family-owned store offering crystals, metaphysical tools, and spiritual gifts. Also hosts workshops and events. Good fit for ceremonial cacao.",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "Magical Unicorn Crystals",
        "address": "7650 Dowdy St",
        "city": "Gilroy",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Specializes in crystals and gemstones, promoting positive energy and spiritual well-being. May carry ceremonial products.",
        "priority": "Medium",
        "status": "Research"
    },
    # ========================================================================
    # BAY AREA - East Bay (Fremont, Newark, Hayward, Oakland, Berkeley, etc.)
    # ========================================================================
    {
        "name": "Fremont Natural Foods/Healing",
        "address": "5180 Mowry Ave",
        "city": "Fremont",
        "state": "CA",
        "type": "Health Food Store",
        "phone": "(510) 792-0163",
        "email": "fremontnatural@gmail.com",
        "instagram": "https://www.facebook.com/FremontNatural",
        "notes": "Natural foods store with healing/wellness products. May have sections for spiritual/wellness items.",
        "priority": "Medium",
        "status": "Manager Follow-up",
        "contact_date": "2025-11-07",
        "contact_method": "In-person",
        "follow_up_date": "2025-11-12",
        "contact_person": "Betty",
        "owner_name": "Monica",
        "referral": "Betty",
        "sales_notes": "Met Betty in-store; Monica (buyer) unavailable. Referred to call Monica next Wednesday."
    },
    {
        "name": "Sublime Journey West Coast",
        "address": "37485 Niles Blvd",
        "city": "Fremont",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(510) 896-8496",
        "website": "https://shopsublimejourney.com/",
        "email": "yoursublimejourney@gmail.com",
        "notes": "Metaphysical shop offering spiritual tools, crystals, tarot cards, anointing oils, and healing services. Open everyday 11am-6pm. Owner Jacqua Carr provides chakra alignment services. Safe space for spiritual seekers.",
        "priority": "High",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    {
        "name": "Queen Hippie Gypsy",
        "address": "337 14th St",
        "city": "Oakland",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(510) 282-7829",
        "website": "https://www.queenhippiegypsy.com/",
        "email": "Queenhippiegypsy@gmail.com",
        "notes": "Metaphysical/spiritual shop. Store keeper: Lily (Lilly Ayers). Check website for specific offerings and hours.",
        "priority": "High",
        "status": "Partnered",
        "contact_date": "2025-11-07",
        "contact_method": "Email",
        "contact_person": "Lilly",
        "owner_name": "Lilly",
        "sales_notes": "Onboarded. Lilly confirmed partnership and received onboarding email."
    },
    {
        "name": "The Sanctuary",
        "address": "3344 Grand Ave",
        "city": "Oakland",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "website": "https://thesanctuary.energy/",
        "notes": "Spiritual shop specializing in Ìṣẹ̀ṣe, Lukumí, and Palo traditions. Offers herbal offerings, botànica items, books, crystals, spiritual tools, and spiritual services (readings, cleansings, counseling). Open Wed-Sun 12pm-6pm.",
        "priority": "High",
        "status": "Followed Up",
        "contact_date": "2025-11-05",
        "contact_method": "Phone",
        "follow_up_date": "2025-11-12",
        "contact_person": "Etecia",
        "owner_name": "Etecia & wife",
        "product_interest": "Cacao nibs, cacao butter",
        "sales_notes": "Spoke with Etecia; she'll speak with her wife. They can use cacao nibs and cacao butter. Follow up via email next Wednesday."
    },
    {
        "name": "Twisted Thistle Apothecary",
        "address": "4156 Piedmont Ave",
        "city": "Oakland",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(510) 644-3727",
        "website": "https://www.twistedthistleapothecary.com/",
        "email": "weborders.tta@gmail.com",
        "notes": "Apothecary offering ethically grown herbal teas, superfoods, healing products, natural beauty, crystals, tarot/oracle cards, ritual items, and homewares. In-house herbal blends. Open Sun-Thurs 11am-6pm, Fri-Sat 11am-7pm.",
        "priority": "High",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    {
        "name": "The Sacred Well",
        "address": "536 Grand Ave",
        "city": "Oakland",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Magical emporium with crystals, herbs, tarot, classes on spirituality. Community-driven approach. Cacao fitting as life-force enhancer.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "Lakshmi Crystals & Gifts",
        "address": "3301 Grand Ave",
        "city": "Oakland",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Crystal shop with spiritual gifts, incense, and healing tools. Community-focused with meditation groups. Good fit for ceremonial cacao.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "Alameda Natural Grocery",
        "address": "1650 Park St",
        "city": "Alameda",
        "state": "CA",
        "type": "Health Food Store",
        "phone": "(510) 865-1500",
        "website": "https://alamedanaturalgrocery.com/",
        "notes": "Woman-owned, independently operated natural grocer with extensive organic and specialty foods. Has wellness department with supplements and natural products. May have sections suitable for ceremonial products. Open Mon-Sat 8am-8pm, Sun 8am-7pm.",
        "priority": "Low",
        "status": "Research"
    },
    {
        "name": "Ancient Future",
        "address": "2903 College Ave",
        "city": "Berkeley",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Global spiritual artifacts, books, wellness products. Nomadic horizon-shifting vibe supports consignment for cacao in settings that evoke impermanence.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "Shambhala Booksellers",
        "address": "2482 Telegraph Ave",
        "city": "Berkeley",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Buddhist and spiritual bookstore with meditation supplies, incense, and ritual items. Community-oriented with classes. Good fit for ceremonial cacao.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "The Berkeley Alembic",
        "address": "2820 7th St",
        "city": "Berkeley",
        "state": "CA",
        "type": "Wellness Center",
        "notes": "Yoga and meditation center with community events. May have retail section or partner with local vendors. Check if they carry wellness products.",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "The Berkeley Herbal Center",
        "address": "1250 Addison St, Suite G",
        "city": "Berkeley",
        "state": "CA",
        "type": "Health Food Store",
        "website": "https://www.berkeleyherbalcenter.org/",
        "notes": "Dedicated to educating individuals in herbal medicine and providing comprehensive herbal health services. Offers herbal consultations and may have retail products. Check if they have a storefront or retail section for herbal products.",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "Feathered Outlaw",
        "address": "1506 Webster Street",
        "city": "Alameda",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(510) 239-4593",
        "email": "featheredoutlaw@gmail.com",
        "notes": "Metaphysical/spiritual shop in Alameda. Check for specific offerings and hours.",
        "priority": "Medium",
        "status": "Manager Follow-up",
        "contact_date": "2025-11-07",
        "contact_method": "In-person",
        "follow_up_date": "2025-11-12",
        "contact_person": "Amber",
        "owner_name": "Marie",
        "sales_notes": "Spoke with Amber; owner Marie was out. Amber will pass along our card. Follow up next Wednesday."
    },
    # ========================================================================
    # Note: I-5 Route (Central California) shops removed - taking Highway 1 instead
    # ========================================================================
    # COASTAL CALIFORNIA (Highway 1 Route: Santa Cruz, Monterey, Big Sur, SLO, Santa Barbara, Ventura)
    # ========================================================================
    {
        "name": "Moon Kissed",
        "address": "1360 Pacific Ave",
        "city": "Santa Cruz",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(831) 423-5477",
        "website": "https://www.serpents-kiss.com/",
        "email": "info@moonkissed.biz",
        "notes": "Magickal Arts Shop offering authentic, hand-crafted ritual and healing tools, crystals, gemstones, magical jewelry, talismans, spiritual statues, and herbal supplies. Open Wed-Mon 11am-7pm, closed Tuesdays. Sister store: Moonstone Metaphysical in Los Gatos.",
        "priority": "High",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    {
        "name": "World of Stones and Mystics",
        "address": "835 Front St",
        "city": "Santa Cruz",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "High-quality selection of crystals, minerals, polished gems, and metaphysical products. Located in downtown Santa Cruz.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "Air & Fire, A Mystical Bazaar",
        "address": "13136 Highway 9",
        "city": "Boulder Creek",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(831) 338-7567",
        "website": "https://www.airandfire.com/",
        "email": "info@airandfire.com",
        "notes": "Handcrafted natural products with essential oils, soaps, magical oils, candles, incense, mists, crystals, stones, ritual tools, books, tarot decks. Open Tue-Sun 11am-6:30pm, Mon 11am-4pm. Near Santa Cruz.",
        "priority": "Medium",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Contact form",
        "sales_notes": ""
    },
    {
        "name": "Mountain Spirit",
        "address": "6299 Highway 9",
        "city": "Felton",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(831) 335-7700",
        "website": "https://mountainspiritstore.com/",
        "notes": "Metaphysical rock shop specializing in raw and polished gems and minerals from around the world, jewelry, beads, books, candles, statues, oils, incense, cards, journals, local art, and classes. Near Santa Cruz in redwood forest.",
        "priority": "Medium",
        "status": "Research"
    },
    {
        "name": "The Mindshop (Gifts from the Heart)",
        "address": "522 Central Ave",
        "city": "Pacific Grove",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(831) 372-2971",
        "website": "https://www.centerforspiritualawakening.org/themindshop.html",
        "email": "themindshop.csa@gmail.com",
        "notes": "Metaphysical shop offering crystals, gemstones, candles, incense, metaphysical books, tarot/oracle cards, handmade jewelry, cards, chimes, and garden decor. Peaceful atmosphere. Part of Center for Spiritual Awakening. Open Tue-Sun 12pm-5pm, closed Mondays.",
        "priority": "Medium",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    {
        "name": "Apotheca",
        "address": "9 E Gabilan St",
        "city": "Salinas",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(831) 783-5852",
        "website": "https://shopapotheca.com/",
        "instagram": "https://www.instagram.com/apotheca.dot/",
        "notes": "Apothecary shop providing 'medicine for the soul.' Specializing in handmade, natural, and made in USA products. Offers crystals, candles, jewelry, books, sage, palo santo, tarot and oracle decks. Located in Oldtown Salinas.",
        "priority": "Medium",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Instagram",
        "sales_notes": ""
    },
    {
        "name": "Untamed Fire",
        "address": "490 Orange Ave, Unit D",
        "city": "Sand City",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(831) 582-1724",
        "website": "https://www.untamedfire.net/",
        "email": "sales@untamedfire.net",
        "notes": "Female-owned metaphysical shop offering hand-made metaphysically charged items, crystals, bracelets, journals, cleansing products. Owner Lynnette Smick runs Fiery Crone Medicinals line. Focus on natural, holistic ingredients. Community-focused with positive energy. Near Monterey.",
        "priority": "High",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    {
        "name": "Esalen Institute Gift Shop",
        "address": "55000 CA-1",
        "city": "Big Sur",
        "state": "CA",
        "type": "Wellness Center",
        "website": "https://www.esalen.org/",
        "notes": "Renowned holistic retreat center offering meditation, yoga, and personal growth workshops. Has a gift shop that may carry wellness products. Check if they sell ceremonial cacao or would be interested. Highway 1 closures may affect access - verify road conditions before visiting.",
        "priority": "Low",
        "status": "Research"
    },
    {
        "name": "Crystal Garden",
        "address": "779 Higuera St",
        "city": "San Luis Obispo",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Metaphysical shop in downtown SLO offering crystals, minerals, spiritual items, books, and ritual supplies. College town with active spiritual community.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "EarthTones Gifts, Gallery & Center for Healing",
        "address": "790 Pine St",
        "city": "Paso Robles",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(805) 238-4413",
        "email": "earthtoneswb@gmail.com",
        "notes": "Gifts, gallery, and healing center. Wine country area with wellness-oriented visitors. Check for specific offerings and hours.",
        "priority": "Medium",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    {
        "name": "Lumin Earth Apothecary",
        "address": "875 Main St, Suite C",
        "city": "Morro Bay",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(805) 225-1466",
        "email": "luminearthapothecary@gmail.com",
        "notes": "Apothecary shop in coastal tourist town. Check for specific offerings and hours.",
        "priority": "Medium",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    {
        "name": "The Natural Toolbox",
        "address": "333 5 Cities Dr, Space 127",
        "city": "Pismo Beach",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "email": "roxi@thenaturaltoolbox.com",
        "instagram": "https://www.facebook.com/thenaturaltoolbox/",
        "notes": "Natural products shop. Located next to Jockey. Check for specific offerings and hours.",
        "priority": "Medium",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    {
        "name": "Witchy Wanderland",
        "address": "705 E Main St, Suite 205",
        "city": "Santa Maria",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(805) 668-4989",
        "email": "Wildflowerhaven888@gmail.com",
        "notes": "Located at Wildflower Haven building. Check for specific offerings and hours.",
        "priority": "Medium",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    {
        "name": "Crystal Rainbow",
        "address": "1006 State St",
        "city": "Santa Barbara",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "notes": "Metaphysical shop on State Street offering crystals, gemstones, spiritual books, incense, candles, and ritual supplies. Upscale coastal city with wellness-oriented demographics.",
        "priority": "High",
        "status": "Research"
    },
    {
        "name": "The Mystic Merchant",
        "address": "1638 Copenhagen Dr",
        "city": "Solvang",
        "state": "CA",
        "type": "Metaphysical/Spiritual",
        "phone": "(805) 693-1424",
        "email": "mysticmerchanstaff@gmail.com",
        "instagram": "https://www.facebook.com/profile.php?id=100063739172721",
        "notes": "Metaphysical shop in Solvang (Danish-themed tourist town). Check for specific offerings and hours.",
        "priority": "Medium",
        "status": "Contacted",
        "contact_date": "2025-11-05",
        "contact_method": "Email",
        "sales_notes": ""
    },
    # ========================================================================
    # SOUTHERN CALIFORNIA (Los Angeles Area)
    # ========================================================================
    # ========================================================================
    # DESERT REGION (Palm Springs, Indio, Slab City, Blythe)
    # ========================================================================
    # ========================================================================
    # ARIZONA (Kingman, Lake Havasu, Parker, Quartzsite)
    # ========================================================================
    {
        "name": "Spiritstone Gems Market",
        "address": "1210 W Main St",
        "city": "Quartzsite",
        "state": "AZ",
        "type": "Metaphysical/Spiritual",
        "phone": "(928) 927-6361",
        "notes": "Permanent gem and mineral shop offering gems, minerals, crystals, and metaphysical products. Open daily 10am-6pm. Year-round operation (not just during gem shows).",
        "priority": "High",
        "status": "Research"
    },
]

def get_google_sheets_client():
    """Authenticate and return Google Sheets client"""
    creds_path = Path(__file__).parent / "google_credentials.json"
    
    if not creds_path.exists():
        raise FileNotFoundError(
            f"Google credentials not found at {creds_path}. "
            "Please add google_credentials.json with service account credentials."
        )
    
    creds = Credentials.from_service_account_file(
        str(creds_path),
        scopes=SCOPES
    )
    
    client = gspread.authorize(creds)
    return client

def create_shop_list_sheet(client, sheet_name="Hit List"):
    """Create or get shop list worksheet"""
    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
    except Exception as e:
        raise Exception(f"Could not access spreadsheet. Make sure it's shared with {SERVICE_ACCOUNT_EMAIL}. Error: {e}")
    
    # Try to get existing worksheet
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        print(f"Found existing worksheet: {sheet_name}")
    except gspread.WorksheetNotFound:
        # Create new worksheet
        worksheet = spreadsheet.add_worksheet(
            title=sheet_name,
            rows=100,
            cols=14
        )
        print(f"Created new worksheet: {sheet_name}")
    
    return worksheet

def ensure_dapp_remarks_sheet(client):
    """Ensure the DApp remarks worksheet exists with headers"""
    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
    except Exception as e:
        raise Exception(f"Could not access spreadsheet. Make sure it's shared with {SERVICE_ACCOUNT_EMAIL}. Error: {e}")

    headers = [
        "Submission ID",
        "Shop Name",
        "Status",
        "Remarks",
        "Submitted By",
        "Submitted At",
        "Processed",
        "Processed At"
    ]

    try:
        worksheet = spreadsheet.worksheet(DAPP_REMARKS_SHEET)
        print(f"Found existing worksheet: {DAPP_REMARKS_SHEET}")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=DAPP_REMARKS_SHEET,
            rows=1000,
            cols=len(headers)
        )
        print(f"Created new worksheet: {DAPP_REMARKS_SHEET}")

    existing_headers = worksheet.row_values(1)
    if existing_headers != headers:
        worksheet.clear()
        worksheet.append_row(headers)
        print(f"Initialized headers for {DAPP_REMARKS_SHEET}")

    return worksheet

def delete_worksheet(client, sheet_name):
    """Delete a worksheet from the spreadsheet"""
    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            spreadsheet.del_worksheet(worksheet)
            print(f"✅ Deleted worksheet: {sheet_name}")
            return True
        except gspread.WorksheetNotFound:
            print(f"⚠️  Worksheet '{sheet_name}' not found - may already be deleted")
            return False
    except Exception as e:
        print(f"❌ Error deleting worksheet '{sheet_name}': {e}")
        return False

def create_itinerary_sheet(client, shops):
    """Create a high-level itinerary sheet with cities organized by route"""
    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
    except Exception as e:
        raise Exception(f"Could not access spreadsheet. Make sure it's shared with {SERVICE_ACCOUNT_EMAIL}. Error: {e}")
    
    sheet_name = "Itinerary"
    
    # Try to get existing worksheet or create new
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        print(f"Found existing worksheet: {sheet_name}")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=sheet_name,
            rows=100,
            cols=7
        )
        print(f"Created new worksheet: {sheet_name}")
    
    # Headers
    headers = [
        "Region/Route",
        "City",
        "State",
        "# of Shops",
        "High Priority Shops",
        "Shop Types",
        "Notes"
    ]
    
    # Organize cities by region
    region_cities = {}
    
    # Define route segments and their order
    route_segments = {
        "Bay Area - San Francisco": ["San Francisco"],
        "Bay Area - South Bay": ["Mountain View", "Palo Alto", "San Jose", "Gilroy"],
        "Bay Area - East Bay": ["Fremont", "Newark", "Hayward", "Castro Valley", "Oakland", "Emeryville", "Alameda", "Berkeley"],
        "Coastal California (Hwy 1)": ["Santa Cruz", "Salinas", "Monterey", "Big Sur", "San Luis Obispo", "Paso Robles", "Morro Bay", "Santa Barbara", "Ventura"],
        "Southern California": ["Los Angeles"],
        "Desert Region": ["Palm Springs", "Indio", "Niland", "Blythe", "Needles"],
        "Arizona": ["Kingman", "Lake Havasu City", "Parker", "Quartzsite"]
    }
    
    # Count shops by city and collect info
    city_data = {}
    for shop in shops:
        # Skip existing partners and rejected for itinerary count
        if shop.get("status") in ["Partnered", "Rejected"]:
            continue
            
        city = shop.get("city", "")
        state = shop.get("state", "")
        city_key = f"{city}, {state}"
        
        if city_key not in city_data:
            city_data[city_key] = {
                "city": city,
                "state": state,
                "count": 0,
                "high_priority": 0,
                "types": set(),
                "notes": [],
                "needs_research": False
            }
        
        # Check if this is a research-needed shop
        if "[Research Needed]" in shop.get("name", ""):
            city_data[city_key]["needs_research"] = True
            city_data[city_key]["notes"].append("Research needed")
        else:
            city_data[city_key]["count"] += 1
            if shop.get("priority") == "High":
                city_data[city_key]["high_priority"] += 1
            if shop.get("type"):
                city_data[city_key]["types"].add(shop.get("type"))
    
    # Build itinerary rows organized by route segment
    rows = []
    for segment_name, cities_in_segment in route_segments.items():
        segment_added = False
        for city in cities_in_segment:
            # Find matching city data
            found = False
            for city_key, data in city_data.items():
                if data["city"].lower() == city.lower():
                    shop_types = ", ".join(sorted(data["types"])) if data["types"] else ("Research needed" if data["needs_research"] else "Various")
                    notes = "; ".join(set(data["notes"])) if data["notes"] else ""
                    
                    rows.append([
                        segment_name if not segment_added else "",  # Only show region once per segment
                        data["city"],
                        data["state"],
                        data["count"] if data["count"] > 0 else "Research",
                        data["high_priority"],
                        shop_types,
                        notes
                    ])
                    segment_added = True
                    found = True
                    break
            
            # If city not found in shop data but is in route, add it anyway
            if not found:
                # Try to determine state from route segments
                state = "CA"  # Default to CA
                if city in ["Kingman", "Lake Havasu City", "Parker", "Quartzsite"]:
                    state = "AZ"
                
                rows.append([
                    segment_name if not segment_added else "",
                    city,
                    state,
                    "Research",
                    0,
                    "Research needed",
                    "City on route - research shops"
                ])
                segment_added = True
    
    # Clear and update the sheet
    try:
        worksheet.clear()
        worksheet.append_row(headers)
        
        if rows:
            worksheet.append_rows(rows)
            print(f"✅ Added {len(rows)} cities to itinerary")
        
        # Format headers
        worksheet.format('A1:G1', {
            'textFormat': {'bold': True},
            'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
        })
        
        print(f"📋 Itinerary sheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={worksheet.id}")
        
    except Exception as e:
        print(f"Error updating itinerary sheet: {e}")
    
    return worksheet

def geocode_address(address, city, state):
    """
    Geocode an address using Google Geocoding API (free tier via Nominatim as fallback)
    Returns (latitude, longitude) or (None, None) if geocoding fails
    """
    # Build full address string
    full_address = f"{address}, {city}, {state}"
    
    # Try Nominatim (OpenStreetMap) - free and no API key needed
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": full_address,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "MarketResearchBot/1.0"  # Required by Nominatim
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            print(f"  ✓ Geocoded: {full_address} → ({lat}, {lon})")
            return lat, lon
    except Exception as e:
        print(f"  ⚠ Geocoding failed for {full_address}: {e}")
    
    return None, None

def add_shops_to_sheet(worksheet, shops):
    """Add shops to Google Sheet with updated column order"""
    # Headers - matching user's column order, with Latitude and Longitude added
    headers = [
        "Shop Name",
        "Status",
        "Priority",
        "Address",
        "City",
        "State",
        "Shop Type",
        "Phone",
        "Website",
        "Email",
        "Instagram",
        "Notes",
        "Contact Date",
        "Contact Method",
        "Follow Up Date",
        "Contact Person",
        "Owner Name",
        "Referral",
        "Product Interest",
        "Follow Up Event Link",
        "Visit Date",
        "Outcome",
        "Sales Process Notes",
        "Latitude",
        "Longitude"
    ]
    
    # Get existing data to preserve any manual edits and existing lat/lng
    existing_lat_lng = {}  # Map shop name to (lat, lng)
    existing_status = {}
    existing_follow_up_links = {}
    try:
        existing_data = worksheet.get_all_values()
        if existing_data and len(existing_data) > 1:
            print(f"Found {len(existing_data) - 1} existing rows (preserving headers and lat/lng)")
            
            # Find column indices for lat/lng in existing data
            existing_headers = existing_data[0] if existing_data else []
            lat_col_idx = None
            lng_col_idx = None
            name_col_idx = None
            status_col_idx = None
            follow_up_link_idx = None
            
            for idx, header in enumerate(existing_headers):
                if header.lower() == "latitude":
                    lat_col_idx = idx
                elif header.lower() == "longitude":
                    lng_col_idx = idx
                elif header.lower() == "shop name":
                    name_col_idx = idx
                elif header.lower() == "status":
                    status_col_idx = idx
                elif header.lower() == "follow up event link":
                    follow_up_link_idx = idx
            
            # Extract existing lat/lng values
            if name_col_idx is not None and lat_col_idx is not None and lng_col_idx is not None:
                for row in existing_data[1:]:
                    if len(row) > max(name_col_idx, lat_col_idx, lng_col_idx):
                        shop_name = row[name_col_idx] if name_col_idx < len(row) else ""
                        lat_str = row[lat_col_idx] if lat_col_idx < len(row) else ""
                        lng_str = row[lng_col_idx] if lng_col_idx < len(row) else ""
                        
                        if shop_name and lat_str and lng_str:
                            try:
                                lat = float(lat_str)
                                lng = float(lng_str)
                                existing_lat_lng[shop_name] = (lat, lng)
                            except ValueError:
                                pass
            
            # Preserve existing statuses
            if name_col_idx is not None and status_col_idx is not None:
                for row in existing_data[1:]:
                    if len(row) > max(name_col_idx, status_col_idx):
                        shop_name = row[name_col_idx]
                        status_value = row[status_col_idx]
                        if shop_name and status_value:
                            existing_status[shop_name] = status_value

            # Preserve existing follow-up event links
            if name_col_idx is not None and follow_up_link_idx is not None:
                for row in existing_data[1:]:
                    if len(row) > max(name_col_idx, follow_up_link_idx):
                        shop_name = row[name_col_idx]
                        event_link = row[follow_up_link_idx]
                        if shop_name and event_link:
                            existing_follow_up_links[shop_name] = event_link
            
            # Update headers if they exist
            if existing_headers != headers:
                # Calculate range for headers (now includes lat/lng)
                num_cols = len(headers)
                if num_cols <= 26:
                    end_col = chr(64 + num_cols)
                else:
                    first_letter = chr(64 + ((num_cols - 1) // 26))
                    second_letter = chr(65 + ((num_cols - 1) % 26))
                    end_col = first_letter + second_letter
                worksheet.update(f'A1:{end_col}1', [headers])
                print("Updated headers to match new column order (including Latitude/Longitude)")
        else:
            # No existing data, add headers
        worksheet.append_row(headers)
            print("Added headers (including Latitude/Longitude)")
    except Exception as e:
        print(f"Warning: Could not read existing data: {e}")
        # Try to add headers if they don't exist
        try:
                worksheet.append_row(headers)
        except:
            pass
    
    # Prepare all rows at once - matching new column order
    print("\n📍 Geocoding addresses (this may take a few minutes)...")
    rows = []
    geocoded_count = 0
    skipped_count = 0
    
    for shop in shops:
        shop_name = shop.get("name", "")
        address = shop.get("address", "")
        city = shop.get("city", "")
        state = shop.get("state", "")
        
        # Check if we already have lat/lng for this shop
        lat, lng = existing_lat_lng.get(shop_name, (None, None))
        
        # If not found, try to geocode
        if lat is None or lng is None:
            if address and city and state:
                lat, lng = geocode_address(address, city, state)
                if lat is not None and lng is not None:
                    geocoded_count += 1
                    # Rate limiting for Nominatim (1 request per second)
                    time.sleep(1)
                else:
                    skipped_count += 1
            else:
                skipped_count += 1
        else:
            skipped_count += 1
        
        existing_status_value = existing_status.get(shop_name, "")
        status_value = existing_status_value or shop.get("status", "Research")

        follow_up_event_link = shop.get("follow_up_event_link", "")
        if not follow_up_event_link:
            follow_up_event_link = existing_follow_up_links.get(shop_name, "")

        row = [
            shop_name,
            status_value,
            shop.get("priority", ""),
            address,
            city,
            state,
            shop.get("type", ""),
            shop.get("phone", ""),
            shop.get("website", ""),
            shop.get("email", ""),
            shop.get("instagram", ""),
            shop.get("notes", ""),
            shop.get("contact_date", ""),
            shop.get("contact_method", ""),
            shop.get("follow_up_date", ""),
            shop.get("contact_person", ""),
            shop.get("owner_name", ""),
            shop.get("referral", ""),
            shop.get("product_interest", ""),
            follow_up_event_link,
            shop.get("visit_date", ""),
            shop.get("outcome", ""),
            shop.get("sales_notes", ""),
            str(lat) if lat is not None else "",
            str(lng) if lng is not None else "",
        ]
        rows.append(row)
    
    print(f"\n✅ Geocoding complete: {geocoded_count} new addresses geocoded, {skipped_count} skipped (already had coordinates or missing address)")
    
    # Replace all data (headers + data rows) using batch_update to avoid duplicates
    try:
        # Get current number of rows to determine range
        all_values = worksheet.get_all_values()
        existing_row_count = len(all_values)
        
        # Build complete data including headers
        all_data = [headers] + rows
        
        # Calculate range needed (now includes lat/lng columns)
        num_cols = len(headers)
        num_rows = len(all_data)
        
        # Use batch_update to replace entire range
        # For columns beyond Z, use column notation like AA, AB, etc.
        if num_cols <= 26:
            end_col = chr(64 + num_cols)
        else:
            # Handle columns beyond Z (AA, AB, etc.)
            first_letter = chr(64 + ((num_cols - 1) // 26))
            second_letter = chr(65 + ((num_cols - 1) % 26))
            end_col = first_letter + second_letter
        
        range_name = f'A1:{end_col}{num_rows}'
        worksheet.batch_update([{
            'range': range_name,
            'values': all_data
        }])
        
        # If we had more rows before, clear the extra ones
        if existing_row_count > num_rows:
            try:
                worksheet.delete_rows(num_rows + 1, existing_row_count)
            except:
                pass  # If delete fails, that's okay - the data is already updated
        
        print(f"✅ Updated worksheet with {len(rows)} shops")
        except Exception as e:
            print(f"Error in batch update: {e}")
        # Fallback: clear and append
        try:
            worksheet.clear()
            worksheet.append_row(headers)
            if rows:
                worksheet.append_rows(rows)
                print(f"✅ Added {len(rows)} shops to worksheet (fallback method)")
                except Exception as e2:
            print(f"Error in fallback update: {e2}")
            raise
    
    print(f"\n📊 Sheet URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={worksheet.id}")

def main():
    """Main execution"""
    print("Generating consolidated Hit List - All shop targets by region...")
    print(f"Target spreadsheet: {SPREADSHEET_ID}")
    
    try:
        # Get Google Sheets client
        client = get_google_sheets_client()
        
        # Delete LA Route sheet if it exists
        print("\n🗑️  Removing LA Route sheet (consolidated into Hit List)...")
        delete_worksheet(client, "LA Route")
        
        # Create or get worksheet
        worksheet = create_shop_list_sheet(client)
        
        # Add shops
        add_shops_to_sheet(worksheet, SHOPS)

        # Ensure DApp remarks sheet exists for inbound submissions
        ensure_dapp_remarks_sheet(client)
        
        # Create itinerary sheet
        print("\n📋 Creating itinerary sheet...")
        create_itinerary_sheet(client, SHOPS)
        
        print("\n✅ Success! Shop list and itinerary updated in Google Sheet")
        print("\n📝 Next Steps:")
        print("1. Research actual shops in each city")
        print("2. Update the Google Sheet with real shop names and addresses")
        print("3. Use the search queries from PARTNER_TARGETING_GUIDE.md")
        print("4. Verify each shop's alignment with our values")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure google_credentials.json exists")
        print(f"2. Verify spreadsheet is shared with {SERVICE_ACCOUNT_EMAIL}")
        print(f"3. Check that spreadsheet ID is correct: {SPREADSHEET_ID}")

if __name__ == "__main__":
    main()

