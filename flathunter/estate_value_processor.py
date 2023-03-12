"""Calculate to retrieve value of real estate"""
import datetime
import time
import urllib
import requests

from flathunter.logging import logger
from flathunter.abstract_processor import Processor
from flathunter.abstract_crawler import Crawler


class HomeDayGetEstateValueProcessor(Processor, Crawler):
    """Implementation of Processor class in order to retrieve value for selling and renting of a real estate (currently only zip code is implemented)"""


    def __init__(self, config):
        self.config = config
        

    def process_expose(self, expose):
        """Determine values of an expose"""
        expose['value_sell'] = self.get_data_sell_values(expose['plz'])
        expose['value_rent'] = self.get_data_rent_values(expose['plz'])
        return expose

    def get_data_sell_values(self, address):
        try:
            URL = 'https://www.homeday.de/de/preisatlas/'+address+'?map_layer=standard&marketing_type=sell&property_type=apartment'
            soup = self.get_page(URL)
        except:          
            logger.error('Could not get any data from network ... connected?')
            soup = '-1'
        try:    
            soup= soup.find("p", {"class": "price-block__price__average"}).text.strip().replace('Ø ', '').replace('\xa0€/m²', '').replace('.', '')
        except:
            logger.error('The location is not known or the provider changed its html layout...')
            soup = '-2'
        
        return float(soup)

    def get_data_rent_values(self, address):
        try:
            URL = 'https://www.homeday.de/de/preisatlas/'+address+'?map_layer=standard&marketing_type=rent&property_type=apartment'
            soup = self.get_page(URL)
        except:
            logger.error('Could not get any data from network ... connected?')
            soup = '-1'
        try:    
            soup= soup.find("p", {"class": "price-block__price__average"}).text.strip().replace('Ø ', '').replace('\xa0€/m²', '').replace(',', '')
        except:
            logger.error('The location is not known or the provider changed its html layout...')
            soup = '-2'
        
        return float(soup)
