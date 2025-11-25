
<div align="center">
  <img width="704" height="69" alt="E-voting app" src="https://github.com/user-attachments/assets/6647c368-971d-4e6f-8009-94bba1557f3a" />
</div>

# E-voting-flask-app - voting system
## 📂 About project:
Project created using ```flask``` python framework for web development  
My app is based using ```HTML templates``` which are rendered using ```flask```  
Project is a system that manage ```votes```
## 💻 Features:
- Database automatic creation
- Creating user account
- Creating vote (vote options, title, key dates, displaying results in real time or not - displaying count of votes all time or only when vote come to end)
- Planning votes (you can select voting start date and end date)
- ```Voting procedure``` by users, when vote have started
- Vote ending, counting votes and displaying ```vote winner```
- Searching ```votes``` by filters
## ⚙️ Run project:
To run this project you must have installed ```python```. Recommended ```Python 3.12.3 or above```
- Clone this repository using:
```
git clone https://github.com/Kamil-Kijak/evoting-flask-app.git
```
- Enter to cloned repository and first create ```virtual environment```:
```
python -m venv venv
```
- After, activate ```venv``` using:
```
venv\Scripts\Activate.ps1
```
or
```
source venv/bin/activate
```
- Install install necessary ```modules``` from *requirements.txt* file using:
```
pip install -r requirements.txt
```
- Finally, run project ```(if you activated virtual environment - venv)``` using:
```
python app.py
```
Server will host project on default port ```3000``` or you can also configure this port  
## 🖋️ Project config
```.env``` file structure  
``` .env
DEBUG=<0 or 1>
PORT=<application port default 3000>

DB_PORT="<database port default 3306>"
DB_NAME="<database name default evoting_flask_app_database>"
DB_HOST="<database host default localhost>"
DB_USER="<database user default root>"
DB_PASSWORD="<database password default ''>"
```
## 👦 Authors:
- Kamil Kijak ```(solo creator)```
## Project protected using MIT license

