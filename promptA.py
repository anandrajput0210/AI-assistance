#write a program for student marks  

name = input("Enter student name: ")
number_of_subjects = int(input("Enter number of subjects: "))

marks = []
for subject_number in range(1, number_of_subjects + 1):
	mark = float(input(f"Enter marks for subject {subject_number} (0-100): "))
	marks.append(mark)

total = sum(marks)
average = total / number_of_subjects

print(f"\nStudent: {name}")
print(f"Total marks: {total:g}")
print(f"Average marks: {average:.2f}")
print("Result:", "Pass" if all(mark >= 40 for mark in marks) else "Fail")
