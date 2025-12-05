from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from Workbook import Workbook

def Login(driver,username,password):
    driver.get('https://weibo.com/login.php')
    time.sleep(30)
    user=driver.find_element(By.XPATH,'//input[@id="loginname"]')
    user.send_keys(username)
    passw=driver.find_element(By.XPATH,'//input[@class="W_input"][@type="password"]')
    passw.send_keys(password)
    button=driver.find_element(By.XPATH,'//a[@class="W_btn_a btn_32px"]')
    button.click()
    print('填写验证码或扫描客户端二维码')
    time.sleep(30)

# 将含省份的字符串转为纯省份
def Convert_Province(text):
    province_list=['河北','山西','黑龙江','吉林','辽宁','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','海南','四川','贵州','云南','陕西','甘肃','青海','台湾','内蒙古','广西','西藏','宁夏','新疆','北京','天津','上海','重庆','香港','澳门']
    for province in province_list:
        if(province in text):
            text=province
            return text
    return '无地理位置信息'


# 在新浪微博中搜索关键词并获取评论
def search_weibo(driver, keyword, start_date, end_date, maxnum, ResultSheet):
    print('主题：%s'%keyword)
    for i in range(1,maxnum+1):
        print('正在爬取第%d页'%(i))
        # https://s.weibo.com/weibo?q=疫情&typeall=1&suball=1&timescope=custom:2022-12-01:2023-01-31&Refer=g&page=1
        driver.get('https://s.weibo.com/weibo?q=%s&typeall=1&suball=1&timescope=custom:%s:%s&Refer=g&page=%d'%(keyword,start_date,end_date,i))
        time.sleep(10)
        Links=driver.find_elements(By.CSS_SELECTOR, 'div.from a[target="_blank"]')
        for link in Links:
            link.click()
            time.sleep(1)
        time.sleep(10)
        handles = driver.window_handles
        for j in range(1,len(handles)):
            driver.switch_to.window(handles[j])
            try:
                # 楼主的贴子
                HostText=driver.find_element(By.CSS_SELECTOR,'div.detail_wbtext_4CRf9').text
                HostPosition=driver.find_element(By.CSS_SELECTOR,'div.head-info_ip_3ywCW').text
                ResultSheet.Add_Line(HostText,Convert_Province(HostPosition))
            except:
                print('第%d页没有内容'%j)
            # 评论
            try:
                CommentTexts=driver.find_elements(By.CSS_SELECTOR,'div.text span')
                CommentsPositions=driver.find_elements(By.CSS_SELECTOR,'div.info woo-box-flex woo-box-alignCenter woo-box-justifyBetween div span')
                for k in range(min(len(CommentTexts),len(CommentsPositions))):
                    ResultSheet.Add_Line(CommentTexts[k].text,Convert_Province(CommentsPositions[k].text))
            except:
                print('第%d页没有评论'%j)
        # 关掉这些窗口
        for j in range(len(handles)-1,0,-1):
            driver.switch_to.window(handles[j])
            driver.close()
            time.sleep(1)
        driver.switch_to.window(handles[0])
        time.sleep(10)
    print('爬取完成')


driver=webdriver.Edge()
driver.maximize_window()
ResultSheet=Workbook()
Login(driver,'18367465680','Prily220621')
search_weibo(driver, '疫情', '2022-12-01', '2023-01-01', 50, ResultSheet)
search_weibo(driver, '新冠', '2022-12-01', '2023-01-01', 50, ResultSheet)
ResultSheet.Save('Data/result.xlsx')
driver.quit()