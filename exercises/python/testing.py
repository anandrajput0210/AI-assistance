try:
	marks = float(input("Enter marks (0-100): "))
except ValueError:
	print("Invalid numeric input")
else:
	if not 0 <= marks <= 100:
		print("Invalid input: marks must be between 0 and 100")
	elif marks == 100:
		print("Highest")
	elif marks >= 75:
		print("Grade")
	elif marks >= 40:
		print("Passing")
	else:
		print("Lowest")
