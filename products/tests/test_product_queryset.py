from django.test import TestCase
from django.db import models

from products.models import Category, Product, Tag


class ProductQuerySetTests(TestCase):
    """Test custom filters added to the product queryset."""

    #
    # Test data
    #

    TAGS = [
        "residential", "commercial",
        "outdoor", "weatherproof",
        "copper", "aluminium",
        "120V", "240V",
        "UL listed",
        "LED",
    ]

    CATEGORIES = [
        "Lighting",
        "Conduit & Fittings",
        "Wires & Cables",
        "Switches & Outlets",
        "Circuit Protection",
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

    #
    # Tests
    #

    @classmethod
    def setUpTestData(cls):
        # Clean up migration seeded data to run tests in isolation
        Product.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()

        # Populate with data defined in this test
        tags = {name: Tag.objects.create(name=name) for name in cls.TAGS}
        categories = {name: Category.objects.create(name=name) for name in cls.CATEGORIES}

        for name, description, category, tag_names in cls.PRODUCTS:
            product = Product.objects.create(
                name=name,
                description=description,
                category=categories[category]
            )
            product.tags.set([tags[t] for t in tag_names])

        # Keep name -> object mappings for the tests
        cls.tags = {t.name: t.pk for t in Tag.objects.all()}
        cls.categories = {c.name: c.pk for c in Category.objects.all()}

    def just_names(self, qs: models.QuerySet) -> list[str]:
        """A utility to extract names from a queryset to simplify reults verification.
        """
        return list(qs.values_list("name", flat=True))

    def test_gives_all_with_empty_filters(self):
        qs = Product.objects.search(None).of_category(None).assigned_tags([])
        self.assertEqual(qs.count(), 20)

    def test_all_filters_combined(self):
        qs = (Product.objects
              .search("outlet")
              .assigned_tags([self.tags["weatherproof"]])
              .of_category(self.categories["Switches & Outlets"])
        )
        self.assertEqual(
            self.just_names(qs),
            ["20A GFCI Receptacle"],
        )

    def test_search_description(self):
        self.assertCountEqual(
            self.just_names(Product.objects.search("outlet")),
            [
                "15A Duplex Receptacle",
                "20A GFCI Receptacle",
                "Weatherproof Junction Box",
            ],
        )

    def test_filter_by_category(self):
        self.assertCountEqual(
            self.just_names(Product.objects.of_category(self.categories["Lighting"])),
            [
                "6 in LED Recessed Downlight",
                "40W LED Wall Pack",
                "4 ft LED Shop Light",
                "A19 LED Bulb 4-Pack",
            ],
        )

    def test_filter_by_tag(self):
        self.assertCountEqual(
            self.just_names(Product.objects.assigned_tags([self.tags["aluminium"]])),
            [
                "6 AWWG XHHWNN Aluminium Wire",
                "Weatherproof Junction Box",
            ],
        )

    def test_filter_by_multiple_tags(self):
        names = self.just_names(
            Product.objects.assigned_tags(
                [
                    self.tags["outdoor"],
                    self.tags["weatherproof"]
                ]
            )
        )
        self.assertEqual(len(names), 8)
        self.assertEqual(len(names), len(set(names)))
