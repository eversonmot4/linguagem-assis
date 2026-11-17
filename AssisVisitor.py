# Generated from Assis.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .AssisParser import AssisParser
else:
    from AssisParser import AssisParser

# This class defines a complete generic visitor for a parse tree produced by AssisParser.

class AssisVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by AssisParser#program.
    def visitProgram(self, ctx:AssisParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#statement.
    def visitStatement(self, ctx:AssisParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#functionDecl.
    def visitFunctionDecl(self, ctx:AssisParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#paramList.
    def visitParamList(self, ctx:AssisParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#param.
    def visitParam(self, ctx:AssisParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#returnStmt.
    def visitReturnStmt(self, ctx:AssisParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#varDecl.
    def visitVarDecl(self, ctx:AssisParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#whileStatement.
    def visitWhileStatement(self, ctx:AssisParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#type.
    def visitType(self, ctx:AssisParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#ifStmt.
    def visitIfStmt(self, ctx:AssisParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#block.
    def visitBlock(self, ctx:AssisParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#exprStmt.
    def visitExprStmt(self, ctx:AssisParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#atribuicao.
    def visitAtribuicao(self, ctx:AssisParser.AtribuicaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#comparacao.
    def visitComparacao(self, ctx:AssisParser.ComparacaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#expressaoAritmetica.
    def visitExpressaoAritmetica(self, ctx:AssisParser.ExpressaoAritmeticaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#exprLog.
    def visitExprLog(self, ctx:AssisParser.ExprLogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:AssisParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:AssisParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#chamadaFuncao.
    def visitChamadaFuncao(self, ctx:AssisParser.ChamadaFuncaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#identificador.
    def visitIdentificador(self, ctx:AssisParser.IdentificadorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#inteiroLiteral.
    def visitInteiroLiteral(self, ctx:AssisParser.InteiroLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#floatLiteral.
    def visitFloatLiteral(self, ctx:AssisParser.FloatLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#charLiteral.
    def visitCharLiteral(self, ctx:AssisParser.CharLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#textoLiteral.
    def visitTextoLiteral(self, ctx:AssisParser.TextoLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#trueLiteral.
    def visitTrueLiteral(self, ctx:AssisParser.TrueLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#falseLiteral.
    def visitFalseLiteral(self, ctx:AssisParser.FalseLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#entreParenteses.
    def visitEntreParenteses(self, ctx:AssisParser.EntreParentesesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AssisParser#entreChaves.
    def visitEntreChaves(self, ctx:AssisParser.EntreChavesContext):
        return self.visitChildren(ctx)



del AssisParser