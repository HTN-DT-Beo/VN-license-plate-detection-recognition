import os
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler

# Danh sách từ khóa tìm kiếm
keywords = [
    "biển số xe",
    "biển số xe Việt Nam",
    "biển số xe máy",
    "biển số xe hơi",
    "biển số xe tải",
    "biển số ô tô",
    "biển số xe buýt",
    "biển số xe khách",
    "biển số xe container",
    "biển số xe công an",
    "biển số xe quân đội",
    "ảnh xe có biển số",
    "xe đang chạy có biển số",
    "biển số xe trước",
    "biển số xe sau",
    "biển số rõ nét",
    "ảnh biển số xe máy",
    "ảnh biển số xe ô tô",
    "góc chụp biển số xe",
    "biển số xe cũ",
    "biển số xe mới",
    "xe máy đang chạy biển số",
    "xe đậu có biển số",
    "xe biển số tỉnh"
]

# Đường dẫn gốc tới thư mục lưu ảnh (từ Sources/ -> ../Dataset/CrawlData/)
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Dataset/Crawl"))

# Tạo thư mục nếu chưa tồn tại
os.makedirs(base_path, exist_ok=True)

# Vòng lặp tìm kiếm từng từ khóa
for kw in keywords:
    print(f"🔍 Start crawling for keyword: {kw}")
    folder_name = kw.replace(" ", "_")
    
    # # Crawl Google Images
    # try:
    #     google_path = os.path.join(base_path, "google", folder_name)
    #     os.makedirs(google_path, exist_ok=True)
    #     google_crawler = GoogleImageCrawler(storage={'root_dir': google_path})
    #     google_crawler.crawl(keyword=kw, max_num=300)
    #     print(f"✅ Google crawl done for: {kw}")
    # except Exception as e:
    #     print(f"❌ Google crawl error for '{kw}': {e}")

    # Crawl Bing Images
    try:
        bing_path = os.path.join(base_path, "bing", folder_name)
        os.makedirs(bing_path, exist_ok=True)
        bing_crawler = BingImageCrawler(storage={'root_dir': bing_path})
        bing_crawler.crawl(keyword=kw, max_num=300)
        print(f"✅ Bing crawl done for: {kw}")
    except Exception as e:
        print(f"❌ Bing crawl error for '{kw}': {e}")

    print()
