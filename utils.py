from datetime import datetime, timedelta

import pytz
from urllib.parse import urlparse, parse_qs
import dateutil.parser
from requests_html import HTMLSession
import requests
import pandas as pd

# hack to load configuration settings
from local_settings import *

CHANGELOG_URL = "http://nightly.changelog.com/{year:04d}/{month:02d}/{day:02d}/"

utc = pytz.UTC

# you can use the following functions
# fetch_trending_projects_from_changelog
# get_stars_data


def _extract_repository_data(repo_element, data_to_add=None):
    """ private function to extract data from html """
    stats, repo_info = repo_element.find("tr")
    star_info = stats.find("span")
    total_start = star_info[0].text
    new_stars = star_info[1].text

    try:
        if star_info[2].attrs.get("title") == 'Language':
            language = star_info[2].text
            times_listed = 0
        else:
            language = star_info[3].text
            times_listed = int(star_info[2].text)
    except IndexError as ie:
        language = ""
        times_listed = 0

    repo_info_text = repo_info.text.split("\n")

    full_name = repo_info_text[0]
    try:
        desc = repo_info_text[1]
    except IndexError as ie:
        desc = ""

    data_row = {
        "full_name": full_name,
        "desc": desc,
        "total_start": total_start,
        "new_stars": new_stars,
        "language": language,
        "times_listed": times_listed,
    }

    if data_to_add:
        data_row.update(data_to_add)
    return data_row


def fetch_trending_projects_from_changelog(
        start_date=datetime(2018, 1, 1),
        duration_days=30):
    """ used to fetch changelog data
        Parameters:
        start_date: first data extraction date, default 1/1/2018
        duration: duration to extract data for from start_date, default 30 days
    """
    daily_dfs = []
    # remember we start from 0
    for d in range(duration_days + 1):
        dt = timedelta(days=d)
        adate = start_date + dt
        url = CHANGELOG_URL.format(
            year=adate.year, month=adate.month, day=adate.day)

        session = HTMLSession()
        r = session.get(url)
        print("working on ", url)
        first_time = r.html.find("table#top-all-firsts", first=True)
        new_repos = r.html.find("table#top-new", first=True)
        repeat_repos = r.html.find("table#top-all-repeats", first=True)

        my_dfs = []

        if first_time:
            first_time_list = [_extract_repository_data(
                x, {"date": adate, "trending_type": "first_time"})
                for x in first_time.find("div.repository")]
            my_dfs.append(pd.DataFrame(first_time_list))
        if new_repos:
            new_repo_list = [_extract_repository_data(
                x, {"date": adate, "trending_type": "new_repo"})
                for x in new_repos.find("div.repository")]
            my_dfs.append(pd.DataFrame(new_repo_list))
        if repeat_repos:
            repeat_repo_list = [_extract_repository_data(
                x, {"date": adate, "trending_type": "repeat_repo"})
                for x in repeat_repos.find("div.repository")]

            my_dfs.append(pd.DataFrame(repeat_repo_list))

#         return pd.concat(my_dfs)
        daily_dfs.append(pd.concat(my_dfs))

    return pd.concat(daily_dfs)


URL_TEMPLATE = "https://api.github.com/repos/{full_name}"

def get_ghdata_from_fullname(full_name):
    """ fetch GitHub project data for repo by tracing its parent
        until main forked repo is found

        Data is returned as Python dictionary
    """
    proj_api_url = URL_TEMPLATE.format(full_name=full_name)

    headers = {
        "Accept": "application/vnd.github.mercy-preview+json",
    }

    print("working on ", proj_api_url)
    r = requests.get(proj_api_url, auth=(
        USERNAME, GITHUB_TOKEN), headers=headers)
    if r.status_code >= 300:
        print("skipping because problem fetching data for proj_api_url:", proj_api_url)
        return None
    proj_data = r.json()

    is_fork = proj_data.get("fork")
    if is_fork:
        print("FOUND PARENT FOR ", proj_api_url)
        proj_data = proj_data.get("parent")

    main_proj_data = {
        "gh_name": proj_data.get("name"),
        "gh_full_name":  proj_data.get("full_name"),
        "gh_owner_login": proj_data.get("owner").get("login"),
        "gh_owner_type": proj_data.get("owner").get("type"),
        "gh_description": proj_data.get("description"),
        "gh_fork": proj_data.get("fork"),
        "gh_created_at": int(dateutil.parser.parse(proj_data.get("created_at")).timestamp()),
        "gh_size": proj_data.get("size"),
        "gh_stargazers_count": proj_data.get("stargazers_count"),
        "gh_watchers_count": proj_data.get("watchers_count"),
        "gh_language": proj_data.get("language"),
        "gh_forks_count": proj_data.get("forks_count"),
        "gh_archived": proj_data.get("archived"),
        "gh_watchers": proj_data.get("watchers"),
        "gh_default_branch": proj_data.get("default_branch"),
        "gh_open_issues_count": proj_data.get("open_issues_count"),
        "gh_network_count": proj_data.get("network_count"),
        "gh_subscribers_count": proj_data.get("subscribers_count"),
        "gh_data_collected_at": int(datetime.now().timestamp()),
        "gh_url": proj_api_url,
    }
    return main_proj_data
