import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('student_marks.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS student_data (
                    stu_name TEXT,
                    stu_subject TEXT,
                    stu_marks INTEGER
                 )''')

students_data = [
    ('John', 'Math', 85), ('John', 'Physics', 78), ('John', 'Chemistry', 92), ('John', 'Biology', 88), ('John', 'English', 76),
    ('Sophie', 'Math', 65), ('Sophie', 'Physics', 58), ('Sophie', 'Chemistry', 72), ('Sophie', 'Biology', 66), ('Sophie', 'English', 62),
    ('Michael', 'Math', 90), ('Michael', 'Physics', 92), ('Michael', 'Chemistry', 94), ('Michael', 'Biology', 93), ('Michael', 'English', 89),
    ('Daniel', 'Math', 45), ('Daniel', 'Physics', 38), ('Daniel', 'Chemistry', 55), ('Daniel', 'Biology', 49), ('Daniel', 'English', 40),
    ('Emily', 'Math', 72), ('Emily', 'Physics', 74), ('Emily', 'Chemistry', 68), ('Emily', 'Biology', 78), ('Emily', 'English', 70),
    ('Jacob', 'Math', 88), ('Jacob', 'Physics', 82), ('Jacob', 'Chemistry', 91), ('Jacob', 'Biology', 85), ('Jacob', 'English', 80),
    ('Olivia', 'Math', 95), ('Olivia', 'Physics', 89), ('Olivia', 'Chemistry', 97), ('Olivia', 'Biology', 92), ('Olivia', 'English', 94),
    ('Emma', 'Math', 60), ('Emma', 'Physics', 64), ('Emma', 'Chemistry', 58), ('Emma', 'Biology', 62), ('Emma', 'English', 59),
    ('Liam', 'Math', 85), ('Liam', 'Physics', 81), ('Liam', 'Chemistry', 83), ('Liam', 'Biology', 87), ('Liam', 'English', 80),
    ('Ava', 'Math', 75), ('Ava', 'Physics', 78), ('Ava', 'Chemistry', 80), ('Ava', 'Biology', 77), ('Ava', 'English', 79),
    ('Ethan', 'Math', 55), ('Ethan', 'Physics', 52), ('Ethan', 'Chemistry', 59), ('Ethan', 'Biology', 57), ('Ethan', 'English', 60),
    ('Isabella', 'Math', 92), ('Isabella', 'Physics', 95), ('Isabella', 'Chemistry', 94), ('Isabella', 'Biology', 91), ('Isabella', 'English', 93),
    ('Noah', 'Math', 70), ('Noah', 'Physics', 72), ('Noah', 'Chemistry', 68), ('Noah', 'Biology', 74), ('Noah', 'English', 69),
    ('Mia', 'Math', 82), ('Mia', 'Physics', 85), ('Mia', 'Chemistry', 89), ('Mia', 'Biology', 87), ('Mia', 'English', 84),
    ('James', 'Math', 43), ('James', 'Physics', 50), ('James', 'Chemistry', 48), ('James', 'Biology', 46), ('James', 'English', 45),
    ('Charlotte', 'Math', 67), ('Charlotte', 'Physics', 62), ('Charlotte', 'Chemistry', 65), ('Charlotte', 'Biology', 68), ('Charlotte', 'English', 66),
    ('Henry', 'Math', 88), ('Henry', 'Physics', 86), ('Henry', 'Chemistry', 92), ('Henry', 'Biology', 89), ('Henry', 'English', 87),
    ('Amelia', 'Math', 77), ('Amelia', 'Physics', 74), ('Amelia', 'Chemistry', 79), ('Amelia', 'Biology', 76), ('Amelia', 'English', 75),
    ('Lucas', 'Math', 58), ('Lucas', 'Physics', 60), ('Lucas', 'Chemistry', 56), ('Lucas', 'Biology', 54), ('Lucas', 'English', 55),
    ('Harper', 'Math', 93), ('Harper', 'Physics', 90), ('Harper', 'Chemistry', 94), ('Harper', 'Biology', 96), ('Harper', 'English', 91)
]

cursor.executemany('INSERT INTO student_data VALUES (?, ?, ?)', students_data)
conn.commit()

df = pd.read_sql_query("SELECT*FROM student_data", conn)

df_grouped = df.groupby('stu_name')['stu_marks'].agg(Total='sum', Average='mean').reset_index()

top_performer = df_grouped.loc[df_grouped['Total'].idxmax()]
low_performer = df_grouped.loc[df_grouped['Total'].idxmin()]

print("\n=== Total and Average Marks for Each Student ===")
print(df_grouped)

print("\n=== Top Performer ===")
print(top_performer)

print("\n=== Low Performer ===")
print(low_performer)

subject_avg = df.groupby('stu_subject')['stu_marks'].mean()

print("\n=== Subject-wise Average Marks ===")
print(subject_avg)

subject_total_contribution = (subject_avg / subject_avg.sum()) * 100

print("\n=== Subject Performance Contribution (Percentage) ===")
print(subject_total_contribution)

plt.figure(figsize=(10, 5))
plt.bar(subject_avg.index, subject_avg.values, color='skyblue')
plt.title('Subject-wise Average Marks')
plt.xlabel('Subjects')
plt.ylabel('Average Marks')
plt.show()

plt.figure(figsize=(10, 5))
plt.pie(subject_total_contribution, labels=subject_avg.index, autopct='%1.1f%%', startangle=140)
plt.title('Subject Performance Contribution')
plt.show()

conn.close()
