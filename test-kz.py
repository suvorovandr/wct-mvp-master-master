## Author: Andrey Suvorov
## Date: 03/02/2023
import sqlite3 as sql
import requests
import csv
import os.path
import time


headers_list = ["Brand","Device name", "Base price", "Discout", 'Bonus', "Gift_Details", "Gift_value"]

with open ('price_monitoring.csv', 'a', newline = '', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(headers_list)
input()


def parse_page(addr_list):
    print("Selected region: KZ")
    print("Selected client: Mechta.kz")
    parse_index = 0
    headers = {'Content-type': 'application/json'}
    for default_addr in addr_list:
        parse_index += 1
        ## print("already parsed " + str(parse_index) + " / " + str(len(addr_list)) + " devices", end ='\r')
        url = default_addr
        print(url)
        market_data = requests.get(url).json()
        ## market_data = page.json()
        device_name = market_data['data'].get('name')
        brand_info = market_data['data'].get('stream24').get('brand')
        ids = market_data['data'].get('id')
        api = "https://www.mechta.kz/api/v1/mindbox/actions/product"
        json_data = requests.post(api, headers=headers, json={'product_ids': ids}).json()
        base_price = json_data['data'].get('prices').get('base_price')
        discounted_price = json_data['data'].get('prices').get('discounted_price')
        bonus = json_data['data'].get('bonus')
        gift_data = json_data['data'].get('has_gift')
        print(gift_data)
        gift_array = []
        if gift_data == True:
            gift_object = json_data['data'].get('gifts')
            print(type(gift_object))
            print(gift_object)
            key = list(gift_object.keys())
            print(len(key))
            for i in range(len(key)):
                gift_details = gift_object.get(key[i])
                for i, keys in enumerate(gift_details):
                    keys[i] = gift_details[0]
                    gift_name = keys['name']
                    print(gift_name)
                    gift_array.append(gift_name)
                    print(keys['id'])
                    gift_json = requests.post(api, headers=headers, json={'product_ids': keys['id']}).json()
                    price_available = gift_json['result']
                    print(type(price_available))
                    if price_available == False: 
                        data = [brand_info, device_name, base_price, discounted_price, bonus, gift_array]
                        writer.writerow(data)
                        continue
                    else:
                        gift_base_price = gift_json['data'].get('prices').get('base_price')
                        print(gift_base_price)
                    ##print(brand_info, device_name, base_price, discounted_price, bonus, gift_array, gift_base_price)
                    data = [brand_info, device_name, base_price, discounted_price, bonus, gift_array, gift_base_price]
                    print(parse_index, device_name)
                    writer.writerow(data)
        else: 
            data = [brand_info, device_name, base_price, discounted_price, bonus]
            print(parse_index, device_name)
            ##print(brand_info, device_name, base_price, discounted_price, bonus, gift_array)
            writer.writerow(data)
    print("CSV file already Ok :)                                             ")
            ##data = [device_name, base_price, discounted_price, bonus, gift_array]
            ##write_file.writerow(data)
            ## print(gift_object)
        ## data = [device_name, base_price, discounted_price, bonus, gift_array, gift_base_price]
        ## write_file.writerow(data)

headers_list = ["Brand","Device name", "Base price", "Discout", 'Bonus', "Gift_Details", "Gift_value"]

parse_page(addr_list = ["https://www.mechta.kz/api/v1/product/telefon-sotovyy-vivo-y55-12128gb-ice-dawn-v2154/", "https://www.mechta.kz/api/v1/product/telefon-sotovyy-vivo-v23e-8128gb-dancing-waves-v2116/"])

















