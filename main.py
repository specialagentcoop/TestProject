from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

data = []

url_list = [
    'https://www.cvmarket.lt/darbo-skelbimai?op=search&search%5Bjob_salary%5D=3&search%5Bcategories%5D%5B0%5D=8&search%5Bkeyword%5D=&ga_track=90',
    'https://www.cvmarket.lt/darbo-skelbimai?op=search&search%5Bjob_salary%5D=3&search%5Bcategories%5D%5B0%5D=8&search%5Bkeyword%5D=&ga_track=90&start=30',
    'https://www.cvmarket.lt/darbo-skelbimai?op=search&search%5Bjob_salary%5D=3&search%5Bcategories%5D%5B0%5D=8&search%5Bkeyword%5D=&ga_track=90&start=60',
    'https://www.cvmarket.lt/darbo-skelbimai?op=search&search%5Bjob_salary%5D=3&search%5Bcategories%5D%5B0%5D=8&search%5Bkeyword%5D=&ga_track=90&start=90',
    'https://www.cvmarket.lt/darbo-skelbimai?op=search&search%5Bjob_salary%5D=3&search%5Bcategories%5D%5B0%5D=8&search%5Bkeyword%5D=&ga_track=90&start=120']

for url in url_list:

    response = requests.get(url)
    # print(response)

    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.prettify())

    jobs = soup.find_all('article', {'data-component-id': True})  # tikrina, ar yra reikšmė data-component-id
    # print(jobs)

    for job in jobs:
        title = job.find('h2', class_='xl:text-xl font-bold mt-2 hover:underline').text.strip()
        company = job.find('span', class_='job-company mr-5').text.strip()
        # salary_range = job.find('div', class_='inline-block mt-2.5 lg:mt-0 salary-block mr-5').text.strip()
        salary_min_element = job.find('div', {'data-salary-from': True})
        salary_min = salary_min_element['data-salary-from'] if salary_min_element else 'N/A'
        salary_max_element = job.find('div', {'data-salary-to': True})
        salary_max = salary_max_element['data-salary-to'] if salary_max_element else 'N/A'
        salary_type_element = job.find('span',
                                       class_='text-slate-200 visited-group:text-gray-300 text-sm font-bold mt-0.5 salary-type')
        salary_type = salary_type_element.text.strip() if salary_type_element else 'N/A'
        location = job.find('span',
                            class_='bg-blue-50 text-slate-500 py-1.5 px-3 font-bold text-sm rounded-full flex w-fit h-fit justify-center items-center space-x-1.5 cursor-defaults leading-4 location').text.strip()
        job_posted = job.find('div', class_='whitespace-nowrap').text.strip()
        data.append({'Title': title,
                     'Company': company,
                     'Min Salary': salary_min,
                     'Max Salary': salary_max,
                     'Salary Type': salary_type,
                     'Location': location,
                     'Job Posted': job_posted
                     })

# df = pd.DataFrame(data)

# df.to_csv('cvmarket.csv', index=False)

job_df = pd.read_csv('cvmarket.csv')

job_df['Max Salary'] = pd.to_numeric(job_df['Max Salary'], errors='coerce')
job_df['Min Salary'] = pd.to_numeric(job_df['Min Salary'], errors='coerce')
# print(job_df)

average_min_salary = job_df['Min Salary'].mean().round(2)
average_max_salary = job_df['Max Salary'].mean().round(2)
total_job_listings = job_df['Title'].count()
job_listings_per_company = job_df['Company'].value_counts()
average_salary_by_title = job_df.groupby('Title')[['Min Salary', 'Max Salary']].mean().round(2)
job_listings_per_location = job_df['Location'].value_counts()

summary = {
    'Average Min Salary': average_min_salary,
    'Average Max Salary': average_max_salary,
    'Total Job Listings': total_job_listings,
    'Job Listings per Company': job_listings_per_company,
    'Average Salary by Title': average_salary_by_title,
    'Job Listings per Location': job_listings_per_location
}


def truncate_title(title, max_length=10):
    if len(title) > max_length:
        return title[:max_length] + '...'
    return title


job_df['Short Title'] = job_df['Title'].apply(truncate_title)
job_df['Average Salary'] = job_df[['Min Salary', 'Max Salary']].mean(axis=1)
sorted_data = job_df.sort_values(by='Average Salary', ascending=False).head(10)

plt.figure(figsize=(12, 8))
plt.bar(sorted_data['Short Title'], sorted_data['Average Salary'], color='skyblue')
plt.xlabel('Job Title')
plt.ylabel('Average Salary')
plt.title('Top 10 Job Titles by Average Salary')
plt.xticks(rotation=45)
plt.show()