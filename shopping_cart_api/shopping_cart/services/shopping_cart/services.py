from shopping_cart.models import ShoppingCart, OrderedProduct


def update_products_quantity_in_cart(cart: ShoppingCart, update_products_info: list[dict]):
    """
    Updates product quantity in the shopping cart.
    """
    product_slug_with_updated_quantity = {
        product['slug']: product['quantity'] for product in update_products_info
    }
    altered_products = []
    for ordered_product in cart.ordered_products.filter(product__slug__in=product_slug_with_updated_quantity):
        ordered_product.quantity = product_slug_with_updated_quantity[ordered_product.product.slug]
        altered_products.append(ordered_product)
    OrderedProduct.objects.bulk_update(altered_products, ['quantity'])
    return altered_products


def delete_products_from_shopping_cart(cart: ShoppingCart, products_to_delete: list[dict]):
    """
    Deletes products from shopping cart. Affects only those records, which
    are in the `products_to_delete` argument.
    """
    deleted_products = cart.ordered_products.filter(
        product__slug__in=[product['slug'] for product in products_to_delete]
    )
    return deleted_products.delete()[0]


def create_shopping_cart() -> ShoppingCart:
    """
    Creates and returns new shopping cart instance.
    """
    return ShoppingCart.objects.create()
