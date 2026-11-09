# پاسخ‌ها

- نام: مسیح مهدوی نیا/ ایلیا حبیبیان فرد/ محمدرضا رضویان
- زبان: Python

| باگ | ابزار و چیزی که دیدید | علت ریشه‌ای (یک جمله) | رفع (فایل و تغییر) |
|---|---|---|---|
| BUG-1 | Stack Trace: `AttributeError: 'NoneType' object has no attribute 'kind'` در `pricing.py` خط 75 (`coupon_discount`)؛ داده‌ی مشکل‌دار سفارش 1052 با کوپن `off20` (حروف کوچیک) بود. | `find_coupon` حروف کوچیک و بزرگ و فاصله‌ی اول و آخر کد رو نرمال نمی‌کرد (پس `off20` پیدا نمی‌شد و `None` برمی‌گشت) و `coupon_discount` حالت `None` (کد ناشناخته) رو چک نمی‌کرد. | `python/pricing.py`: `find_coupon` حالا `COUPONS.get(code.strip().upper())` رو برمی‌گردونه و `coupon_discount` برای کوپن ناشناخته `0` برمی‌گردونه. |
| BUG-2 | Breakpoint شرطی روی `order.id == 1047` در `price_order`؛ با Watch دیدم `bulk` برابر `0` بود چون K07 توی دو ردیف جدا (۶ + ۶) اومده بود و هر ردیف جدا با شرط `qty >= 10` سنجیده می‌شد. | `bulk_discount` تعداد رو برای هر ردیف جدا می‌سنجید، نه برای مجموع تعداد هر SKU توی سفارش. | `python/pricing.py`: `bulk_discount` تعداد و مبلغ رو به تفکیک SKU جمع می‌کنه و برای SKUهای با مجموع ۱۰ عدد یا بیشتر ۱۰٪ تخفیف می‌ده. |
| BUG-4 | `git bisect start main v1.0` و `git bisect run python3 -m unittest discover -s python -k TaxTest`؛ Commit `fd7b52c` («refactor: tidy up pricing code») به‌عنوان اولین Commit خراب پیدا شد. | Commit تمیزکاری، گرد کردن مالیات به نزدیک‌ترین تومان رو به تقسیم صحیح ساده (`amount * 9 // 100`) تبدیل کرد که رو به پایین گرد می‌کنه (مثلاً ۹۰٫۹ می‌شه ۹۰). | `python/pricing.py`: `tax_for` حالا `(amount * TAX_PERCENT + 50) // 100` رو برمی‌گردونه (۰٫۵ به بالا). |
| BUG-3 (اختیاری) | Breakpoint روی خط محاسبه‌ی `grand total` در `report.py` و Step Into به `grand_total` و `apply_percent`؛ دیدم `grand_total` برای هر سفارش دوباره `price_order` رو صدا می‌زنه و سفارش‌های با کوپن درصدی (`OFF10` و `OFF20`) توی بار دوم قیمت متفاوتی می‌گیرن. | `apply_percent` قیمت واحد ردیف‌های سفارش (`item.unit_price`) رو تغییر می‌داد، پس بار اول (چاپ ردیف) درست حساب می‌شد ولی بار دوم (توی `grand_total`) روی قیمت‌های قبلاً کم‌شده تخفیف دوباره اعمال می‌شد. | `python/pricing.py`: `apply_percent` دیگه `item.unit_price` رو تغییر نمی‌ده و فقط مبلغ تخفیف رو حساب می‌کنه. |

- نام تست بازتولید BUG-2: `test_bulk_discount_counts_same_sku_across_lines`
- هش `first bad commit` در BUG-4: `fd7b52c23dbffe2b999d6864ee0724b1b8f6f445`