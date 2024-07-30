from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup  
import io

url="https://www.cosmodern.vn/"
loader=RecursiveUrlLoader(url=url,
             max_depth=10,
             extractor=lambda x:Soup(x,"html.parser").text
             )
docs=loader.load()
# print(docs)
# Write only the links containing "/product" to a file
with io.open("product_links.txt", "w", encoding="utf-8") as f1:
    for doc in docs:
        source = doc.metadata["source"]
        if "/product" in source:
            f1.write(source + "\n")
    
    f1.close()
