"""
Script to visualize B+ Tree indices in a database.
"""

import os
from db_engine import Database, BPlusTreeVisualizer

def main():
    """Create a database with tables and visualize the indices."""
    # Create a database
    db = Database('visualization_demo')
    
    # Create a students table
    students_schema = {
        'id': {'type': 'int', 'primary_key': True},
        'name': {'type': 'string', 'nullable': False},
        'age': {'type': 'int', 'nullable': False},
        'gpa': {'type': 'float', 'nullable': True}
    }
    students_table = db.create_table('students', students_schema)
    
    # Insert some students
    students = [
        {'id': 1, 'name': 'Alice', 'age': 20, 'gpa': 3.8},
        {'id': 2, 'name': 'Bob', 'age': 22, 'gpa': 3.5},
        {'id': 3, 'name': 'Charlie', 'age': 21, 'gpa': 3.9},
        {'id': 4, 'name': 'David', 'age': 23, 'gpa': 3.2},
        {'id': 5, 'name': 'Eve', 'age': 20, 'gpa': 4.0},
        {'id': 6, 'name': 'Frank', 'age': 22, 'gpa': 3.7},
        {'id': 7, 'name': 'Grace', 'age': 21, 'gpa': 3.6},
        {'id': 8, 'name': 'Hannah', 'age': 23, 'gpa': 3.8},
        {'id': 9, 'name': 'Ian', 'age': 20, 'gpa': 3.4},
        {'id': 10, 'name': 'Julia', 'age': 22, 'gpa': 3.9}
    ]
    
    for student in students:
        students_table.insert(student)
    
    # Create indices on age and gpa
    students_table.create_index('age')
    students_table.create_index('gpa')
    
    # Visualize the primary key index (id)
    id_visualizer = BPlusTreeVisualizer(students_table.indices['id'], 'students_id_index')
    id_path = id_visualizer.visualize()
    print(f'Primary key index visualization saved to: {id_path}')
    
    # Visualize the age index
    age_visualizer = BPlusTreeVisualizer(students_table.indices['age'], 'students_age_index')
    age_path = age_visualizer.visualize()
    print(f'Age index visualization saved to: {age_path}')
    
    # Visualize the gpa index
    gpa_visualizer = BPlusTreeVisualizer(students_table.indices['gpa'], 'students_gpa_index')
    gpa_path = gpa_visualizer.visualize()
    print(f'GPA index visualization saved to: {gpa_path}')
    
    # Create a courses table
    courses_schema = {
        'id': {'type': 'int', 'primary_key': True},
        'name': {'type': 'string', 'nullable': False},
        'credits': {'type': 'int', 'nullable': False},
        'department': {'type': 'string', 'nullable': False}
    }
    courses_table = db.create_table('courses', courses_schema)
    
    # Insert some courses
    courses = [
        {'id': 101, 'name': 'Database Systems', 'credits': 4, 'department': 'CS'},
        {'id': 102, 'name': 'Data Structures', 'credits': 3, 'department': 'CS'},
        {'id': 103, 'name': 'Algorithms', 'credits': 4, 'department': 'CS'},
        {'id': 104, 'name': 'Operating Systems', 'credits': 3, 'department': 'CS'},
        {'id': 105, 'name': 'Computer Networks', 'credits': 3, 'department': 'CS'},
        {'id': 201, 'name': 'Calculus', 'credits': 4, 'department': 'MATH'},
        {'id': 202, 'name': 'Linear Algebra', 'credits': 3, 'department': 'MATH'},
        {'id': 203, 'name': 'Probability', 'credits': 3, 'department': 'MATH'},
        {'id': 301, 'name': 'Physics I', 'credits': 4, 'department': 'PHYS'},
        {'id': 302, 'name': 'Physics II', 'credits': 4, 'department': 'PHYS'}
    ]
    
    for course in courses:
        courses_table.insert(course)
    
    # Create indices on credits and department
    courses_table.create_index('credits')
    courses_table.create_index('department')
    
    # Visualize the primary key index (id)
    id_visualizer = BPlusTreeVisualizer(courses_table.indices['id'], 'courses_id_index')
    id_path = id_visualizer.visualize()
    print(f'Courses primary key index visualization saved to: {id_path}')
    
    # Visualize the credits index
    credits_visualizer = BPlusTreeVisualizer(courses_table.indices['credits'], 'courses_credits_index')
    credits_path = credits_visualizer.visualize()
    print(f'Credits index visualization saved to: {credits_path}')
    
    # Visualize the department index
    dept_visualizer = BPlusTreeVisualizer(courses_table.indices['department'], 'courses_department_index')
    dept_path = dept_visualizer.visualize()
    print(f'Department index visualization saved to: {dept_path}')
    
    print("\nAll database visualizations completed!")
    print("You can find the visualizations in the 'visualizations' directory.")

if __name__ == '__main__':
    main()
