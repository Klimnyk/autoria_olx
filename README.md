# AutoRia OLX

<a href="https://lookerstudio.google.com/reporting/e899b21f-1f3a-4a48-aac1-085a2b84f151"><b>Looker Studio
Link<b/><br><br></a>
EN

This Python code collects data on car ads from two websites, olx.ua and auto.ria.com, and writes it to a Google
Sheet. It uses the gspread and gspread_dataframe libraries to interact with the Google Sheets API and pandas library to
process data. The code loads region data from JSON files and sends requests to the API endpoints of OLX and Auto.ria to
retrieve the number of car ads posted in each region. Then, it combines the new data with the existing data in the
Google Sheet and overwrites it. The credentials for accessing the Google Sheets API are stored in a JSON file.

UA

Цей код Python збирає дані про автомобільні оголошення з двох сайтів, olx.ua і auto.ria.com, і записує їх у Google Sheet. Він
використовує бібліотеки gspread і gspread_dataframe для взаємодії з API Google Таблиць і бібліотекою pandas для обробки
даних. Код завантажує дані регіону з файлів JSON і надсилає запити до кінцевих точок API OLX і Auto.ria для отримання
кількості оголошень про автомобілі, розміщених у кожному регіоні. Потім він поєднує нові дані з наявними даними в
таблиці Google і перезаписує їх. Облікові дані для доступу до API Google Таблиць зберігаються у файлі JSON.

