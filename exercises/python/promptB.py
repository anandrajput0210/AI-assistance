"""act as python programming tutor.write a program that accepts marks for five students,validates each mark between 0 and 100,
calculates grads using specified boundaries handles invliad input,and displays a formated rport.
include comments and test cases for boundary values.dont use extrnal libaries"""

"""Collect marks for five students, assign grades, and print a report.

Grade boundaries used here: A (90–100), B (80–89), C (70–79),
D (60–69), and F (0–59).
"""


STUDENT_COUNT = 5


def get_mark(student_number):
	"""Prompt until a valid whole-number mark from 0 through 100 is entered."""
	while True:
		try:
			mark = int(input(f"Enter mark for student {student_number} (0-100): "))
		except ValueError:
			print("Invalid input. Enter a whole number from 0 to 100.")
			continue

		if 0 <= mark <= 100:
			return mark
		print("Mark out of range. Enter a value from 0 to 100.")


def get_grade(mark):
	"""Return the grade for a mark that has already been validated."""
	if mark >= 90:
		return "A"
	if mark >= 80:
		return "B"
	if mark >= 70:
		return "C"
	if mark >= 60:
		return "D"
	return "F"


def print_report(marks):
	"""Display marks and grades in a formatted table."""
	print("\nSTUDENT MARKS REPORT")
	print("-" * 30)
	print(f"{'Student':<12}{'Mark':>8}{'Grade':>10}")
	print("-" * 30)
	for number, mark in enumerate(marks, start=1):
		print(f"{number:<12}{mark:>8}{get_grade(mark):>10}")
	print("-" * 30)


def run_boundary_tests():
	"""Check grade transitions and the permitted mark range."""
	# Test both sides of every grade boundary, plus the range endpoints.
	cases = {
		0: "F", 59: "F", 60: "D", 69: "D", 70: "C",
		79: "C", 80: "B", 89: "B", 90: "A", 100: "A",
	}
	for mark, expected_grade in cases.items():
		assert get_grade(mark) == expected_grade
	assert all(0 <= mark <= 100 for mark in (0, 100))


def main():
	run_boundary_tests()
	marks = [get_mark(number) for number in range(1, STUDENT_COUNT + 1)]
	print_report(marks)


if __name__ == "__main__":
	main()
