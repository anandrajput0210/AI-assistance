"""
write calculate_average(marks) in python.It must reject an empty list and any mark outside the range 0 and 100,
preserve the original list,and return the arithmetic mean.state how invlaid inouts are handled.
provide normal,boundary and invlaid-input tests.explain why the implementaion meets every requirement.
"""

"""Validated mark averaging.

An empty list or a mark outside 0..100 raises ValueError. A non-numeric
mark (including a boolean) raises TypeError.
"""

from numbers import Real


def calculate_average(marks):
	"""Return the arithmetic mean without modifying the original list."""
	if len(marks) == 0:
		raise ValueError("marks must not be empty")

	for mark in marks:
		if isinstance(mark, bool) or not isinstance(mark, Real):
			raise TypeError("each mark must be a real number")
		if not 0 <= mark <= 100:
			raise ValueError("each mark must be between 0 and 100")

	return sum(marks) / len(marks)


if __name__ == "__main__":
	# Normal test, including confirmation that the input list is unchanged.
	marks = [75, 80, 95]
	original = marks.copy()
	assert calculate_average(marks) == 250 / 3
	assert marks == original

	# Boundary tests: 0 and 100 are both valid.
	assert calculate_average([0]) == 0
	assert calculate_average([100]) == 100
	assert calculate_average([0, 100]) == 50

	# Invalid-input tests.
	for invalid_marks in ([], [-1], [101]):
		try:
			calculate_average(invalid_marks)
		except ValueError:
			pass
		else:
			raise AssertionError(f"Expected ValueError for {invalid_marks!r}")

	try:
		calculate_average(["90"])
	except TypeError:
		pass
	else:
		raise AssertionError("Expected TypeError for a non-numeric mark")
