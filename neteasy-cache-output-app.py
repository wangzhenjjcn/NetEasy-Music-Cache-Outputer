#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
import os,sys
import re
import requests
 
UC_PATH =os.path.dirname(os.path.realpath(sys.argv[0]))+ '/'  # 缓存路径 例 D:/CloudMusic/Cache/
MP3_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))+'/'  # 存放歌曲路径
 
class Transform():
    def do_transform(self):
        files = os.listdir(UC_PATH)
        for file in files:
            if file[-2:] == 'uc':  # 后缀uc结尾为歌曲缓存
                print(file)
                song_id = self.get_songid_by_filename(file)
                song_name, singer_name = self.get_song_info(song_id)
                song_name=str(song_name).replace("\xa0"," ").replace("/","-").replace("^","-").replace("*","-").replace("$","-").replace("&","-")
                mp3_file_name = MP3_PATH + '%s - %s.mp3' % (singer_name, song_name)
                if not os.path.exists(mp3_file_name):
                    uc_file = open(UC_PATH + file, mode='rb')
                    uc_content = uc_file.read()
                    mp3_content = bytearray()
                    for byte in uc_content:
                        byte ^= 0xa3
                        mp3_content.append(byte)
                    mp3_file = open(mp3_file_name, 'wb')
                    mp3_file.write(mp3_content)
                    mp3_file.close()
                    uc_file.close()
                print('success %s' % mp3_file_name)
 
    def get_songid_by_filename(self, file_name):
        match_inst = re.match('\d*', file_name)  # -前面的数字是歌曲ID，例：1347203552-320-0aa1
        if match_inst:
            return match_inst.group()
        return ''
 
    def get_song_info(self, song_id):
        if not song_id:
            return str(song_id), ''
 
        try:
            url = 'https://api.imjad.cn/cloudmusic/'  # 请求url例子：https://api.imjad.cn/cloudmusic/?type=detail&id=1347203552
            payload = {'type': 'detail', 'id': song_id}
            reqs = requests.get(url, params=payload)
            jsons = reqs.json()
            song_name = jsons['songs'][0]['name']
            singer = jsons['songs'][0]['ar'][0]['name']



            return song_name, singer
        except:
            return str(song_id), ''
 
def check_path():
    global UC_PATH, MP3_PATH
 
    if not os.path.exists(UC_PATH):
        print('缓存路径错误: %s' % UC_PATH)
        return False
    if not os.path.exists(MP3_PATH):
        print('目标路径错误: %s' % MP3_PATH)
        return False
 
    if UC_PATH[-1] != '/':  # 容错处理 防止绝对路径结尾不是/
        UC_PATH += '/'
    if MP3_PATH[-1] != '/':
        MP3_PATH += '/'
    return True
 
if __name__ == '__main__':
     
    path="~/AppData/Local/Netease/CloudMusic/Cache/Cache"
    chachepath=os.path.expanduser(path)
    if os.path.exists(chachepath):
        print("path founded:[%s]" % (chachepath))
        UC_PATH = chachepath + "/"
 


    if not check_path():
        exit()
 
    transform = Transform()
    transform.do_transform()







 