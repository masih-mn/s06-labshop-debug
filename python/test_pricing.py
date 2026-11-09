import unittest

from pricing import Item, Order, price_order, shipping_for, tax_for


class PriceOrderTest(unittest.TestCase):
    def test_order_without_coupon(self):
        order = Order(1, "test", "", [Item("A01", 100_000, 2), Item("B01", 50_000, 1)])
        bill = price_order(order)
        self.assertEqual(bill.subtotal, 250_000)
        self.assertEqual(bill.discount, 0)
        self.assertEqual(bill.tax, 22_500)
        self.assertEqual(bill.shipping, 40_000)
        self.assertEqual(bill.total, 312_500)

    def test_fixed_coupon(self):
        order = Order(2, "test", "FIX50", [Item("A01", 300_000, 1)])
        bill = price_order(order)
        self.assertEqual(bill.discount, 50_000)
        self.assertEqual(bill.total, 312_500)

    def test_percent_coupon(self):
        order = Order(3, "test", "OFF10", [Item("A01", 200_000, 1)])
        bill = price_order(order)
        self.assertEqual(bill.discount, 20_000)
        self.assertEqual(bill.total, 236_200)

    def test_bulk_discount_counts_same_sku_across_lines(self):
        # BUG-2: order 1047, 6 + 6 = 12 units of K07 on two lines
        order = Order(1047, "parisa", "", [
            Item("K07", 38_500, 6),
            Item("M21", 12_990, 1),
            Item("K07", 38_500, 6),
        ])
        bill = price_order(order)
        self.assertEqual(bill.subtotal, 474_990)
        self.assertEqual(bill.discount, 46_200)
        self.assertEqual(bill.total, 507_381)


class ShippingTest(unittest.TestCase):
    def test_free_shipping_from_one_million(self):
        self.assertEqual(shipping_for(999_990), 40_000)
        self.assertEqual(shipping_for(1_000_000), 0)


class TaxTest(unittest.TestCase):
    def test_tax_is_nine_percent(self):
        self.assertEqual(tax_for(1_000), 90)

    def test_tax_is_rounded_to_nearest_toman(self):
        self.assertEqual(tax_for(1_010), 91)  # 90.9
        self.assertEqual(tax_for(1_030), 93)  # 92.7


if __name__ == "__main__":
    unittest.main()
