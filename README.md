# bili_moren
 膜人经卷



# 简介

一个简单的Python程序

检测到名单内用户投稿，自动在视频下发送彩虹屁评论

使用轮子：

- [bilibili_api](https://github.com/Passkou/bilibili_api/)


# 使用

1.`sample_config.json`：认证信息，监听名单

```json
{
    "secrect": {
        "SESSDATA": "SESSDATA",
        "CSRF": "CSRF"
    },
    "user": [{
            "uid": 114514,
            "name": [
                "可填入多种称呼",
                "a"
            ]
        }
    ]
}
```

获取 SESSDATA 和 CSRF 后填入`BiliVerift`

`uid`内填写监听的用户的`uid`

`name`内填写你对他的称呼方式，可以填写多个

配置后运行`moren.py`即可