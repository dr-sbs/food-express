from decimal import Decimal
from django.conf import settings

from cart.models import Cart as cart_model, CartItem
from coupons.models import Coupon


class Cart(object):
    def __init__(self,request):
        try:
            if request.user.is_customer:
                self.customer = request.user.customer
            try:
                cart = self.customer.cart
            except Exception:
                cart = cart_model.objects.create(customer=self.customer)
            self.cart = cart
        except Exception:
            self.cart = None
        
        # Store the current applied coupon
        # self.coupon_id = self.session.get('coupon_id')

    def add(self, food, quantity=1, override_quantity=False):
        try:
            cart_item = CartItem.objects.get(cart=self.cart, food=food)
        except:
            cart_item = CartItem.objects.create(cart=self.cart, food=food,
                                    quantity=0, price=food.get_selling_price)
        
        if override_quantity:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()
    
    def remove(self, food):
        cart_item = CartItem.objects.get(cart=self.cart, food=food)
        if cart_item:
            cart_item.delete()
    
    def __len__(self):
        cart_items = self.get_all_items()
        return sum(item.quantity for item in cart_items)

    def get_total_price(self):
        cart_items = self.get_all_items()
        return sum(Decimal(item.price) * item.quantity for item in cart_items)
    
    def get_all_items(self):
        return CartItem.objects.filter(cart=self.cart)
    
    def get_foods_list(self):
        cart_items = CartItem.objects.filter(cart=self.cart)
        foods = []
        for item in cart_items:
            foods.append(item.food)
        return foods

    def clear(self):
        self.cart.delete()
    
    def add_coupon(self, coupon_code):
        self.cart.coupon_code = coupon_code
        self.cart.save()

    @property
    def coupon(self):
        if self.cart.coupon_code:
            try:
                return Coupon.objects.get(code__iexact = self.cart.coupon_code)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def clear_coupon(self):
        if self.cart.coupon_code:
            self.cart.coupon_code = ''
            self.cart.save()
        return
    
    def identity(self):
        return self.cart.id

    def get_discount(self):
        if self.cart.coupon_code:
            return round((self.coupon.discount / Decimal(100)) * self.get_total_price(),2)
        return Decimal(0)
    
    def get_total_price_after_discount(self):
        return round(self.get_total_price() - self.get_discount(), 2)
    
    def get_total_price_in_paisa(self):
        return self.get_total_price_after_discount() * 100