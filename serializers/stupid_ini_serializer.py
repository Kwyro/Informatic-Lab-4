def create_ini( data: dict, section: str, config) -> None:

        config.add_section(section)

        # Проход по простым полям
        for key, value in data.items():
            if isinstance(value, list):
                if all( not( isinstance(item, list) or isinstance(item, dict)) for item in value ):
                    config[section][key] = ', '.join(map(str, value))
            elif not isinstance(value, dict):
                config[section][key] = str(value)

        # Проход по вложенным вещам
        for key, value in data.items():
            if isinstance(value, dict):
                create_ini(value, f'{section}.{key}', config)
            elif isinstance(value, list) and len(value) != 0:
                if all(isinstance(item, dict) for item in value):
                    for index, item in enumerate(value):
                        create_ini(item, f'{section}.{key}.{index}', config)