import argparse
from src.randomizer import Randomizer
from src.comment_fetcher import Fetcher


def main():

    parser = argparse.ArgumentParser(description="YouTube comment randomizer")
    parser.add_argument(
        "--video_id", "-v", required=True, help="YouTube video ID",
    )
    parser.add_argument(
        "--fetch_only",
        "-f",
        action="store_true",
        help="Fetch comments, do not randomize",
    )
    parser.add_argument("--dev_key", "-d", required=True, help="YouTube API key")
    parser.add_argument(
        "--remove_duplicates",
        "-r",
        action="store_true",
        help="Remove duplicate authors",
    )
    parser.add_argument("--specific_text", "-s", help="Filter based on specific text")

    args = parser.parse_args()

    fetcher = Fetcher(args.dev_key, args.video_id, "snippet")
    all_comments = fetcher.fetch()
    print(len(all_comments), "comments were fetched.")
    if args.fetch_only:
        for comment in all_comments:
            print(comment)
        return 0
    randomizer = Randomizer(all_comments, args.remove_duplicates, args.specific_text)
    random_comment = randomizer.randomize()
    print(random_comment)
    return 0


if __name__ == "__main__":
    main()
