import csv
import os
import time

from facebook_scraper import get_posts


def create_output_files_struct():
    if not os.path.exists(path):
        os.makedirs(path)

    save_posts_to_csv(
        ["id", "page", "post_id", "time", "post_url", "images_lowquality", "likes", "comments_number", "shares",
         "text", "reaction_count", "reactions_likes", "reactions_care", "reactions_haha", "reactions_wow",
         "reactions_love", "reactions_angry", "was_live"])

    save_comments_to_csv(["id", "page", "comment_id", "comment_text", "comment_time", "comment_url", "commenter_name",
                          "commenter_url", "replies_number", "post_id"])

    save_reactors_to_csv(["id", "link", "name", "type", "post_id"])


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
            save_posts_to_csv([
                p_no,
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
            save_posts_to_csv([
                p_no,
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
                save_reactors_to_csv([
                    r_no,
                    reactor['link'],
                    reactor['name'],
                    reactor['type'],
                    post['post_id']
                ])
                # print(f">>>> REACTOR NO={post_counter}")
                r_no = r_no + 1

        print(f">>>> POST NO={p_no}")
        p_no = p_no + 1

        if post['comments'] != 0:
            print("Downloading comments...")
            try:
                org = next(get_posts(post_urls=[post["post_id"]],
                                     cookies=cookie_file,
                                     options={"comments": True,
                                              "allow_extra_requests": True}))
                for comment in org['comments_full']:
                    save_comments_to_csv([
                        c_no,
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
                    if c_no in range(100, 50000, 100):
                        print(">>>> Delay for a five minutes to avoid being blocked.")
                        time.sleep(300)
                    c_no = c_no + 1
            except TypeError:
                print("TypeError for post_id=" + post["post_id"])

        if p_no in range(500, 9000, 500):
            print(">>>> Delay for a five minutes to avoid being blocked.")
            time.sleep(300)


def save_comments_to_csv(data):
    with open(path + project_name + "_comments.csv", "a", newline='') as comments_file:
        writer = csv.writer(comments_file)
        writer.writerow(data)
    return comments_file


def save_reactors_to_csv(data):
    with open(path + project_name + "_reactors.csv", "a", newline='') as reactors_file:
        writer = csv.writer(reactors_file)
        writer.writerow(data)
    return reactors_file


def save_posts_to_csv(data):
    with open(path + project_name + "_posts.csv", "a", newline='') as posts_file:
        writer = csv.writer(posts_file)
        writer.writerow(data)
    return posts_file


def get_posts_from_fb(page: str):
    return get_posts(page,
                     pages=pages_no,
                     cookies=cookie_file,
                     extra_info=True,
                     options={
                         "reactions": True,
                         "reactors": "generator",
                         "posts_per_page": 50,
                         "allow_extra_requests": True
                     })


if __name__ == "__main__":
    pages = ('Microsoft.Polska', 'MicrosoftCEE', 'MicrosoftUKEducation', 'Microsoft')
    project_name = "microsoft"
    date = "08_12_2021"
    pages_no = 100
    cookie_file = "cookie.json"
    path = project_name + '/' + date + '/'

    create_output_files_struct()

    for page in pages:
        get_and_save_posts(page)
