# src/api/tiktok_api.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time
import pickle
# import config.config

class TiktokApi:
    """
    Automates TikTok video uploads using Selenium.
    """

    def __init__(self, cookiesPath="./tiktok_cookies.pkl"):
        """
        Initialize TikTokAPI instance with Selenium WebDriver.

        :param driverPath: Path to ChromeDriver executable.
        :param cookiesPath: Path to saved TikTok cookies for authentication.
        """
        self.cookiesPath = cookiesPath
        self.driver = None

    def startDriver(self):
        """
        Start the Selenium WebDriver and open TikTok login page.
        """
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # self.driver.maximize_window()                                           # selenium4.6 ou superieur utilise SERVICE pour gérer le driver 

        # service = Service(ChromeDriverManager().install())
        # options = webdriver.ChromeOptions() 
        # # self.driver = webdriver.Chrome(service=service, options=options)
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")  # Désactiver l'utilisation du GPU
        options.add_argument("--disable-software-rasterizer")  # Désactiver le rendu logiciel
        options.add_argument("--disable-dev-shm-usage")  # Empêcher Chrome d'utiliser /dev/shm
        options.add_argument("--disable-web-security")  # Désactiver la sécurité WebRTC
        options.add_argument("--disable-features=WebRTC")  # Désactiver WebRTC (souvent lié à la vidéo)
        options.add_argument("--use-fake-ui-for-media-stream")  # Simuler une webcam/micro (évite les erreurs de permission)
        options.add_argument("--disable-blink-features=AutomationControlled")  # Rendre le bot moins détectable
        options.add_argument("--disable-accelerated-video")
        options.add_argument("--disable-accelerated-2d-canvas")



        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    def dezoom(self) : 
        self.driver.fullscreen_window()
        self.driver.execute_script("document.body.style.zoom='70%'")

    def dezoom_40(self) : 
        self.driver.fullscreen_window()
        self.driver.execute_script("document.body.style.zoom='40%'")

    def login(self, username, password):
        """
        Log in to TikTok and save cookies for reuse.

        :param username: TikTok username or email.
        :param password: TikTok password.
        """

        self.driver.get("https://www.tiktok.com/login/phone-or-email/email")
        time.sleep(3)

        self.dezoom() 

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)  #EC = expected conditions 

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Mot de passe']"))).send_keys(password)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='login-button']"))).click()

        # Handle CAPTCHA manually if it appears 
        time.sleep(30)

        # # Save cookies for future use
        # with open(self.cookiesPath, "wb") as file:
        #     pickle.dump(self.driver.get_cookies(), file)
        # logging.info("Cookies saved for future sessions.")

    def uploadVideo(self, videoPath, description):
        """
        Upload a video to TikTok with a description.

        :param videoPath: Path to the video file.
        # :param description: Description text for the video.
        # """
        self.driver.get("https://www.tiktok.com/upload")
        self.dezoom()
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        ).send_keys(videoPath)

        time.sleep(1)  # Allow video upload to process
        self.dezoom()

        descriptionInput = WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )

        descriptionInput.clear()
        descriptionInput.send_keys(description)

        self.dezoom_40()

        WebDriverWait(self.driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-e2e='post_video_button']"))
        ).click()

        time.sleep(15)

        logging.info(f"Video {videoPath} uploaded with description: {description}")


    def closeDriver(self):
        """
        Close the Selenium WebDriver.
        """
        if self.driver:
            self.driver.quit()

    # def publication (self) : 
    #     instance = TiktokApi() 
    #     instance.startDriver() 