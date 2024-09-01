import datetime
from datetime import datetime
from requests_html import HTMLSession
from .database import SessionLocal
from .crud import create_news
from .schemas import NewsCreate, News

def single_news_scraper(url: str):
    session = HTMLSession()
    try:
        response = session.get(url)
        #response.html.render()  # This will download Chromium if not found

        publisher_website = url.split('/')[2]
        publisher = publisher_website.split('.')[-2]

        title = response.html.find('div.h1', first=True).text

        reporter = response.html.find('.author-name', first=True).text

        date_elements = response.html.find('div.date:not(.color-white)')

        
        for date_element in date_elements:
            text = date_element.text.strip()
            try:
                news_datetime = datetime.strptime(text, '%d %B, %Y, %I:%M %p')
                break
            except ValueError:
                continue
        else:
            news_datetime = None

        category = response.html.find('h2.news-details-cat', first=True).text

        # Find the div with the specified class
        section_div = response.html.find('div.section-content.clearfix.margin-bottom-2', first=True)

        # Extract all <p> elements within this div
        filtered_paragraphs = [p.text for p in section_div.find('p')]

        # Join the filtered paragraphs into a single string
        news_body = '\n'.join(filtered_paragraphs)

        img_tags = response.html.find('img')
        images = [img.attrs['src'] for img in img_tags if 'src' in img.attrs]
        
        #news_datetime = datetime.datetime.now()

        print(f"Scraped news from {url}")
        print(f"Title: {title}")
        print(f"Reporter: {reporter}")
        print(f"Date: {news_datetime}")
        print(f"Category: {category}")
        print(f"Images: {images}")


        return NewsCreate(
            publisher_website=publisher_website,
            news_publisher=publisher,
            title=title,
            news_reporter=reporter,
            datetime=news_datetime,
            link=url,
            news_category=category,
            body=news_body,
            images=images,
        )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def scrape_and_store_news(url: str, db: SessionLocal): # type: ignore
    # db = SessionLocal()
    news_data = single_news_scraper(url)
    print(news_data)
    inserted_news = ""
    if news_data:
        # print(news_data)
        inserted_news = create_news(db=db, news=news_data)
    db.close()

    return inserted_news
