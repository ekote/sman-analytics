import os
import time

from facebook_scraper import *


def create_output_files_struct():
    path = f"{project_name}/{date}"
    if not os.path.exists(path):
        os.makedirs(path)

    save_to_csv("posts",
                ["page", "post_id", "time", "post_url", "images_lowquality", "likes", "comments_number", "shares",
                 "text", "reaction_count", "reactions_likes", "reactions_care", "reactions_haha", "reactions_wow",
                 "reactions_love", "reactions_angry", "was_live"])

    save_to_csv("comments", ["page", "comment_id", "comment_text", "comment_time", "comment_url", "commenter_name",
                             "commenter_url", "replies_number", "post_id"])

    save_to_csv("reactors", ["link", "name", "type", "post_id"])


def get_and_save_posts(page: str):
    p_no, c_no, r_no = 1, 1, 1

    posts = get_posts_from_fb(page)

    for post in posts:
        print(f">>>> Saving post for {page}: ID={post['post_id']} - {p_no}")
        # print("-----------------------------------------------------------------")
        # print(f"-----------------------------{post_counter}-----------------------------------")
        # parsed = json.dumps(post, indent=4, sort_keys=True, default=str, ensure_ascii=False).encode('utf8')
        # print(parsed.decode())
        # print("-----------------------------------------------------------------")
        # print("-----------------------------------------------------------------")

        if post['reactions']:
            save_to_csv("posts", [
                page,
                post['post_id'],
                post['time'],
                post['post_url'],
                post['images_lowquality'],
                post['likes'],
                post['comments'],
                post['shares'],
                post['post_text'].replace(',', ' '),
                post['reaction_count'],
                post['reactions']['like'] if post.get('reactions', {}).get('like') else 0,
                post['reactions']['care'] if post.get('reactions', {}).get('care') else 0,
                post['reactions']['haha'] if post.get('reactions', {}).get('haha') else 0,
                post['reactions']['wow'] if post.get('reactions', {}).get('wow') else 0,
                post['reactions']['love'] if post.get('reactions', {}).get('love') else 0,
                post['reactions']['angry'] if post.get('reactions', {}).get('angry') else 0,
                post['was_live']
            ])
        else:
            save_to_csv("posts", [
                page,
                post['post_id'],
                post['time'],
                post['post_url'],
                post['images_lowquality'],
                post['likes'],
                post['comments'],
                post['shares'],
                post['post_text'].replace(',', ' '),
                post['reaction_count'],
                0,
                0,
                0,
                0,
                0,
                0,
                post['was_live']
            ])

        if post['reactors']:
            for reactor in post['reactors']:
                save_to_csv("reactors", [
                    reactor['link'],
                    reactor['name'],
                    reactor['type'],
                    post['post_id']
                ])
                r_no = r_no + 1

        print(f">>>> POST NO={p_no}")
        p_no = p_no + 1

        if post['comments'] != 0:
            print("Downloading comments...")
            try:
                org = next(get_posts(post_urls=[post["post_id"]],
                                     options={"comments": "generator",
                                              "allow_extra_requests": True}))
                for comment in org['comments_full']:
                    save_to_csv("comments", [
                        page,
                        comment['comment_id'],
                        comment['comment_text'].replace(',', ' '),
                        comment['comment_time'],
                        comment['comment_url'],
                        comment['commenter_name'].replace(',', ' '),
                        comment['commenter_url'],
                        len(comment['replies']) if comment.get('replies') else 0,
                        post['post_id']
                    ])
                    time.sleep(3)
                    print(f">>>> COMMENT NUMBER={c_no}")
                    if c_no in range(100, 50000, 50):
                        print(">>>> Delay for a five minutes to avoid being blocked.")
                        time.sleep(300)
                    c_no = c_no + 1
            except TypeError:
                print("TypeError for post_id=" + post["post_id"])

        if p_no in range(249, 9000, 50):
            print(">>>> Delay for a five minutes to avoid being blocked.")
            time.sleep(300)


def save_to_csv(file: str, row: list):
    assert (file == 'comments' or file == 'posts' or file == 'reactors')
    with open(f"{project_name}/{date}/{project_name}_{file}.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)
    return file


def get_posts_from_fb(page: str):
    return get_posts(page,
                     pages=pages_no,
                     extra_info=True,
                     options={
                         "reactions": True,
                         "reactors": "generator",
                         "posts_per_page": 50,
                         "allow_extra_requests": True
                     })


if __name__ == "__main__":
    pages = ('Microsoft.Polska', 'Microsoft', 'MicrosoftCEE', 'MicrosoftUKEducation')
    project_name = "microsoft"
    date = "09_12_2021"
    pages_no = 10
    set_cookies("cookie.json")
    first_run = True

    if first_run:
        create_output_files_struct()

    for page in pages:
        get_and_save_posts(page)
