// currently struggling with introspection in writing the visitor class

#include <cstring>
#include <stdexcept>
#include <string>
using namespace std;

string INT = "INT", PLUS = "PLUS", MINUS = "MINUS", MUL = "MUL", DIV = "DIV",
       LP = "LP", RP = "RP", EOS = "EOS";

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
  Lexer(const string &text)
      : m_text(text), pos(0), maxLen(text.size()), ch(text[0]) {}

  Token getNextToken() {
    if (pos >= maxLen) {
      return Token(EOS, "\0");
    }

    if (isdigit(ch)) {
      advance();
      return Token(INT, getInt());
    }

    if (ch == '+') {
      advance();
      return Token(PLUS, "+");
    }

    if (ch == '-') {
      advance();
      return Token(MINUS, "-");
    }

    if (ch == '*') {
      advance();
      return Token(MUL, "*");
    }

    if (ch == '/') {
      advance();
      return Token(DIV, "/");
    }

    if (ch == '(') {
      advance();
      return Token(LP, "(");
    }

    if (ch == ')') {
      advance();
      return Token(RP, ")");
    }

    throw runtime_error("Invalid input!");
  }

private:
  bool advance() {
    if (pos < maxLen) {
      pos++;
      ch = m_text[pos];
      return true;
    } else {
      return false;
    }
  }
  string getInt() {
    string intStr = &""[ch]; // TODO: check this
    while (isdigit(ch)) {
      intStr += ch;
      if (!advance()) {
        break;
      }
    }
    return intStr;
  }

  string m_text;
  int pos;
  size_t maxLen;
  char ch;
};

class AST {};

class BinOp : public AST {
public:
  BinOp(const AST &left, const Token &op, const AST &right)
      : m_left(left), m_op(op), m_right(right) {}

  AST getLeft() { return m_left; }
  AST getRight() { return m_right; }
  string getOp() { return m_op.getKind(); }

private:
  AST m_left;
  Token m_op;
  AST m_right;
};

class Num : public AST {
public:
  Num(const Token &token) : m_token(token) {}

  string getValue() { return m_token.getValue(); }

private:
  Token m_token;
};

class Parser {
public:
  Parser(Lexer lexer) : m_lexer(lexer), currToken(lexer.getNextToken()) {}

  void eat(const string &type) {
    if (currToken.getKind() == type) {
      currToken = m_lexer.getNextToken();
    } else {
      throw runtime_error("Invalid syntax!");
    }
  }

  AST parse() { return expr(); }

  AST expr() {
    AST node = term();

    while (currToken.getKind() == PLUS || currToken.getKind() == MINUS) {
      if (currToken.getKind() == PLUS) {
        eat(PLUS);
        node = BinOp(node, currToken, term());
      } else if (currToken.getKind() == MINUS) {
        eat(MINUS);
        node = BinOp(node, currToken, term());
      }
    }
    return node;
  }

  AST term() {
    AST node = factor();

    while (currToken.getKind() == MUL || currToken.getKind() == DIV) {
      if (currToken.getKind() == MUL) {
        eat(MUL);
        node = BinOp(node, currToken, factor());
      } else if (currToken.getKind() == DIV) {
        eat(DIV);
        node = BinOp(node, currToken, factor());
      }
    }
    return node;
  }

  AST factor() {
    if (currToken.getKind() == INT) {
      eat(INT);
      return Num(currToken);
    } else if (currToken.getKind() == LP) {
      eat(LP);
      AST result = expr();
      eat(RP);
      return result;
    }
    throw runtime_error("Parser error!");
  }

private:
  Lexer m_lexer;
  Token currToken;
};

// class NodeVisitor {
// public:
//   int visit(AST &node) {
//     string name = typeid(node).name();
//     // the class will contain a function like visit_BinOp()
//     // want to do:
//     // return (this->visitBinOp(node))
//     // how to do this without introspection??

//     // int (*visitor)()
//   }
// }

class Interpreter {
public:
  Interpreter(Lexer &parser) : m_parser(parser) {}

  int visit(AST &node) { ... }

private:
  Parser m_parser;
}
