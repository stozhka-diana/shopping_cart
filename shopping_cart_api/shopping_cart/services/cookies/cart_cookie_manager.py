class CartCookieManager:
    """
    Manages shopping cart id in the request cookies.
    """

    def __init__(self, response_cookies: dict):
        self.cart_cookie_name = 'cart_id'
        self.cookies = response_cookies

    def get_shopping_cart_id(self) -> str | None:
        """
        Returns the shopping cart id if it is in request cookies. Otherwise,
        returns `None`.
        """
        return self.cookies.get(self.cart_cookie_name)

    def set_shopping_cart_id(self, shopping_cart_id: str):
        """
        Sets the shopping cart id in request cookies. Even if the
        such cookie is already exists, it will update it.
        """
        self.cookies[self.cart_cookie_name] = shopping_cart_id
