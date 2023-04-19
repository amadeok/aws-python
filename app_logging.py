
import logging
import git, os, random
import argparse, distro

parser = argparse.ArgumentParser()
parser.add_argument("--log_to_file", help="log to file", default=False)
parser.add_argument("--log_level", help="log level", default=logging.DEBUG )

args = parser.parse_args()

pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)

if args.log_to_file:
    logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=args.log_level)
else: 
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

ubuntu_ver = distro.info()["version"]


repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha
logging.info(f"repo : {repo} sha: {sha}")



possible_texts = []
with open("possible_texts.txt", "r") as inp:
    possible_texts = inp.read()
    possible_texts = possible_texts.split("\n\n")
    logging.info("Possible texts: ")
    for i, text in enumerate( possible_texts):
        # possible_texts[i] = possible_texts[i].replace("\\n ", "\n")
        # possible_texts[i] = possible_texts[i].replace("\\n", "\n")
        print(f"-# Possible text n{i}:\n{possible_texts[i]}")

    #print(possible_texts)

hashtags_list = ""
with open("hashtags_list.txt", "r") as inp:
    logging.info("Hashtags list: ")
    hashtags_list = inp.read()
    hashtags_list = hashtags_list.replace("\n", " ")
    hashtags_list = hashtags_list.replace("   ", " ")
    hashtags_list = hashtags_list.replace("  ", " ")
    hashtags_list = hashtags_list.split(" ")

    print(hashtags_list)

def get_hashtags(n):
    l = random.sample(hashtags_list, n)
    ll = " ".join(l)
    return ll

print(get_hashtags(5))