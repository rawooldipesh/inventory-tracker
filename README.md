# 🏷️ Inventory Tracking System – Django MVP

This is a minimal inventory management system built as part of an internship assignment.

## 🔧 Features
- Track current stock levels of products
- View stock movement history (IN/OUT)
- Update stock via a simple UI
- Backend modeled using `Prodmast`, `Stckmain`, and `Stckdetail` tables

## 🚀 Technologies Used
- Django
- SQLite
- Bootstrap (optional for styling)

## 📌 URLs
- Inventory Page: `/stock-summary-ui/`
- Stock History: `/stock-history-ui/`

## ▶️ How to Run

```bash
# Step 1: Clone the repo
git clone https://github.com/yourusername/inventory-tracker.git
cd inventory-tracker

# Step 2: Create virtual env (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run migrations
python manage.py migrate

# Step 5: Start server
python manage.py runserver
