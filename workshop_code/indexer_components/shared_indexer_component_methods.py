from bs4 import BeautifulSoup, SoupStrainer


def soup_get_text(html_content: str, soupStrainerClass: list[str], soup_features: str) -> str:
    only_post_text = SoupStrainer(class_=soupStrainerClass) # TODO: Add the classes to parse here
    soup = BeautifulSoup(html_content, soup_features, parse_only=only_post_text)
    cleaned_text = soup.get_text()
    return cleaned_text
