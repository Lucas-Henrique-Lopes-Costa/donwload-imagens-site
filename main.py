import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse


def clean_url(url):
    parsed_url = urlparse(url)
    clean_path = parsed_url.path
    clean_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, clean_path, "", "", "")
    )
    return clean_url


def download_gallery_images(url):
    # Faz uma requisição para a página
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extrai o nome da página para criar o diretório
    page_name = url.split("//")[1].replace("/", "_").replace(".", "_")
    if not os.path.exists(page_name):
        os.makedirs(page_name)

    # Encontra o container da galeria
    gallery_container = soup.find("div", class_="elementor-gallery__container")
    if not gallery_container:
        print("Galeria não encontrada.")
        return

    # Encontra todas as tags de link na galeria
    img_tags = gallery_container.find_all("a", class_="e-gallery-item")
    for img_tag in img_tags:
        img_url = img_tag.get("href")
        if img_url:
            # Remove os parâmetros da URL
            img_url = clean_url(img_url)
            # Garante que a URL da imagem seja completa
            img_url = urljoin(url, img_url)
            img_name = os.path.basename(urlparse(img_url).path)

            # Baixa e salva a imagem
            img_response = requests.get(img_url)
            with open(os.path.join(page_name, img_name), "wb") as f:
                f.write(img_response.content)

    print(f"Todas as imagens foram baixadas para a pasta: {page_name}")


if __name__ == "__main__":
    urls = [
        "https://mansoesescarpas.com.br/casa-00067/",
        "https://mansoesescarpas.com.br/casa-00064/",
        "https://mansoesescarpas.com.br/casa-00061/",
    ]
    for url in urls:
        download_gallery_images(url)
