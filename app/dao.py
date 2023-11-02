from app.models import Categories, Product

def load_categories():
   return Categories.query.all()


def load_products(kw=None):
    products = Product.query

    if kw:
        products = products.filter(Product.name.contains(kw))

    return products.all()