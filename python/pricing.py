"""Pricing rules for LabShop orders. All amounts are in toman."""
from dataclasses import dataclass, field

BULK_MIN_QTY = 10
BULK_PERCENT = 10
TAX_PERCENT = 9
SHIPPING_FEE = 40_000
FREE_SHIPPING_FROM = 1_000_000


@dataclass
class Item:
    sku: str
    unit_price: int
    qty: int


@dataclass
class Order:
    id: int
    customer: str
    coupon_code: str
    items: list = field(default_factory=list)


@dataclass
class Bill:
    subtotal: int
    discount: int
    tax: int
    shipping: int
    total: int


@dataclass(frozen=True)
class Coupon:
    kind: str  # "percent" or "fixed"
    value: int


COUPONS = {
    "OFF10": Coupon("percent", 10),
    "OFF20": Coupon("percent", 20),
    "FIX50": Coupon("fixed", 50_000),
}


def find_coupon(code):
    return COUPONS.get(code.strip().upper())


def price_order(order):
    subtotal = sum(item.unit_price * item.qty for item in order.items)
    bulk = bulk_discount(order.items)
    coupon = coupon_discount(order, subtotal - bulk)
    taxable = subtotal - bulk - coupon
    tax = tax_for(taxable)
    shipping = shipping_for(taxable)
    return Bill(subtotal, bulk + coupon, tax, shipping, taxable + tax + shipping)


def bulk_discount(items):
    # 10% off every SKU whose total qty in the order is BULK_MIN_QTY or more
    qty_by_sku = {}
    amount_by_sku = {}
    for item in items:
        qty_by_sku[item.sku] = qty_by_sku.get(item.sku, 0) + item.qty
        amount_by_sku[item.sku] = amount_by_sku.get(item.sku, 0) + item.unit_price * item.qty
    discount = 0
    for sku, qty in qty_by_sku.items():
        if qty >= BULK_MIN_QTY:
            discount += amount_by_sku[sku] * BULK_PERCENT // 100
    return discount


def coupon_discount(order, amount):
    if order.coupon_code == "":
        return 0
    coupon = find_coupon(order.coupon_code)
    if coupon is None:
        return 0
    if coupon.kind == "fixed":
        return min(coupon.value, amount)
    return apply_percent(order.items, coupon.value)


def apply_percent(items, percent):
    # lower each unit price so the invoice shows the discounted prices
    discount = 0
    for item in items:
        cut = item.unit_price * percent // 100
        item.unit_price -= cut
        discount += cut * item.qty
    return discount


def tax_for(amount):
    # VAT, rounded to the nearest toman (0.5 rounds up)
    return (amount * TAX_PERCENT + 50) // 100


def shipping_for(amount):
    if amount >= FREE_SHIPPING_FROM:
        return 0
    return SHIPPING_FEE
