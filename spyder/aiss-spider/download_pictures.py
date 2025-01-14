import os
import json
import requests
import time
from multiprocessing import Process, Pool, Queue

def get_info():
    """从文件中读取内容"""
    res=[]
    with open('data/info.txt', 'r') as f:
        for line in f:
          data = json.loads(line)
          res.extend(data['data']['list'])
    return res


def get_info_imgs(info):
    """获取要下载的所有图片的url、目录名、要存储的名字"""

    res = []
    for item in info:
        nickname = item['author']['nickname']
        catalog = item['source']['catalog']
        name = item['source']['name']
        issue = item['issue']
        picturecount = item['pictureCount']
        for pic_idx in range(picturecount):
            url = "http://com-pmkoo-img.oss-cn-beijing.aliyuncs.com/picture/%s/%s/%s.jpg" % (catalog, issue, pic_idx)
            directory = os.path.join('data', name, "%s-%s" % (issue, nickname))
            filepath = os.path.join(directory, "%s.jpg" % pic_idx)
            res.append((url, directory, filepath))
    return res

def setup_dir(directory):
    """设置文件夹，文件夹名称为传入的directory，若不存在则会自动创建"""
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            pass
    return True

def download_one(img):
    """ 异步下载每一张图片 """
    url, directory, filepath = img
    # 首先判断文件是否存在
    if os.path.exists(filepath):
        return

    # 设置图片下载的文件夹
    setup_dir(directory)
    rep = requests.get(url)
    print("start download url")
    with open(filepath, 'wb') as f:
        f.write(rep.content)
        print("end download url")


def download(imgs, process):
    """ 并发下载每张图片 """
    start_time = time.time()
    pool = Pool(process)
    for img in imgs:
        pool.apply_async(download_one, (img,))

    pool.close()
    pool.join()
    end_time = time.time()
    print("take %s second to download all imgs " % (end_time - start_time))

if __name__ == '__main__':
    fileData = get_info()
    imgs = get_info_imgs(fileData)
    download(imgs, 10)

