import requests
from lxml import etree
import json 

def extract_elements_by_xpath(html, xpath_expression):
    try:
        root = etree.HTML(html)
        elements = root.xpath(xpath_expression)
        return elements
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_html_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # エラーチェック

        html_content = response.text
        return html_content
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def scrape_and_generate_json(url_template, start_page, end_page, xpath_mapping):
    result_json = []
    
    for page in range(start_page, end_page ):
        target_url = url_template.format(page)
        html = get_html_from_url(target_url)
        
        if html:
            for xpath_dict in xpath_mapping:
                title_elements = extract_elements_by_xpath(html, xpath_dict["title"])
                author_elements = extract_elements_by_xpath(html, xpath_dict["author"])

                for title, author in zip(title_elements, author_elements):
                    entry = {
                        "title": title.text if title is not None else None,
                        "author": author.text if author is not None else None
                    }
                    result_json.append(entry)
        else:
            print(f"HTML for page {page} could not be fetched.")
    
    # 整形してJSONを出力
    formatted_json = json.dumps(result_json, indent=4, ensure_ascii=False)
    print(formatted_json)

if __name__ == "__main__":
    xpath_mapping = [
        {"title": "//div[@class='tit']", "author": "//div[@class='author']"}
    ]
    
    url_template = "https://bookclub.kodansha.co.jp/product_list?page={}&code=bungei-bunko"
    start_page = 1
    end_page = 66
    
    scrape_and_generate_json(url_template, start_page, end_page, xpath_mapping)