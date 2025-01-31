import requests

from utils import predict_salary


def fetch_all_vacancies_hh(language):
    url = "https://api.hh.ru/vacancies"
    all_vacancies = []
    page = 0
    per_page = 100
    moscow = 1

    while True:
        params = {
            "text": f"Программист {language}",
            "area": moscow,
            "per_page": per_page,
            "page": page
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        vacancies_data = response.json()
        all_vacancies.extend(vacancies_data.get("items", []))

        if page >= vacancies_data.get("pages") - 1:
            break
        page += 1

    return all_vacancies


def extract_salaries_hh(vacancies):
    salaries = []
    for vacancy in vacancies:
        salary = vacancy.get("salary")
        if not salary or salary.get("currency") != "RUR":
            continue

        predicted_salary = predict_salary(salary.get("from"), salary.get("to"))
        if predicted_salary:
            salaries.append(predicted_salary)
    return salaries


def calculate_statistics_hh(vacancies):
    salaries = extract_salaries_hh(vacancies)
    average_salary = int(sum(salaries) / len(salaries)) if salaries else 0

    return {
        "vacancies_found": len(vacancies),
        "vacancies_processed": len(salaries),
        "average_salary": average_salary
    }