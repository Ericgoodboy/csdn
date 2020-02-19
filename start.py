from scrapy import cmdline
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
cmdline.execute("scarpy crawl classspider".split())