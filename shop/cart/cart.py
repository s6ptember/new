from decimal import Decimal
from django.conf import settings
from main.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self, product, quantity=1, override_quantity=False):
        product_sku = product.sku  # Используем sku вместо id
        if product_sku not in self.cart:
            self.cart[product_sku] = {'quantity': 0,
                                       'price': str(product.price)}
        if override_quantity:
            self.cart[product_sku]['quantity'] = quantity
        else:
            self.cart[product_sku]['quantity'] += quantity
        self.save()
        
        
    def save(self):
        self.session.modified = True


    def remove(self, product):
        product_sku = product.sku  # Используем sku вместо id
        if product_sku in self.cart:
            del self.cart[product_sku]
            self.save()


    def __iter__(self):
        product_skus = self.cart.keys()
        products = Product.objects.filter(sku__in=product_skus)  # Используем sku для выборки
        cart = self.cart.copy()
        for product in products:
            cart[product.sku]['product'] = product  # Добавляем продукт в корзину
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]


    def get_total_price(self):
        total = Decimal('0.00')
        for item in self.cart.values():
            price = Decimal(item['price'])
            quantity = item['quantity']
            product = item.get('product')
            discount = Decimal(product.discount) if product else Decimal('0.00')  # Убедитесь, что discount по умолчанию равен 0
            total += (price - (price * (discount / 100))) * quantity
        return format(total, '.2f')
        