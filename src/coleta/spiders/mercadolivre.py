import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida?matt_tool=86626453&matt_word=Default_URL_MLB&matt_source=google&matt_campaign_id=11616247427&matt_ad_group_id=111803272303&matt_match_type=p&matt_network=g&matt_device=c&matt_creative=479753867413&matt_keyword=t%C3%AAnis%20de%20corrida%20mercado%20livre&matt_ad_position=&matt_ad_type=&matt_merchant_id=&matt_product_id=&matt_product_partition_id=&matt_target_id=aud-2009166904988:kwd-1018889522096&cq_src=google_ads&cq_cmp=11616247427&cq_net=g&cq_plt=gp&cq_med=&gad_source=1&gclid=CjwKCAiA9IC6BhA3EiwAsbltOEKI5CGsgACO8Kv4a4yQDmXyXixChQ3LicyO7eJKgiQLVLeTngSAuxoCubsQAvD_BwE"]
    page_count = 1
    max_pages = 20
    def parse(self, response):
        products = response.css('div.poly-card__content') #54 products
    
        for product in products:
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()
            yield {
                 'brand': product.css('span.poly-component__brand::text').get(),
                 'name': product.css('h2.poly-box.poly-component__title::text').get(),
                 'old_price_reais': prices[0] if len(prices) > 0 else None,
                 'old_price_centavos': cents[0] if len(cents) > 0 else None,
                 'new_price_reais': prices[1] if len(prices) > 1 else None,
                 'new_price_centavos': cents[1] if len(cents) > 1 else None,
                 'reviews_rating_number': product.css('span.poly-reviews__rating::text').get(),
                 'reviews_amount': product.css('span.poly-reviews__total::text').get()
            }

        if self.page_count < self.max_pages:      
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)    