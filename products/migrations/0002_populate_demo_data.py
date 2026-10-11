from django.db import migrations

TAGS = [
    "residential", "commercial",
    "outdoor", "weatherproof",
    "copper", "aluminium",
    "120V", "240V",
    "UL listed",
    "LED",
]

CATEGORIES = [
    "Conduit & Fittings",
    "Wires & Cables",
    "Switches & Outlets",
    "Circuit Protection",
    "Lighting",
]

# (name, description, category, tags)
PRODUCTS = [
    ("50A Double-Pole Circuit Breaker",
     "Two-pole breaker for ranges, dryers and EV chargers on 240V circuits.",
     "Circuit Protection", ["240V", "residential", "UL listed"]),
    ("Whole-House Surge Protector",
     "Type 2 surge protective device mounted at the main panel, 50KA per phase.",
     "Circuit Protection", ["240V", "residential", "UL listed"]),
    ("30A Fused Safety Switch",
     "Disconnect for outdoor HVAC equipment, includes cartridge fuses.",
     "Circuit Protection", ["240V", "outdoor", "weatherproof", "commercial"]),
    ("15A Duplex Receptacle",
     "Tamper-resistant duplex outlet, white, back and side wired.",
     "Switches & Outlets", ["120V", "residential", "UL listed"]),
    ("20A GFCI Receptacle",
     "Self-testing ground fault outlet with weather-resistant face for kitchens, baths and outdoors.",
     "Switches & Outlets", ["120V", "outdoor", "weatherproof", "UL listed"]),
    ("Single-Pole Toggle Switch",
     "15A 120V toggle light switch, ivory, with grounding screw.",
     "Switches & Outlets", ["120V", "residential"]),
    ("Smart Dimmer Switch",
     "Wi-Fi dimmer compatible with LED and incandescent loads, neutral wire required.",
     "Switches & Outlets", ["LED", "120V", "residential"]),
    ("6 in LED Recessed Downlight",
     "Canless retrofit downlight, 12W, selectable color temperature 2700K-5000K.",
     "Lighting", ["LED", "residential", "UL listed"]),
    ("40W LED Wall Pack",
     "Dusk-to-dawn outdoor wall light for building perimeters, 5000K, photocell included.",
     "Lighting", ["LED", "outdoor", "weatherproof", "commercial"]),
    ("12 AWWG THHNN Copper Wire",
     "Solid copper building wire, 500 ft spool, rated 600V for conduit and raceway installations.",
     "Wires & Cables", ["copper", "commercial", "UL listed"]),
    ("14/2 NM-B Romeeex Cable",
     "Non-metallic sheathed copper cable with ground, 250 ft coil for indoor residential branch circuits.",
     "Wires & Cables", ["copper", "residential", "120V", "UL listed"]),
    ("6 AWWG XHHWNN Aluminium Wire",
     "Stranded aluminium feeder wire, moisture and heat resistant, sold per foot.",
     "Wires & Cables", ["aluminium", "commercial", "outdoor"]),
    ("12/3 Outdoor Extension Cord",
     "Heavy-duty 50 ft copper extension cord with weatherproof jacket and lighted ends.",
     "Wires & Cables", ["copper", "outdoor", "weatherproof", "120V"]),
    ("20A Single-Pole Circuit Breaker",
     "Plug-on breaker for residential load centers, 120V branch circuit protection.",
     "Circuit Protection", ["120V", "residential", "UL listed"]),
    ("4 ft LED Shop Light",
     "Linkable 40W linear fixture, 4000 lumens, for garages and workshops.",
     "Lighting", ["LED", "120V", "commercial"]),
    ("A19 LED Bulb 4-Pack",
     "60W-equivalent 9W bulbs, 800 lumens, soft white 2700K, dimmable.",
     "Lighting", ["LED", "residential"]),
    ("3/4 in EMTTT Conduit",
     "10 ft electrical metallic tubing, galvanized steel, for exposed commercial runs.",
     "Conduit & Fittings", ["commercial", "UL listed"]),
    ("Weatherproof Junction Box",
     "Single-gang die-cast aluminium box with three 1/2 in threaded outlets.",
     "Conduit & Fittings", ["aluminium", "outdoor", "weatherproof"]),
    ("1/2 in PVC Schedullle 40 Conduit",
     "10 ft rigid PVC conduit, sunlight resistant, for underground and outdoor use.",
     "Conduit & Fittings", ["outdoor", "weatherproof"]),
    ("1/2 in Liquid-Tight Flexible Conduit",
     "25 ft coil of flexible metal conduit with PVC jacket for wet locations.",
     "Conduit & Fittings", ["outdoor", "weatherproof", "commercial"]),
]

def populate_demo_data(apps, schema_editor):
    Tag = apps.get_model("products", "Tag")
    Category = apps.get_model("products", "Category")
    Product = apps.get_model("products", "Product")

    tags = {name: Tag.objects.create(name=name) for name in TAGS}
    categories = {name: Category.objects.create(name=name) for name in CATEGORIES}

    for name, description, category, tag_names in PRODUCTS:
        product = Product.objects.create(
            name=name,
            description=description,
            category=categories[category]
        )
        product.tags.set([tags[t] for t in tag_names])

def remove_demo_data(apps, schema_editor):
    apps.get_model("products", "Product").objects.filter(
        name__in=[p[0] for p in PRODUCTS]
    ).delete()
    apps.get_model("products", "Tag").objects.filter(name__in=TAGS).delete()
    apps.get_model("products", "Category").objects.filter(name__in=CATEGORIES).delete()

class Migration(migrations.Migration):
    dependencies = [("products", "0001_initial")]
    operations = [migrations.RunPython(populate_demo_data, remove_demo_data)]
