from selenium import webdriver
import json

driver = webdriver.Firefox()
driver.get("https://snoopsnoo.com/subreddits/")

links = []


def SubcategoryExtractor(id_val):
    id_exp = '//*[@id="' + str(id_val.get_attribute("id")) + '"]/div/div/a'
    subcategory = driver.find_elements_by_xpath(id_exp)
    subcategory_decode = [(subcategory[i].get_attribute("href")).replace("#d_reddit_","") for i in range(len(subcategory))]
    return subcategory_decode


for i in range(1,22):
    search="/html/body/div[2]/div/div[2]/div[1]/div["+str(i)+"]"
    hrefs2 = driver.find_element_by_xpath(search)
    title = driver.find_element_by_xpath(search+'/h2/a/span')
    url = driver.find_element_by_xpath(search+'/h2/a')
    id_val = driver.find_element_by_xpath(search+'/div')
    subcategory_decode=SubcategoryExtractor(id_val)
    sub2 = driver.find_elements_by_xpath('//*[@id="' + str(id_val.get_attribute("id")) + '"]/div/div')
    sub2_decode=[[elem.get_attribute("id"),SubcategoryExtractor(elem)] for elem in sub2 if elem.get_attribute("id") != ""]
    for x in sub2_decode:
        sub3 = driver.find_elements_by_xpath('//*[@id="' + str(x[0]) + '"]/div/div')
        sub3_decode = [[elem.get_attribute("id"), SubcategoryExtractor(elem)] for elem in sub3 if
                       elem.get_attribute("id") != ""]
        x.append(sub3_decode)

    links.append([title.text,url.get_attribute("href"),id_val.get_attribute("id"),subcategory_decode,sub2_decode])
driver.close()

def flatten(A):
    rt = []
    for i in A:
        if isinstance(i,list): rt.extend(flatten(i))
        else: rt.append(i)
    return rt

def url_filter(url,tag):
    if url.startswith("http") and (url.endswith(tag) or url.endswith(tag+'/')) and url != tag:
        return True
    else:
        return False


categories = []
for x in links:
    categories.append(x[0])
tag_url_dict=dict.fromkeys(categories)
for p,l in enumerate(links):
    data=flatten(l)
    tags = []
    urls = []
    category=categories[p]
    for i in range(len(data)):
        if data[i].startswith('d_reddit_'):
            tag=data[i].replace('d_reddit_','')
            tags.append(tag.upper())
            url = list(filter(lambda url: url_filter(url, tag=tag),data))[0]
            urls.append(url)
    zip_data = zip(tags, urls)
    tag_url_dict[category]=dict(zip_data)

json = json.dumps(tag_url_dict)
f = open("tag_url.json","w")
print('Writing to the file ...')
f.write(json)
f.close()
print('Complete')