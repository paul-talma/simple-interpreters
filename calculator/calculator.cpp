#include <cctype>
#include <iostream>
#include <stdexcept>
#include <string>

using namespace std;

string INT = "INT", PLUS = "PLUS", MINUS = "MINUS", MUL = "MUL", DIV = "DIV", LP = "LP", RP = "RP",
       EOS = "EOS";

class Token {
public:
  Token(const string &kind, const string &value)
      : m_kind(kind), m_value(value) {}

  string getKind() { return m_kind; }

  string getValue() { return m_value; }

private:
  string m_kind;
  string m_value;
};

class Lexer {
public:
  Lexer(string &text)
      : m_text(text), pos(0), currentChar(text[pos]), maxLen(text.size()) {}

  Token getNextToken() {
    if (pos >= maxLen) {
      return Token(EOS, "\0"); // todo: check this
    }

    if (isdigit(currentChar)) {
      string intToken = getInt();
      return Token(INT, intToken);
    }

    if (isspace(currentChar)) {
      skipSpace();
      return getNextToken();
    }

    if (currentChar == '+') {
      advance();
      return Token(PLUS, "+");
    }

    if (currentChar == '-') {
      advance();
      return Token(MINUS, "-");
    }

    if (currentChar == '*') {
      advance();
      return Token(MUL, "*");
    }

    if (currentChar == '/') {
      advance();
      return Token(DIV, "/");
    }

    if (currentChar == '(') {
      advance();
      return Token(LP, "(");
    }

    if (currentChar == ')') {
      advance();
      return Token(RP, ")");
    }

    throw runtime_error("Invalid character!");
  }

private:
  bool advance() {
    pos++;
    if (pos < maxLen) {
      currentChar = m_text[pos];
      return true;
    } else {
      return false;
    }
  }

  void skipSpace() {
    while (isspace(currentChar)) {
      advance();
    }
  }

  string getInt() {
    string res = "";
    while (isdigit(currentChar)) {
      res += currentChar;
      if (!advance()) {
        break;
      }
    }
    return res;
  }

  const string m_text;
  int pos;
  const size_t maxLen;
  char currentChar;
};

class Interpreter {
public:
  Interpreter(Lexer & lexer) : m_lexer(lexer), currentToken(m_lexer.getNextToken()) {}

  int divisor(int fac) {
    if (fac == 0) {
      throw runtime_error("Dividing by 0!");
    } else {
      return fac;
    }
    
  }

  void eat(string kind) {
    if (currentToken.getKind() == kind) {
      currentToken = m_lexer.getNextToken();
    } else {
      error();
    }
  }

  int factor() {
    if (currentToken.getKind() == INT) {
      string val = currentToken.getValue();
      eat(INT);
      return stoi(val);
    } else if (currentToken.getKind() == LP) {
      eat(LP);
      int result = expr();
      eat(RP);
      return result;
    }
    error();
  }

  int term() {
    int result = factor();

    while (currentToken.getKind() == MUL || currentToken.getKind() == DIV) {
      string op = currentToken.getKind();

      if (op == MUL) {
        eat(MUL);
        result *= factor();
      }

      if (op == DIV) {
        eat(DIV);
        int fac = factor();
        if (fac == 0) {
            throw runtime_error("Dividing by 0!");
          }
        result /= factor();
      }
    }
    return result;
  }

  int expr() {
    int result = term();

    while (currentToken.getKind() == PLUS || currentToken.getKind() == MINUS) {
      string op = currentToken.getKind();

      if (op == PLUS) {
        eat(PLUS);
        result += term();
      }

      else if (op == MINUS) {
        eat(MINUS);
        result -= term();
      }
    }
    return result;
  }

  void error() { throw runtime_error("Invalid syntax."); }

private:
  Lexer m_lexer;
  Token currentToken;
};

int main() {
  string prompt = "calc>";
  string text;
  while (true) {
    cout << prompt << endl;
    getline(cin, text);
    Lexer lexer(text);
    Interpreter interpreter(lexer);
    cout << interpreter.expr() << endl;
  }
  return 0;
}
