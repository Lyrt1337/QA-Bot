# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# pipelines.py
from scrapy.pipelines.files import FilesPipeline

class cpipe(FilesPipeline):
    def file_path(self, results, response = None, item = None, *,  info = None):
        return item.get('filename')