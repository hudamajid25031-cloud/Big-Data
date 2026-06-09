import sqlite3
import pandas as pd

# =========================================================
# STEP 1: THE ETL PIPELINE (Extract & Load)
# =========================================================

print("Starting the Data Pipeline...")

# 1. Create a connection to a brand new SQL database file
conn = sqlite3.connect('student_wellbeing.db')

# 2. Extract: Python reads your 3 NEW CSV files
# Make sure you exported them with these exact names!
path = r"C:\Users\pc alkazaz\OneDrive\Desktop\access.microsoft\\"

try:
    students_data = pd.read_csv(path + "Students_Tbl.csv")
    mental_health_data = pd.read_csv(path + "Mental_Health_Tbl.csv")
    habits_data = pd.read_csv(path + "Daily_Habits_Tbl.csv")
except FileNotFoundError:
    print("\nERROR: Could not find the files. Please ensure you exported Students_Tbl.csv, Mental_Health_Tbl.csv, and Daily_Habits_Tbl.csv to your folder.")
    exit()

# 3. Load: Python pushes the tables into the SQL database
students_data.to_sql('Students', conn, if_exists='replace', index=False)
mental_health_data.to_sql('MentalHealth', conn, if_exists='replace', index=False)
habits_data.to_sql('DailyHabits', conn, if_exists='replace', index=False)

print("Data Pipeline successful! SQL Database is built and ready.\n")

# =========================================================
# STEP 2: THE INTERACTIVE SQL REPORTS
# =========================================================

print("Welcome to the Student Wellbeing Data System!")
print("Type 1: Find Students by Course (e.g., B.Sc)")
print("Type 2: Find Students with High Anxiety (Uses a JOIN)")
print("Type 3: See Study Hours vs. Stress Levels (Uses a Double JOIN)")

choice = input("Enter your choice (1, 2, or 3): ")

if choice == '1':
    course_choice = input("Which course are you looking for? ")
    
    # Simple Query
    query1 = """
    SELECT student_id, age, gender, course 
    FROM Students 
    WHERE course = ?
    """
    report1 = pd.read_sql_query(query1, conn, params=(course_choice,))
    print(f"\n--- Students in {course_choice} ---")
    print(report1 if not report1.empty else "No students found.")

elif choice == '2':
    anxiety_threshold = input("Enter minimum anxiety score to flag (e.g., 7): ")
    
    # Advanced Query: JOINing Students and Mental Health tables
    query2 = """
    SELECT Students.student_id, Students.course, MentalHealth.anxiety_score, MentalHealth.stress_level 
    FROM Students 
    JOIN MentalHealth ON Students.student_id = MentalHealth.student_id 
    WHERE MentalHealth.anxiety_score >= ?
    ORDER BY MentalHealth.anxiety_score DESC
    """
    report2 = pd.read_sql_query(query2, conn, params=(anxiety_threshold,))
    print("\n--- High Anxiety Alert List ---")
    print(report2 if not report2.empty else "No students match this criteria.")

elif choice == '3':
    study_hours = input("Show students who study more than how many hours? (e.g., 5): ")
    
    # Master Query: JOINing all 3 tables!
    query3 = """
    SELECT Students.student_id, DailyHabits.daily_study_hours, MentalHealth.stress_level 
    FROM Students 
    JOIN DailyHabits ON Students.student_id = DailyHabits.student_id
    JOIN MentalHealth ON Students.student_id = MentalHealth.student_id
    WHERE DailyHabits.daily_study_hours >= ?
    ORDER BY DailyHabits.daily_study_hours DESC
    """
    report3 = pd.read_sql_query(query3, conn, params=(study_hours,))
    print("\n--- Study Hours vs Stress Level Report ---")
    print(report3 if not report3.empty else "No students match this criteria.")

else:
    print("Invalid choice.")

# Close the connection
conn.close()