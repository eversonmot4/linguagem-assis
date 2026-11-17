# Generated from Assis.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AssisParser import AssisParser
else:
    from AssisParser import AssisParser

# This class defines a complete listener for a parse tree produced by AssisParser.
class AssisListener(ParseTreeListener):

    # Enter a parse tree produced by AssisParser#program.
    def enterProgram(self, ctx:AssisParser.ProgramContext):
        pass

    # Exit a parse tree produced by AssisParser#program.
    def exitProgram(self, ctx:AssisParser.ProgramContext):
        pass


    # Enter a parse tree produced by AssisParser#statement.
    def enterStatement(self, ctx:AssisParser.StatementContext):
        pass

    # Exit a parse tree produced by AssisParser#statement.
    def exitStatement(self, ctx:AssisParser.StatementContext):
        pass


    # Enter a parse tree produced by AssisParser#functionDecl.
    def enterFunctionDecl(self, ctx:AssisParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by AssisParser#functionDecl.
    def exitFunctionDecl(self, ctx:AssisParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by AssisParser#paramList.
    def enterParamList(self, ctx:AssisParser.ParamListContext):
        pass

    # Exit a parse tree produced by AssisParser#paramList.
    def exitParamList(self, ctx:AssisParser.ParamListContext):
        pass


    # Enter a parse tree produced by AssisParser#param.
    def enterParam(self, ctx:AssisParser.ParamContext):
        pass

    # Exit a parse tree produced by AssisParser#param.
    def exitParam(self, ctx:AssisParser.ParamContext):
        pass


    # Enter a parse tree produced by AssisParser#returnStmt.
    def enterReturnStmt(self, ctx:AssisParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by AssisParser#returnStmt.
    def exitReturnStmt(self, ctx:AssisParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by AssisParser#varDecl.
    def enterVarDecl(self, ctx:AssisParser.VarDeclContext):
        pass

    # Exit a parse tree produced by AssisParser#varDecl.
    def exitVarDecl(self, ctx:AssisParser.VarDeclContext):
        pass


    # Enter a parse tree produced by AssisParser#whileStatement.
    def enterWhileStatement(self, ctx:AssisParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by AssisParser#whileStatement.
    def exitWhileStatement(self, ctx:AssisParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by AssisParser#type.
    def enterType(self, ctx:AssisParser.TypeContext):
        pass

    # Exit a parse tree produced by AssisParser#type.
    def exitType(self, ctx:AssisParser.TypeContext):
        pass


    # Enter a parse tree produced by AssisParser#ifStmt.
    def enterIfStmt(self, ctx:AssisParser.IfStmtContext):
        pass

    # Exit a parse tree produced by AssisParser#ifStmt.
    def exitIfStmt(self, ctx:AssisParser.IfStmtContext):
        pass


    # Enter a parse tree produced by AssisParser#block.
    def enterBlock(self, ctx:AssisParser.BlockContext):
        pass

    # Exit a parse tree produced by AssisParser#block.
    def exitBlock(self, ctx:AssisParser.BlockContext):
        pass


    # Enter a parse tree produced by AssisParser#exprStmt.
    def enterExprStmt(self, ctx:AssisParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by AssisParser#exprStmt.
    def exitExprStmt(self, ctx:AssisParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by AssisParser#atribuicao.
    def enterAtribuicao(self, ctx:AssisParser.AtribuicaoContext):
        pass

    # Exit a parse tree produced by AssisParser#atribuicao.
    def exitAtribuicao(self, ctx:AssisParser.AtribuicaoContext):
        pass


    # Enter a parse tree produced by AssisParser#comparacao.
    def enterComparacao(self, ctx:AssisParser.ComparacaoContext):
        pass

    # Exit a parse tree produced by AssisParser#comparacao.
    def exitComparacao(self, ctx:AssisParser.ComparacaoContext):
        pass


    # Enter a parse tree produced by AssisParser#expressaoAritmetica.
    def enterExpressaoAritmetica(self, ctx:AssisParser.ExpressaoAritmeticaContext):
        pass

    # Exit a parse tree produced by AssisParser#expressaoAritmetica.
    def exitExpressaoAritmetica(self, ctx:AssisParser.ExpressaoAritmeticaContext):
        pass


    # Enter a parse tree produced by AssisParser#exprLog.
    def enterExprLog(self, ctx:AssisParser.ExprLogContext):
        pass

    # Exit a parse tree produced by AssisParser#exprLog.
    def exitExprLog(self, ctx:AssisParser.ExprLogContext):
        pass


    # Enter a parse tree produced by AssisParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:AssisParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by AssisParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:AssisParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by AssisParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:AssisParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by AssisParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:AssisParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by AssisParser#chamadaFuncao.
    def enterChamadaFuncao(self, ctx:AssisParser.ChamadaFuncaoContext):
        pass

    # Exit a parse tree produced by AssisParser#chamadaFuncao.
    def exitChamadaFuncao(self, ctx:AssisParser.ChamadaFuncaoContext):
        pass


    # Enter a parse tree produced by AssisParser#identificador.
    def enterIdentificador(self, ctx:AssisParser.IdentificadorContext):
        pass

    # Exit a parse tree produced by AssisParser#identificador.
    def exitIdentificador(self, ctx:AssisParser.IdentificadorContext):
        pass


    # Enter a parse tree produced by AssisParser#inteiroLiteral.
    def enterInteiroLiteral(self, ctx:AssisParser.InteiroLiteralContext):
        pass

    # Exit a parse tree produced by AssisParser#inteiroLiteral.
    def exitInteiroLiteral(self, ctx:AssisParser.InteiroLiteralContext):
        pass


    # Enter a parse tree produced by AssisParser#floatLiteral.
    def enterFloatLiteral(self, ctx:AssisParser.FloatLiteralContext):
        pass

    # Exit a parse tree produced by AssisParser#floatLiteral.
    def exitFloatLiteral(self, ctx:AssisParser.FloatLiteralContext):
        pass


    # Enter a parse tree produced by AssisParser#charLiteral.
    def enterCharLiteral(self, ctx:AssisParser.CharLiteralContext):
        pass

    # Exit a parse tree produced by AssisParser#charLiteral.
    def exitCharLiteral(self, ctx:AssisParser.CharLiteralContext):
        pass


    # Enter a parse tree produced by AssisParser#textoLiteral.
    def enterTextoLiteral(self, ctx:AssisParser.TextoLiteralContext):
        pass

    # Exit a parse tree produced by AssisParser#textoLiteral.
    def exitTextoLiteral(self, ctx:AssisParser.TextoLiteralContext):
        pass


    # Enter a parse tree produced by AssisParser#trueLiteral.
    def enterTrueLiteral(self, ctx:AssisParser.TrueLiteralContext):
        pass

    # Exit a parse tree produced by AssisParser#trueLiteral.
    def exitTrueLiteral(self, ctx:AssisParser.TrueLiteralContext):
        pass


    # Enter a parse tree produced by AssisParser#falseLiteral.
    def enterFalseLiteral(self, ctx:AssisParser.FalseLiteralContext):
        pass

    # Exit a parse tree produced by AssisParser#falseLiteral.
    def exitFalseLiteral(self, ctx:AssisParser.FalseLiteralContext):
        pass


    # Enter a parse tree produced by AssisParser#entreParenteses.
    def enterEntreParenteses(self, ctx:AssisParser.EntreParentesesContext):
        pass

    # Exit a parse tree produced by AssisParser#entreParenteses.
    def exitEntreParenteses(self, ctx:AssisParser.EntreParentesesContext):
        pass


    # Enter a parse tree produced by AssisParser#entreChaves.
    def enterEntreChaves(self, ctx:AssisParser.EntreChavesContext):
        pass

    # Exit a parse tree produced by AssisParser#entreChaves.
    def exitEntreChaves(self, ctx:AssisParser.EntreChavesContext):
        pass



del AssisParser