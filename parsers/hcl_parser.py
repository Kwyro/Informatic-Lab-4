class HCL_Parser:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def parse(self) -> dict:
        """Разбор всего файла"""
        ...

    def skip_whitespace(self) -> None:
        """Пропускет пробелы, переносы строк и табуляцию"""
        
        while (
                self.pos < len(self.text)
                and self.text[self.pos].isspace()
                ):
            self.pos += 1

    def skip_comment(self) -> None:
        """Пропускает однострочные комментарии"""
        
        while (
                self.pos < len(self.text)
                and self.text[self.pos] != '\n'
                ):
            self.pos += 1

    def skip_multiline_comment(self) -> None:
        """Пропускает многострочные комментарии"""

        self.pos += 2 # Пропускаем открывающиеся /*
        
        while (
                self.pos < len(self.text)
                and self.text[self.pos: self.pos + 2] != "*/"  
                ):
            self.pos += 1

        # Проверка на то, что комментарий закрыли
        if self.pos == len(self.text):
            raise ValueError("Незакрытый многострочный комментарий")

        self.pos += 2 # Пропускаем закрывающие */

    def skip_ignored(self) -> None:
        """Пропускает комментарии и пробельные символы"""

        while (self.pos < len(self.text)):
            self.skip_whitespace()

            if self.text.startswith("#", self.pos):
                self.skip_comment()

            elif self.text.startswith("//", self.pos):
                self.skip_comment()

            elif self.text.startswith("/*", self.pos):
                self.skip_multiline_comment()

            else:
                break

    def expect(self, symbol):
        """Проверка, что на позиции находится ожидаемый символ"""

        if self.pos < len(self.text) and self.text[self.pos] == symbol:
            self.pos += 1
        else:
            raise ValueError("Неправильный символ или текст закончился")

    def parse_identifier(self) -> str:
        """Чтение имени поля"""
        
        identifier = ""

        if self.pos >= len(self.text):
            raise ValueError("Ожидалось имя поля")

        if not (self.text[self.pos].isalpha() or self.text[self.pos] == "_"):
            raise ValueError("Первый символ имени поля должен быть буквой или _")

        while (
            self.pos < len(self.text)
            and (self.text[self.pos].isalnum() or self.text[self.pos] == "_")
        ):
            identifier += self.text[self.pos]
            self.pos += 1

        return identifier

    def parse_string(self) -> str:
        """Чтение строки"""

        escapes = {
            '"': '"',
            "\\": "\\",
            "n": "\n",
            "r": "\r",
            "t": "\t",
        }
        
        string = ""

        self.expect('"')

        while (
            self.pos < len(self.text)
            and self.text[self.pos] != '"'
        ):  
            if self.text[self.pos] == '\\':
                self.pos += 1

                if self.pos >= len(self.text):
                    raise ValueError("Текст закончился после обратной косой черты")
                
                if self.text[self.pos] not in escapes.keys():
                    raise ValueError("Неизвестное экранирование")

                string += escapes[self.text[self.pos]]
            else:
                string += self.text[self.pos]
            
            self.pos += 1

        if self.pos >= len(self.text):
            raise ValueError("Незакрытая строка")

        self.pos += 1 # Пропуск закрывающей ковычки

        return string

    def parse_number(self) -> int | float:
        """Чтение числа"""
        
        number = ""

        if self.pos >= len(self.text):
            raise ValueError("Ожидалось число")

        if self.text[self.pos] == '-':
            number += '-'
            self.pos += 1

        # Проверка целой части

        if self.pos >= len(self.text) or not self.text[self.pos].isdigit():
            raise ValueError("Ожидалась цифра")

        while (
            self.pos < len(self.text)
            and self.text[self.pos].isdigit()
        ):
            number += self.text[self.pos]
            self.pos += 1

        if self.pos < len(self.text) and self.text[self.pos] == '-':
            raise ValueError("Неверный формат числа")

        # Проверка дробной части

        if self.pos < len(self.text) and self.text[self.pos] == '.':
            number += '.'
            self.pos += 1

            if self.pos >= len(self.text) or not self.text[self.pos].isdigit():
                raise ValueError("Ожидалась цифра")

            while (
                self.pos < len(self.text)
                and self.text[self.pos].isdigit()
            ):
                number += self.text[self.pos]
                self.pos += 1

        if self.pos < len(self.text) and self.text[self.pos] in ['.', '-']:
            raise ValueError("Неверный формат числа")

        # Вывод

        if number.count('.') == 1: return float(number)
        
        return int(number)

    def parse_list(self) -> list:
        """Чтение [...]"""
        ...

    def parse_object(self) -> dict:
        """Чтение {...}. Внутри имена полей и значения"""
        ...

    def parse_value(self):
        """Выбор нужного способа разбора"""
        ...
