import os
import logging

from dataclasses import dataclass
from transformers import BertConfig, BertTokenizer


def init_logger():  # 日志初始化
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)


def get_intent_labels():  # 获取意图标签
    return [label.strip() for label in
            open("api/data/osqa/intent_label.txt", 'r', encoding='utf-8')]


def get_slot_labels():  # 获得槽位标签
    return [label.strip() for label in
            open("api/data/osqa/slot_label.txt", 'r', encoding='utf-8')]


def get_split(text):
    """处理输入文本转为单字序列"""
    temp = []
    for word in text:
        temp.append(word)
    return temp


def load_tokenizer(args):  # 加载分词器
    return BertTokenizer.from_pretrained(args.model_name_or_path)


@dataclass
class PredData:
    sentence: str
    intent_label: str
    slot_words: str
    slot_label: str
