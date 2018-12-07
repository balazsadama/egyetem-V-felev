%{
#include "bison.tab.h"
#include <iostream>
#include <stdio.h>
using namespace std;

int columnCount = 1;
%}
%option noyywrap
%option yylineno

%%


[+-]?[0-9]+ { //cout << "INTEGER LITERAL " << yytext << "\n";
        yylval.num_integer = atoi(yytext); return INTEGER; }
[+-]?[0-9]+("."[0-9]+)+ { //cout << "REAL LITERAL " << yytext << "\n";
        yylval.num_real = atof(yytext); return REAL; }
\"(\\\"|[^"])*\" { //cout << "STRING LITERAL " << yytext << "\n";
        yylval.text_string = yytext; return STRING; }

"===" { return EQUALS_REFERENCE; }
"==" { return EQUALS_VALUE; }

[+\-*/] { //cout << "arithmetic operator " << yytext << "\n";
        return yytext[0]; }

"given " { //cout << "beginning of conditional" << "\n";
        return GIVEN; }
" then" { //cout << "end of conditional" << "\n";
        return THEN; }
"otherwise" { //cout << "beginning of else" << "\n";
        return OTHERWISE; }

"while " { //cout << "beginning of while" << "\n";
        return WHILE; }
" do" { //cout << "end of while" << "\n";
        return DO; }


"integer" { //cout << "TYPE " << yytext << "\n";
        return TYPE_INTEGER; }
"real" { //cout << "TYPE " << yytext << "\n";
        return TYPE_REAL; }
([_a-zA-Z]+[_a-zA-Z0-9]*) { //cout << "variable " << yytext << "\n";
        return VARIABLE; }
"=" { return yytext[0]; }



[ \t\r]+ { columnCount++; }
\n	{ columnCount = 1; return NEWLINE; }

%%
