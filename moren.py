import json
import time
from bilibili_api import utils, video, user, Verify, exceptions
from generater import generate_content, get_random_item


def get_config(key: str):
    """
        key =
            secrect(1): 认证信息
            uesr(2): 用户列表
    """
    if key == 1:
        key = 'secrect'
    elif key == 2:
        key = 'user'
    with open('./config.json', 'r', encoding='utf-8') as f:
        return json.load(f)[key]
    return False


def get_uname(uid: int):
    """
        从config中抽取一个对uid用户的称呼
    """
    return get_random_item(get_config(2)['name'])


def get_new_video(uid: int, verify: utils.Verify = None):
    """
        uid: 用户的id
        verify: 认证信息
    """
    try:
        video_generator = user.get_videos_g(uid=uid, verify=verify)
    except (
        exceptions.BilibiliException,
        exceptions.NetworkException,
        exceptions.NoIdException,
        exceptions.NoPermissionException
    ) as exc:
        with open('./error.log', 'w+', encoding='utf-8') as err:
            err.write(
                '{time}\t\t {error}\n'.format(
                    time=time.strftime('%Y-%m-%d', time.localtime()),
                    error=exc
                )
            )
        return False
    else:
        video = []
        for v in video_generator:
            video.append({
                'aid': v['aid'],
                'pubtime': v['created']
            })
            if len(video) == 3:
                break
        return video


def moren(uname: str, aid: int, verify: utils.Verify):
    """
        uname: 称呼
        aid: 视频av号
        verify: 认证信息
    """
    try:
        video.send_comment(
            text=generate_content(uname),
            aid=aid,
            verify=verify
        )
    except (
        exceptions.BilibiliException,
        exceptions.NetworkException,
        exceptions.NoIdException,
        exceptions.NoPermissionException
    ) as exc:
        with open('./error.log', 'w+', encoding='utf-8') as err:
            err.write(
                '{time}\t\t {error}\n'.format(
                    time=time.strftime('%Y-%m-%d', time.localtime()),
                    error=exc
                )
            )


def run():
    secrect = get_config(1)
    verify = Verify(
        sessdata=secrect['SESSDATA'],
        csrf=secrect['CSRF']
    )
    users = get_config(2)
    new_videos = []
    for u in users:
        u_new_video = get_new_video(u['uid'], verify)
        if u_new_video:
            u_videos = [{
                'uid': u['uid'],
                'video': u_new_video
            }]
            new_videos.extend(u_videos)
    cur_time = time.time()
    mo_count = 0
    for i in new_videos:
        uid = i['uid']
        for v in i['video']:
            if abs(cur_time - v['pubtime']) < 70:
                uname = get_uname(uid)
                moren(
                    uname=uname,
                    aid=v['aid'],
                    verify=verify
                )
                print('\t\t在 {time} 膜了 {name}, AV={aid}'.format(
                    time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                    name=uname,
                    aid=v['aid']
                ))
                mo_count += 1
    if mo_count > 0:
        print('{time}\t膜了{count}次，名单如下：'.format(
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            count=mo_count
        ))
    else:
        print('{time}\t没有人可以膜 -_-!'.format(
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ))


def main():
    while True:
        run()
        time.sleep(60)


if __name__ == '__main__':
    main()
