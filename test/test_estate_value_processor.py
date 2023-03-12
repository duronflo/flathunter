import unittest
from functools import reduce
from flathunter.estate_value_processor import HomeDayGetEstateValueProcessor
from flathunter.logging import logger, configure_logging, LoggerHandler
from test.utils.config import StringConfig
import logging
import sys

class HomeDayGetEstateValueProcessorTest(unittest.TestCase):
    TEST_URL1 = 'https://www.homeday.de/de/preisatlas/68259?map_layer=standard&marketing_type=sell&property_type=apartment'
    TEST_URL2 = 'https://www.homeday.de/de/preisatlas/68259?map_layer=standard&marketing_type=rent&property_type=apartment'
       
    DUMMY_CONFIG = """
    urls:
      - https://www.wg-gesucht.de/wohnungen-in-Munchen.90.2.1.0.html
        """

    def setUp(self):
        self.GetEstateValueProcessor = HomeDayGetEstateValueProcessor(StringConfig(string=self.DUMMY_CONFIG))
        self.log = logging.getLogger("Unittest.Logger")

    def test_get_estate_values_sell(self):
        plz = '86650'
        value = self.GetEstateValueProcessor.get_data_sell_values(plz)
        logger.info('For %s the sell value is %f', plz, value)
        self.assertEqual( value, 4000 )

    def test_get_estate_values_rent(self):
        plz = '86650'
        value = self.GetEstateValueProcessor.get_data_rent_values(plz)
        logger.info('For %s the rent value is %f', plz, value)
        self.assertEqual( value, 9.8 )

    def test_get_estate_values_rent_with_wrong_input(self):
        value = self.GetEstateValueProcessor.get_data_rent_values('99999')
        self.assertEqual( value, -2 )    


if __name__ == '__main__':
    # Setup Flathunter logger
    logger_handler = LoggerHandler()
    logging.basicConfig(level=logging.INFO, handlers=[logger_handler])
    logger = logging.getLogger('flathunt_testcase')
    
    unittest.main()