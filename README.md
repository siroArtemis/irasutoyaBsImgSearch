# irasutoyaBsImgSearch

## Process Overview
1.**Initial setup**.
   - Prepare a `data` directory to store images locally.
   - Get the URL (`searchUrl`) for scraping from the command line argument. 2.

2. **Initialize the Selenium WebDriver**.
   - Controls the Edge browser using Selenium.

3.**Collect image links**.
   - Scraping the page with the specified URL.
   - Retrieve the image URLs within the page.
   - If there is a “next page”, click on it to collect the next page's image as well. 4.

4.**Download images**.
   - Download images based on the collected image URLs and save them in the local `data` folder. 5.

5. **Exit Process**.
   - Close the browser and release resources.

## HOW TO USE
1. specify the URL as an argument when executing the script.
   ```bash
   python script.py https://www.irasutoya.com/search/label/%E6%A9%9F%E6%A2%B0
   ````
After execution, the images on the page with the given URL will be saved in the `data` folder.

Translated with DeepL.com (free version)
