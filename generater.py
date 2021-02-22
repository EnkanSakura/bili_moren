import random
from chp import CHP, QH, partStart, partEnd, sentenceStart, sentenceEnd

startProb = 30
endProb = 30


def is_in_array(arr: list, value):
    for i in arr:
        if value == i:
            return True
    return False


def add_dot(str: str):
    """
        给句子加上结尾的句号
        str: 句子
    """
    if not is_in_array(['，', '。', '？'], str[len(str) - 1]):
        str += '。'
    return str


def get_random(start: int = 0, stop: int = 100):
    """
    default:
        start = 0
        stop = 100
    """
    return random.randrange(start=start, stop=stop)


def get_random_thing(arr: list, name: str):
    """
        arr: 传入句子列表
        name: 被膜人的名字
    """
    min = 0
    max = len(arr) - 1
    if max == -1:
        return ''
    random = get_random(min, max)
    result = arr[random].replace('NAME', name)
    return result


def get_random_item(arr: list):
    """
        从指定列表中抽取一项
        arr: 抽取的列表
    """
    return arr[get_random(0, len(arr) - 1)]


def generate_sentence(name: str):
    """
        生成句子
        name: 被膜人的名字
    """
    sentence = ''
    if get_random() > startProb:
        sentence += get_random_thing(sentenceStart, name)
    mainPart = get_random_item([CHP, QH])
    sentence += get_random_thing(mainPart, name)
    if get_random() > endProb:
        sentence += get_random_thing(sentenceEnd, name)
    return add_dot(sentence)


def generate_part(name: str):
    """
        生成段落
        name: 被膜人的名字
    """
    part = ''
    if get_random() > startProb:
        part += get_random_thing(partStart, name)
    sentenceCount = get_random(4, 8)
    for i in range(sentenceCount):
        part += generate_sentence(name)
    if get_random() > endProb:
        part += get_random_thing(partEnd, name)
    return part


def generate_content(name: str):
    """
        生成文章
        name: 被膜人的名字
    """
    content = ''
    for i in range(get_random(2, 5)):
        content += generate_part(name)
    content += add_dot(get_random_thing(CHP, name))
    return content
