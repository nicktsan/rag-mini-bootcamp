from __future__ import annotations
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, SoupStrainer
from workshop_code.indexer_components.shared_indexer_component_methods import soup_get_text

GITHUB_BLOG_POST = "https://lilianweng.github.io/posts/2023-06-23-agent/"
ARXIV_RAG_SURVEY_PAPER = "https://arxiv.org/html/2312.10997v5"

class Preprocessor(ABC):
    @abstractmethod
    def get_text(self, html_content: str) -> str:
        pass

    @staticmethod
    def get_preprocessor(doc_uri: str) -> Preprocessor:
        if doc_uri == GITHUB_BLOG_POST:
            preprocessor = GithubBlogpostPreprocessor()
        elif doc_uri == ARXIV_RAG_SURVEY_PAPER:
            preprocessor = ArxivHtmlPaperPreprocessor()
        else:
            raise ValueError(f"Unsupported document URI: {doc_uri}.") 
        return preprocessor

class GithubBlogpostPreprocessor(Preprocessor):
    def get_text(self, html_content: str) -> str:
        """
        Extracts and returns clean text from the post content, title, and header.

        Args:
            html_content (str): The HTML content to process.

        Returns:
            str: Cleaned text from specified parts of the HTML content.
        """
        cleaned_text = soup_get_text(html_content, ["post-title", "post-meta", "post-content"], "html.parser")
        return cleaned_text

class ArxivHtmlPaperPreprocessor(Preprocessor):
    def get_text(self, html_content: str) -> str:
        """
        Extracts and returns clean text from the title, authors, affiliations, abstract, and sections.

        Args:
            html_content (str): The HTML content to process.

        Returns:
            str: Cleaned text from specified parts of the HTML content.
        """
        title = self._extract_title(html_content)
        authors_affiliations = self._extract_authors_and_affiliations(html_content)
        abstract = self._extract_abstract(html_content)
        
        sections = []
        for i in range(1, 9):
            section_id = "S" + str(i)
            section_text = self._extract_section_with_subheadings(html_content, section_id)
            sections.append(section_text)

        cleaned_text = title + "\n\n" + authors_affiliations + "\n\n" + abstract + "\n\n" + "\n\n".join(sections)
        return cleaned_text

    def _extract_title(self, html_content: str) -> str:
        title = soup_get_text(html_content, ["ltx_title ltx_title_document"], "html.parser")
        # return "ArxivHtmlPaperPreprocessor._extract_title() not implemented"
        return title
    
    def _extract_authors_and_affiliations(self, html_content: str) -> str:
        strainer = SoupStrainer('div', class_="ltx_authors")
        soup = BeautifulSoup(html_content, 'html.parser', parse_only=strainer)

        result = []
        for author in soup.find_all('span', class_='ltx_creator ltx_role_author'):
            name = author.find('span', class_='ltx_personname').get_text(strip=True)
            affil = ' '.join(span.get_text(strip=True) for span in author.find_all('span', class_='ltx_contact ltx_role_affiliation'))
            result.append(f"{name}: {affil}\n\n")
        final_result = "\n".join(result)
        return final_result

    def _extract_abstract(self, html_content: str) -> str:
        strainer_id = SoupStrainer(class_="ltx_abstract")
        abstract = BeautifulSoup(html_content, 'html.parser', parse_only=strainer_id)
        child_to_exclude = abstract.find(class_='ltx_note ltx_role_footnote')
        # Remove the child element from the parent
        if child_to_exclude:
            child_to_exclude.decompose()  # Or you can use .extract() to remove it
        desired_info = abstract.get_text()
        return desired_info
    
    def _extract_section_with_subheadings(self, html_content: str, section_id: str) -> str:
        strainer_id = SoupStrainer(class_=['ltx_para'])
        abstract = BeautifulSoup(html_content, 'html.parser', parse_only=strainer_id).get_text()
        return abstract
