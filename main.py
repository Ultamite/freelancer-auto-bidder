from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import ollama
from dotenv import find_dotenv, load_dotenv

# Configure Selenium
os.environ['PATH'] += r"C:/SeleniumDrivers"
driver = webdriver.Chrome()

credentials_path = find_dotenv()
load_dotenv(credentials_path)


username = os.getenv("freelancer_username")
password = os.getenv("freelancer_password")


def timed_generate(model, prompt, **kwargs):
	"""Call ollama.generate and return (text, elapsed_seconds).

	This wraps the existing API and normalizes the response into a string.
	"""
	start = time.perf_counter()
	resp = ollama.generate(model=model, prompt=prompt, **kwargs)
	end = time.perf_counter()
	elapsed = end - start
	# normalize response to string
	if isinstance(resp, dict):
		text = resp.get("response", "") or resp.get("output", "") or str(resp)
	else:
		text = str(resp)
	return text, elapsed

projects = "PyTorch Gans, SciKit Learn Models, Flask Web Apps, Tkinter GUI Apps, Data Analysis Scripts, Web Scraping Scripts"

model = "llama3.1:8b"

template = f"""
The bid should be written in this format:

The first ten words you write should identify the client's primary specific business need.  Fundamentally, what does he REALLY need, starting with: "I understand that you need ...";

The next ten words should summarize how your skills, sometimes referred to as your “unique selling points” will solve his problems.  Effectively, what makes you special or what can you do that nobody else can;

In the next paragraph you should define each element of the job the buyer needs you to do, and how you will address those needs.  Note the word “needs”.  It is his problem you are solving.  Don't talk about your profile content;

In the next paragraph you provide a realistic breakdown of the cost, just as I did with my Australian client and his educational activity toys;

In the next paragraph remind the client of the specific skills you have that will solve his problems.  If he asked for SEO, then talk about SEO.  If he didn't ask for Google AdWords, don't mention Google AdWords.  If someone mentioned something for which the buyer had not asked then the buyer would probably ignore the proposal;

Next, invite the buyer to check your profile.  Yes you can put a link to your profile in at this point, but NOT an off-site link, as that means you would be breaching this site's terms and conditions.

Next, ask the buyer a relevant question.  For example, if he hasn't asked for the job to be done in a specific period of time, ask him if he does have a preferred completion date;

My projects are: {projects}

Your proposal must not be greater than 1500 characters

Write the bid like you are an actual programmer
"""

url = input("Enter project url:")


# Run Bidder
driver.get(url)

login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), 'Log In')]")))

login_button.click()

email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='NativeElement ng-tns-c904158372-9 ng-untouched ng-pristine ng-invalid ng-star-inserted']")))
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='NativeElement ng-tns-c904158372-10 HasIconEnd ng-untouched ng-pristine ng-invalid ng-star-inserted']")))
login_button_final = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Log in')]")))

email_input.send_keys(username)
password_input.send_keys(password)
login_button_final.click()

print("Logged In")

project_description = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='font-normal text-foreground text-xsmall whitespace-pre-line']"))).text
project_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='descriptionTextArea']")))

prompt = f""" {template} \n Here is the project description: {project_description} \n Write the bid below:"""

generated_text, elapsed = timed_generate(model=model, prompt=prompt)
print(generated_text)
print(f"[timing] generation took {elapsed:.2f}s")

project_input.send_keys(generated_text)

breakpoint()
