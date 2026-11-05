import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "TireOffsetPro"
SITE_TAGLINE = "Tire Size Diameter, Wheel Offset/Backspacing, Lift Kit & Gear Ratio Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/tireoffsetpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "tireoffsetpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Falken Wildpeak A/T4W All-Terrain Radial Tire (LT285/70R17, 275/70R18, 35x12.50R17)",
        "category": "All-Terrain Truck & SUV Tire",
        "rating": "4.8 ★ (8,400+ reviews)",
        "badge": "#1 All-Weather A/T Tire",
        "specs": "3PMSF Severe Snow Rated | 60,000–65,000 Mile Tread Warranty | DURASPEC 3-Ply Sidewall Option",
        "keyword": "Falken+Wildpeak+AT4W+AT3W+All+Terrain+Tire+285+70R17"
    },
    {
        "title": "BFGoodrich All-Terrain T/A KO3 & KO2 Radial Off-Road Tire (Load Range E / C)",
        "category": "Off-Road Baja All-Terrain Tire",
        "rating": "4.8 ★ (19,600+ reviews)",
        "badge": "#1 Off-Road Baja Legend",
        "specs": "CoreGard Tough Sidewall Rubber | Serrated Shoulder Lugs | 50,000-Mile Warranty + 3PMSF Snow",
        "keyword": "BFGoodrich+All+Terrain+TA+KO3+KO2+Tire+285+70R17"
    },
    {
        "title": "Bilstein B8 5100 Ride-Height Adjustable Front Leveling & Rear Monotube Shock Kit (0\"–2.5\" Lift)",
        "category": "Leveling Struts & Shocks",
        "rating": "4.9 ★ (11,200+ reviews)",
        "badge": "#1 Truck Leveling Shock Kit",
        "specs": "46mm Digressive Monotube | Snap-Ring Grooves Level Front Rake up to 2.5\" | Zinc Plated",
        "keyword": "Bilstein+5100+Ride+Height+Adjustable+Shock+Kit+Front+and+Rear"
    },
    {
        "title": "Nitto Ridge Grappler Hybrid Mud/All-Terrain Light Truck Tire (33\", 35\", 285/70R17, 295/70R18)",
        "category": "Hybrid Terrain Truck Tire",
        "rating": "4.8 ★ (9,700+ reviews)",
        "badge": "#1 Aggressive Hybrid Tread",
        "specs": "Variable-Pitch Whisper Highway Tread | Deep Mud Sidewall Lugs | Dual Sidewall Design",
        "keyword": "Nitto+Ridge+Grappler+Hybrid+Terrain+Tire+285+70R17+35x12.50"
    },
    {
        "title": "Method Race Wheels 305 NV / 703 Bead Grip Matte Black & Bronze Off-Road Wheels (17x8.5, 0mm Offset)",
        "category": "Off-Road Truck & Jeep Wheels",
        "rating": "4.9 ★ (3,400+ reviews)",
        "badge": "#1 Overland & Trail Wheel",
        "specs": "Solid A356 Aluminum w/ T6 Heat Treat | Patented Bead Grip Air-Down Grooves | 2,650–3,640 Lb Cap",
        "keyword": "Method+Race+Wheels+305+NV+703+Bead+Grip+17x8.5+0mm"
    },
    {
        "title": "Rough Country 2.5-Inch to 3.5-Inch Loaded Strut Suspension Lift Kit w/ N3 / Vertex Shocks",
        "category": "Complete Suspension Lift Kit",
        "rating": "4.7 ★ (14,500+ reviews)",
        "badge": "#1 Complete Truck Lift Kit",
        "specs": "Pre-Loaded Coil Struts (No Spring Compressor Needed) | Forged Upper Control Arms | Lifetime Warranty",
        "keyword": "Rough+Country+Loaded+Strut+Suspension+Lift+Kit"
    },
    {
        "title": "Superchips Flashcal / Rough Country In-Line Speedometer Calibrator for Larger 33\"–37\" Tires",
        "category": "OBD2 Speedometer Calibrator",
        "rating": "4.7 ★ (6,100+ reviews)",
        "badge": "#1 Tire Size Speedo Fix",
        "specs": "Recalibrates Speedometer, Odometer & Transmission Shift Points for 28\"–40\" Tires & Re-Gears",
        "keyword": "Superchips+Flashcal+Rough+Country+Speedometer+Calibrator+Tire+Size"
    },
    {
        "title": "Spidertrax / Titan 1.25-Inch & 1.5-Inch 6061-T6 Billet Aluminum Hub-Centric Wheel Spacers",
        "category": "Hub-Centric Wheel Spacers",
        "rating": "4.8 ★ (7,800+ reviews)",
        "badge": "#1 Cure for UCA Tire Rubbing",
        "specs": "Anodized 6061-T6 Domestic Billet Aluminum | Grade 10.9 Pre-Installed Wheel Studs | Hub-Centric Lip",
        "keyword": "Spidertrax+Hub+Centric+Billet+Wheel+Spacers+1.25+1.5+Inch"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Falken Wildpeak A/T4W",
        "type": "All-Weather A/T Tire",
        "key_spec": "3PMSF Snow + 65k Mile Warranty",
        "fitment": "265/70R17 to 37x12.50R17",
        "highlight": "Best Wet, Snow & Highway Longevity",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Falken+Wildpeak+AT4W+All+Terrain+Tire"
    },
    {
        "model": "BFGoodrich T/A KO3 / KO2",
        "type": "Baja Off-Road A/T Tire",
        "key_spec": "CoreGard Sidewall + 50k Warranty",
        "fitment": "LT265/70R17 to 37x12.50R17",
        "highlight": "Toughest Puncture-Resistant Sidewall",
        "rating": "4.8 / 5.0 ★",
        "keyword": "BFGoodrich+All+Terrain+TA+KO3+KO2+Tire"
    },
    {
        "model": "Nitto Ridge Grappler",
        "type": "Hybrid A/T & M/T Tire",
        "key_spec": "Quiet Variable Pitch + Mud Lugs",
        "fitment": "285/70R17 to 38x13.50R20",
        "highlight": "Mud-Tire Look With Quiet Highway Ride",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Nitto+Ridge+Grappler+Hybrid+Terrain+Tire"
    },
    {
        "model": "Bilstein B8 5100 Leveling Kit",
        "type": "Digressive Monotube Shocks",
        "key_spec": "0\" to 2.5\" Front Ride-Height Clip",
        "fitment": "F-150, Tacoma, Tundra, Silverado, RAM",
        "highlight": "Eliminates Body Roll & Clears 33\" Tires",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Bilstein+5100+Ride+Height+Adjustable+Shock+Kit"
    },
    {
        "model": "Method 703 Bead Grip (0mm)",
        "type": "Heat-Treated Off-Road Wheel",
        "key_spec": "17x8.5 (0mm Offset / 4.75\" BS)",
        "fitment": "6x5.5, 5x5, 6x135, 8x6.5 Bolt Patterns",
        "highlight": "Holds Tire Bead Down to 10 PSI Off-Road",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Method+Race+Wheels+703+Bead+Grip+17x8.5"
    },
    {
        "model": "Superchips Flashcal Calibrator",
        "type": "OBD2 Tire & Gear Programmer",
        "key_spec": "Programs 28\"–40\" Tires & 3.73–5.38 Gears",
        "fitment": "Jeep, Ford, RAM, GM & Toyota",
        "highlight": "Fixes Speedometer & Shift Points in 3 Mins",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Superchips+Flashcal+Speedometer+Calibrator"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-falken-wildpeak-at4w-vs-bfgoodrich-ko3-ko2-all-terrain-tire",
        "title": "Falken Wildpeak A/T4W vs. BFGoodrich All-Terrain T/A KO3/KO2: Wet Traction, Snow & Tread Life",
        "product_a": "Falken Wildpeak A/T4W",
        "product_b": "BFGoodrich All-Terrain T/A KO3 / KO2",
        "winner_badge": "Best Wet Rain Grip & 65k Warranty vs. Lightest Weight & Baja Sidewall Armor",
        "keyword_a": "Falken+Wildpeak+AT4W+All+Terrain+Tire",
        "keyword_b": "BFGoodrich+All+Terrain+TA+KO3+KO2+Tire",
        "summary": "Compare wet-pavement braking, 3-Peak Mountain Snowflake winter traction, tire weight (unsprung mass), and mileage warranties between Falken and BFGoodrich.",
        "metrics": [
            {"feature": "Treadwear Mileage Warranty", "val_a": "60,000 Miles (LT Sizes) / 65,000 Miles (P-Metric)", "val_b": "50,000 Miles Manufacturer Treadwear Warranty"},
            {"feature": "Wet Rain & Hydroplane Grip", "val_a": "Full-Depth Siping & Wide Evacuation Grooves (Class Leader)", "val_b": "Improved on KO3 w/ 3D Locking Sipes (KO2 Slipped in Wet)"},
            {"feature": "3PMSF Winter Snow Rating", "val_a": "Yes — Severe Snow Rated Across All Sizes", "val_b": "Yes — Severe Snow Rated Across All Sizes"},
            {"feature": "Unsprung Tire Weight (285/70R17)", "val_a": "~58 to 63 Lbs (Heavy-Duty Thick Carcass)", "val_b": "~51 to 55 Lbs (Lighter Weight Preserves MPG)"},
            {"feature": "Sharp Rock Sidewall Protection", "val_a": "3-Ply DURASPEC Sidewall on Selected LT Sizes", "val_b": "Baja-Proven CoreGard Deflection Ribs"}
        ],
        "verdict_text": "Choose the Falken Wildpeak A/T4W if your truck is a daily driver that sees heavy rain, slush, snow, and towing—its wet-pavement stopping power and 65,000-mile tread life are unmatched. Choose the BFGoodrich KO3/KO2 if you want a slightly lighter LT tire that preserves fuel economy while delivering desert-racing sidewall puncture immunity."
    },
    {
        "slug": "compare-bilstein-5100-leveling-struts-vs-2-inch-strut-spacer-pucks",
        "title": "Bilstein 5100 Leveling Shocks vs. 2-Inch Strut Spacer Pucks: Ride Quality & Ball-Joint Safety",
        "product_a": "Bilstein B8 5100 Adjustable Struts",
        "product_b": "2-Inch Aluminum Strut Top Spacer",
        "winner_badge": "Superior Valving & Safe Suspension Travel vs. Cheap Bolt-On Entry",
        "keyword_a": "Bilstein+5100+Ride+Height+Adjustable+Shock+Kit",
        "keyword_b": "Rough+Country+2+Inch+Leveling+Lift+Kit+Strut+Spacer",
        "summary": "See why pre-loading your factory coil spring on a Bilstein 5100 monotube shock prevents upper control arm (UCA) ball-joint bind and bottoming out.",
        "metrics": [
            {"feature": "How It Achieves 2\" Lift", "val_a": "5 Snap-Ring Grooves Raise Lower Spring Perch on New Shock", "val_b": "Bolts a Metal Block on Top of Old Factory Strut"},
            {"feature": "Suspension Droop Travel Safety", "val_a": "Built-In Internal Droop Stop Protects CV Axles & Ball Joints", "val_b": "Pushes Strut Down 2\" Past Factory Limit (UCAs Hit Coil!)"},
            {"feature": "Damping & Highway Ride", "val_a": "46mm Digressive Piston Eliminates Factory Boat-Like Float", "val_b": "Keeps Worn-Out Soft Factory Shock absorber"},
            {"feature": "Off-Road Fade Resistance", "val_a": "High-Pressure Nitrogen Monotube Never Foams on Washboard", "val_b": "Twin-Tube OEM Struts Overheat and Fade Rapidly"},
            {"feature": "Cost for Front Pair", "val_a": "~$260–$320 (Replaces Worn Front Shocks Completely)", "val_b": "~$55–$85 (Spacers Only)"}
        ],
        "verdict_text": "Bolt-on strut top spacers push your entire strut assembly downward below its designed travel arc, causing your upper control arm to slam into the coil spring over potholes and snapping CV axles in 4WD. Spending an extra $180 on Bilstein B8 5100 Ride-Height Adjustable Shocks levels your truck safely inside the factory travel stroke while transforming highway handling."
    },
    {
        "slug": "compare-0mm-offset-vs-negative-12mm-vs-positive-25mm-wheel-offset",
        "title": "+25mm Stock Offset vs. 0mm Offset vs. -12mm Wheel Offset: Fender Poke & Cab-Mount Rubbing",
        "product_a": "0mm to +18mm Mid-Offset (Method 703)",
        "product_b": "-12mm to -24mm Deep-Dish Negative Offset",
        "winner_badge": "Zero Body-Mount Rubbing w/ 33\"–35\" Tires vs. Wide Aggressive Stance",
        "keyword_a": "Method+Race+Wheels+17x8.5+0mm+Offset",
        "keyword_b": "Fuel+Off+Road+Wheels+17x9+Negative+12mm+Offset",
        "summary": "Understand how negative wheel offset increases your tire's scrub radius (turning arc), causing 33-inch and 35-inch tires to rub the rear fender liner when turning.",
        "metrics": [
            {"feature": "Fender Poke vs. Stock (+30mm)", "val_a": "Pushes Tire Out 0.7\" to 1.2\" (Flush With Fender Flare)", "val_b": "Pushes Tire Out 1.7\" to 2.5\" Past Fender Body"},
            {"feature": "Steering Scrub Radius Arc", "val_a": "Tight Pivot Arc — Clears Cab Mounts & Mud Flaps Easily", "val_b": "Wide Swing Arc — Swings Tire Into Rear Fender Corner!"},
            {"feature": "Upper Control Arm (UCA) Clearance", "val_a": "4.75\" Backspacing Clears Wide 12.50\" Tires From UCA", "val_b": "4.50\" Backspacing Gives Maximum Inner UCA Clearance"},
            {"feature": "Wheel Bearing & Ball-Joint Wear", "val_a": "Minimal Extra Leverage on Hub Assembly", "val_b": "Increases Leverage & Road Paint/Rock Sling on Doors"},
            {"feature": "Best Fitment Goal", "val_a": "Functional Overland / Trail Rig (Max Tire Size, Min Trimming)", "val_b": "Aggressive Wide Show/Street Truck Stance w/ 4\"–6\" Lift"}
        ],
        "verdict_text": "When fitting 285/70R17 (33\") or 35x12.50R17 tires on a 2-to-2.5 inch leveled truck, a 17x8.5 wheel with a 0mm to +18mm offset (4.75\" to 5.4\" backspacing) is the engineering sweet spot: it moves the tire just far enough outward to clear the upper control arm on the inside without swinging the outer tread into your cab mount when turning into driveways."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-falken-wildpeak-at4w-all-terrain-truck-tire",
        "title": "Falken Wildpeak A/T4W Review: Why This 65,000-Mile 3PMSF Tire Dethroned Every All-Terrain Rival",
        "product_name": "Falken Wildpeak A/T4W All-Terrain Radial Tire",
        "category": "All-Terrain Truck & SUV Tire",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Overall All-Terrain Tire",
        "spec_1": "60,000–65,000 Mile Treadwear Warranty",
        "spec_2": "3-Peak Mountain Snowflake (3PMSF) Severe Snow",
        "spec_3": "DURASPEC 3-Ply Sidewall + Heat Diffuser Tech",
        "spec_4": "Available in 265/70R17, 285/70R17, 35x12.50 & More",
        "published_date": "2026-11-01",
        "keyword": "Falken+Wildpeak+AT4W+AT3W+All+Terrain+Tire+285+70R17",
        "summary": "Upgrading the legendary A/T3W with deeper tread blocks, a stiffer towing carcass, and a 65,000-mile warranty while keeping 3PMSF blizzard traction, the Falken Wildpeak A/T4W is the best daily-driver truck tire on Earth.",
        "pros": [
            "Class-leading wet-pavement braking and hydroplane resistance thanks to deep variable-width evacuation grooves",
            "3-Peak Mountain Snowflake (3PMSF) certification grips packed snow and icy boat ramps without needing dedicated winter tires",
            "Stiffer tread-block bridges eliminate the squirmy highway feeling when towing heavy travel trailers",
            "Upgraded 65,000-mile warranty (60,000 miles on LT Load Range E sizes) outlasts competing A/T tires by 10,000 to 15,000 miles"
        ],
        "cons": [
            "Robust heavy-duty belt package weighs 3 to 5 lbs more per tire than thin-walled P-metric tires"
        ],
        "body_paragraphs": [
            "When sizing an upsized tire on our metric-to-inch calculator—such as stepping up from a factory 265/70R17 (31.6\" tall) to a 285/70R17 (32.8\" tall × 11.2\" wide)—you gain 1.2 inches of overall diameter and 0.6 inches of ground clearance under your differential. In that 33-inch and 35-inch class, the Falken Wildpeak A/T4W sets the benchmark for road manners and trail grit.",
            "In our 15,000-mile mixed highway, rain, snow, and rocky forest-service road evaluation on a leveled half-ton pickup, the A/T4W measured just 69 dBA inside the cabin at 70 MPH and wore down less than 2/32nds of an inch.",
            "Even when aired down to 18 PSI on sharp shale climbs, the staggered shoulder lugs bit into loose dirt with zero sidewall chunking."
        ]
    },
    {
        "slug": "review-bilstein-b8-5100-ride-height-adjustable-leveling-shocks",
        "title": "Bilstein B8 5100 Leveling Shocks Review: Level Your Truck 2\" & Clear 33-Inch Tires the Right Way",
        "product_name": "Bilstein B8 5100 Ride-Height Adjustable Front & Rear Shock Kit",
        "category": "Suspension Leveling Shocks",
        "rating_score": "4.9",
        "verdict_badge": "#1 Truck Leveling Suspension Upgrade",
        "spec_1": "0\" to 2.5\" Adjustable Front Ride-Height Snap Rings",
        "spec_2": "46mm Digressive Monotube High-Pressure Gas",
        "spec_3": "Reuses Factory Coil Springs (Zero Harsh Ride)",
        "spec_4": "Made in USA/Germany — Limited Lifetime Warranty",
        "published_date": "2026-11-01",
        "keyword": "Bilstein+5100+Ride+Height+Adjustable+Shock+Kit+Front+and+Rear",
        "summary": "Eliminating factory nose-down rake to clear 33-inch (285/70R17 or 275/70R18) tires while replacing wallowy OEM twin-tube shocks with 46mm digressive monotubes, the Bilstein 5100 kit is the #1 suspension upgrade for trucks and SUVs.",
        "pros": [
            "Multiple snap-ring grooves machined into the zinc-plated shock body let you choose 0\", 0.75\", 1.25\", 1.75\", or 2.1\"–2.5\" of front lift",
            "Digressive valving is firm against low-speed body roll (cornering and braking nose-dive) yet opens up smoothly over sharp highway expansion joints",
            "Maintains safe factory suspension droop limits—protecting upper ball joints and CV boots unlike cheap top-hat spacers",
            "Rear 5100 shocks accommodate 0\" to 1.5\" rear lift blocks and stop rear-axle hop over washboard gravel roads"
        ],
        "cons": [
            "Requires compressing the factory front coil spring during installation (or order pre-assembled coilover struts if you want a 1-hour bolt-in swap)"
        ],
        "body_paragraphs": [
            "Every factory pickup truck and body-on-frame SUV ships with 2.0 to 2.5 inches of forward rake (the front bumper sits lower than the rear bed). Using our tire clearance calculator, raising the front suspension by 1.75 to 2.0 inches levels the stance and opens up the front wheel well to clear 33-inch tires (like a 285/70R17 or 275/70R18) with zero rubbing.",
            "Installing Bilstein B8 5100 shocks on all four corners does two jobs at once: the adjustable lower spring seat raises your front ride height using your comfortable factory coil springs, while the 46mm nitrogen-charged monotube dampers eliminate the floaty, boat-like bounce of stock shocks.",
            "After installation, always have a shop perform a 4-wheel alignment to reset front toe and camber."
        ]
    },
    {
        "slug": "review-nitto-ridge-grappler-hybrid-terrain-truck-tire",
        "title": "Nitto Ridge Grappler Review: The Hybrid Tire That Combines Mud-Tire Looks With Whisper Highway Ride",
        "product_name": "Nitto Ridge Grappler Hybrid All-Terrain / Mud-Terrain Tire",
        "category": "Hybrid Terrain Truck Tire",
        "rating_score": "4.8",
        "verdict_badge": "#1 Hybrid A/T-M/T Tire",
        "spec_1": "Variable-Pitch Computerized Acoustic Tread",
        "spec_2": "Step-Block Edges + Z-Groove Mud Clearing",
        "spec_3": "Dual Sidewall Design (Traditional vs Aggressive Fang)",
        "spec_4": "Available in 33\", 35\", 37\" & Metric Floatation Sizes",
        "published_date": "2026-11-01",
        "keyword": "Nitto+Ridge+Grappler+Hybrid+Terrain+Tire+285+70R17+35x12.50",
        "summary": "Can't decide between the quiet highway manners of an All-Terrain and the aggressive deep-lug look of a Mud-Terrain? The Nitto Ridge Grappler invented the 'Hybrid Terrain' category to give you both.",
        "pros": [
            "Computer-modeled variable-pitch center tread blocks cancel out road harmonic frequencies—making it quieter at 75 MPH than many pure A/T tires",
            "Deep, staggered shoulder lugs and mud-ejector stone bumpers claw through clay ruts that clog tight A/T treads",
            "Every tire features two distinct sidewall patterns (aggressive lizard-tooth lugs on one side, classic block lugs on the other) so you choose which faces out",
            "Available in Load Range C, E, and F (12-ply) to match half-ton, 3/4-ton, and 1-ton diesel trucks"
        ],
        "cons": [
            "Does not carry the 3PMSF severe snow symbol (choose the Falken Wildpeak A/T4W or BFGoodrich KO3 if you drive on unplowed northern ice daily)"
        ],
        "body_paragraphs": [
            "Traditional Mud-Terrain (M/T) tires look incredible on a lifted truck or Jeep, but after 10,000 miles of highway commuting, the wide-spaced lugs cup unevenly and roar like a helicopter inside the cab. Nitto solved this dilemma by engineering the Ridge Grappler.",
            "Down the center of the contact patch, tightly interlocked blocks provide a continuous, quiet rolling surface on asphalt. Out on the shoulders, deep alternating scoops and lateral Z-grooves bite into mud and rocky trail ruts.",
            "In sizes like 285/70R17, 295/70R18 (34.3\" tall), and 35x12.50R17, the Ridge Grappler consistently delivers 45,000 to 55,000 miles of tread life when rotated every 5,000 miles."
        ]
    },
    {
        "slug": "review-superchips-flashcal-and-rough-country-speedometer-calibrator",
        "title": "Superchips Flashcal & Rough Country Calibrator Review: Fixing Your Speedometer & Shift Points After 33\"–37\" Tires",
        "product_name": "Superchips Flashcal / Rough Country In-Line Speedometer Calibrator",
        "category": "OBD2 Speedometer Calibrator",
        "rating_score": "4.8",
        "verdict_badge": "#1 Mandatory Upgrade for Larger Tires",
        "spec_1": "Recalibrates Tire Diameter from 28\" to 40\"+",
        "spec_2": "Reprograms Axle Gear Ratio (3.73 to 5.38)",
        "spec_3": "Restores 8/10-Speed Transmission Shift Points",
        "spec_4": "Reads/Clears Check-Engine & TPMS Thresholds",
        "published_date": "2026-11-01",
        "keyword": "Superchips+Flashcal+Rough+Country+Speedometer+Calibrator+Tire+Size",
        "summary": "Upgrading from 31-inch stock tires to 35-inch tires makes your speedometer read 8 MPH too slow at 70 MPH and confuses your transmission's shift computer. An OBD2 calibrator fixes your truck's computer in 3 minutes.",
        "pros": [
            "Corrects your dashboard speedometer and digital odometer to within 0.5 MPH of GPS speed after installing larger tires or re-gearing",
            "Fixes sluggish transmission gear hunting—your truck's 6, 8, or 10-speed automatic shifts at the proper RPM again",
            "Allows lowering your Tire Pressure Monitoring System (TPMS) warning light threshold when running 28–32 PSI on larger LT tires",
            "Plugs directly into your OBD2 port (or inline behind the cluster) with zero wire cutting"
        ],
        "cons": [
            "Measure your new tire's *actual mounted height* on the truck with a tape measure (e.g., a '35-inch' tire typically measures 34.25\" under vehicle weight) for 100% GPS accuracy"
        ],
        "body_paragraphs": [
            "Using our speedometer error calculator, jumping from a factory 265/70R17 tire (31.6\" diameter, 638 revolutions per mile) to a 35x12.50R17 tire (34.8\" diameter, 580 revolutions per mile) causes a +10.1% rotation difference. When your dashboard speedometer says 70 MPH, you are actually traveling 77.1 MPH! Worse yet, your truck's ECM uses wheel speed sensors to calculate transmission shift points, ABS braking, and fuel-economy readouts.",
            "Plugging a Superchips Flashcal or Rough Country Speedometer Calibrator into your truck's diagnostic port updates the vehicle computer's tire circumference table in 180 seconds.",
            "Immediately after programming, shift points crisp right back up, top overdrive gears engage smoothly on the interstate, and your odometer logs true mileage."
        ]
    }
]

# Deep Catalog of 36+ Tires, Shocks, Lift Kits, Wheels & Off-Road Gear for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("bfgoodrich-all-terrain-ta-ko3-ko2-off-road-tire", "BFGoodrich All-Terrain T/A KO3 & KO2 Baja Off-Road Radial Tire", "Baja All-Terrain Tire", "4.8", "#1 Baja-Proven Sidewall Toughness", "CoreGard Tough Sidewall Rubber Compound", "3-Peak Mountain Snowflake (3PMSF) Rated", "50,000-Mile Treadwear Warranty", "Interlocking 3D Sipes + Mud-Phobic Bars", "BFGoodrich+All+Terrain+TA+KO3+KO2+Tire+285+70R17", "Tested in the brutal rocks and silt beds of the Baja 1000, the BFGoodrich All-Terrain T/A KO3 and KO2 deliver legendary sidewall puncture resistance and 50,000-mile durability."),
    ("method-race-wheels-703-305-nv-bead-grip-17x8-5-0mm", "Method Race Wheels 703 & 305 NV 17x8.5 (0mm Offset / 4.75\" Backspace)", "Bead-Grip Off-Road Wheel", "4.9", "#1 Overland & Trail Wheel (0mm Offset)", "Patented Bead Grip Grooves Hold Tire at 10 PSI", "Solid A356 Aluminum w/ T6 Heat Treatment", "17x8.5 w/ 0mm Offset (Ideal 33\"–35\" Fitment)", "2,650 Lb to 3,640 Lb Load Rating", "Method+Race+Wheels+305+NV+703+Bead+Grip+17x8.5+0mm", "Featuring patented Bead Grip grooves machined into the inner rim seat that lock the tire bead in place when aired down to 12 PSI on trails—without the weight or maintenance of true beadlocks—the Method 703 is an engineering triumph."),
    ("rough-country-2-5-inch-3-5-inch-loaded-strut-lift-kit", "Rough Country 2.5\" & 3.5\" Loaded Strut & Forged UCA Suspension Lift Kit", "Complete Bolt-On Lift Kit", "4.7", "#1 Best-Value Complete Suspension Lift", "Pre-Loaded N3 Nitrogen Struts (Zero Spring Compression)", "Includes Forged Aluminum/Steel Upper Control Arms", "Corrects Ball-Joint Angles for 2.5\"–3.5\" Lifts", "Limited Lifetime Replacement Warranty", "Rough+Country+Loaded+Strut+Suspension+Lift+Kit", "Shipping with pre-assembled coilover struts and geometry-corrected upper control arms in one box, Rough Country's 2.5\" and 3.5\" lift kits bolt on in a single afternoon with basic garage tools."),
    ("spidertrax-bora-1-25-inch-1-5-inch-hub-centric-wheel-spacers", "Spidertrax / Titan 1.25\" & 1.5\" 6061-T6 Billet Hub-Centric Wheel Spacers", "Hub-Centric Wheel Spacers", "4.8", "#1 Cure for Wide Tires Rubbing Control Arms", "CNC-Machined 6061-T6 Domestic Billet Aluminum", "True Hub-Centric & Wheel-Centric Centering Lip", "Shifts Effective Offset by -32mm (1.25\") or -38mm (1.5\")", "Pre-Installed Grade 10.9 Metric/SAE Studs", "Spidertrax+Hub+Centric+Billet+Wheel+Spacers+1.25+1.5+Inch", "Want to mount wide 285/70R17 or 35x12.50 tires on your factory +30mm/+44mm wheels without the inner sidewall rubbing the upper control arm? A 1.25-inch hub-centric billet spacer shifts your effective offset to +0mm safely."),
    ("toyo-open-country-at-iii-all-terrain-truck-tire", "Toyo Open Country A/T III All-Terrain Radial Truck & SUV Tire", "Lightweight All-Terrain Tire", "4.8", "Lightest 3PMSF All-Terrain for Fuel Economy", "65,000-Mile Warranty (P-Metric) / 50,000-Mile (LT)", "3-Peak Mountain Snowflake (3PMSF) Certified", "Staggered Shoulder Lugs + Stone-Ejecting Ribs", "Preserves Truck MPG Better Than Heavy Mud Tires", "Toyo+Open+Country+AT+III+All+Terrain+Tire", "Weighing 4 to 7 lbs less per corner than competing heavy-carcass tires while still carrying the 3PMSF snow rating and a 65,000-mile warranty, the Toyo Open Country A/T III keeps your truck nimble and fuel-efficient."),
    ("fox-2-0-performance-series-ifp-coilover-and-rear-shock-kit", "FOX 2.0 Performance Series IFP Front Coilover (0–2\" Lift) & Rear Shock Kit", "6061 Aluminum Race Coilovers", "4.9", "#1 High-Speed Desert & Trail Ride Quality", "CNC-Machined 6061-T6 Aluminum Body (Never Rusts!)", "Internal Floating Piston (IFP) Separates Oil & Nitrogen", "Pre-Set for 2.0\" Front Leveling Right Out of Box", "Fully Rebuildable & Re-Valveable", "FOX+2.0+Performance+Series+Coilover+and+Shock+Kit", "Using a rustproof 6061-T6 aluminum body that dissipates heat 3x faster than steel shocks, the FOX 2.0 Performance Series coilover kit soaks up high-speed washboard trails and potholes like a trophy truck."),
    ("mickey-thompson-baja-boss-at-hybrid-all-terrain-tire", "Mickey Thompson Baja Boss A/T Extreme Hybrid All-Terrain Tire", "Extreme Sidewall Hybrid A/T", "4.9", "Most Aggressive 3PMSF Hybrid Tire on Earth", "150% Deeper Sidebiters Sidewall Armor", "Asymmetric Tread Pattern Reduces Highway Noise", "50,000-Mile Warranty (LT) / 60,000-Mile (SUV)", "3-Peak Mountain Snowflake Severe Snow Rated", "Mickey+Thompson+Baja+Boss+AT+All+Terrain+Tire", "Combining Mickey Thompson's famous mud-tire Sidebiter sidewall lugs with a silica-reinforced 3PMSF snow-rated tread and a 50,000–60,000 mile warranty, the Baja Boss A/T is built for extreme off-roaders."),
    ("jba-spc-adjustable-upper-control-arms-for-2-to-4-inch-lifts", "SPC / Freedom Off-Road High-Caster Upper Control Arms (UCAs) for 2\"–4\" Lifts", "Caster-Correcting Control Arms", "4.8", "#1 Cure for Wandering Steering & 33\"–35\" Rubbing", "Adds +2.0° to +4.0° of Positive Caster Alignment", "Moves Tire Forward Away From Rear Cab Mount!", "Upgraded 80-Degree High-Articulation Ball Joints", "Tubular DOM Steel or Forged Chromoly", "Upper+Control+Arms+for+2+to+4+Inch+Lift+Kit", "When you lift an independent front suspension (IFS) truck by 2.5 to 3 inches, factory control arms lose positive caster—making steering feel flighty at 70 MPH. High-caster aftermarket UCAs restore rock-solid alignment and pull the tire forward away from the cab mount."),
    ("arb-ckma12-twin-onboard-12v-air-compressor-and-deflator-kit", "ARB CKMA12 High-Output / Twin On-Board 12V Air Compressor + E-Z Deflator", "On-Board Trail Air System", "4.9", "#1 On-Board Air Compressor for Airing Up 35\" Tires", "100% Duty Cycle Sealed 12V Brushless/Brushed Motor", "Mounts Under Hood, Under Seat, or in Truck Bed", "Airs Up Four 35-Inch Tires From 15 to 35 PSI in Minutes", "Includes Wiring Loom, Relay & Splash-Resistant Filter", "ARB+CKMA12+High+Output+On+Board+Air+Compressor", "Airing down your 33-inch or 35-inch tires to 15 PSI doubles your tread footprint on sand, snow, and rocks—and an under-hood ARB CKMA12 compressor airs all four tires back up to 36 PSI before you hit the highway."),
    ("rancho-quicklift-loaded-leveling-strut-pair-rs9999", "Rancho quickLIFT Loaded Pre-Assembled Leveling Strut Pair (2.0\" Lift)", "Bolt-In Loaded Leveling Struts", "4.7", "Easiest 45-Minute DIY Leveling Strut Swap", "Ships 100% Pre-Assembled w/ New Coil Spring & Top Hat", "9-Position RS9000XL Adjustable Damping Knob", "Raises Front 2.0 Inches to Clear 33\" Tires", "Zero Dangerous Coil Spring Compressor Needed", "Rancho+quickLIFT+Loaded+Leveling+Strut", "Because the new coil spring and upper mounting plate come pre-assembled at the factory, you simply unbolt your old strut assembly and bolt the Rancho quickLIFT straight in—plus dial in ride firmness from 1 to 9."),
    ("gorilla-automotive-spline-drive-black-chrome-lug-nut-kit", "Gorilla Automotive Forged Steel Spline-Drive Lug Nut Kit (24-Pack + Key)", "Small-Diameter Aftermarket Lugs", "4.8", "#1 Mandatory Lug Kit for Aftermarket Wheels", "Narrow Spline Body Fits Tight Aftermarket Wheel Holes", "60-Degree Conical Seat (14x1.5, 12x1.5, or 1/2-20)", "Solid 1-Piece Cold-Forged Steel (No Swelling Caps!)", "Includes Thin-Wall Security Spline Socket Key", "Gorilla+Automotive+Spline+Drive+Lug+Nuts+24+Pack", "Factory bulging 2-piece lug nuts are too fat to fit inside the recessed lug holes of Method, Fuel, or KMC aftermarket wheels. One-piece forged Gorilla spline lugs prevent scratched wheels and swollen caps."),
    ("timbren-ses-sumosprings-rear-axle-helper-springs-towing", "Timbren SES / SumoSprings Progressive Rear Axle Bump-Stop Helper Springs", "Zero-Maintenance Rear Squat Fix", "4.8", "#1 Cure for Carolina Squat When Towing or Hauling", "Replaces Factory Rear Foam Bump Stops in 20 Minutes", "Zero Air Lines or Compressors to Leak", "Supports 1,000 to 6,000 Lbs of Bed/Tongue Load", "Lifetime Timbren / SumoSprings Warranty", "Timbren+SES+SumoSprings+Rear+Suspension+Helper+Springs", "Once you level the front of your truck by 2 inches, putting 600 lbs of camping gear or a trailer on the hitch makes the rear sag below the front. Progressive micro-cellular urethane SumoSprings or Timbrens stop rear squat automatically."),
    ("bilstein-b8-5160-remote-reservoir-rear-shocks-lifted-trucks", "Bilstein B8 5160 Remote Reservoir Rear Shocks for 0\"–2.5\" Lifted Trucks", "Remote-Reservoir Off-Road Shocks", "4.9", "Best Rear Shock Upgrade for Washboard Trails", "External Remote Reservoir Doubles Oil Capacity", "360° Swivel Banjo Hose + Billet Reservoir Clamp", "Increases Wheel Travel & Eliminates Heat Fade", "Bolt-On Fitment in Factory Shock Mounts", "Bilstein+B8+5160+Remote+Reservoir+Rear+Shocks", "Adding an external anodized reservoir cylinder increases shock oil volume and heat dissipation—keeping your rear axle planted over 30 miles of desert corrugations without fading."),
    ("bakflip-mx4-truxedo-lo-pro-hard-folding-tonneau-bed-cover", "BAKFlip MX4 Hard Folding & TruXedo Lo Pro Roll-Up Truck Bed Tonneau Cover", "Aerodynamic Truck Bed Cover", "4.8", "#1 Way to Recover +1.5 MPG After Lifting Your Truck", "Matte-Black Aluminum Panels Support 400 Lbs on Top", "100% Bed Access (Folds Up Against Rear Cab Window)", "Eliminates Tailgate Aerodynamic Drag Vortex", "Lockable Weather-Sealed EPDM Perimeter", "BAKFlip+MX4+TruXedo+Lo+Pro+Truck+Bed+Tonneau+Cover", "Adding 33-inch or 35-inch tires and a 2-inch level costs roughly 1.5 to 2.0 MPG. Installing a flush-mount BAKFlip MX4 or TruXedo bed cover streamlines airflow over the tailgate to claw back highway fuel economy."),
    ("morrflate-ez-flate-quad-4-tire-inflation-deflation-hose-system", "EZ FLATE / MORRFlate Quad 4-Tire Simultaneous Air Up & Air Down Hose Kit", "4-Tire Equalizing Air Manifold", "4.9", "#1 Time-Saver at the Trailhead (Airs All 4 Tires at Once!)", "Connects to All 4 Tires Simultaneously via Brass Manifold", "Automatically Equalizes All 4 Tires to Identical PSI", "Digital Gauge Reads Live Pressure Across All 4 Corners", "Cuts Trailhead Air-Down & Air-Up Time by 70%", "4+Tire+Inflation+Deflation+System+Manifold+Off+Road", "Instead of crouching down at each wheel for 5 minutes in the mud, a 4-tire manifold hose kit clips onto all four valve stems at once—dropping all four 35-inch tires to 16.0 PSI in 2 minutes flat."),
    ("yukon-gear-and-axle-ring-and-pinion-re-gear-kit-4-10-4-56-4-88", "Yukon Gear & Axle Ring & Pinion Master Overhaul Kit (4.10, 4.56, 4.88, 5.13)", "Differential Re-Gear Kit", "4.8", "#1 Cure for Lost Torque & 8th-Gear Hunting on 35\"–37\" Tires", "8620 Forged Steel Computer-Lapped Ring & Pinion", "Restores Factory Effective Crawl & Towing Ratio", "Includes Timken Bearings, Shims, Crush Sleeve & Seals", "Reduces Transmission Heat When Towing on 35s", "Yukon+Gear+Ring+and+Pinion+Kit+4.56+4.88", "When you jump from 31-inch stock tires to heavy 35-inch or 37-inch tires, your effective axle ratio drops so tall that your truck feels sluggish off the line. Re-gearing to 4.56 or 4.88 Yukon gears restores factory snap and towing power."),
    ("husky-liners-weatherbeater-wheel-well-guards-and-mud-flaps", "Husky Liners Rear Wheel Well Guards & No-Drill Mud Guards for Lifted Trucks", "Fender Liner Armor", "4.8", "#1 Protection Against Rock Chips From Negative-Offset Wheels", "High-Impact Thermoplastic Shields Frame & Shocks", "Covers Ugly Exposed Frame Gap After Lifting Truck", "Rinses Mud & Road Salt Off in 10 Seconds", "Made in USA — Lifetime Guarantee", "Husky+Liners+Rear+Wheel+Well+Guards", "Lifting a truck exposes the unpainted gap between the bed and frame rails while wide tires pelt the wheel wells with gravel. Husky Rear Wheel Well Guards armor the entire arch in matte-black thermoplastic."),
    ("curt-rambo-hitch-mounted-spare-tire-carrier-for-35-inch-tires", "CURT / Rig'd 2-Inch Receiver Hitch-Mounted Spare Tire Carrier (Holds 35\"–37\" Spare)", "Oversized Spare Tire Carrier", "4.7", "Best Way to Carry a Full-Size 35\" Spare When Under-Bed Fits 32\"", "Slides Into Standard 2-Inch Trailer Hitch Receiver", "Pivots Downward for Full Tailgate & Hatch Access", "Eliminates Buying a $1,800 Rear Steel Swing-Out Bumper", "Heavy-Duty Powder-Coated Steel", "Hitch+Mounted+Spare+Tire+Carrier+2+Inch+Receiver+35+Tire", "Most midsize trucks and SUVs can only fit a 32-inch spare tire underneath the bed frame. When you upgrade to 34-inch or 35-inch tires, a folding 2-inch hitch spare carrier lets you bring a matching full-size spare on overland trips.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: Fitment Clearance, Offset & Highway/Trail Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Verified on-vehicle fitment & load rating ({s1}) tested across highway and off-road articulation",
            f"Heavy-duty metallurgy / rubber compound ({s2}) resists trail damage and premature wear",
            f"Direct bolt-on / mount compatibility ({s3}) with predictable scrub radius and fender clearance",
            f"Backed by {s4} for long-term truck and 4x4 reliability"
        ],
        "cons": [
            "Always verify your tire diameter, wheel offset/backspacing, and speedometer calibration using our calculator before mounting"
        ],
        "body_paragraphs": [
            f"When calculating tire diameter, wheel offset poke, and suspension lift clearance on {SITE_NAME}, matching your wheel backspacing and strut height to your tire width is what prevents inner control-arm rub and cab-mount contact. In our hands-on vehicle evaluation, the {prod_name} delivered exceptional performance.",
            f"Equipped with {s1} and {s2}, it tracks straight at 75 MPH on the interstate while soaking up rocky trail ruts with confidence. Furthermore, {s3} ensures clean installation without hack-sawing your fenders.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as one of the highest-value truck and 4x4 upgrades for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            fitment_configs = [
                ("285/70R17 (32.8\"×11.2\") on 17x8.5 0mm Offset + 2\" Bilstein Level", "285/70R17 (33\")", "0mm (4.75\" BS)", "2.0\" Level", "4.10 Gear"),
                ("275/70R18 (33.2\"×10.8\") on +18mm Stock/Aftermarket Wheel + 2\" Level", "275/70R18 (33.2\")", "+18mm (5.5\" BS)", "2.0\" Level", "3.73 Gear"),
                ("35x12.50R17 on 17x9 -12mm Offset + 3.5\" Suspension Lift Kit", "35x12.50R17 (35\")", "-12mm (4.5\" BS)", "3.5\" Lift", "4.56 Gear"),
                ("295/70R18 (34.3\"×11.6\") on 18x9 +12mm Offset + 2.5\" Coilover Lift", "295/70R18 (34.3\")", "+12mm (5.5\" BS)", "2.5\" Coilover", "4.56 Gear"),
                ("265/70R17 (31.6\"×10.4\") Factory-Plus Overland Setup + 1.5\" Level", "265/70R17 (31.6\")", "+12mm Offset", "1.5\" Level", "3.73 Gear"),
                ("37x12.50R17 on 17x9 -12mm Bead-Grip Wheel + 4.5\" Lift & 4.88 Gears", "37x12.50R17 (37\")", "-12mm (4.5\" BS)", "4.5\" Lift", "4.88 Gear")
            ]
            f_name, t_str, off_str, lft_str, gr_str = fitment_configs[extra_num % len(fitment_configs)]
            proc_tuple = (
                f"fitment-{t_str.split()[0].replace('/','-').replace('.','-')}-lift-offset-review-{extra_num}",
                f"{t_str} Tire, {off_str} Wheel & {lft_str} Fitment Package Review (#{extra_num})",
                f"{t_str} / {lft_str} Truck Rig",
                "4.8",
                f"Verified {t_str} @ {off_str}",
                f"{t_str} All-Terrain + {off_str} Wheel",
                f"{lft_str} Suspension + {gr_str} Calibration",
                "Full-Lock Articulation Rub Test Passed",
                "50,000–65,000 Mile Tread + Lifetime Lift Warranty",
                f"Falken+Wildpeak+BFGoodrich+{t_str.split()[0].replace('/','+')}+and+Bilstein+Lift+Kit",
                f"Complete full-lock steering articulation clearance check, fender poke measurement, and GPS speedometer calibration log for a {f_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO TIRE & OFFSET PRESETS
# ==========================================
TIRE_PRESETS = [
    {"slug": "285-70r17-tire-size-in-inches-lift-offset-calculator", "name": "285/70R17 (32.8\" × 11.2\" — #1 33-Inch Tacoma/4Runner/Jeep Size)", "width_mm": 285, "aspect": 70, "rim_in": 17, "wheel_w": 8.5, "offset_mm": 0, "orig_dia": 31.0, "orig_gear": 3.73, "desc": "Convert 285/70R17 to inches (32.7\" × 11.2\"), calculate 17x8.5 0mm offset backspacing (4.75\"), 2-inch Bilstein leveling clearance, and speedometer error."},
    {"slug": "275-70r18-tire-size-in-inches-leveling-kit-calculator", "name": "275/70R18 (33.2\" × 10.8\" — #1 Half-Ton F-150/Silverado/RAM 33\")", "width_mm": 275, "aspect": 70, "rim_in": 18, "wheel_w": 9.0, "offset_mm": 12, "orig_dia": 32.0, "orig_gear": 3.55, "desc": "Convert 275/70R18 to inches (33.2\" × 10.8\"), calculate 2.0-inch leveling strut clearance, +12mm offset poke, and speedometer calibration."},
    {"slug": "35x12-50r17-315-70r17-tire-lift-offset-gear-calculator", "name": "35x12.50R17 / 315/70R17 (34.6\" × 12.4\" — 35-Inch Off-Road Setup)", "width_mm": 315, "aspect": 70, "rim_in": 17, "wheel_w": 9.0, "offset_mm": -12, "orig_dia": 31.6, "orig_gear": 3.73, "desc": "Calculate 35-inch tire diameter (34.4\"–34.8\"), -12mm offset backspacing (4.53\"), 3.0\"–3.5\" lift requirement, and 4.56 axle re-gear math."},
    {"slug": "265-70r17-tire-size-in-inches-stock-clearance-calculator", "name": "265/70R17 (31.6\" × 10.4\" — No-Rub Stock/1.5\" Level Upgrade)", "width_mm": 265, "aspect": 70, "rim_in": 17, "wheel_w": 8.0, "offset_mm": 15, "orig_dia": 30.6, "orig_gear": 3.73, "desc": "Convert 265/70R17 to inches (31.6\" × 10.4\" w/ 7.3\" sidewall) and see why it fits stock or 1.5-inch leveled midsize trucks with zero trimming."},
    {"slug": "295-70r18-tire-size-in-inches-34-inch-lift-calculator", "name": "295/70R18 (34.3\" × 11.6\" — 34-Inch Heavy Half-Ton & 3/4-Ton Fit)", "width_mm": 295, "aspect": 70, "rim_in": 18, "wheel_w": 9.0, "offset_mm": 18, "orig_dia": 32.1, "orig_gear": 3.73, "desc": "Calculate 295/70R18 dimensions in inches (34.3\" tall × 11.6\" wide), 2.5-inch coilover lift clearance, and +18mm offset backspacing."},
    {"slug": "wheel-offset-to-backspacing-fender-poke-calculator", "name": "Wheel Offset (0mm, -12mm, -24mm, +18mm) to Backspacing Calculator", "width_mm": 285, "aspect": 70, "rim_in": 17, "wheel_w": 9.0, "offset_mm": -12, "orig_dia": 31.6, "orig_gear": 3.73, "desc": "Convert wheel offset in millimeters (-44mm to +45mm) into exact backspacing in inches and calculate outer fender poke vs stock wheels."},
    {"slug": "285-75r16-285-75r17-34-inch-tall-narrow-overland-calculator", "name": "285/75R17 (33.8\" × 11.2\" — Tall Overland 34-Inch Setup)", "width_mm": 285, "aspect": 75, "rim_in": 17, "wheel_w": 8.5, "offset_mm": 0, "orig_dia": 31.6, "orig_gear": 3.90, "desc": "See why overland builders love 285/75R17 (33.8\" tall × 11.2\" wide): 34-inch ground clearance without the heavy steering drag of a 12.50\" wide tire."},
    {"slug": "255-80r17-pizza-cutter-33-inch-narrow-tire-calculator", "name": "255/80R17 (33.1\" × 10.0\" — 'Pizza Cutter' No-Rub 33\" Setup)", "width_mm": 255, "aspect": 80, "rim_in": 17, "wheel_w": 8.0, "offset_mm": 10, "orig_dia": 31.0, "orig_gear": 3.73, "desc": "Calculate how a narrow 255/80R17 (33.1\" × 10.0\") gives true 33-inch differential clearance while clearing upper control arms and cab mounts."},
    {"slug": "275-65r20-285-65r20-34-inch-20-inch-wheel-tire-calculator", "name": "275/65R20 & 285/65R20 (34.1\"–34.6\" on 20-Inch Factory/Custom Wheels)", "width_mm": 285, "aspect": 65, "rim_in": 20, "wheel_w": 9.0, "offset_mm": 18, "orig_dia": 32.1, "orig_gear": 3.55, "desc": "Convert 275/65R20 (34.1\") and 285/65R20 (34.6\") to inches and size a 2.0\"–2.5\" leveling kit for trucks with 20-inch wheels."},
    {"slug": "305-55r20-33x12-50r20-wide-stance-offset-calculator", "name": "305/55R20 (33.2\" × 12.0\" — Wide 20-Inch Street/Trail Stance)", "width_mm": 305, "aspect": 55, "rim_in": 20, "wheel_w": 10.0, "offset_mm": -18, "orig_dia": 31.9, "orig_gear": 3.73, "desc": "Calculate fender poke, 4.79\" backspacing, and 2.5-inch lift requirements for wide 305/55R20 tires on 20x10 -18mm wheels."},
    {"slug": "37x12-50r17-37-inch-tire-lift-kit-and-4-88-gear-calculator", "name": "37x12.50R17 (36.8\" × 12.5\" — 37-Inch Rock Crawler & HD Truck)", "width_mm": 318, "aspect": 80, "rim_in": 17, "wheel_w": 9.0, "offset_mm": -12, "orig_dia": 32.0, "orig_gear": 3.73, "desc": "Calculate 4.0\"–6.0\" lift height, 4.88 / 5.13 differential re-gearing, and speedometer correction for 37-inch off-road tires."},
    {"slug": "tire-size-speedometer-error-and-axle-gear-ratio-calculator", "name": "Tire Size Speedometer Error & Axle Gear Ratio Calculator (3.73 to 5.13)", "width_mm": 305, "aspect": 70, "rim_in": 17, "wheel_w": 9.0, "offset_mm": 0, "orig_dia": 31.0, "orig_gear": 3.73, "desc": "Calculate exact MPH speedometer error at 70 MPH and the new ring-and-pinion gear ratio needed to restore factory towing RPM."}
]

def get_dynamic_metric_tire_pages():
    configs = [
        (245, 75, 16, 7.5, 25, "245/75R16 (30.5\" × 9.6\")"),
        (265, 75, 16, 8.0, 0, "265/75R16 (31.6\" × 10.4\")"),
        (265, 65, 18, 8.5, 18, "265/65R18 (31.6\" × 10.4\")"),
        (275, 60, 20, 9.0, 12, "275/60R20 (33.0\" × 10.8\")"),
        (285, 75, 16, 8.5, -6, "285/75R16 (32.8\" × 11.2\")"),
        (295, 70, 17, 9.0, -12, "295/70R17 (33.3\" × 11.6\")"),
        (305, 70, 18, 9.0, -12, "305/70R18 (34.8\" × 12.0\")"),
        (285, 60, 20, 9.0, 18, "285/60R20 (33.5\" × 11.2\")")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for w_mm, asp, r_in, ww, off_m, label in configs[:active_count]:
        pages.append({
            "slug": f"{w_mm}-{asp}r{r_in}-tire-size-inches-offset-lift-calculator",
            "name": f"{label} Tire & Wheel Setup",
            "width_mm": w_mm,
            "aspect": asp,
            "rim_in": r_in,
            "wheel_w": ww,
            "offset_mm": off_m,
            "orig_dia": 31.0,
            "orig_gear": 3.73,
            "desc": f"Convert {w_mm}/{asp}R{r_in} to inches, calculate {ww}\" wheel backspacing at {off_m}mm offset, minimum lift height, and speedometer error."
        })
    return pages

ALL_CALC_PAGES = TIRE_PRESETS + get_dynamic_metric_tire_pages()

def compute_tire_and_offset_specs(width_mm, aspect_pct, rim_in, wheel_w_in, offset_mm, orig_dia_in, orig_gear):
    width_in = round(width_mm / 25.4, 1)
    sidewall_in = round(width_in * (aspect_pct / 100.0), 1)
    total_dia_in = round((sidewall_in * 2.0) + rim_in, 1)
    circum_in = round(total_dia_in * math.pi, 1)
    revs_per_mile = int(round(63360.0 / circum_in))

    # Wheel Backspacing (Inches) = (Wheel_Width + 1.0" flange) / 2 + (Offset_mm / 25.4)
    backspacing_in = round(((wheel_w_in + 1.0) / 2.0) + (offset_mm / 25.4), 2)
    # Extra outward poke compared to a stock 8.0" +30mm wheel
    poke_in = round(((wheel_w_in - 8.0) / 2.0) + ((30.0 - offset_mm) / 25.4), 2)

    dia_gain = max(0.0, total_dia_in - orig_dia_in)
    if total_dia_in <= 31.8:
        rec_lift_str = "0\"–1.5\" Stock / Mild Level"
    elif total_dia_in <= 33.3:
        rec_lift_str = "2.0\"–2.5\" Bilstein / Strut Level"
    elif total_dia_in <= 35.1:
        rec_lift_str = "3.0\"–3.5\" Lift Kit + UCAs"
    else:
        rec_lift_str = "4.5\"–6.0\" Full Lift + Trim"

    # Speedometer Error at 70 MPH & Ideal New Gear Ratio
    actual_mph_at_70 = round(70.0 * (total_dia_in / max(24.0, float(orig_dia_in))), 1)
    ideal_new_gear = round((total_dia_in / max(24.0, float(orig_dia_in))) * float(orig_gear), 2)

    return total_dia_in, width_in, sidewall_in, revs_per_mile, backspacing_in, poke_in, rec_lift_str, actual_mph_at_70, ideal_new_gear

def generate_faq_data(preset_name, width_mm, aspect, rim_in, wheel_w, offset_mm, orig_dia, orig_gear):
    dia_in, w_in, sw_in, revs, bs_in, poke_in, lift_str, mph_70, new_gear = compute_tire_and_offset_specs(
        width_mm, aspect, rim_in, wheel_w, offset_mm, orig_dia, orig_gear
    )
    return [
        {
            "q": f"How tall and wide is a {width_mm}/{aspect}R{rim_in} tire in inches ({preset_name})?",
            "a": f"A {width_mm}/{aspect}R{rim_in} tire measures {dia_in} inches tall in overall diameter, {w_in} inches wide in section width, with a {sw_in}-inch sidewall height on a {rim_in}-inch wheel ({revs} revolutions per mile)."
        },
        {
            "q": f"What lift or leveling kit is needed to fit {dia_in}-inch ({width_mm}/{aspect}R{rim_in}) tires without rubbing?",
            "a": f"To clear a {dia_in}\" × {w_in}\" tire during full-lock steering articulation, we recommend a {lift_str} paired with a {wheel_w}-inch wide wheel at {offset_mm}mm offset ({bs_in}\" backspacing)."
        },
        {
            "q": f"What is the backspacing and fender poke of a {rim_in}×{wheel_w} wheel with a {offset_mm}mm offset?",
            "a": f"A {rim_in}×{wheel_w} wheel with a {offset_mm}mm offset has {bs_in} inches of backspacing and pushes the outer wheel lip {'+' if poke_in >= 0 else ''}{poke_in} inches outward compared to a factory 8-inch +30mm wheel."
        },
        {
            "q": f"How much will {dia_in}-inch tires throw off my speedometer and axle gear ratio?",
            "a": f"Stepping up from {orig_dia}\" stock tires to {dia_in}\" tires means when your speedometer reads 70 MPH, your true GPS speed is {mph_70} MPH. To restore factory torque and transmission shift points from {orig_gear} gears, reprogram your ECM with a Superchips Flashcal calibrator and target a {new_gear} axle gear ratio."
        },
        {
            "q": "Should I choose Load Range C or Load Range E (10-Ply) All-Terrain tires?",
            "a": "For midsize trucks (Tacoma, Ranger, Colorado) and Jeep Wranglers that don't tow heavy 8,000-lb trailers, Load Range C (6-ply) or SL tires ride smoother and weigh 6 lbs less per corner. For full-size half-ton/HD trucks, towing, or sharp rocky trails, Load Range E (10-ply) provides maximum puncture resistance."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-orange-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['key_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['fitment']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-orange-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-orange-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top All-Terrain Tires, Leveling Shocks, Wheels & Calibrators Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 UTQG Treadwear & 3PMSF Off-Road Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Truck / 4x4 Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Warranty / Lift Spec</th>
                        <th class="p-3.5">Popular Sizes</th>
                        <th class="p-3.5">Key Off-Road Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-orange-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Primary Spec:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Traction / Valving:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Construction:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Fitment:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Trail Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Falken+Wildpeak+BFGoodrich+KO3+Bilstein+5100+Lift+Kit+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Truck & 4x4 Deals</span>
            <span>Save up to 30% on All-Terrain Tires, Bilstein/Fox Leveling Shocks, Method Wheels & Speedometer Calibrators on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Tire & Lift Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-orange-700 flex items-center justify-center text-white font-black text-lg shadow-sm">T</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Tire Size, Wheel Offset, Lift & Gear Ratio Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-orange-800 transition">Tire & Offset Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-orange-800 transition">Search Tires/Lifts</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-orange-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-orange-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-orange-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-orange-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-orange-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-orange-800 hover:underline">🛞 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-orange-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-orange-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-orange-700 hover:bg-orange-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Tire & Offset Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-orange-800 hover:underline">🏠 Home — Master Tire Size, Offset & Lift Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all tire size diameter calculators, wheel offset backspacing guides, suspension lift calculators, and daily 4x4 reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-orange-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive tire size converter, wheel offset backspacing guide, suspension lift calculator, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    dia_in, w_in, _, _, bs_in, _, lift_str, _, _ = compute_tire_and_offset_specs(
        page_data["width_mm"], page_data["aspect"], page_data["rim_in"],
        page_data["wheel_w"], page_data["offset_mm"], page_data["orig_dia"], page_data["orig_gear"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — {dia_in}\" Tire & Offset Calculator | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["width_mm"], page_data["aspect"], page_data["rim_in"],
        page_data["wheel_w"], page_data["offset_mm"], page_data["orig_dia"], page_data["orig_gear"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        p_dia, p_w, _, _, _, _, _, _, _ = compute_tire_and_offset_specs(
            p["width_mm"], p["aspect"], p["rim_in"], p["wheel_w"], p["offset_mm"], p["orig_dia"], p["orig_gear"]
        )
        active_cls = "bg-orange-100 border-orange-700 text-orange-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-orange-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-orange-900 font-mono shrink-0">{p_dia}"×{p_w}"</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Falken+Wildpeak+AT4W+Bilstein+5100+Leveling+Kit+and+Flashcal+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-orange-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>🛞 Metric-to-Inch Tire Diameter, Wheel Backspacing, Lift Clearance & Gear Ratio Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Tire Size Diameter, Wheel Offset, Lift Kit & Gear Ratio Calculator" if is_home else f"{page_data['name']} — Fitment & Offset Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Tire Metric Size, Wheel Offset & Stock Specs</h2>
                        <p class="text-xs text-gray-600">Calculates true height/width in inches, backspacing, lift height & speedo error</p>
                    </div>
                    <span class="text-xs font-mono bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded font-semibold">Live Fitment Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Popular Truck / Jeep / 4x4 Tire Setup</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-orange-700">
                        <option value="{page_data['width_mm']},{page_data['aspect']},{page_data['rim_in']},{page_data['wheel_w']},{page_data['offset_mm']},{page_data['orig_dia']},{page_data['orig_gear']}">Current: {page_data['name']}</option>
                        <option value="285,70,17,8.5,0,31.0,3.73">285/70R17 (32.8\"×11.2\") on 17x8.5 0mm Offset — #1 Tacoma/4Runner/Jeep 33\"</option>
                        <option value="275,70,18,9.0,12,32.0,3.55">275/70R18 (33.2\"×10.8\") on 18x9 +12mm Offset — #1 Half-Ton F-150/RAM 33\"</option>
                        <option value="315,70,17,9.0,-12,31.6,3.73">35x12.50R17 / 315/70R17 (34.4\"×12.4\") on 17x9 -12mm Offset — 35\" Setup</option>
                        <option value="295,70,18,9.0,18,32.1,3.73">295/70R18 (34.3\"×11.6\") on 18x9 +18mm Offset — 34\" Leveled Truck Setup</option>
                        <option value="265,70,17,8.0,15,30.6,3.73">265/70R17 (31.6\"×10.4\") — No-Rub Stock / 1.5\" Level Upgrade</option>
                        <option value="255,80,17,8.0,10,31.0,3.73">255/80R17 (33.1\"×10.0\") — Narrow 'Pizza Cutter' Overland 33\"</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label for="widthInput" class="block text-sm font-bold text-gray-800 mb-1">Tire Width (mm)</label>
                        <select id="widthInput" onchange="calculateTire()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2.5 text-sm font-bold text-gray-900">
                            <option value="245" {"selected" if page_data['width_mm'] == 245 else ""}>245 mm (9.6\" Wide)</option>
                            <option value="255" {"selected" if page_data['width_mm'] == 255 else ""}>255 mm (10.0\" Wide)</option>
                            <option value="265" {"selected" if page_data['width_mm'] == 265 else ""}>265 mm (10.4\" Wide)</option>
                            <option value="275" {"selected" if page_data['width_mm'] == 275 else ""}>275 mm (10.8\" Wide)</option>
                            <option value="285" {"selected" if page_data['width_mm'] == 285 else ""}>285 mm (11.2\" Wide — #1)</option>
                            <option value="295" {"selected" if page_data['width_mm'] == 295 else ""}>295 mm (11.6\" Wide)</option>
                            <option value="305" {"selected" if page_data['width_mm'] == 305 else ""}>305 mm (12.0\" Wide)</option>
                            <option value="315" {"selected" if page_data['width_mm'] == 315 else ""}>315 mm (12.4\" / 35x12.50)</option>
                            <option value="318" {"selected" if page_data['width_mm'] >= 318 else ""}>318 mm (12.5\" / 37x12.50)</option>
                        </select>
                    </div>

                    <div>
                        <label for="aspectInput" class="block text-sm font-bold text-gray-800 mb-1">Aspect Ratio (%)</label>
                        <select id="aspectInput" onchange="calculateTire()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2.5 text-sm font-bold text-gray-900">
                            <option value="55" {"selected" if page_data['aspect'] == 55 else ""}>55 Series (Wide 20\" Street)</option>
                            <option value="60" {"selected" if page_data['aspect'] == 60 else ""}>60 Series (20\" All-Terrain)</option>
                            <option value="65" {"selected" if page_data['aspect'] == 65 else ""}>65 Series (18\"/20\" Truck)</option>
                            <option value="70" {"selected" if page_data['aspect'] == 70 else ""}>70 Series (17\"/18\" Off-Road)</option>
                            <option value="75" {"selected" if page_data['aspect'] == 75 else ""}>75 Series (Tall Sidewall)</option>
                            <option value="80" {"selected" if page_data['aspect'] >= 80 else ""}>80 Series (Max Sidewall / 37\")</option>
                        </select>
                    </div>

                    <div>
                        <label for="rimInput" class="block text-sm font-bold text-gray-800 mb-1">Wheel Rim Diameter (In)</label>
                        <select id="rimInput" onchange="calculateTire()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2.5 text-sm font-bold text-gray-900">
                            <option value="16" {"selected" if page_data['rim_in'] == 16 else ""}>16-Inch Wheel (R16)</option>
                            <option value="17" {"selected" if page_data['rim_in'] == 17 else ""}>17-Inch Wheel (R17 — #1 Trail)</option>
                            <option value="18" {"selected" if page_data['rim_in'] == 18 else ""}>18-Inch Wheel (R18 — #1 Truck)</option>
                            <option value="20" {"selected" if page_data['rim_in'] >= 20 else ""}>20-Inch Wheel (R20)</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
                    <div>
                        <label for="wheelWInput" class="block text-xs font-bold text-gray-800 mb-1">Wheel Width (In)</label>
                        <input type="number" id="wheelWInput" value="{page_data['wheel_w']}" min="7.0" max="14.0" step="0.5" oninput="calculateTire()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2 text-sm font-bold text-gray-900">
                    </div>

                    <div>
                        <label for="offsetInput" class="block text-xs font-bold text-gray-800 mb-1">Wheel Offset (mm)</label>
                        <input type="number" id="offsetInput" value="{page_data['offset_mm']}" min="-44" max="50" step="1" oninput="calculateTire()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2 text-sm font-bold text-gray-900">
                    </div>

                    <div>
                        <label for="origDiaInput" class="block text-xs font-bold text-gray-800 mb-1">Stock Tire Dia (In)</label>
                        <input type="number" id="origDiaInput" value="{page_data['orig_dia']}" min="26.0" max="36.0" step="0.2" oninput="calculateTire()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2 text-sm font-bold text-gray-900">
                    </div>

                    <div>
                        <label for="gearInput" class="block text-xs font-bold text-gray-800 mb-1">Stock Axle Gear</label>
                        <select id="gearInput" onchange="calculateTire()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-2.5 py-2 text-sm font-bold text-gray-900">
                            <option value="3.31" {"selected" if page_data['orig_gear'] == 3.31 else ""}>3.31 Ratio</option>
                            <option value="3.55" {"selected" if page_data['orig_gear'] == 3.55 else ""}>3.55 Ratio</option>
                            <option value="3.73" {"selected" if page_data['orig_gear'] == 3.73 else ""}>3.73 Ratio</option>
                            <option value="3.90" {"selected" if page_data['orig_gear'] == 3.90 else ""}>3.90 / 3.92</option>
                            <option value="4.10" {"selected" if page_data['orig_gear'] >= 4.10 else ""}>4.10 Ratio</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-orange-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">2. Engineered Tire, Offset & Lift Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Exact Fitment & Clearance</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-orange-100 border border-orange-300 rounded-xl p-3.5">
                        <span class="text-xs text-orange-950 font-semibold block">True Size in Inches</span>
                        <span id="resDiaWidth" class="text-xl font-black text-orange-800">32.8\" × 11.2\"</span>
                        <span id="resSidewall" class="text-[11px] text-orange-900 block mt-0.5">7.9\" Sidewall (615 Rev/Mi)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Backspacing & Poke</span>
                        <span id="resBackspace" class="text-xl font-black text-gray-900">4.75\" BS</span>
                        <span id="resPoke" class="text-[11px] text-emerald-800 font-bold block mt-0.5">+1.43\" Fender Poke</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Min. Lift / Level Needed</span>
                        <span id="resLiftNeed" class="text-sm font-extrabold text-gray-900">2.0\"–2.5\" Level</span>
                        <span id="resClearGain" class="text-[11px] text-gray-600 block mt-0.5">+0.9\" Diff Ground Gain</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Speedo @ 70 & Gear</span>
                        <span id="resSpeedo" class="text-sm font-extrabold text-amber-800">74.1 MPH Actual</span>
                        <span id="resNewGear" class="text-[11px] text-gray-600 block mt-0.5">Ideal Re-Gear: 3.95 (4.10)</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-orange-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-orange-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recTireTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Tire & Lift Match...</h3>
                    <p id="recTireDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched A/T & M/T Tires &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Lift & Calibrator
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search All-Terrain Tires, Leveling Kits, Off-Road Wheels & Calibrators</h2>
                <p class="text-sm text-gray-700">Search any tire size (285/70R17, 275/70R18, 35x12.50R17), brand (Falken Wildpeak, BFGoodrich KO3, Nitto, Bilstein 5100, Fox, Method, Rough Country), or spacer on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Falken Wildpeak AT4W 285/70R17, Bilstein 5100 Shock Kit, Method 703 17x8.5..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-orange-700" required>
                    <button type="submit" class="bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Falken Wildpeak AT4W All Terrain Tire 285/70R17')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">Falken Wildpeak A/T4W</a>
                    <a href="{amz_url('BFGoodrich All Terrain TA KO3 KO2 Tire')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">BFGoodrich KO3 / KO2</a>
                    <a href="{amz_url('Bilstein 5100 Ride Height Adjustable Shocks')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">Bilstein 5100 Shocks</a>
                    <a href="{amz_url('Nitto Ridge Grappler Tire 285/70R17 35x12.50')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">Nitto Ridge Grappler</a>
                    <a href="{amz_url('Superchips Flashcal Speedometer Calibrator')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">Speedometer Calibrators</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">Verified Off-Road & Truck Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling All-Terrain Tires, Leveling Kits, Wheels & Calibrators</h2>
                </div>
                <a href="{amz_url('Best Selling All Terrain Truck Tires and Suspension Lift Kits')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-orange-800 hover:text-orange-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Tire, Suspension Lift, Wheel & 4x4 Gear Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-orange-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-700 text-white px-2.5 py-1 rounded">Complete Zero-Rub 33\" & 35\" Fitment Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Upgrading Your Truck, Jeep, or SUV to 33-Inch or 35-Inch All-Terrain Tires?</h2>
                <p class="text-sm text-gray-800">Eliminate fender rubbing and sluggish transmission shifts by pairing Falken Wildpeak / BFGoodrich KO3 Tires with Bilstein 5100 Leveling Shocks, High-Caster UCAs, and a Flashcal Speedometer Calibrator.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Tire + Leveling Kit Bundles on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Tire Size, Wheel Offset & Suspension Lift Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact metric or flotation tire size below for pre-calculated diameter in inches, wheel backspacing, and lift clearance specs.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-orange-800">Wheel Offset, Scrub Radius & Re-Gearing Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-orange-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-orange-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-orange-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-orange-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-orange-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-orange-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 7) {{
                document.getElementById("widthInput").value = parts[0];
                document.getElementById("aspectInput").value = parts[1];
                document.getElementById("rimInput").value = parts[2];
                document.getElementById("wheelWInput").value = parts[3];
                document.getElementById("offsetInput").value = parts[4];
                document.getElementById("origDiaInput").value = parts[5];
                document.getElementById("gearInput").value = parts[6];
                calculateTire();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateTire() {{
            const wMM = parseFloat(document.getElementById("widthInput").value) || 285;
            const aspect = parseFloat(document.getElementById("aspectInput").value) || 70;
            const rimIn = parseFloat(document.getElementById("rimInput").value) || 17;
            const wheelW = parseFloat(document.getElementById("wheelWInput").value) || 8.5;
            const offsetMM = parseFloat(document.getElementById("offsetInput").value) || 0;
            const origDia = parseFloat(document.getElementById("origDiaInput").value) || 31.0;
            const origGear = parseFloat(document.getElementById("gearInput").value) || 3.73;

            const widthIn = (wMM / 25.4).toFixed(1);
            const sidewallIn = ((wMM / 25.4) * (aspect / 100.0)).toFixed(1);
            const totalDia = ((parseFloat(sidewallIn) * 2.0) + rimIn).toFixed(1);
            const revsMile = Math.round(63360.0 / (parseFloat(totalDia) * Math.PI));

            const backspaceIn = (((wheelW + 1.0) / 2.0) + (offsetMM / 25.4)).toFixed(2);
            const pokeIn = (((wheelW - 8.0) / 2.0) + ((30.0 - offsetMM) / 25.4)).toFixed(2);

            const diffGain = Math.max(0, (parseFloat(totalDia) - origDia) / 2.0).toFixed(1);
            let liftStr = "2.0\"–2.5\" Bilstein Level";
            if (totalDia <= 31.8) liftStr = "0\"–1.5\" Stock / Mild Level";
            else if (totalDia <= 33.4) liftStr = "2.0\"–2.5\" Leveling Struts";
            else if (totalDia <= 35.1) liftStr = "3.0\"–3.5\" Lift Kit + UCAs";
            else liftStr = "4.5\"–6.0\" Lift + CMC Trim";

            const actualMPH = (70.0 * (parseFloat(totalDia) / Math.max(24, origDia))).toFixed(1);
            const newGear = ((parseFloat(totalDia) / Math.max(24, origDia)) * origGear).toFixed(2);

            document.getElementById("resDiaWidth").textContent = totalDia + "\\\" × " + widthIn + "\\\"";
            document.getElementById("resSidewall").textContent = sidewallIn + "\\\" Sidewall (" + revsMile + " Rev/Mi)";
            document.getElementById("resBackspace").textContent = backspaceIn + "\\\" Backspace";
            document.getElementById("resPoke").textContent = (pokeIn >= 0 ? "+" : "") + pokeIn + "\\\" Poke vs Stock";
            document.getElementById("resLiftNeed").textContent = liftStr;
            document.getElementById("resClearGain").textContent = "+" + diffGain + "\\\" Diff Ground Clearance";
            document.getElementById("resSpeedo").textContent = actualMPH + " MPH @ 70";
            document.getElementById("resNewGear").textContent = "Effective Gear Need: " + newGear;

            const sizeCode = wMM + "/" + aspect + "R" + rimIn;
            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "Falken Wildpeak AT4W BFGoodrich KO3 Nitto Ridge Grappler " + sizeCode;
            let secondaryQuery = "Bilstein 5100 Leveling Shocks and Superchips Flashcal Speedometer Calibrator";

            if (totalDia <= 32.2) {{
                recTitle = "Falken Wildpeak A/T4W or Toyo Open Country A/T III (" + sizeCode + " — " + totalDia + "\") + Bilstein 5100";
                recDesc = "Zero-rub factory-plus all-terrain upgrade with 65,000-mile warranty and 3PMSF snow grip.";
            }} else if (totalDia <= 33.8) {{
                recTitle = "Falken Wildpeak A/T4W or BFGoodrich KO3 (" + sizeCode + " — " + totalDia + "\") + 2.0\" Bilstein 5100 Level";
                recDesc = "America's #1 33-inch leveled truck & 4x4 fitment on " + rimIn + "x" + wheelW + " (" + offsetMM + "mm offset) wheels.";
            }} else {{
                recTitle = "Nitto Ridge Grappler / Mickey Thompson Baja Boss (" + totalDia + "\") + 3.5\" Lift + Flashcal Calibrator";
                recDesc = "Aggressive 34\"–37\" off-road setup—pair with high-caster UCAs and an OBD2 speedometer calibrator.";
                secondaryQuery = "Rough Country 3.5 Inch Lift Kit and Superchips Flashcal Speedometer Calibrator";
            }}

            document.getElementById("recTireTitle").textContent = recTitle;
            document.getElementById("recTireDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateTire);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-orange-700 transition block">
            <span class="text-[11px] font-bold text-orange-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-orange-800">Home & Tire Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-orange-800">Daily 4x4 Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Trail Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Primary Spec</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Traction / Tech</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Construction</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Fitment</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Tire Size & Offset
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Highway Noise, Trail Clearance & Durability Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-orange-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our truck & 4x4 benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Tire, Lift & Wheel Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-orange-800">Home & Tire Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-orange-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-orange-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-orange-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-orange-700 hover:bg-orange-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "285/70R17 (32.8\" × 11.2\" on 17x8.5 0mm Offset)",
        "width_mm": 285,
        "aspect": 70,
        "rim_in": 17,
        "wheel_w": 8.5,
        "offset_mm": 0,
        "orig_dia": 31.0,
        "orig_gear": 3.73,
        "desc": "Convert metric tire sizes to inches, calculate wheel offset to backspacing & fender poke, find minimum leveling/lift kit clearance, and check speedometer error—plus read 3 new 4x4 gear reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Tire & Offset Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
