from meety_orm import Minute
import re

def gen_min(full_text):
    minutes_phrases_dict = {'RU01' :r'[Вв]ношу\sв\sпротокол.+?[А-ЯA-Z]',
                            'RU02' :r'[Вв]носим\sв\sпротокол.+?[А-ЯA-Z]',
                            'RU03' :r'[Вв]нести\sв\sпротокол.+?[А-ЯA-Z]',
                            'RU04' :r'|[Дд]обавить\sв\sпротокол.+?[А-ЯA-Z]',
                            'RU05' :r'[Дд]обавил[аи]?\sв\sпротокол.+?[А-ЯA-Z]',
                            'GER01':r'[Pp]rotocol\shinzufügen.+?[А-ЯA-Z]',
                            'FR01' :r'Ajout.{1,3}\sau\sprotocole.+?[А-ЯA-Z]',
                            'ENG01':r'[Aa]dd\sto\sprotocol.+?[А-ЯA-Z]',
                            'ENG02':r'[Aa]dded\sto\sprotocol.+?[А-ЯA-Z]',
                            'ENG03':r'[Aa]dd\sin\sprotocol.+?[А-ЯA-Z]',
                            'ENG04':r'[Aa]dded\sin\sprotocol.+?[А-ЯA-Z]',
                            'ENG05':r'[Aa]dd\sinto\sprotocol.+?[А-ЯA-Z]',
                            'ENG06':r'[Aa]dded\sinto\sprotocol.+?[А-ЯA-Z]'}
    minutes_phrases = '|'.join(minutes_phrases_dict.values())
    return [{'text':x.capitalize()[:-2],
             'sort_num':i} for i,x in enumerate(re.findall(minutes_phrases,full_text))]
