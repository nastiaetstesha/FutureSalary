import os

from dotenv import load_dotenv
from superjob import fetch_all_vacancies_sj, calculate_statistics_sj
from headhunter import fetch_all_vacancies_hh, calculate_statistics_hh
from utils import display_statistics


def main():
    load_dotenv()
    access_token = os.getenv("SUPERJOB_TOKEN")
    
    if not access_token:
        raise Exception("Токен SuperJob не найден в .env!")

    languages = ["Python", "Java", "JavaScript", "C#", "C++", "TypeScript", "PHP", "Ruby", "Go", "Swift"]
    hh_statistics = {}
    sj_statistics = {}

    for language in languages:
        hh_vacancies = fetch_all_vacancies_hh(language)
        hh_statistics[language] = calculate_statistics_hh(hh_vacancies)
        sj_vacancies = fetch_all_vacancies_sj(language, access_token)
        sj_statistics[language] = calculate_statistics_sj(sj_vacancies)

    display_statistics(hh_statistics, "HeadHunter Moscow")
    display_statistics(sj_statistics, "SuperJob Moscow")


if __name__ == "__main__":
    main()
