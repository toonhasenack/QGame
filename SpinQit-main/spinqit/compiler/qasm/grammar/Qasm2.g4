/***** ANTLRv4  grammar for OpenQASM2.0. *****/

grammar Qasm2;

/**** Parser grammar ****/

program
    : header (globalStatement | statement)* EOF
    ;

header
    : version? include*
    ;

version
    : 'OPENQASM' ( Integer | RealNumber ) SEMICOLON
    ;

include
    : 'include' StringLiteral SEMICOLON
    ;

globalStatement
    : quantumDeclarationStatement  // qubits are declared globally
    | quantumGateDefinition
    | classicalDeclarationStatement
    ;

statement
    : quantumStatement
    | assignmentStatement
    | branchingStatement
    ;

quantumDeclarationStatement : quantumDeclaration SEMICOLON ;

classicalDeclarationStatement
    : ( classicalDeclaration | constantDeclaration ) SEMICOLON
    ;

//classicalAssignment
//    : Identifier designator? ( assignmentOperator expression )?
//    ;

assignmentStatement : quantumMeasurementAssignment SEMICOLON ;

returnSignature
    : ARROW classicalType
    ;

/*** Types and Casting ***/

designator
    : LBRACKET expression RBRACKET
    ;

doubleDesignator
    : LBRACKET expression COMMA expression RBRACKET
    ;

identifierList
    : ( Identifier COMMA )* Identifier
    ;

/** Quantum Types **/
quantumDeclaration
    : 'qreg' Identifier designator?
    ;

quantumArgument
    : 'qreg' Identifier designator? | 'qubit' designator? Identifier
    ;

quantumArgumentList
    : ( quantumArgument COMMA )* quantumArgument
    ;

/** Classical Types **/
bitType
    : 'bit'
    | 'creg'
    ;

singleDesignatorType
    : 'int'
    | 'uint'
    | 'float'
    | 'angle'
    ;

doubleDesignatorType
    : 'fixed'
    ;

noDesignatorType
    : 'bool'
    ;

classicalType
    : singleDesignatorType designator
    | doubleDesignatorType doubleDesignator
    | noDesignatorType
    | bitType designator?
    ;

constantDeclaration
    : 'const' Identifier equalsExpression?
    ;

// if multiple variables declared at once, either none are assigned or all are assigned
// prevents ambiguity w/ qubit arguments in subroutine calls
singleDesignatorDeclaration
    : singleDesignatorType designator Identifier equalsExpression?
    ;

doubleDesignatorDeclaration
    : doubleDesignatorType doubleDesignator Identifier equalsExpression?
    ;

noDesignatorDeclaration
    : noDesignatorType Identifier equalsExpression?
    ;

bitDeclaration
    : ( 'creg' Identifier designator? | 'bit' designator? Identifier ) equalsExpression?
    ;

classicalDeclaration
    : singleDesignatorDeclaration
    | doubleDesignatorDeclaration
    | noDesignatorDeclaration
    | bitDeclaration
    ;

classicalTypeList
    : ( classicalType COMMA )* classicalType
    ;

classicalArgument
    :
    (
        singleDesignatorType designator |
        doubleDesignatorType doubleDesignator |
        noDesignatorType
    ) Identifier
    | 'creg' Identifier designator?
    | 'bit' designator? Identifier
    ;

classicalArgumentList
    : ( classicalArgument COMMA )* classicalArgument
    ;

/** Aliasing **/
//aliasStatement
//    : 'let' Identifier EQUALS indexIdentifier SEMICOLON
//    ;

/** Register Concatenation and Slicing **/

indexIdentifier
    : Identifier rangeDefinition
    | Identifier ( LBRACKET expressionList RBRACKET )?
    | indexIdentifier '||' indexIdentifier
    ;

indexIdentifierList
    : ( indexIdentifier COMMA )* indexIdentifier
    ;

rangeDefinition
    : LBRACKET expression? COLON expression? ( COLON expression )? RBRACKET
    ;

/*** Gates and Built-in Quantum Instructions ***/

quantumGateDefinition
    : 'gate' quantumGateSignature quantumBlock
    ;

quantumGateParameter
    : LPAREN identifierList? RPAREN
    ;

quantumGateName
    : 'U'
    | 'CX'
    | Identifier
    ;

quantumGateSignature
    : Identifier ( quantumGateParameter )? identifierList
    ;

quantumBlock
    : LBRACE ( quantumStatement )* RBRACE
    ;

quantumLoopBlock
    : quantumStatement
    | LBRACE quantumStatement* RBRACE
    ;

quantumStatement
    : quantumInstruction SEMICOLON
    ;

quantumInstruction
    : quantumGateCall
    | quantumMeasurement
    | quantumBarrier
    ;

// quantumPhase
//     : 'gphase' LPAREN expression RPAREN
//     ;

// quantumReset
//    : 'reset' indexIdentifierList
//    ;

quantumMeasurement
    : 'measure' indexIdentifierList
    ;

quantumMeasurementAssignment
    : quantumMeasurement ( ARROW indexIdentifierList)?
    | indexIdentifierList EQUALS quantumMeasurement
    ;

quantumBarrier
    : 'barrier' indexIdentifierList
    ;

// quantumGateModifier
//    : ( 'inv' | 'pow' LPAREN expression RPAREN | 'ctrl' ) '@'
//    ;

quantumGateCall
    : quantumGateName ( LPAREN expressionList? RPAREN )? indexIdentifierList
    ;

/*** Classical Instructions ***/

unaryOperator
    : '~' | '!' | '-'
    ;

comparisonOperator
    : '>'
    | '<'
    | '>='
    | '<='
    ;

equalityOperator
    : '=='
    | '!='
    ;

logicalOperator
    : '&&'
    | '||'
    ;

expressionStatement
    : expression SEMICOLON
    ;

expression
    // include terminator/unary as base cases to simplify parsing
    : expressionTerminator
    | unaryExpression
    // expression hierarchy
    | logicalAndExpression
    | expression '||' logicalAndExpression
    | builtInMath expressionTerminator
    ;

/**  Expression hierarchy for non-terminators. Adapted from ANTLR4 C
  *  grammar: https://github.com/antlr/grammars-v4/blob/master/c/C.g4
  * Order (first to last evaluation):
    Terminator (including Parens),
    Unary Op,
    Multiplicative
    Additive
    Bit Shift
    Comparison
    Equality
    Bit And
    Exlusive Or (xOr)
    Bit Or
    Logical And
    Logical Or
**/

logicalAndExpression
    : bitOrExpression
    | logicalAndExpression '&&' bitOrExpression
    ;

bitOrExpression
    : xOrExpression
    | bitOrExpression '|' xOrExpression
    ;

xOrExpression
    : bitAndExpression
    | xOrExpression '^' bitAndExpression
    ;

bitAndExpression
    : equalityExpression
    | bitAndExpression '&' equalityExpression
    ;

equalityExpression
    : comparisonExpression
    | equalityExpression equalityOperator comparisonExpression
    ;

comparisonExpression
    : bitShiftExpression
    | comparisonExpression comparisonOperator bitShiftExpression
    ;

bitShiftExpression
    : additiveExpression
    | bitShiftExpression ( '<<' | '>>' ) additiveExpression
    ;

additiveExpression
    : multiplicativeExpression
    | additiveExpression ( PLUS | MINUS ) multiplicativeExpression
    ;

multiplicativeExpression
    // base case either terminator or unary
    : expressionTerminator
    | unaryExpression
    | multiplicativeExpression ( MUL | DIV | MOD ) ( expressionTerminator | unaryExpression )
    ;

unaryExpression
    : unaryOperator expressionTerminator
    ;

expressionTerminator
    : Constant
    | Integer
    | RealNumber
    | booleanLiteral
    | Identifier
    | StringLiteral
    | LPAREN expression RPAREN
    | expressionTerminator LBRACKET expression RBRACKET
    | expressionTerminator incrementor
    | builtInMath LPAREN expression RPAREN
    ;
/** End expression hierarchy **/

booleanLiteral
    : 'true' | 'false'
    ;

incrementor
    : '++'
    | '--'
    ;

builtInCall
    : ( builtInMath | castOperator ) LPAREN expressionList RPAREN
    ;

builtInMath
    : 'sin' | 'cos' | 'tan' | 'exp' | 'ln' | 'sqrt' | 'rotl' | 'rotr' | 'popcount' | 'lengthof'
    ;

castOperator
    : classicalType
    ;

expressionList
    : ( expression COMMA )* expression
    ;

equalsExpression
    : EQUALS expression
    ;

assignmentOperator
    : EQUALS
    | '+=' | '-=' | '*=' | '/=' | '&=' | '|=' | '~=' | '^=' | '<<=' | '>>='
    ;

setDeclaration
    : LBRACE expressionList RBRACE
    | rangeDefinition
    | Identifier
    ;

programBlock
    : statement 
    | LBRACE ( statement )* RBRACE
    ;


branchingStatement
    : 'if' LPAREN expression RPAREN programBlock ( 'else' programBlock )?
    ;

//returnStatement
//    : 'return' ( expression | quantumMeasurement )? SEMICOLON;

//kernelDeclaration
//    : 'kernel' Identifier ( LPAREN classicalTypeList? RPAREN )? returnSignature? SEMICOLON
//    ;

// if have kernel w/ out args, is ambiguous; may get matched as identifier
//kernelCall
//    : Identifier LPAREN expressionList? RPAREN
//    ;

/*** Subroutines ***/


/*** Directives ***/

//pragma
//    : '#pragma' LBRACE statement* RBRACE  // match any valid openqasm statement
//    ;

/*** Circuit Timing ***/


/*** Pulse Level Descriptions of Gates and Measurement ***/
// TODO: Update when pulse grammar is formalized






/**** Lexer grammar ****/

LBRACKET : '[' ;
RBRACKET : ']' ;

LBRACE : '{' ;
RBRACE : '}' ;

LPAREN : '(' ;
RPAREN : ')' ;

COLON: ':' ;
SEMICOLON : ';' ;

DOT : '.' ;
COMMA : ',' ;

EQUALS : '=' ;
ARROW : '->' ;

PLUS : '+';
MINUS : '-' ;
MUL : '*';
DIV : '/';
MOD : '%';


Constant : ( 'pi' | 'π' | 'tau' | '𝜏' | 'euler' | 'ℇ' );

Whitespace : [ \t]+ -> skip ;
Newline : [\r\n]+ -> skip ;

fragment Digit : [0-9] ;
Integer : Digit+ ;

fragment ValidUnicode : [\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}] ; // valid unicode chars
fragment Letter : [A-Za-z] ;
fragment FirstIdCharacter : '_' | '$' | ValidUnicode | Letter ;
fragment GeneralIdCharacter : FirstIdCharacter | Integer;

StretchN : 'stretch' Digit* ;
Identifier : FirstIdCharacter GeneralIdCharacter* ;

fragment SciNotation : [eE] ;
fragment PlusMinus : PLUS | MINUS ;
fragment Float : Digit+ DOT Digit* ;
RealNumber : Float (SciNotation PlusMinus? Integer )? ;

fragment TimeUnit : 'dt' | 'ns' | 'us' | 'µs' | 'ms' | 's' ;
// represents explicit time value in SI or backend units
TimingLiteral : (Integer | RealNumber ) TimeUnit ;

// allow ``"str"`` and ``'str'``
StringLiteral
    : '"' ~["\r\t\n]+? '"'
    | '\'' ~['\r\t\n]+? '\''
    ;

// skip comments
LineComment : '//' ~[\r\n]* -> skip;
BlockComment : '/*' .*? '*/' -> skip;
