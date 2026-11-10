# Своя реализация
from serializers.ini_serializer import INI_Serializer
from parsers.hcl_parser import HCL_Parser
from serializers.xml_serializer import XML_Serializer

# Десериалзиция HCL - Обязательное
with open("data/schedule.hcl", 'r', encoding="utf-8") as file:
    text = file.read()
    myHCL = HCL_Parser(text).parse()

# Сериализация в INI - Доп 1
with open("data/schedule.ini", 'w', encoding="utf-8") as file:
    myINI = INI_Serializer().serialize(myHCL)
    file.write(myINI)

# Сериализация в XML - Доп 3
with open("data/schedule.xml", 'w', encoding="utf-8") as file:
    myXML = XML_Serializer().serialize(myHCL)
    file.write(myXML)



# Готовая реалиация - Доп 2
import hcl2
from hcl2 import SerializationOptions
import configparser
from serializers.stupid_ini_serializer import create_ini

# Десереализация HCL
with open("data/schedule.hcl", 'r', encoding="utf-8") as file:
    HCL = hcl2.load(
        file,
        serialization_options=SerializationOptions(
            strip_string_quotes=True, # Делаем так, чтобы в объекте было не '"строка"', а обычные строки "строка"
            with_comments=False,      # Чтобы он не сохранял комментарии в объект
        )
    )

print(myHCL == HCL) # Проверка, что они похожи

# Сереализация в INI
config = configparser.ConfigParser(interpolation=None)

create_ini(HCL, "schedule", config)

with open("data/schedule_stupid.ini", 'w', encoding="utf-8") as file:
    config.write(file)