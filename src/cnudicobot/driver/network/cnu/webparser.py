import pandas as pd

from .webcrawler import Crawler, NoticeCrawler


class Parser:
    def __init__(self, soup):
        self.soup = soup
        self.posts = []

    def parse_post_list(self, base_url):
        rows = self.soup.find_all("tr")
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
                         "본문링크": base_url + title_box.a['href'] if title_box and title_box.a else ''}
            self.posts.append(post_data)

    def parse_contents(self, post, content_soup):
        content = content_soup.find("div", class_="fr-view")
        post["내용"] = content.get_text(strip=True).strip() if content else ''

    def parse_images(self, post, content_soup):
        div = content_soup.find("div", class_="fr-view")
        img_tags = div.find_all('img')
        if img_tags:
            img_srcs = [img['src'] if 'src' in img.attrs and "https://homepage.cnu.ac.kr" in img['src'] else 'https://ai.cnu.ac.kr' + img['src'] for img in img_tags]
            post["이미지"] = ''.join(img_srcs) if len(img_srcs) == 1 else img_srcs
        else:
            post["이미지"] = None

    def parse_files(self, post, content_soup):
        total_file = []
        file_box = content_soup.find("div", class_="b-file-box")
        lis = file_box.find_all("li") if file_box else []
        for li in lis:
            file_dict = {}
            file = li.find_all("a")
            if len(file) > 0:
                file_dict["다운로드"] = "https://ai.cnu.ac.kr/ai/board/notice.do?" + file[0]["href"]
            if len(file) > 1:
                file_dict["미리보기"] = "https://ai.cnu.ac.kr" + file[1]["href"]
            if file_dict:
                total_file.append(file_dict)
        if total_file:
            if len(total_file) >= 2:
                post["첨부파일"] = total_file
            else:
                post["첨부파일"] = ''.join(str(a) for a in total_file)
        else:
            post["첨부파일"] = None


class DataCleaner:
    def __init__(self, posts):
        self.posts = posts

    def clean_data(self):
        if self.posts:
            self.posts.pop(0)
        for post in self.posts:
            view = post["조회수"].replace("조회수", "").strip()
            post["조회수"] = view


class TableParser:
    def __init__(self, base_url):
        self.base_url = base_url

    def parse_html_table(self, table):
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

        # Check if table_data and columns have the correct format and if columns contain meaningful data
        if len(columns) > 1 and all(len(row) == len(columns) for row in table_data) and len(table_data) > 0:
            # Check if columns contain actual text
            if any(column.strip() for column in columns):
                return pd.DataFrame(table_data, columns=columns)

        return None

    def find_valid_tables(self, soup):
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
                        df = self.parse_html_table(nested_table)
                        if df is not None:
                            valid_tables.append(df)
            else:
                table_str = str(table)
                if table_str not in seen_tables:
                    seen_tables.add(table_str)
                    df = self.parse_html_table(table)
                    if df is not None:
                        valid_tables.append(df)

        return valid_tables

    def table_main(self, post_url):
        soup = BeautifulSoup(Crawler(self.base_url).get_html(post_url), 'html.parser')
        tables = self.find_valid_tables(soup)
        dfs = []
        for table in tables:
            dfs.append(table)
        return dfs
