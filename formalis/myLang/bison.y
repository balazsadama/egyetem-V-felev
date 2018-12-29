%{
#include <iostream>
#include <cstring>
#include <string>
#include <map>
#include <list>
using namespace std;

int yyerror(const char*);
extern int yylex();
extern int poz[];

map<string, int> symbolTable;	// 0-int, 1-real, 2-string
list<map<string, int>> listOfMaps;

void declare(char* varName, int varType);
void verifyVariable(char* varName);
void verifyType(int t1, int t2);
void verifyType(char* t1, int t2);
int getType(char* varName);

%}
%error-verbose

%union {
  char* varName;
	int varType;
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

declaration: TYPE_INTEGER VARIABLE '=' expression { declare($<varName>2, 0); verifyType(listOfMaps.back()[$<varName>2], $<varType>4);}
           | TYPE_REAL VARIABLE '=' expression { declare($<varName>2, 1); verifyType(listOfMaps.back()[$<varName>2], $<varType>4); }
           | TYPE_STRING VARIABLE '=' expression { declare($<varName>2, 2); verifyType(listOfMaps.back()[$<varName>2], $<varType>4); }
           | TYPE_INTEGER VARIABLE { declare($<varName>2, 0); }
           | TYPE_REAL VARIABLE { declare($<varName>2, 1); }
           | TYPE_STRING VARIABLE { declare($<varName>2, 2); }
;

input: READ VARIABLE
;

expression: INTEGER { $<varType>$ = 0; }
          | REAL { $<varType>$ = 1; }
          | STRING { $<varType>$ = 2; }
          | VARIABLE { verifyVariable($<varName>1); $<varType>$ = listOfMaps.back()[$<varName>1]; }
          | '(' expression ')'
          | '(' expression error ')' { yyerrok; }
          | expression '+' expression { verifyType($<varType>1, $<varType>3); }
          | expression '-' expression { verifyType($<varType>1, $<varType>3); }
          | expression '*' expression { verifyType($<varType>1, $<varType>3); }
          | expression '/' expression { verifyType($<varType>1, $<varType>3); }
          | condition {}
          | VARIABLE '[' expression ']' { verifyVariable($<varName>1); }
          | VARIABLE '[' expression error ']' { verifyVariable($<varName>1); yyerrok; }
;


assignment: VARIABLE '=' expression { verifyType($<varName>1, $<varType>3);/*verifyType(listOfMaps.back()[$<varName>1], $<varType>3);*/ /*cout << $<varName>1 << " " << listOfMaps.back()[$<varName>1] << " with " << $<varType>3 << endl;*/ }
          | VARIABLE '=' error expression { yyerrok; }
;


conditional: startcond longer_condition THEN program endcond {}
           | startcond longer_condition THEN program OTHERWISE program endcond {}
;
startcond: GIVEN { listOfMaps.push_back(*(new map<string, int>)); }
;
endcond: ENDCOND { /*delete &(listOfMaps.back());*/ listOfMaps.pop_back(); }
;

while: startwhile longer_condition DO program endwhile
;
startwhile: WHILE { listOfMaps.push_back(*(new map<string, int>)); }
;
endwhile: ENDWHILE { /*delete &(listOfMaps.back());*/ listOfMaps.pop_back(); }
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
  listOfMaps.push_back(symbolTable);
  yyparse();
}

int yyerror(const char* s) {
	cout << "(" << poz[0] << ", " << poz[1]-poz[2] << "): ";
	cout << s << endl;
}

void declare(char* varName, int varType){
	if (listOfMaps.back().find(varName) != listOfMaps.back().end()) {
		char* errorMsg = strcat(varName," already declared!\n");
		yyerror(errorMsg);
	}
	else {
		listOfMaps.back()[varName] = varType;
		//program += (varType==0?"int ":"double ") + varName + ";\n";
	}
}

void verifyVariable(char* varName) {
	for (list<map<string, int>>::reverse_iterator it = listOfMaps.rbegin(); it != listOfMaps.rend(); ++it) {
    if (it->find(varName) != it->end()) {
      return;
    }
  }
  char* errorMsg = strcat(varName," not declared!\n");
  yyerror(errorMsg);
}

void verifyType(int t1, int t2) {
	if (t1 != t2) {
		char errorMsg[] = "Types don't match!";
		yyerror(errorMsg);
	}
}

void verifyType(char* varName, int t2) {
	verifyType(getType(varName), t2);
}

int getType(char* varName) {
  for (list<map<string, int>>::reverse_iterator it = listOfMaps.rbegin(); it != listOfMaps.rend(); ++it) {
    if (it->find(varName) != it->end()) {
      return it->find(varName)->second;
    }
  }
  // char* errorMsg = strcat(varName," not declared!\n");
  // yyerror(errorMsg);
  return -1;
}