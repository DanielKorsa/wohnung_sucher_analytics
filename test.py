

# real_prices = []
# prices = ['1.160', '650','874,50', '1.012,77']

# def clean_prices(prices):
#     real_prices = []

#     for price in prices:

#         if '.' in price:

#             clean_price = price.replace('.', '')
            
#             if ',' in clean_price:
#                 real_prices.append(int(clean_price.split(',')[0]))

#             else:
#                 real_prices.append(int(clean_price))

#         elif ',' in price:
#                 real_prices.append(int(price.split(',')[0]))

#         else:
#             real_prices.append(int(price))
                

#     return real_prices



price = '808 €'

a = price.split(' ')[0]
print(a)
