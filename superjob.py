import requests

from utils import predict_salary


def fetch_all_vacancies_sj(language, access_token):
    url = "https://api.superjob.ru/2.0/vacancies/"
    all_vacancies = []
    page = 0
    per_page = 100

    while True:
        params = {
            "keyword": f"Программист {language}",
            "town": 4,
            "catalogues": 33,
            "page": page,
            "count": per_page
        }
        headers = {"X-Api-App-Id": access_token}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Ошибка: {response.status_code}, {response.text}")

        data = response.json()
        all_vacancies.extend(data.get("objects", []))

        if not data.get("more"):
            break
        page += 1

    return all_vacancies, data.get("total", 0)


def calculate_statistics_sj(language, access_token):
    vacancies, vacancies_found = fetch_all_vacancies_sj(language, access_token)
    salaries = []
    for vacancy in vacancies:
        payment_from = vacancy.get("payment_from")
        payment_to = vacancy.get("payment_to")
        currency = vacancy.get("currency")
        if currency == "rub":
            salary = predict_salary(payment_from, payment_to)
            if salary is not None:
                salaries.append(salary)

    average_salary = int(sum(salaries) / len(salaries)) if salaries else 0

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": len(salaries),
        "average_salary": average_salary
    }
