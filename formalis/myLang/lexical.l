%{
#include "bison.tab.h"
#include <iostream>
#include <stdio.h>
using namespace std;

//int columnCount = 1;
int poz[] = {1, 1, 0};
%}
%option noyywrap
%option yylineno

%%


[+-]?[0-9]+ { poz[1] += yyleng;  poz[2] = yyleng;
        return INTEGER; }
[+-]?[0-9]+("."[0-9]+)+ { poz[1] += yyleng;  poz[2] = yyleng;
        return REAL; }
\"(\\\"|[^"])*\" { poz[1] += yyleng;  poz[2] = yyleng;
        return STRING; }

[\(\)\[\],] { poz[1] += yyleng;  poz[2] = yyleng; return yytext[0]; }

"===" { poz[1] += yyleng;  poz[2] = yyleng; return EQUALS_REFERENCE; }
"==" { poz[1] += yyleng;  poz[2] = yyleng; return EQUALS_VALUE; }
"<" { poz[1] += yyleng;  poz[2] = yyleng; return LESS_THAN; }
"<=" { poz[1] += yyleng;  poz[2] = yyleng; return LESS_THAN_OR_EQUAL_TO; }
">" { poz[1] += yyleng;  poz[2] = yyleng; return GREATER_THAN; }
">=" { poz[1] += yyleng;  poz[2] = yyleng; return GREATER_THAN_OR_EQUAL_TO; }
"!" { poz[1] += yyleng;  poz[2] = yyleng; return NOT; }
" not " { poz[1] += yyleng;  poz[2] = yyleng; return NOT; }

" and " { poz[1] += yyleng;  poz[2] = yyleng; return AND; }
" or " { poz[1] += yyleng;  poz[2] = yyleng; return OR; }

[+\-*/] { poz[1] += yyleng;  poz[2] = yyleng; return yytext[0]; }

"given " { poz[1] += yyleng;  poz[2] = yyleng; return GIVEN; }
" then" { poz[1] += yyleng;  poz[2] = yyleng; return THEN; }
"otherwise" { poz[1] += yyleng;  poz[2] = yyleng; return OTHERWISE; }
"endcond" { poz[1] += yyleng;  poz[2] = yyleng; return ENDCOND; }

"while " { poz[1] += yyleng;  poz[2] = yyleng; return WHILE; }
" do" { poz[1] += yyleng;  poz[2] = yyleng; return DO; }
"endwhile" { poz[1] += yyleng;  poz[2] = yyleng; return ENDWHILE; }

"integer" { poz[1] += yyleng;  poz[2] = yyleng; return TYPE_INTEGER; }
"real" { poz[1] += yyleng;  poz[2] = yyleng; return TYPE_REAL; }
"string" { poz[1] += yyleng;  poz[2] = yyleng; return TYPE_STRING; }
([_a-zA-Z]+[_a-zA-Z0-9]*) { poz[1] += yyleng;  poz[2] = yyleng; yylval.varName = strdup(yytext); return VARIABLE; }
"=" { poz[1] += yyleng;  poz[2] = yyleng; return yytext[0]; }

"read " { poz[1] += yyleng;  poz[2] = yyleng; return READ; }
"print " { poz[1] += yyleng;  poz[2] = yyleng; return PRINT; }

[ \t\r]+ { poz[1]+=yyleng; poz[2] = yyleng; }
\n	{ poz[1] = 1; poz[0]++; poz[2] = 1; }

%%
