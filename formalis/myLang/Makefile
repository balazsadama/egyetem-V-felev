all: compile

bison.tab.c bison.tab.h: bison.y
	bison -dvt bison.y

lex.yy.c: lexical.l bison.tab.h
	flex lexical.l

compile: lex.yy.c bison.tab.c bison.tab.h
	g++ bison.tab.c lex.yy.c

clean:
	rm bison.tab.c lex.yy.c bison.tab.h bison.output
