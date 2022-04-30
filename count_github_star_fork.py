from argparse import ArgumentParser
import json

import requests


def parse_args():
    parser = ArgumentParser(description="Run program.")
    parser.add_argument(
        "--username", nargs="?", default="Ezharjan", help="Input username."
    )
    parser.add_argument(
        "--topK",
        type=int,
        default=10,
        help="Display name of repos which is in the topK list ranked by stars and forks.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    url = "https://api.github.com/users/%s/repos" % args.username
    response = requests.get(url)
    result = json.loads(response.text)

    star_count = 0
    fork_count = 0
    repo_count = len(result)

    # 1.build dict
    repo_info = {}
    for i in range(repo_count):
        repo_name = result[i]["full_name"]
        repo_name = repo_name[repo_name.rfind("/") + 1 :]

        repo_info.setdefault(repo_name, {})
        repo_info[repo_name]["stars_count"] = result[i]["stargazers_count"]
        repo_info[repo_name]["forks_count"] = result[i]["forks_count"]

        star_count += repo_info[repo_name]["stars_count"]
        fork_count += repo_info[repo_name]["forks_count"]

    # 2.convert dict to list
    repo_info_list = []
    for repo_name, info in repo_info.items():
        repo_info_list.append([repo_name, info["stars_count"], info["forks_count"]])

    # 3.print the statisitical result
    print("User %s's Statisitical Result" % args.username)
    print("-----------------------------------------------")
    print("total repo: %d, star: %d, fork: %d" % (repo_count, star_count, fork_count))
    result_list = sorted(
        repo_info_list, key=lambda x: (x[1], x[2], x[0]), reverse=True
    )[: args.topK]
    for repo_name, stars, forks in result_list:
        print("%s\tstar:%d\tfork:%d" % (repo_name, stars, forks))


if __name__ == "__main__":
    main()
