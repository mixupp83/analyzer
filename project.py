import os
import csv
from typing import List, Dict


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path: str) -> List[Dict]:
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Папка не найдена: {file_path}")

        for filename in os.listdir(file_path):
            if 'price' in filename:
                file_path_full = os.path.join(file_path, filename)
                try:
                    with open(file_path_full, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file, delimiter=',')
                        for row in reader:
                            product_name = self._get_value(row, ["название", "продукт", "товар", "наименование"])
                            price = self._get_value(row, ["цена", "розница"])
                            weight = self._get_value(row, ["фасовка", "масса", "вес"])
                            if product_name and price and weight:
                                self.data.append({
                                    "наименование": product_name,
                                    "цена": float(price),
                                    "вес": float(weight),
                                    "файл": filename,
                                    "цена за кг": float(price) / float(weight)
                                })
                except Exception as e:
                    print(f"Ошибка при чтении файла {filename}: {e}")
        return self.data

    def _get_value(self, item: Dict[str, str], keys: List[str]) -> str:
        for key in keys:
            if key in item:
                return item[key]
        return None

    def export_to_html(self, fname: str = 'output.html') -> str:
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table border='0'>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for idx, item in enumerate(sorted(self.data, key=lambda x: x["цена за кг"]), start=1):
            result += f'''
                <tr>
                    <td>{idx}</td>
                    <td>{item['наименование']}</td>
                    <td>{item['цена']}</td>
                    <td>{item['вес']}</td>
                    <td>{item['файл']}</td>
                    <td>{item['цена за кг']:.2f}</td>
                </tr>
            '''
        result += '''
            </table>
        </body>
        </html>
        '''
        with open(fname, 'w', encoding='utf-8') as html_file:
            html_file.write(result)
        return result

    def find_text(self, text: str) -> List[Dict]:
        results = []
        for item in self.data:
            if text.lower() in item['наименование'].lower():
                results.append(item)
        return sorted(results, key=lambda x: x["цена за кг"])

    def interactive_search(self):
        while True:
            search_text = input("Введите текст для поиска (или 'exit' для выхода): ")
            if search_text.lower() == 'exit':
                print("Работа завершена.")
                break
            results = self.find_text(search_text)
            if results:
                print(f"{'№':<5}{'Наименование':<40}{'цена':<10}{'вес':<10}{'файл':<15}{'цена за кг.':<10}")
                for idx, item in enumerate(results, start=1):
                    print(
                        f"{idx:<5}{item['наименование']:<40}{item['цена']:<10.2f}{item['вес']:<10.2f}{item['файл']:<15}{item['цена за кг']:<10.2f}")
            else:
                print("Ничего не найдено.")


if __name__ == "__main__":
    folder_path = input("Введите путь к папке с файлами: ")
    pm = PriceMachine()
    try:
        print(pm.load_prices(file_path=folder_path))
        pm.export_to_html()
        pm.interactive_search()
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    print('the end')