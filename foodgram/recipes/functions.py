import io

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from .models import Ingredient, IngredientAmount, Recipe


def get_tags_and_recipes_list(request):
    meals = request.GET.get("tags", "bld")
    recipes_list = (
        Recipe.objects.filter(tags__value__in=meals)
        .order_by("-pub_date")
        .distinct()
    )
    return meals, recipes_list


def check_ingredients(request):
    ingredients = []
    for key, value in request.POST.items():
        if "nameIngredient" in key:
            title = value
        elif "valueIngredient" in key:
            amount = value
        elif "unitsIngredient" in key:
            dimension = value
            ingredient = Ingredient.objects.filter(
                title=title, dimension=dimension
            ).first()
            if ingredient is not None:
                ingredients.append([ingredient, amount])
            else:
                return False
    return ingredients


def create_ingredient_amount(ingredients, recipe):
    objs = [
        IngredientAmount(ingredient=ingredient, amount=amount, recipe=recipe)
        for ingredient, amount in ingredients
    ]
    IngredientAmount.objects.bulk_create(objs)


def pdf_create(ingredients):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create a new canvas for cyrillic pdf file
    c = canvas.Canvas(buffer, bottomup=0)

    # fname - the font file name without extension
    fname = "a010013l"

    # faceName - view a010013l.AFM file as a plain text and look at
    # row beginning with 'FontName' word (it's usually the fourth row).
    # The word after 'FontName' is the faceName ('URWGothicL-Book').
    faceName = "URWGothicL-Book"

    # Define new Type 1 font
    cyrFace = pdfmetrics.EmbeddedType1Face(fname + ".afm", fname + ".pfb")

    # Create a new encoding called 'CP1251'
    cyrenc = pdfmetrics.Encoding("CP1251")

    # Fill in the tuple with Unicode glyphs in accordance with cp1251 (win1251)
    # encoding
    cp1251 = (
        "afii10051",
        "afii10052",
        "quotesinglbase",
        "afii10100",
        "quotedblbase",
        "ellipsis",
        "dagger",
        "daggerdbl",
        "Euro",
        "perthousand",
        "afii10058",
        "guilsinglleft",
        "afii10059",
        "afii10061",
        "afii10060",
        "afii10145",
        "afii10099",
        "quoteleft",
        "quoteright",
        "quotedblleft",
        "quotedblright",
        "bullet",
        "endash",
        "emdash",
        "tilde",
        "trademark",
        "afii10106",
        "guilsinglright",
        "afii10107",
        "afii10109",
        "afii10108",
        "afii10193",
        "space",
        "afii10062",
        "afii10110",
        "afii10057",
        "currency",
        "afii10050",
        "brokenbar",
        "section",
        "afii10023",
        "copyright",
        "afii10053",
        "guillemotleft",
        "logicalnot",
        "hyphen",
        "registered",
        "afii10056",
        "degree",
        "plusminus",
        "afii10055",
        "afii10103",
        "afii10098",
        "mu1",
        "paragraph",
        "periodcentered",
        "afii10071",
        "afii61352",
        "afii10101",
        "guillemotright",
        "afii10105",
        "afii10054",
        "afii10102",
        "afii10104",
        "afii10017",
        "afii10018",
        "afii10019",
        "afii10020",
        "afii10021",
        "afii10022",
        "afii10024",
        "afii10025",
        "afii10026",
        "afii10027",
        "afii10028",
        "afii10029",
        "afii10030",
        "afii10031",
        "afii10032",
        "afii10033",
        "afii10034",
        "afii10035",
        "afii10036",
        "afii10037",
        "afii10038",
        "afii10039",
        "afii10040",
        "afii10041",
        "afii10042",
        "afii10043",
        "afii10044",
        "afii10045",
        "afii10046",
        "afii10047",
        "afii10048",
        "afii10049",
        "afii10065",
        "afii10066",
        "afii10067",
        "afii10068",
        "afii10069",
        "afii10070",
        "afii10072",
        "afii10073",
        "afii10074",
        "afii10075",
        "afii10076",
        "afii10077",
        "afii10078",
        "afii10079",
        "afii10080",
        "afii10081",
        "afii10082",
        "afii10083",
        "afii10084",
        "afii10085",
        "afii10086",
        "afii10087",
        "afii10088",
        "afii10089",
        "afii10090",
        "afii10091",
        "afii10092",
        "afii10093",
        "afii10094",
        "afii10095",
        "afii10096",
        "afii10097",
    )

    # Replace glyphs from code 128 to code 256 with cp1251 values
    for i in range(128, 256):
        cyrenc[i] = cp1251[i - 128]

    # Register newly created encoding
    pdfmetrics.registerEncoding(cyrenc)

    # Register type face
    pdfmetrics.registerTypeFace(cyrFace)

    # Register the font with adding '1251' to its name
    pdfmetrics.registerFont(
        pdfmetrics.Font(faceName + "1251", faceName, "CP1251")
    )

    # Use this font and set font size
    c.setFont(faceName + "1251", 18)
    header = "Список покупок сгенерирован на сайте Foodgram"
    # Draw this text at last
    c.drawCentredString(297, 20, header)
    c.line(10, 32, 585, 32)
    for key, ing in enumerate(ingredients):
        c.drawString(
            30,
            60 + 25 * key,
            f'{ing["ingredients__title"]}('
            f'{ing["ingredients__dimension"]}) - {ing["amount"]}',
        )

    # Stop drawing on the current page
    c.showPage()

    # Save pdf file
    c.save()
    buffer.seek(0)
    return buffer
