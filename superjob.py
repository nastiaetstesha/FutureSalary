import requests

from utils import predict_salary


def fetch_all_vacancies_sj(language, access_token):
    url = "https://api.superjob.ru/2.0/vacancies/"
    all_vacancies = []
    page = 0
    per_page = 100
    moscow = 4
    catalogues_development_id = 33

    while True:
        params = {
            "keyword": f"Программист {language}",
            "town": moscow,
            "catalogues": catalogues_development_id,
            "page": page,
            "count": per_page
        }
        headers = {"X-Api-App-Id": access_token}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        vacancies_data = response.json()
        all_vacancies.extend(vacancies_data.get("objects", []))

        if not vacancies_data.get("more"):
            break
        page += 1

    return all_vacancies


def extract_salaries_sj(vacancies):
    salaries = []
    for vacancy in vacancies:
        payment_from = vacancy.get("payment_from")
        payment_to = vacancy.get("payment_to")
        currency = vacancy.get("currency")

        if currency == "rub":
            predicted_salary = predict_salary(payment_from, payment_to)
            if predicted_salary:
                salaries.append(predicted_salary)

    return salaries


def calculate_statistics_sj(vacancies):
    salaries = extract_salaries_sj(vacancies)
    average_salary = int(sum(salaries) / len(salaries)) if salaries else 0

    return {
        "vacancies_found": len(vacancies),
        "vacancies_processed": len(salaries),
        "average_salary": average_salary
    }