%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(char *s);
int yylex(void);
%}

%token INT CHAR IDENTIFIER INTEGER CHARACTER
%token LESS GREATER LESSEQUAL GREATEREQUAL EQUAL
%token PLUS MINUS MULTIPLY DIVIDE
%token ASSIGN
%token CIN COUT
%token SEMICOLON

%%

program     : stmt
            | stmt program
            ;

stmt        : simpl_stmt
            | struct_stmt
            ;

struct_stmt : cmpd_stmt
            | if_stmt
            | while_stmt
            ;

if_stmt     : "if" "(" cond_stmt ")" "{" cmpd_stmt "}"
            ;

while_stmt  : "while" "(" cond_stmt ")" "{" cmpd_stmt "}"
            ;

cmpd_stmt   : simpl_stmt
            | simpl_stmt cmpd_stmt
            ;

simpl_stmt  : assign_stmt
            | io_stmt
            ;

io_stmt     : io_op identifier SEMICOLON
            | io_op INTEGER SEMICOLON
            | io_op CHARACTER SEMICOLON
            ;

assign_stmt : identifier ASSIGN INTEGER SEMICOLON
            | identifier ASSIGN CHARACTER SEMICOLON
            | identifier ASSIGN arith_exp SEMICOLON
            ;

cond_stmt   : identifier comp_op identifier
            | identifier comp_op INTEGER
            | INTEGER comp_op INTEGER
            | INTEGER comp_op identifier
            ;

arith_exp   : arith_operand arith_op arith_operand
            ;

arith_operand : identifier
              | INTEGER
              ;

decl_stmt   : INT identifier SEMICOLON
            | CHAR identifier SEMICOLON
            ;

identifier  : IDENTIFIER
            ;

io_op       : CIN
            | COUT
            ;

comp_op     : LESS
            | GREATER
            | LESSEQUAL
            | GREATEREQUAL
            | EQUAL
            ;

arith_op    : PLUS
            | MINUS
            | MULTIPLY
            | DIVIDE
            ;

%%

void yyerror(char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    yyparse();
    return 0;
}
