from IPython.display import display
import pandas as pd
import requests
from bs4 import BeautifulSoup
from info import urls



def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def post_crawler(html):
    soup = BeautifulSoup(html, 'html.parser')
    posts = []
    rows = soup.find_all("tr")
    for row in rows:
        number = row.find('td', class_="b-num-box")
        title_box = row.find('div', class_="b-title-box")
        date = row.find('span', class_="b-date")
        writer = row.find('span', class_="b-writer")
        views = row.find('span', class_="hit")
        post_data = {'번호': number.get_text(strip=True) if number else '',
                     '제목': title_box.a.get_text(strip=True) if title_box and title_box.a else '',
                     "작성자": writer.get_text(strip=True) if writer else '',
                     '날짜': date.get_text(strip=True) if writer else '',
                     "조회수": views.get_text(strip=True) if views else '',
                     "본문링크": url + title_box.a['href'] if title_box and title_box.a else ''}
        posts.append(post_data)
    return posts


def contents_crawler(posts):
    contents_list = []
    for post in posts:
        post_url = post["본문링크"]
        soup = BeautifulSoup(get_html(post_url), 'html.parser')
        content = soup.find("div", class_="fr-view")
        contents_list.append(content.get_text(strip=True).strip()) if content else contents_list.append('')
    return contents_list


def image_crawler(posts):
    img_list = []
    for post in posts:
        post_url = post["본문링크"]
        soup = BeautifulSoup(get_html(post_url), 'html.parser')
        div = soup.find("div", "fr-view")
        img_tags = div.find_all('img')
        if img_tags:
            img_srcs = [img['src'] if 'src' in img.attrs and "https://homepage.cnu.ac.kr" in img['src'] else 'https://ai.cnu.ac.kr' + img['src'] for img in img_tags]
            img_list.append(''.join(img_srcs) if len(img_srcs) == 1 else img_srcs)
        else:
            img_list.append(None)
    return img_list


def add_post_images(posts, imgs):
    for num in range(len(posts)):
        posts[num]["이미지"] = imgs[num]


def clean_data(posts):
    posts.pop(0)
    for post in posts:
        view = post["조회수"].replace("조회수", "").strip()
        post["조회수"] = view
    return posts


def add_post_contents(posts, contents):
    for num in range(len(posts)):
        posts[num]["내용"] = contents[num]


def add_post_tables(posts, dfs):
    if len(dfs) != 0:
        post["is_table"] = 1
        post["table"] = [df.to_json(orient='split') for df in dfs]
    else:
        post["is_table"] = 0
        post["table"] = None


def parse_html_table(table):
    rows = table.find_all("tr")
    table_data = []
    columns = []
    rowspan_dict = {}

    for i, row in enumerate(rows):
        tds = row.find_all(["td", "th"])
        row_data = []
        col_idx = 0
        while col_idx in rowspan_dict:
            if rowspan_dict[col_idx][1] > 0:
                row_data.append(rowspan_dict[col_idx][0])
                rowspan_dict[col_idx][1] -= 1
                if rowspan_dict[col_idx][1] == 0:
                    del rowspan_dict[col_idx]
                col_idx += 1
            else:
                del rowspan_dict[col_idx]

        for td in tds:
            spans = td.find_all("span")
            ps = td.find_all("p")
            if spans:
                cell_text = " ".join([span.get_text(strip=True) for span in spans])
            elif ps:
                cell_text = " ".join([p.get_text(strip=True) for p in ps])
            else:
                cell_text = td.get_text(strip=True)
            colspan = int(td.get("colspan", 1))
            rowspan = int(td.get("rowspan", 1))

            for _ in range(colspan):
                row_data.append(cell_text)
                if rowspan > 1:
                    rowspan_dict[col_idx] = [cell_text, rowspan - 1]
                col_idx += 1

        if i == 0:
            columns = row_data
        else:
            while len(row_data) < len(columns):
                row_data.append("")
            table_data.append(row_data)

    # Check if table_data and columns have the correct format
    if len(columns) > 1 and all(len(row) == len(columns) for row in table_data):
        return pd.DataFrame(table_data, columns=columns)
    else:
        return None


def find_valid_tables(soup):
    div = soup.find("div", class_="fr-view")
    if not div:
        return []

    tables = div.find_all("table")
    valid_tables = []
    seen_tables = set()

    for table in tables:
        nested_tables = table.find_all("table")
        if nested_tables:
            for nested_table in nested_tables:
                table_str = str(nested_table)
                if table_str not in seen_tables:
                    seen_tables.add(table_str)
                    df = parse_html_table(nested_table)
                    if df is not None:
                        valid_tables.append(df)
        else:
            table_str = str(table)
            if table_str not in seen_tables:
                seen_tables.add(table_str)
                df = parse_html_table(table)
                if df is not None:
                    valid_tables.append(df)

    return valid_tables


def table_main(post_url):
    soup = BeautifulSoup(get_html(post_url), 'html.parser')
    tables = find_valid_tables(soup)
    dfs = []
    for table in tables:
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_columns', None)
        dfs.append(table)
    return dfs


if __name__ == "__main__":
    url = urls["학사공지"]
    html = get_html(url)
    posts = post_crawler(html)
    posts = clean_data(posts)
    contents = contents_crawler(posts)
    add_post_contents(posts, contents)
    img = image_crawler(posts)
    add_post_images(posts, img)
    for post in posts:
        print(post)
    for post in posts:
        post_url = post["본문링크"]
        print(post["번호"])
        dfs = table_main(post_url)
        add_post_tables(posts, dfs)
        for df in dfs:
            display(df)


