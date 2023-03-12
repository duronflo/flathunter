import unittest
import yaml
import re
from flathunter.crawl_immowelt import CrawlImmowelt
from flathunter.hunter import Hunter
from flathunter.idmaintainer import IdMaintainer
from flathunter.processor import ProcessorChain, AddressResolver
from test.dummy_crawler import DummyCrawler
from test.test_util import count
from test.utils.config import StringConfig
from flathunter.logging import logger, configure_logging, LoggerHandler
import logging




class ProcessorTest(unittest.TestCase):

    DUMMY_CONFIG = """
urls:
  - https://www.example.com/liste/berlin/wohnungen/mieten?roomi=2&prima=1500&wflmi=70&sort=createdate%2Bdesc

google_maps_api:
  key: SOME_KEY
  url: https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={dest}&mode={mode}&sensor=true&key={key}&arrival_time={arrival}
  enable: true
    """

    # def test_addresses_are_processed_by_hunter(self):
    #     config = StringConfig(string=self.DUMMY_CONFIG)
    #     config.set_searchers([DummyCrawler(addresses_as_links=True)])
    #     hunter = Hunter(config, IdMaintainer(":memory:"))
    #     exposes = hunter.hunt_flats()
    #     self.assertTrue(count(exposes) > 4, "Expected to find exposes")
    #     for expose in exposes:
    #         self.assertFalse(expose['address'].startswith('http'), "Expected addresses to be processed by default")

    
    def test_extract_plz_success(self):
        self.AdressResolver = AddressResolver(self.DUMMY_CONFIG)
        string = 'This some text and within the text is a plz (86650) hidden.'
        plz = self.AdressResolver.extract_plz(string)
        logger.info('The plz %s was extracted from: %s', plz, string)
        self.assertTrue(plz, '86650')

    def test_extract_no_plz(self):
        self.AdressResolver = AddressResolver(self.DUMMY_CONFIG)
        string = 'This some text and within the text is a plz (77) hidden.'
        plz = self.AdressResolver.extract_plz(string)
        logger.info('The plz %s was extracted from: %s', plz, string)
        self.assertTrue(plz, '0')
    
    def test_address_processor(self):
        crawler = DummyCrawler(addresses_as_links=True)
        config = StringConfig(string=self.DUMMY_CONFIG)
        config.set_searchers([crawler])
        exposes = crawler.get_results("https://www.example.com/search")
        for expose in exposes:
            self.assertTrue(expose['address'].startswith('http'), "Expected addresses not yet to be processed")
        chain = ProcessorChain.builder(config) \
            .resolve_addresses() \
            .build()
        exposes = chain.process(exposes)
        for expose in exposes:
            self.assertFalse(expose['address'].startswith('http'), "Expected addresses to be processed")



if __name__ == '__main__':
    # Setup Flathunter logger
    logger_handler = LoggerHandler()
    logging.basicConfig(level=logging.INFO, handlers=[logger_handler])
    logger = logging.getLogger('flathunt_testcase')
    
    unittest.main()
