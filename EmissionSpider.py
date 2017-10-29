import requests
from scrapy import Selector
import sys
import csv
import re

reload(sys)
sys.setdefaultencoding('utf-8')


def get_text(url):
    req = requests.get(url)
    return req.text


def get_base_page_url(country_code, page):
    base_url = 'http://ec.europa.eu/environment/ets/oha.do?form=oha&languageCode=en&account.registryCodes={' \
               '}&accountHolder=&installationIdentifier=&installationName=&permitIdentifier=&mainActivityType=-1' \
               '&searchType=oha&currentSortSettings=&resultList.currentPageNumber={}&nextList=Next%3E '
    return base_url.format(country_code, page - 1)


def get_detail_page_url(account_id):
    base_url = 'http://ec.europa.eu/environment/ets/ohaDetails.do?accountID={' \
               '}&languageCode=en&action=all&registryCode=DK&returnURL=permitIdentifier%3D%26backList%3DBack' \
               '%26languageCode%3Den%26form%3Doha%26installationName%3D%26accountHolder%3D%26installationIdentifier' \
               '%3D%26resultList.currentPageNumber%3D2%26account.registryCodes%3DDK%26searchType%3Doha' \
               '%26mainActivityType%3D-1%26currentSortSettings%3D '
    return base_url.format(account_id)


def get_uniq(arr):
    res = []
    for each in arr:
        if each not in res:
            res.append(each)
    return res


def get_detail_page(text):
    sel = []
    tb_sel = Selector(text=text).xpath('//td[@class="bgcelllist"]')
    for each in tb_sel:
        t = each.extract()
        info_sel = Selector(text=t).xpath('//span[@class="classictext"]').xpath('string(.)')
        if len(info_sel) == 1:
            sel.append(info_sel[0].extract().strip())
        elif len(info_sel) > 1:
            r = []
            for each in info_sel:
                if each.extract().strip():
                    content = each.extract().strip()
                    num = re.findall('\d+', content)
                    if num:
                        r.append(num[0])
            if not r:
                sel.append('')
            else:
                if int(r[0]) == 0:
                    sel.append(r[-1])
                else:
                    sel.append(r[0])
    info = [sel[5], sel[8], sel[10], sel[11]]
    year = sel[-14 - 96:-14]
    other = [[], [], []]
    for i in range(0, 16):
        other[0].append(year[i * 6 + 0])
        other[1].append(year[i * 6 + 1])
        other[2].append(year[i * 6 + 2])
    info.extend(other[0])
    info.extend(other[1])
    info.extend(other[2])
    return info


def handle_base_page(text):
    info_sel = Selector(text=text).xpath('//span[@class="classictext"]/text()')
    ids_sel = Selector(text=text).xpath('//td[@class="bgtitlelist"]/a/@href').re('.*accountID=(\d+).*')
    ids = get_uniq(ids_sel)
    sel = [each.extract().strip() for each in info_sel]
    info = []
    for i in range(0, len(info_sel), 10):
        a_info = [sel[i + 0], sel[i + 1], sel[i + 2], sel[i + 5], sel[i + 7]]
        a_id = ids[i / 10]
        detail_url = get_detail_page_url(a_id)
        detail_info = get_detail_page(get_text(detail_url))
        a_info.extend(detail_info)
        info.append(a_info)
    return info


if __name__ == '__main__':
    out = open('/Users/Lion/PycharmProjects/germany.csv', 'a')
    csv_writer = csv.writer(out, dialect='excel')
    csv_writer.writerow(
        ['Country', 'Account Type', 'Account Holder Name', 'Company Registration No', 'Permit/Plan Date', 'Account status',
         'Main Address Line', 'Postal Code', 'City', 'Allowance In Allocation In 2005',
         'Allowance In Allocation In 2006',
         'Allowance In Allocation In 2007',
         'Allowance In Allocation In 2008',
         'Allowance In Allocation In 2009',
         'Allowance In Allocation In 2010',
         'Allowance In Allocation In 2011',
         'Allowance In Allocation In 2012',
         'Allowance In Allocation In 2013',
         'Allowance In Allocation In 2014',
         'Allowance In Allocation In 2015',
         'Allowance In Allocation In 2016',
         'Allowance In Allocation In 2017',
         'Allowance In Allocation In 2018',
         'Allowance In Allocation In 2019',
         'Allowance In Allocation In 2020',
         'Verified Emissions In 2005',
         'Verified Emissions In 2006',
         'Verified Emissions In 2007',
         'Verified Emissions In 2008',
         'Verified Emissions In 2009',
         'Verified Emissions In 2010',
         'Verified Emissions In 2011',
         'Verified Emissions In 2012',
         'Verified Emissions In 2013',
         'Verified Emissions In 2014',
         'Verified Emissions In 2015',
         'Verified Emissions In 2016',
         'Verified Emissions In 2017',
         'Verified Emissions In 2018',
         'Verified Emissions In 2019',
         'Verified Emissions In 2020',
         'Units Surrendered In 2005',
         'Units Surrendered In 2006',
         'Units Surrendered In 2007',
         'Units Surrendered In 2008',
         'Units Surrendered In 2009',
         'Units Surrendered In 2010',
         'Units Surrendered In 2011',
         'Units Surrendered In 2012',
         'Units Surrendered In 2013',
         'Units Surrendered In 2014',
         'Units Surrendered In 2015',
         'Units Surrendered In 2016',
         'Units Surrendered In 2017',
         'Units Surrendered In 2018',
         'Units Surrendered In 2019',
         'Units Surrendered In 2020'])
    out.close()
    for i in range(116, 136):
        print i
        url = get_base_page_url('DE', i)
        text = get_text(url)
        info = handle_base_page(text)
        out = open('/Users/Lion/PycharmProjects/germany.csv', 'a')
        csv_writer = csv.writer(out, dialect='excel')
        for each in info:
            csv_writer.writerow(each)
