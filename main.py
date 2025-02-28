# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import struct
import os
import requests
from pypinyin import lazy_pinyin, Style

fullwidth_to_halfwidth = str.maketrans(
    "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｓｙｚ",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")


def getpinyin_initials(text):
    # 去掉字符串中的空格、制表符和换行符
    text = re.sub(r'\s+', '', text)
    # 将全角字符转换为半角字符
    text = text.translate(fullwidth_to_halfwidth)
    # 结果字符串，用来存放拼音首字母
    result = []
    # 遍历每个字符
    for char in text:
        if '\u4e00' <= char <= '\u9fff':  # 判断是否是中文字符
            # 装取拼音的首字母(首字母大写)
            initial = lazy_pinyin(char, style=Style.FIRST_LETTER)[0].upper()
            result.append(initial)
        elif char.isalpha() or char == '*':  # 保留字母和*号
            result.append(char)

    # 将结果连接成字符串返回
    return ''.join(result)


def get_xgb_rdjd():
    url = 'https://flash-api.xuangubao.cn/api/surge_stock/stocks?normal=true&uplimit=true'
    response = requests.get(url)
    items = response.json()['data']['items']
    if items:
        plates_num = {}
        plates_stocks = {}
        for item in items:
            # 检查最后两个字符，并根据规则生成股票代码
            if item[0][-2:] == 'SZ':  # 如果最后两个字符是 'SZ'
                code = '0' + item[0][:6]
            elif item[0][-2:] == 'SS':  # 如果最后两个字符是'SS'
                code = '1' + item[0][:6]
            else:  # 其他情况
                code = '2' + item[0][:6]
            plates = item[8]
            for plate in plates:
                pName = plate['name'].split('/')[0]
                if pName not in ['其他', 'ST股']:
                    if pName in plates_num:
                        plates_num[pName] += 1
                    else:
                        plates_num[pName] = 1

                    if pName in plates_stocks:
                        plates_stocks[pName] += [code]
                    else:
                        plates_stocks[pName] = [code]
        top = sorted(
            (k for k, v in plates_num.items()),  # 筛选值大于5的键
            key=lambda k: plates_num[k],  # 按对应的值排序
            reverse=True  # 降序
        )[:7]
        return plates_stocks, top


def get_map_and_remove_blocks(path):
    """
        获取板块名称与简称的映射关系，并删除特定的热点板块
    """
    # 定义记录格式:50字节的板块名称和70字节的板块简称
    record_format = '<50s70s'
    # 计算记录大小
    record_size = struct.calcsize(record_format)
    # 指定编码方式
    encoding = 'gb2312'
    # 用于存储有效的板块映射
    block_map = []
    # 打开配置文件

    with open(os.path.join(path, 'blocknew.cfg'), 'rb+') as f:
        # 逐条读取记录
        # 逐条读取记录
        while True:
            # 读取一条记录
            record_bytes = f.read(record_size)
            # 如果读取到文件末尾，退出循环
            if not record_bytes:
                break
            # 解析记录
            record = struct.unpack(record_format, record_bytes)
            try:
                # 解码板块名称和简称
                name = record[0].split(b'\0', 1)[0].decode(encoding).strip()
                spell = record[1].split(b'\0', 1)[0].decode(encoding).strip()
            except Exception as e:
                # 捕获解码异常并打印错误信息
                print(f"Error decoding record:{e}")
                continue

            # 判断是否为特定板块
            if name.startswith('RD_') and spell.startswith('RD_'):
                # 构造板块交件路径
                filepath = os.path.join(path, f"{spell}.BLK")
                # 如果板块文件存在
                if os.path.exists(filepath):
                    # 删除板块文件
                    os.remove(filepath)
                    print(f"Deleted block:{name}")
                else:
                    print(f"Block file does not exist:{name}")
            else:
                print(name, spell)
                # 保存有效的板块映射
                block_map.append((name, spell))
    # 返回有效的板块映射
    return block_map


def write_data(path, file_name, data):
    with open(os.path.join(path, file_name + '.blk'), 'w') as file:
        for code in data:
            file.write(code + '\n')


def update_cfg(path, rd_map, block_map):
    map = rd_map + block_map
    # 定义记录格式:50字节的板块名称和70字节的板块简称
    record_format = '<50s70s'
    # 指定编码方式
    encoding = 'gb2312'
    with open(os.path.join(path, 'blocknew.cfg'), 'wb') as f:
        for name, abbr in map:
            name_bytes = name.encode(encoding).ljust(50, b'\0')
            abbr_bytes = abbr.encode(encoding).ljust(70, b'\0')
            f.write(struct.pack(record_format,name_bytes, abbr_bytes))

def get_rd_map_and_write(path, top, p_stocks):
    rd_map =[]
    for rd in top:
        spell ='RD_'+ getpinyin_initials(rd)
        rd_map.append(('RD_'+ rd,spell))
        write_data(path,spell,p_stocks[rd])
    return rd_map



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tdx_path = "F:\\常用软件\\湘财\\T0002\\blocknew"
    block_map = get_map_and_remove_blocks(tdx_path)
    p_stocks, top = get_xgb_rdjd()
    rd_map = get_rd_map_and_write(tdx_path, top, p_stocks)
    update_cfg(tdx_path, rd_map, block_map)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
