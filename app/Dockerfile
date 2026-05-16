# שימוש בגרסה יציבה וקלה
FROM python:3.9-alpine

# הגדרת תיקיית העבודה
WORKDIR /app

# העתקת קובץ הדרישות והתקנה
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל שאר הקבצים
COPY . .

# אבטחה: יצירת משתמש והענקת הרשאות לתיקיית העבודה
RUN adduser -D myuser && chown -R myuser /app
USER myuser

# הגדרת משתני סביבה ל-Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

# הרצה דרך מודול flask (יותר יציב בתוך קונטיינר)
CMD ["python", "app.py"]