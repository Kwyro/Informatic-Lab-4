from io import StringIO
import hcl2
from hcl2 import SerializationOptions
import configparser

from serializers.ini_serializer import INI_Serializer
from parsers.hcl_parser import HCL_Parser
from serializers.stupid_ini_serializer import create_ini

from time import perf_counter

options = SerializationOptions(
            strip_string_quotes=True, # Делаем так, чтобы в объекте было не '"строка"', а обычные строки "строка"
            with_comments=False,      # Чтобы он не сохранял комментарии в объект
        )

def own_hcl_to_ini(text: str) -> str:
    """Своя реализация HCL -> INI"""
    data = HCL_Parser(text).parse()
    return INI_Serializer().serialize(data)

def library_hcl_to_ini(text: str) -> str:
    data = hcl2.loads(
        text,
        serialization_options=options
    )

    config = configparser.ConfigParser(interpolation=None)
    create_ini(data, "schedule", config)

    out = StringIO()
    config.write(out)

    return out.getvalue() 

with open("data/schedule.hcl", 'r', encoding="utf-8") as file:
    text = file.read()

# Проврека собственной реализации
start = perf_counter()

for _ in range(100):
    own_hcl_to_ini(text)

end = perf_counter()
tm = end - start

print(f"Своя реализация HCL -> INI, 100 повторений: {tm:.06f} секунд")

# Проверка готовой реализации
start = perf_counter()

for _ in range(100):
    library_hcl_to_ini(text)

end = perf_counter()
tm = end - start

print(f"Готовая реализация HCL -> INI, 100 повторений: {tm:.06f} секунд")