%{
#include <iostream>
using namespace std;

int yyerror(const char*);
extern int yylex();

int nrBegunConditionals = 0;
%}
%error-verbose

%union {
  int num_integer;
  double num_real;
  char* text_string;
}

%left '+' '-'
%left '*' '/'
%nonassoc EQUALS_VALUE
%nonassoc EQUALS_REFERENCE

%token<num_integer> INTEGER
%token<num_real> REAL
%token<text_string> STRING
%token NEWLINE

%type<num_integer> expression_integer
%type<num_real> expression_real
%type<text_string> expression_string

%token TYPE_REAL TYPE_INTEGER TYPE_STRING VARIABLE EQUALS_VALUE EQUALS_REFERENCE
%token GIVEN THEN OTHERWISE
%token WHILE DO

%%

program :
        | program expression
        | program assignment
        | program conditional
        | program NEWLINE
;


expression: expression_integer
          | expression_real
          | expression_string
          | VARIABLE
          | expression '+' expression { /*cout << "BISON arithmetic expression +\n";*/ }
          | expression '-' expression { /*cout << "BISON arithmetic expression -\n";*/ }
          | expression '*' expression { /*cout << "BISON arithmetic expression *\n";*/ }
          | expression '/' expression { /*cout << "BISON arithmetic expression /\n";*/ }
          | condition { /*cout << "BISON EQUALITY\n";*/ }
          | while
;

expression_integer: INTEGER { /*$$ = $1; cout << $1 << endl;*/ };
expression_real: REAL { /*$$ = $1; cout << $1 << endl;*/ };
expression_string: STRING { /*$$ = $1; cout << $1 << endl;*/ };

assignment: VARIABLE '=' expression { /*cout << "BISON assignment\n";*/ }
;


conditional: GIVEN condition THEN { //cout << "BISON conditional if\n"; 
                                      nrBegunConditionals++; }
           | OTHERWISE { if (nrBegunConditionals) { //cout << "BISON conditional else\n"; 
                                      nrBegunConditionals--;} else yyerror("syntax error"); }
;

while: WHILE condition DO { /*cout << "BISON WHILE\n";*/ }

condition: expression EQUALS_VALUE expression
;

%%

int main() {
  yyparse();
}

int yyerror(const char* s) {
	cout << s << endl;
}
