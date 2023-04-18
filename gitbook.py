from typing import Dict, List
from urllib.parse import urlparse
from langchain.document_loaders import GitbookLoader as OriginalGitbookLoader

class Document:
    def __init__(self, page_content: str, metadata: Dict[str, str]):
        self.page_content = page_content
        self.metadata = metadata

class GitbookLoader(OriginalGitbookLoader):
    def __init__(self, web_page, load_all_paths=False, base_url=''):
        # Call the parent constructor with the same arguments
        super().__init__(web_page, load_all_paths, base_url)

        # Check if the web_page attribute ends with a slash and update self.base_url accordingly
        if self.base_url is None and self.web_page.endswith('/'):
            self.base_url = self.web_page[:-1]

    def remove_prefix(self, prefix: str, lst: List[str]) -> List[str]:
        """Remove prefix from all elements in lst."""
        return [s[len(prefix):] if s.startswith(prefix) else s for s in lst]

    def load(self) -> List[Document]:
        """Fetch text from one single GitBook page."""
        if self.load_all_paths:
            soup_info = self.scrape()
            relative_paths = self._get_paths(soup_info)
            # Extract the prefix from the given URL
            url_path = urlparse(self.base_url).path
            prefix_to_remove = url_path.split("/", 2)[1]  # Get the first part of the path
            # Remove the dynamic prefix from the relative paths
            relative_paths = self.remove_prefix(f"/{prefix_to_remove}", relative_paths)            
            documents = []
            for path in relative_paths:
                url = self.base_url + path
                print(f"Fetching text from {url}")
                soup_info = self._scrape(url)
                documents.append(self._get_document(soup_info, url))
            return documents
        else:
            soup_info = self.scrape()
            return [self._get_document(soup_info, self.web_path)]