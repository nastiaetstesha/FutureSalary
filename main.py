import os

from dotenv import load_dotenv
from superjob import calculate_statistics_sj
from headhunter import calculate_statistics_hh
from utils import display_statistics


def main():
    load_dotenv()
    access_token = os.getenv("SUPERJOB_TOKEN")
    languages = ["Python", "Java", "JavaScript", "C#", "C++", "TypeScript", "PHP", "Ruby", "Go", "Swift"]
    hh_statistics = {}
    sj_statistics = {}

    for language in languages:
        hh_statistics[language] = calculate_statistics_hh(language)

    access_token = "v3.r.138858904.2ed0007cca4f22c7bfdd6f7d4182373153fbc849.ba16a31edfb20164e991f59e3344b4811a00e243"
    for language in languages:
        sj_statistics[language] = calculate_statistics_sj(language, access_token)

    display_statistics(hh_statistics, "HeadHunter Moscow")
    display_statistics(sj_statistics, "SuperJob Moscow")

if __name__ == "__main__":
    main()
