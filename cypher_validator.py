import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from CypherLexer import CypherLexer
from CypherParser import CypherParser

class CypherErrorListener(ErrorListener):
  def __init__(self):
    super(CypherErrorListener, self).__init__()
    self.errors = []

  def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
    self.errors.append(f"line {line}:{column} {msg}")

  def has_errors(self):
    return len(self.errors) > 0

  def get_errors(self):
    return self.errors

def validate_query(query):
  multi_line_query = ""
  while True:
    line = input("Enter next line of your Cypher query (or press Enter to finish): ")
    if not line:
      break
    multi_line_query += line + "\n"

  input_stream = InputStream(multi_line_query)
  lexer = CypherLexer(input_stream)
  stream = CommonTokenStream(lexer)
  parser = CypherParser(stream)
  error_listener = CypherErrorListener()
  parser.removeErrorListeners()
  parser.addErrorListener(error_listener)

  try:
    parser.oC_Cypher()
    if error_listener.has_errors():
      print(f"{ANSI_RED}Cypher query is invalid:{ANSI_RESET}")
      for error in error_listener.get_errors():
        print(error)
    else:
      print(f"{ANSI_GREEN}Cypher query is valid.{ANSI_RESET}")
  except Exception as e:
    print(f"{ANSI_RED}Cypher query is invalid: {e}{ANSI_RESET}")

ANSI_RED = "\033[91m"
ANSI_GREEN = "\033[92m"
ANSI_RESET = "\033[0m"

if __name__ == "__main__":
  validate_query(None)