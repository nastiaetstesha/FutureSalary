import requests

from utils import predict_salary


def fetch_all_vacancies_hh(language):
    url = "https://api.hh.ru/vacancies"
    all_vacancies = []
    page = 0
    per_page = 100

    while True:
        params = {
            "text": f"Программист {language}",
            "area": 1,
            "per_page": per_page,
            "page": page
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Ошибка: {response.status_code}, {response.text}")

        data = response.json()
        all_vacancies.extend(data.get("items", []))

        if page >= data.get("pages") - 1:
            break
        page += 1

    return all_vacancies, data.get("found", 0)


def calculate_statistics_hh(language):
    vacancies, vacancies_found = fetch_all_vacancies_hh(language)
    salaries = []
    for vacancy in vacancies:
        salary = vacancy.get("salary")
        if salary and salary.get("currency") == "RUR":
            salary = predict_salary(salary.get("from"), salary.get("to"))
            if salary is not None:
                salaries.append(salary)

    average_salary = int(sum(salaries) / len(salaries)) if salaries else 0

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": len(salaries),
        "average_salary": average_salary
    }
