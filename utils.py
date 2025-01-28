from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):

    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    return None


def display_statistics(statistics, title):

    table_data = [["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for language, stats in statistics.items():
        table_data.append([
            language,
            stats["vacancies_found"],
            stats["vacancies_processed"],
            stats["average_salary"]
        ])
    table = AsciiTable(table_data, title=title)
    print(table.table)
