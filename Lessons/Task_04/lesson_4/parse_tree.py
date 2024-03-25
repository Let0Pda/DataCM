from lxml import etree


def print_tree(element, depth=0):
    """Рекурсивная функция для вывода дерева XML в консоль"""
    # Вывод текущего элемента с соответствующим отступом
    print("-" * depth, element.tag)

    # Рекурсивно выводить все его дочерние элементы с увеличенным отступом
    for child in element:
        print_tree(child, depth + 1)


# Парсинг XML-файла
data = r"D:\GitTest\DataC&M\DataCM\Lessons\Task_04\lesson_4/src/"
tree = etree.parse(f"{data}web_page.html")

# Получение корневого элемента дерева XML
root = tree.getroot()

# Вывод структуры дерева XML в консоль
print_tree(root)
