import site_api
import configparser
import os
import json
import traceback


def initial():
    if 'ggn_links.txt' not in os.listdir():
        with open('ggn_links.txt', 'w'):
            pass

    if 'cookies.json' not in os.listdir() or 'config.ini' not in os.listdir():
        if 'cookies.json' not in os.listdir():
            print('检测到cookies文件不存在，请手动输入cookies：')
            ggn_cookie = input('请输入GGn的cookie：')
            pter_cookie = input('请输入PTer的cookie：')
            cookies = {"ggn": ggn_cookie, "pter": pter_cookie}
            with open('cookies.json', 'w') as coo:
                json.dump(cookies, coo)

        if 'config.ini' not in os.listdir():
            print('检测到config文件不存在，接下来将引导生成配置文件')
            config = configparser.ConfigParser()
            passkey = input('请输入猫站passkey：')
            anonymous = input('是否匿名发布(yes/no)：')
            torrent_dir = input('请输入种子下载路径，默认为当前目录下的torrents文件夹:')
            elite_gamer = input('是否为GGn elite gamer 及以上(yes/no 默认为是)')
            ggn_api = input('请输入ggn的apikey，留空则放弃输入：')
            if torrent_dir == '':
                torrent_dir = 'torrents'
            if elite_gamer != 'no':
                elite_gamer = 'yes'
            config['PTER'] = {'pter_key': passkey, 'anonymous': anonymous}
            config['WORKDIR'] = {'torrent_dir': torrent_dir}
            config['GGN'] = {'elite_gamer':elite_gamer,'ggn_api':ggn_api}
            config.write(open('config.ini', 'w'))
        print('初始化完毕，请重新运行！')
        exit()


if __name__ == "__main__":
    initial()
    ggn_link = input('请输入一个GGn种子下载连接或者直接回车开始扫描\'ggn_links.txt\'文件：')
    if ggn_link == '':
        with open('ggn_links.txt') as games:
            ggn_links = games.read().splitlines()
    else:
        ggn_links = [ggn_link]
    for ggn_link in ggn_links.copy():
        ggn = site_api.GGnApi(ggn_link)
        try:
            ggn_info = ggn.worker()
        except Exception:
            print('获取ggn信息出错：{}'.format(traceback.format_exc()))
            continue
        pter = site_api.PTerApi(ggn_info)
        try:
            pter.worker()
        except ValueError:
            print('上传至猫站出错{}'.format(traceback.format_exc()))
            continue
        ggn_links.remove(ggn_link)
    with open('ggn_links.txt', 'w') as gls:
        for link in ggn_links:
            gls.write(link + '\n')
    input('列队完成，输入任意字符退出')
