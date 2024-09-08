"""
1.爬取豆瓣的短影评 ----阿甘正传
2.保存在本地.
-------- 只能查看前200条影评
"""

import requests
import re
import time
import random



class Spider_db:
    def __init__(self):
        self.comment_url = "https://movie.douban.com/subject/1292720/comments?start={}&limit=20&status=P&sort=new_score"
        self.comment_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"}

    def get_comment_url(self):
        url_list = []
        for i in range(10):
            url_list.append(self.comment_url.format(i * 20))

        return url_list

    def comment_db(self, url):

        resp = requests.get(url=url, headers=self.comment_headers)

        comments = re.findall('<span class="short">(.*)</span>', resp.content.decode())
        return comments

    def save_text(self, db_text):
        file_path = __file__.replace('豆瓣电影获取.py',"阿甘正传--影评.txt")
        with open(file_path, "a+", encoding="utf-8") as f:
            f.write(db_text)
            f.write("\n")

    def run(self):
        # 1.页面规律总结，得到要爬取数据的页面
        comment_list = self.get_comment_url()
        # 2.准备字符串
        result=''
        # 3.进入阿甘正传页面爬取影评
        for url in comment_list:
            comments = self.comment_db(url)
            page_num = comment_list.index(url) + 1
            for content in comments:
                result+=content
            time.sleep(random.random() * 5)
        # 4.保存在本地
        self.save_text(result)


if __name__ == '__main__':
    spider = Spider_db()
    spider.run()