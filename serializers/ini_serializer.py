class INI_Serializer:

    def serialize(self, data: dict) -> str:
        return self.serialize_section(data, "schedule")

    def serialize_section(self, data: dict, section: str) -> str:
        txt = ""

        txt += f'\n[{section}]\n'

        # Проход по простым полям
        for key, value in data.items():
            if isinstance(value, list):
                if all( not( isinstance(item, list) or isinstance(item, dict)) for item in value ):
                    txt += f'{key} = {', '.join(map(str, value))}\n'
            elif not isinstance(value, dict):
                txt += f'{key} = {value}\n'

        # Проход по вложенным вещам
        for key, value in data.items():
            if isinstance(value, dict):
                txt += self.serialize_section(value, f'{section}.{key}')
            elif isinstance(value, list) and len(value) != 0:
                if all(isinstance(item, dict) for item in value):
                    for index, item in enumerate(value):
                        txt += self.serialize_section(item, f'{section}.{key}.{index}')

        return txt