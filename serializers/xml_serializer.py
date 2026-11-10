class XML_Serializer:
    def serialize(self, data: dict) -> str:
        return self.serializer_section(data, "schedule")

    def serializer_section(self, data: dict, section: str, level: int = 0) -> str:
        txt = ""

        if level == 0:
            txt += '<?xml version="1.0" encoding="UTF-8"?>\n'

        txt += "\t" * level + f"<{section}>\n" # Открывает тег

        # Проход по простым полям и спискам
        for key, value in data.items():
            if isinstance(value, list):
                if all( not( isinstance(item, list) or isinstance(item, dict)) for item in value ):
                    txt += "\t" * (level + 1) + f"<{key}>\n" # Открываем список

                    for item in value:
                        txt += "\t" * (level + 2) + f"<item>{item}</item>\n"

                    txt += "\t" * (level + 1) + f"</{key}>\n" # Закрываем список
            elif not isinstance(value, dict):
                txt += "\t" * (level + 1) + f"<{key}>{value}</{key}>\n"


        # Проход по вложенным полям
        for key, value in data.items():
            if isinstance(value, dict):
                txt += self.serializer_section(value, key, level + 1)
            elif isinstance(value, list) and len(value) != 0:
                if all( isinstance(item, dict) for item in value):
                    txt += "\t" * (level + 1) + f"<{key}>\n" # Открываем список

                    for obj in value:
                        txt += self.serializer_section(obj, "item", level + 2)

                    txt += "\t" * (level + 1) + f"</{key}>\n" # Закрываем список

        txt += "\t" * level +  f"</{section}>\n" # Закрывает тег

        return txt