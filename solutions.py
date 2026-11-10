# Своя реализация
from typing import Any
from serializers.ini_serializer import INI_Serializer
from parsers.hcl_parser import HCL_Parser

with open("data/schedule.hcl", 'r', encoding="utf-8") as file:
    text = file.read()
    myHCL = HCL_Parser(text).parse()

with open("data/schedule.ini", 'w', encoding="utf-8") as file:
    myINI = INI_Serializer().serialize(myHCL)
    file.write(myINI)

# Готовая реалиация
import hcl2
from hcl2 import SerializationOptions

with open("data/schedule.hcl", 'r', encoding="utf-8") as file:
    HCL = hcl2.load(
        file,
        serialization_options=SerializationOptions(
            strip_string_quotes=True, # Делаем так, чтобы в объекте было не '"строка"', а обычные строки "строка"
            with_comments=False,      # Чтобы он не сохранял комментарии в объект
        )
    )

print(myHCL == HCL)

import configparser
from serializers.stupid_ini_serializer import create_ini

config = configparser.ConfigParser(interpolation=None)

create_ini(HCL, "schedule", config)

with open("data/schedule_stupid.ini", 'w', encoding="utf-8") as file:
    config.write(file)

# XML - своё решение

from serializers.xml_serializer import XML_Serializer

with open("data/schedule.xml", 'w', encoding="utf-8") as file:
    myXML = XML_Serializer().serialize(myHCL)
    file.write(myXML)