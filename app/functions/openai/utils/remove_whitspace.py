def remove_whitespace(string):
  # Remove leading and trailing whitespace.
  string = string.strip()

  # Remove leading indents.
  string = string.lstrip()

  # Remove newlines.
  string = string.replace("\n", "")

  return string