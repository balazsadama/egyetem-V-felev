%{
#include <iostream>
using namespace std;

int yyerror(const char*);
extern int yylex();

int nrBegunConditionals = 0;
//extern int columnCount;
extern int poz[];
%}
%error-verbose

%union {
  int num_integer;
  double num_real;
  char* text_string;
}


%nonassoc EQUALS_VALUE EQUALS_REFERENCE
%nonassoc LESS_THAN LESS_THAN_OR_EQUAL_TO
%nonassoc GREATER_THAN GREATER_THAN_OR_EQUAL_TO
%right NOT
%left AND OR
%left '+' '-'
%left '*' '/'

%token<num_integer> INTEGER
%token<num_real> REAL
%token<text_string> STRING
%token NEWLINE

%type<num_integer> expression_integer
%type<num_real> expression_real
%type<text_string> expression_string

%token TYPE_REAL TYPE_INTEGER TYPE_STRING VARIABLE
%token GIVEN THEN OTHERWISE
%token WHILE DO

%token EQUALS_VALUE EQUALS_REFERENCE
%token LESS_THAN LESS_THAN_OR_EQUAL_TO
%token GREATER_THAN GREATER_THAN_OR_EQUAL_TO
%token NOT
%token PRINT READ

%token ENDCOND ENDWHILE

%%

program :
        | program expression
        | program assignment
        | program conditional
        | program while
        | program print
        | program NEWLINE
        | program declaration
        | program input
;

declaration: TYPE_INTEGER assignment
           | TYPE_REAL assignment
           | TYPE_STRING assignment
           | TYPE_INTEGER VARIABLE
           | TYPE_REAL VARIABLE
           | TYPE_STRING VARIABLE
;

input: READ VARIABLE
;

expression: expression_integer
          | expression_real
          | expression_string
          | VARIABLE
          | '(' expression ')'
          | '(' expression error ')' { yyerrok; }
          | expression '+' expression {}
          | expression '-' expression {}
          | expression '*' expression {}
          | expression '/' expression {}
          | condition {}
          | VARIABLE '[' expression ']'
          | VARIABLE '[' expression error ']' { yyerrok; }
;

expression_integer: INTEGER { /*$$ = $1; cout << $1 << endl;*/ };
expression_real: REAL { /*$$ = $1; cout << $1 << endl;*/ };
expression_string: STRING { /*$$ = $1; cout << $1 << endl;*/ };

assignment: VARIABLE '=' expression
          | VARIABLE '=' error expression { yyerrok; }
;


conditional: GIVEN longer_condition THEN program ENDCOND {}
          
           | GIVEN longer_condition THEN program OTHERWISE program ENDCOND {}
          
;

while: WHILE longer_condition DO program ENDWHILE
     
;

condition: expression EQUALS_VALUE expression
         | expression EQUALS_REFERENCE expression
         | expression LESS_THAN expression
         | expression LESS_THAN_OR_EQUAL_TO expression
         | expression GREATER_THAN expression
         | expression GREATER_THAN_OR_EQUAL_TO expression
         
         | expression NOT EQUALS_VALUE expression
         | expression NOT EQUALS_REFERENCE expression
         | expression NOT LESS_THAN expression
         | expression NOT LESS_THAN_OR_EQUAL_TO expression
         | expression NOT GREATER_THAN expression
         | expression NOT GREATER_THAN_OR_EQUAL_TO expression
;



longer_condition: longer_condition AND longer_condition
                | longer_condition OR longer_condition
                | condition 
                | condition error { yyerrok; }
;

print: PRINT longer_expression
;

longer_expression: expression
                 | longer_expression ',' expression { yyerrok; }
;

%%

int main() {
  yyparse();
}

int yyerror(const char* s) {
	//cout << "(" << yylineno << ", " << columnCount << ") " << s << endl;
  cout << "(" << poz[0] << ", " << poz[1]-poz[2] << "): ";
	cout << s << endl;
}
