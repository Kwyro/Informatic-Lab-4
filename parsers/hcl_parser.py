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
        ...

    def parse_string(self) -> str:
        """Чтение строки"""
        ...

    def parse_number(self) -> int | float:
        """Чтение числа"""
        ...

    def parse_list(self) -> list:
        """Чтение [...]"""
        ...

    def parse_object(self) -> dict:
        """Чтение {...}. Внутри имена полей и значения"""
        ...

    def parse_value(self):
        """Выбор нужного способа разбора"""
        ...
