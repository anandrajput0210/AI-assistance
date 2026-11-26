"""Collect five students' marks and display their grades.

Grade boundaries: A = 90-100, B = 80-89, C = 70-79,
D = 60-69, and F = 0-59. Invalid numbers and marks outside
0-100 are rejected and prompted again.

The program reads each student's name and a valid mark, assigns a grade
using these boundaries, and prints the results in a formatted table.

Test cases (marks -> expected grades):
1. 95, 84, 73, 62, 0 -> A, B, C, D, F
2. 90, 80, 70, 60, 100 -> A, B, C, D, A
3. 89, 79, 69, 59, 40 -> B, C, D, F, F
   In case 3, entering "abc" or 101 is rejected and prompts for the
   mark again.
"""

import math

def get_mark(name):
	while True:
		try:
			mark = float(input(f"Enter marks for {name} (0-100): ").strip())
		except ValueError:
			print("Invalid input. Please enter a number.")
			continue

		if not math.isfinite(mark) or not 0 <= mark <= 100:
			print("Marks must be between 0 and 100. Please try again.")
			continue
		return mark


def get_grade(mark):
	if mark >= 90:
		return "A"
	if mark >= 80:
		return "B"
	if mark >= 70:
		return "C"
	if mark >= 60:
		return "D"
	return "F"


def main():
	students = []
	for number in range(1, 6):
		name = input(f"Enter name of student {number}: ").strip()
		mark = get_mark(name)
		students.append((name, mark, get_grade(mark)))

	print("\nStudent Results")
	print(f"{'Name':<20}{'Marks':>10}{'Grade':>10}")
	print("-" * 40)
	for name, mark, grade in students:
		print(f"{name:<20}{mark:>10.2f}{grade:>10}")


if __name__ == "__main__":
	main()
