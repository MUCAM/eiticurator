def default_input(prompt, default_value, choices=None, closing_sign=":"):
  import readline
  if default_value in [None, ""] and len(choices)==1:
    default_value = choices[0]
  if choices == None:
    prompt = prompt + ": "
  else:
    prompt = prompt + ' [' + ", ".join(choices) + ']: '
  readline.set_startup_hook(lambda: readline.insert_text(default_value))
  try:
    return raw_input(prompt)
  finally:
    readline.set_startup_hook()


