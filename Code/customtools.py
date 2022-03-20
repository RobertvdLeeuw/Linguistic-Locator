def CheckFile(function):  # Requires the first argument (no keyword) to be  the filepath (Path).
	def wrapper(*args, **kwargs):
		file = args[0]

		if file.exists():
			'''if file.is_file:
				output = function(*args, **kwargs)

				return output
			else:
				print(f"ERROR: '{filePath}' is not a file.")'''

			output = function(*args, **kwargs)
			return output
		else:
			print(f"ERROR: '{file}'not found.")

	return wrapper
