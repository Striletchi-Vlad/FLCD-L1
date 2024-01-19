%{
#include "y.tab.h"
extern int yylval;
%}

%%

"int"               { return INT; }
"char"              { return CHAR; }
"<"                 { return LESS; }
">"                 { return GREATER; }
"<="                { return LESSEQUAL; }
">="                { return GREATEREQUAL; }
"=="                { return EQUAL; }
"+"                 { return PLUS; }
"-"                 { return MINUS; }
"*"                 { return MULTIPLY; }
"/"                 { return DIVIDE; }
"="                 { return ASSIGN; }
"cin>>"             { return CIN; }
"cout<<"            { return COUT; }
";"                 { return SEMICOLON; }
[0-9]+              { yylval = atoi(yytext); return INTEGER; }
\'[a-zA-Z]\'        { yylval = yytext[1]; return CHARACTER; }
[a-zA-Z_][a-zA-Z0-9_]*  { yylval = strdup(yytext); return IDENTIFIER; }

[ \t\n]             { /* Ignore whitespace. */ }
.                   { printf("Unexpected character: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}
