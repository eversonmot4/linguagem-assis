// Generated from /home/everson/Vscode/Linguagem Assis/Assis.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class AssisParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		TP_INT=1, TP_FLOAT=2, TP_CHAR=3, TP_BOOL=4, TP_STRING=5, KW_IF=6, KW_ELSE=7, 
		KW_ELSEIF=8, TRUE=9, FALSE=10, FUNC=11, RETURN=12, WHILE=13, REAL=14, 
		INT=15, ID=16, CHAR=17, STRING=18, ATRIB=19, OP_SOMA=20, OP_SUB=21, OP_MULT=22, 
		OP_DIV=23, OP_LE=24, OP_GE=25, OP_EQ=26, OP_NE=27, OP_LT=28, OP_GT=29, 
		PAR_ESQ=30, PAR_DIR=31, CHAVE_ESQ=32, CHAVE_DIR=33, VIRGULA=34, PONTO_VIRGULA=35, 
		PONTO=36, LINE_COMMENT=37, BLOCK_COMMENT=38, WS=39;
	public static final int
		RULE_program = 0, RULE_statement = 1, RULE_functionDecl = 2, RULE_paramList = 3, 
		RULE_param = 4, RULE_returnStmt = 5, RULE_varDecl = 6, RULE_whileStatement = 7, 
		RULE_type = 8, RULE_ifStmt = 9, RULE_block = 10, RULE_exprStmt = 11, RULE_expr = 12, 
		RULE_exprLog = 13, RULE_additiveExpr = 14, RULE_multiplicativeExpr = 15, 
		RULE_primaryExpr = 16;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "statement", "functionDecl", "paramList", "param", "returnStmt", 
			"varDecl", "whileStatement", "type", "ifStmt", "block", "exprStmt", "expr", 
			"exprLog", "additiveExpr", "multiplicativeExpr", "primaryExpr"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'int'", "'float'", "'char'", "'bool'", "'String'", "'si'", "'aliter'", 
			"'alitersi'", "'verum'", "'falsum'", "'funct'", "'redire'", "'dum'", 
			null, null, null, null, null, "'='", "'+'", "'-'", "'*'", "'/'", "'<='", 
			"'>='", "'=='", "'!='", "'<'", "'>'", "'('", "')'", "'{'", "'}'", "','", 
			"';'", "'.'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "TP_INT", "TP_FLOAT", "TP_CHAR", "TP_BOOL", "TP_STRING", "KW_IF", 
			"KW_ELSE", "KW_ELSEIF", "TRUE", "FALSE", "FUNC", "RETURN", "WHILE", "REAL", 
			"INT", "ID", "CHAR", "STRING", "ATRIB", "OP_SOMA", "OP_SUB", "OP_MULT", 
			"OP_DIV", "OP_LE", "OP_GE", "OP_EQ", "OP_NE", "OP_LT", "OP_GT", "PAR_ESQ", 
			"PAR_DIR", "CHAVE_ESQ", "CHAVE_DIR", "VIRGULA", "PONTO_VIRGULA", "PONTO", 
			"LINE_COMMENT", "BLOCK_COMMENT", "WS"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "Assis.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public AssisParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(AssisParser.EOF, 0); }
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(37);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 5369233022L) != 0)) {
				{
				{
				setState(34);
				statement();
				}
				}
				setState(39);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(40);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class StatementContext extends ParserRuleContext {
		public VarDeclContext varDecl() {
			return getRuleContext(VarDeclContext.class,0);
		}
		public IfStmtContext ifStmt() {
			return getRuleContext(IfStmtContext.class,0);
		}
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public ExprStmtContext exprStmt() {
			return getRuleContext(ExprStmtContext.class,0);
		}
		public FunctionDeclContext functionDecl() {
			return getRuleContext(FunctionDeclContext.class,0);
		}
		public WhileStatementContext whileStatement() {
			return getRuleContext(WhileStatementContext.class,0);
		}
		public ReturnStmtContext returnStmt() {
			return getRuleContext(ReturnStmtContext.class,0);
		}
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_statement);
		try {
			setState(49);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(42);
				varDecl();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(43);
				ifStmt();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(44);
				block();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(45);
				exprStmt();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(46);
				functionDecl();
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(47);
				whileStatement();
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(48);
				returnStmt();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FunctionDeclContext extends ParserRuleContext {
		public TerminalNode FUNC() { return getToken(AssisParser.FUNC, 0); }
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public TerminalNode ID() { return getToken(AssisParser.ID, 0); }
		public TerminalNode PAR_ESQ() { return getToken(AssisParser.PAR_ESQ, 0); }
		public TerminalNode PAR_DIR() { return getToken(AssisParser.PAR_DIR, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public ParamListContext paramList() {
			return getRuleContext(ParamListContext.class,0);
		}
		public FunctionDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_functionDecl; }
	}

	public final FunctionDeclContext functionDecl() throws RecognitionException {
		FunctionDeclContext _localctx = new FunctionDeclContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_functionDecl);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(51);
			match(FUNC);
			setState(52);
			type();
			setState(53);
			match(ID);
			setState(54);
			match(PAR_ESQ);
			setState(56);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 62L) != 0)) {
				{
				setState(55);
				paramList();
				}
			}

			setState(58);
			match(PAR_DIR);
			setState(59);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ParamListContext extends ParserRuleContext {
		public List<ParamContext> param() {
			return getRuleContexts(ParamContext.class);
		}
		public ParamContext param(int i) {
			return getRuleContext(ParamContext.class,i);
		}
		public List<TerminalNode> VIRGULA() { return getTokens(AssisParser.VIRGULA); }
		public TerminalNode VIRGULA(int i) {
			return getToken(AssisParser.VIRGULA, i);
		}
		public ParamListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_paramList; }
	}

	public final ParamListContext paramList() throws RecognitionException {
		ParamListContext _localctx = new ParamListContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_paramList);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(61);
			param();
			setState(66);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==VIRGULA) {
				{
				{
				setState(62);
				match(VIRGULA);
				setState(63);
				param();
				}
				}
				setState(68);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ParamContext extends ParserRuleContext {
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public TerminalNode ID() { return getToken(AssisParser.ID, 0); }
		public ParamContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_param; }
	}

	public final ParamContext param() throws RecognitionException {
		ParamContext _localctx = new ParamContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_param);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(69);
			type();
			setState(70);
			match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ReturnStmtContext extends ParserRuleContext {
		public TerminalNode RETURN() { return getToken(AssisParser.RETURN, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode PONTO_VIRGULA() { return getToken(AssisParser.PONTO_VIRGULA, 0); }
		public ReturnStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_returnStmt; }
	}

	public final ReturnStmtContext returnStmt() throws RecognitionException {
		ReturnStmtContext _localctx = new ReturnStmtContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_returnStmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(72);
			match(RETURN);
			setState(73);
			expr();
			setState(74);
			match(PONTO_VIRGULA);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class VarDeclContext extends ParserRuleContext {
		public TypeContext type() {
			return getRuleContext(TypeContext.class,0);
		}
		public TerminalNode ID() { return getToken(AssisParser.ID, 0); }
		public TerminalNode ATRIB() { return getToken(AssisParser.ATRIB, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode PONTO_VIRGULA() { return getToken(AssisParser.PONTO_VIRGULA, 0); }
		public VarDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_varDecl; }
	}

	public final VarDeclContext varDecl() throws RecognitionException {
		VarDeclContext _localctx = new VarDeclContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_varDecl);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(76);
			type();
			setState(77);
			match(ID);
			setState(78);
			match(ATRIB);
			setState(79);
			expr();
			setState(80);
			match(PONTO_VIRGULA);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class WhileStatementContext extends ParserRuleContext {
		public TerminalNode WHILE() { return getToken(AssisParser.WHILE, 0); }
		public TerminalNode PAR_ESQ() { return getToken(AssisParser.PAR_ESQ, 0); }
		public ExprLogContext exprLog() {
			return getRuleContext(ExprLogContext.class,0);
		}
		public TerminalNode PAR_DIR() { return getToken(AssisParser.PAR_DIR, 0); }
		public StatementContext statement() {
			return getRuleContext(StatementContext.class,0);
		}
		public WhileStatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_whileStatement; }
	}

	public final WhileStatementContext whileStatement() throws RecognitionException {
		WhileStatementContext _localctx = new WhileStatementContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_whileStatement);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(82);
			match(WHILE);
			setState(83);
			match(PAR_ESQ);
			setState(84);
			exprLog();
			setState(85);
			match(PAR_DIR);
			setState(86);
			statement();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TypeContext extends ParserRuleContext {
		public TerminalNode TP_INT() { return getToken(AssisParser.TP_INT, 0); }
		public TerminalNode TP_FLOAT() { return getToken(AssisParser.TP_FLOAT, 0); }
		public TerminalNode TP_CHAR() { return getToken(AssisParser.TP_CHAR, 0); }
		public TerminalNode TP_BOOL() { return getToken(AssisParser.TP_BOOL, 0); }
		public TerminalNode TP_STRING() { return getToken(AssisParser.TP_STRING, 0); }
		public TypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_type; }
	}

	public final TypeContext type() throws RecognitionException {
		TypeContext _localctx = new TypeContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_type);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(88);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 62L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class IfStmtContext extends ParserRuleContext {
		public TerminalNode KW_IF() { return getToken(AssisParser.KW_IF, 0); }
		public List<TerminalNode> PAR_ESQ() { return getTokens(AssisParser.PAR_ESQ); }
		public TerminalNode PAR_ESQ(int i) {
			return getToken(AssisParser.PAR_ESQ, i);
		}
		public List<ExprLogContext> exprLog() {
			return getRuleContexts(ExprLogContext.class);
		}
		public ExprLogContext exprLog(int i) {
			return getRuleContext(ExprLogContext.class,i);
		}
		public List<TerminalNode> PAR_DIR() { return getTokens(AssisParser.PAR_DIR); }
		public TerminalNode PAR_DIR(int i) {
			return getToken(AssisParser.PAR_DIR, i);
		}
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public List<TerminalNode> KW_ELSEIF() { return getTokens(AssisParser.KW_ELSEIF); }
		public TerminalNode KW_ELSEIF(int i) {
			return getToken(AssisParser.KW_ELSEIF, i);
		}
		public TerminalNode KW_ELSE() { return getToken(AssisParser.KW_ELSE, 0); }
		public IfStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ifStmt; }
	}

	public final IfStmtContext ifStmt() throws RecognitionException {
		IfStmtContext _localctx = new IfStmtContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_ifStmt);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(90);
			match(KW_IF);
			setState(91);
			match(PAR_ESQ);
			setState(92);
			exprLog();
			setState(93);
			match(PAR_DIR);
			setState(94);
			statement();
			setState(103);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(95);
					match(KW_ELSEIF);
					setState(96);
					match(PAR_ESQ);
					setState(97);
					exprLog();
					setState(98);
					match(PAR_DIR);
					setState(99);
					statement();
					}
					} 
				}
				setState(105);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
			}
			setState(108);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
			case 1:
				{
				setState(106);
				match(KW_ELSE);
				setState(107);
				statement();
				}
				break;
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BlockContext extends ParserRuleContext {
		public TerminalNode CHAVE_ESQ() { return getToken(AssisParser.CHAVE_ESQ, 0); }
		public TerminalNode CHAVE_DIR() { return getToken(AssisParser.CHAVE_DIR, 0); }
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public BlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_block; }
	}

	public final BlockContext block() throws RecognitionException {
		BlockContext _localctx = new BlockContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_block);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(110);
			match(CHAVE_ESQ);
			setState(114);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 5369233022L) != 0)) {
				{
				{
				setState(111);
				statement();
				}
				}
				setState(116);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(117);
			match(CHAVE_DIR);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExprStmtContext extends ParserRuleContext {
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode PONTO_VIRGULA() { return getToken(AssisParser.PONTO_VIRGULA, 0); }
		public ExprStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_exprStmt; }
	}

	public final ExprStmtContext exprStmt() throws RecognitionException {
		ExprStmtContext _localctx = new ExprStmtContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_exprStmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(119);
			expr();
			setState(120);
			match(PONTO_VIRGULA);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExprContext extends ParserRuleContext {
		public ExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expr; }
	 
		public ExprContext() { }
		public void copyFrom(ExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AtribuicaoContext extends ExprContext {
		public TerminalNode ID() { return getToken(AssisParser.ID, 0); }
		public TerminalNode ATRIB() { return getToken(AssisParser.ATRIB, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public AtribuicaoContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ComparacaoContext extends ExprContext {
		public ExprLogContext exprLog() {
			return getRuleContext(ExprLogContext.class,0);
		}
		public ComparacaoContext(ExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ExpressaoAritmeticaContext extends ExprContext {
		public AdditiveExprContext additiveExpr() {
			return getRuleContext(AdditiveExprContext.class,0);
		}
		public ExpressaoAritmeticaContext(ExprContext ctx) { copyFrom(ctx); }
	}

	public final ExprContext expr() throws RecognitionException {
		ExprContext _localctx = new ExprContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_expr);
		try {
			setState(127);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,7,_ctx) ) {
			case 1:
				_localctx = new AtribuicaoContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(122);
				match(ID);
				setState(123);
				match(ATRIB);
				setState(124);
				expr();
				}
				break;
			case 2:
				_localctx = new ComparacaoContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(125);
				exprLog();
				}
				break;
			case 3:
				_localctx = new ExpressaoAritmeticaContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(126);
				additiveExpr();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExprLogContext extends ParserRuleContext {
		public List<AdditiveExprContext> additiveExpr() {
			return getRuleContexts(AdditiveExprContext.class);
		}
		public AdditiveExprContext additiveExpr(int i) {
			return getRuleContext(AdditiveExprContext.class,i);
		}
		public TerminalNode OP_EQ() { return getToken(AssisParser.OP_EQ, 0); }
		public TerminalNode OP_NE() { return getToken(AssisParser.OP_NE, 0); }
		public TerminalNode OP_LT() { return getToken(AssisParser.OP_LT, 0); }
		public TerminalNode OP_GT() { return getToken(AssisParser.OP_GT, 0); }
		public TerminalNode OP_LE() { return getToken(AssisParser.OP_LE, 0); }
		public TerminalNode OP_GE() { return getToken(AssisParser.OP_GE, 0); }
		public ExprLogContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_exprLog; }
	}

	public final ExprLogContext exprLog() throws RecognitionException {
		ExprLogContext _localctx = new ExprLogContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_exprLog);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(129);
			additiveExpr();
			setState(130);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 1056964608L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			setState(131);
			additiveExpr();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AdditiveExprContext extends ParserRuleContext {
		public List<MultiplicativeExprContext> multiplicativeExpr() {
			return getRuleContexts(MultiplicativeExprContext.class);
		}
		public MultiplicativeExprContext multiplicativeExpr(int i) {
			return getRuleContext(MultiplicativeExprContext.class,i);
		}
		public List<TerminalNode> OP_SOMA() { return getTokens(AssisParser.OP_SOMA); }
		public TerminalNode OP_SOMA(int i) {
			return getToken(AssisParser.OP_SOMA, i);
		}
		public List<TerminalNode> OP_SUB() { return getTokens(AssisParser.OP_SUB); }
		public TerminalNode OP_SUB(int i) {
			return getToken(AssisParser.OP_SUB, i);
		}
		public AdditiveExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_additiveExpr; }
	}

	public final AdditiveExprContext additiveExpr() throws RecognitionException {
		AdditiveExprContext _localctx = new AdditiveExprContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_additiveExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(133);
			multiplicativeExpr();
			setState(138);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==OP_SOMA || _la==OP_SUB) {
				{
				{
				setState(134);
				_la = _input.LA(1);
				if ( !(_la==OP_SOMA || _la==OP_SUB) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(135);
				multiplicativeExpr();
				}
				}
				setState(140);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class MultiplicativeExprContext extends ParserRuleContext {
		public List<PrimaryExprContext> primaryExpr() {
			return getRuleContexts(PrimaryExprContext.class);
		}
		public PrimaryExprContext primaryExpr(int i) {
			return getRuleContext(PrimaryExprContext.class,i);
		}
		public List<TerminalNode> OP_MULT() { return getTokens(AssisParser.OP_MULT); }
		public TerminalNode OP_MULT(int i) {
			return getToken(AssisParser.OP_MULT, i);
		}
		public List<TerminalNode> OP_DIV() { return getTokens(AssisParser.OP_DIV); }
		public TerminalNode OP_DIV(int i) {
			return getToken(AssisParser.OP_DIV, i);
		}
		public MultiplicativeExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_multiplicativeExpr; }
	}

	public final MultiplicativeExprContext multiplicativeExpr() throws RecognitionException {
		MultiplicativeExprContext _localctx = new MultiplicativeExprContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_multiplicativeExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(141);
			primaryExpr();
			setState(146);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==OP_MULT || _la==OP_DIV) {
				{
				{
				setState(142);
				_la = _input.LA(1);
				if ( !(_la==OP_MULT || _la==OP_DIV) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(143);
				primaryExpr();
				}
				}
				setState(148);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrimaryExprContext extends ParserRuleContext {
		public PrimaryExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_primaryExpr; }
	 
		public PrimaryExprContext() { }
		public void copyFrom(PrimaryExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class EntreParentesesContext extends PrimaryExprContext {
		public TerminalNode PAR_ESQ() { return getToken(AssisParser.PAR_ESQ, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode PAR_DIR() { return getToken(AssisParser.PAR_DIR, 0); }
		public EntreParentesesContext(PrimaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ChamadaFuncaoContext extends PrimaryExprContext {
		public TerminalNode ID() { return getToken(AssisParser.ID, 0); }
		public TerminalNode PAR_ESQ() { return getToken(AssisParser.PAR_ESQ, 0); }
		public TerminalNode PAR_DIR() { return getToken(AssisParser.PAR_DIR, 0); }
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public List<TerminalNode> VIRGULA() { return getTokens(AssisParser.VIRGULA); }
		public TerminalNode VIRGULA(int i) {
			return getToken(AssisParser.VIRGULA, i);
		}
		public ChamadaFuncaoContext(PrimaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FalseLiteralContext extends PrimaryExprContext {
		public TerminalNode FALSE() { return getToken(AssisParser.FALSE, 0); }
		public FalseLiteralContext(PrimaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class EntreChavesContext extends PrimaryExprContext {
		public TerminalNode CHAVE_ESQ() { return getToken(AssisParser.CHAVE_ESQ, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode CHAVE_DIR() { return getToken(AssisParser.CHAVE_DIR, 0); }
		public EntreChavesContext(PrimaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FloatLiteralContext extends PrimaryExprContext {
		public TerminalNode REAL() { return getToken(AssisParser.REAL, 0); }
		public FloatLiteralContext(PrimaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CharLiteralContext extends PrimaryExprContext {
		public TerminalNode CHAR() { return getToken(AssisParser.CHAR, 0); }
		public CharLiteralContext(PrimaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TrueLiteralContext extends PrimaryExprContext {
		public TerminalNode TRUE() { return getToken(AssisParser.TRUE, 0); }
		public TrueLiteralContext(PrimaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class InteiroLiteralContext extends PrimaryExprContext {
		public TerminalNode INT() { return getToken(AssisParser.INT, 0); }
		public InteiroLiteralContext(PrimaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TextoLiteralContext extends PrimaryExprContext {
		public TerminalNode STRING() { return getToken(AssisParser.STRING, 0); }
		public TextoLiteralContext(PrimaryExprContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IdentificadorContext extends PrimaryExprContext {
		public TerminalNode ID() { return getToken(AssisParser.ID, 0); }
		public IdentificadorContext(PrimaryExprContext ctx) { copyFrom(ctx); }
	}

	public final PrimaryExprContext primaryExpr() throws RecognitionException {
		PrimaryExprContext _localctx = new PrimaryExprContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_primaryExpr);
		int _la;
		try {
			setState(177);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,12,_ctx) ) {
			case 1:
				_localctx = new ChamadaFuncaoContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(149);
				match(ID);
				setState(150);
				match(PAR_ESQ);
				setState(159);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 5369218560L) != 0)) {
					{
					setState(151);
					expr();
					setState(156);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==VIRGULA) {
						{
						{
						setState(152);
						match(VIRGULA);
						setState(153);
						expr();
						}
						}
						setState(158);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(161);
				match(PAR_DIR);
				}
				break;
			case 2:
				_localctx = new IdentificadorContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(162);
				match(ID);
				}
				break;
			case 3:
				_localctx = new InteiroLiteralContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(163);
				match(INT);
				}
				break;
			case 4:
				_localctx = new FloatLiteralContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(164);
				match(REAL);
				}
				break;
			case 5:
				_localctx = new CharLiteralContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(165);
				match(CHAR);
				}
				break;
			case 6:
				_localctx = new TextoLiteralContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(166);
				match(STRING);
				}
				break;
			case 7:
				_localctx = new TrueLiteralContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(167);
				match(TRUE);
				}
				break;
			case 8:
				_localctx = new FalseLiteralContext(_localctx);
				enterOuterAlt(_localctx, 8);
				{
				setState(168);
				match(FALSE);
				}
				break;
			case 9:
				_localctx = new EntreParentesesContext(_localctx);
				enterOuterAlt(_localctx, 9);
				{
				setState(169);
				match(PAR_ESQ);
				setState(170);
				expr();
				setState(171);
				match(PAR_DIR);
				}
				break;
			case 10:
				_localctx = new EntreChavesContext(_localctx);
				enterOuterAlt(_localctx, 10);
				{
				setState(173);
				match(CHAVE_ESQ);
				setState(174);
				expr();
				setState(175);
				match(CHAVE_DIR);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001\'\u00b4\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0001\u0000\u0005\u0000$\b\u0000\n\u0000\f\u0000"+
		"\'\t\u0000\u0001\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0003\u00012\b\u0001"+
		"\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0003\u0002"+
		"9\b\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0003\u0001\u0003"+
		"\u0001\u0003\u0005\u0003A\b\u0003\n\u0003\f\u0003D\t\u0003\u0001\u0004"+
		"\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007"+
		"\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001"+
		"\t\u0001\t\u0001\t\u0001\t\u0001\t\u0005\tf\b\t\n\t\f\ti\t\t\u0001\t\u0001"+
		"\t\u0003\tm\b\t\u0001\n\u0001\n\u0005\nq\b\n\n\n\f\nt\t\n\u0001\n\u0001"+
		"\n\u0001\u000b\u0001\u000b\u0001\u000b\u0001\f\u0001\f\u0001\f\u0001\f"+
		"\u0001\f\u0003\f\u0080\b\f\u0001\r\u0001\r\u0001\r\u0001\r\u0001\u000e"+
		"\u0001\u000e\u0001\u000e\u0005\u000e\u0089\b\u000e\n\u000e\f\u000e\u008c"+
		"\t\u000e\u0001\u000f\u0001\u000f\u0001\u000f\u0005\u000f\u0091\b\u000f"+
		"\n\u000f\f\u000f\u0094\t\u000f\u0001\u0010\u0001\u0010\u0001\u0010\u0001"+
		"\u0010\u0001\u0010\u0005\u0010\u009b\b\u0010\n\u0010\f\u0010\u009e\t\u0010"+
		"\u0003\u0010\u00a0\b\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010"+
		"\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010"+
		"\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010"+
		"\u0003\u0010\u00b2\b\u0010\u0001\u0010\u0000\u0000\u0011\u0000\u0002\u0004"+
		"\u0006\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u001e \u0000"+
		"\u0004\u0001\u0000\u0001\u0005\u0001\u0000\u0018\u001d\u0001\u0000\u0014"+
		"\u0015\u0001\u0000\u0016\u0017\u00bd\u0000%\u0001\u0000\u0000\u0000\u0002"+
		"1\u0001\u0000\u0000\u0000\u00043\u0001\u0000\u0000\u0000\u0006=\u0001"+
		"\u0000\u0000\u0000\bE\u0001\u0000\u0000\u0000\nH\u0001\u0000\u0000\u0000"+
		"\fL\u0001\u0000\u0000\u0000\u000eR\u0001\u0000\u0000\u0000\u0010X\u0001"+
		"\u0000\u0000\u0000\u0012Z\u0001\u0000\u0000\u0000\u0014n\u0001\u0000\u0000"+
		"\u0000\u0016w\u0001\u0000\u0000\u0000\u0018\u007f\u0001\u0000\u0000\u0000"+
		"\u001a\u0081\u0001\u0000\u0000\u0000\u001c\u0085\u0001\u0000\u0000\u0000"+
		"\u001e\u008d\u0001\u0000\u0000\u0000 \u00b1\u0001\u0000\u0000\u0000\""+
		"$\u0003\u0002\u0001\u0000#\"\u0001\u0000\u0000\u0000$\'\u0001\u0000\u0000"+
		"\u0000%#\u0001\u0000\u0000\u0000%&\u0001\u0000\u0000\u0000&(\u0001\u0000"+
		"\u0000\u0000\'%\u0001\u0000\u0000\u0000()\u0005\u0000\u0000\u0001)\u0001"+
		"\u0001\u0000\u0000\u0000*2\u0003\f\u0006\u0000+2\u0003\u0012\t\u0000,"+
		"2\u0003\u0014\n\u0000-2\u0003\u0016\u000b\u0000.2\u0003\u0004\u0002\u0000"+
		"/2\u0003\u000e\u0007\u000002\u0003\n\u0005\u00001*\u0001\u0000\u0000\u0000"+
		"1+\u0001\u0000\u0000\u00001,\u0001\u0000\u0000\u00001-\u0001\u0000\u0000"+
		"\u00001.\u0001\u0000\u0000\u00001/\u0001\u0000\u0000\u000010\u0001\u0000"+
		"\u0000\u00002\u0003\u0001\u0000\u0000\u000034\u0005\u000b\u0000\u0000"+
		"45\u0003\u0010\b\u000056\u0005\u0010\u0000\u000068\u0005\u001e\u0000\u0000"+
		"79\u0003\u0006\u0003\u000087\u0001\u0000\u0000\u000089\u0001\u0000\u0000"+
		"\u00009:\u0001\u0000\u0000\u0000:;\u0005\u001f\u0000\u0000;<\u0003\u0014"+
		"\n\u0000<\u0005\u0001\u0000\u0000\u0000=B\u0003\b\u0004\u0000>?\u0005"+
		"\"\u0000\u0000?A\u0003\b\u0004\u0000@>\u0001\u0000\u0000\u0000AD\u0001"+
		"\u0000\u0000\u0000B@\u0001\u0000\u0000\u0000BC\u0001\u0000\u0000\u0000"+
		"C\u0007\u0001\u0000\u0000\u0000DB\u0001\u0000\u0000\u0000EF\u0003\u0010"+
		"\b\u0000FG\u0005\u0010\u0000\u0000G\t\u0001\u0000\u0000\u0000HI\u0005"+
		"\f\u0000\u0000IJ\u0003\u0018\f\u0000JK\u0005#\u0000\u0000K\u000b\u0001"+
		"\u0000\u0000\u0000LM\u0003\u0010\b\u0000MN\u0005\u0010\u0000\u0000NO\u0005"+
		"\u0013\u0000\u0000OP\u0003\u0018\f\u0000PQ\u0005#\u0000\u0000Q\r\u0001"+
		"\u0000\u0000\u0000RS\u0005\r\u0000\u0000ST\u0005\u001e\u0000\u0000TU\u0003"+
		"\u001a\r\u0000UV\u0005\u001f\u0000\u0000VW\u0003\u0002\u0001\u0000W\u000f"+
		"\u0001\u0000\u0000\u0000XY\u0007\u0000\u0000\u0000Y\u0011\u0001\u0000"+
		"\u0000\u0000Z[\u0005\u0006\u0000\u0000[\\\u0005\u001e\u0000\u0000\\]\u0003"+
		"\u001a\r\u0000]^\u0005\u001f\u0000\u0000^g\u0003\u0002\u0001\u0000_`\u0005"+
		"\b\u0000\u0000`a\u0005\u001e\u0000\u0000ab\u0003\u001a\r\u0000bc\u0005"+
		"\u001f\u0000\u0000cd\u0003\u0002\u0001\u0000df\u0001\u0000\u0000\u0000"+
		"e_\u0001\u0000\u0000\u0000fi\u0001\u0000\u0000\u0000ge\u0001\u0000\u0000"+
		"\u0000gh\u0001\u0000\u0000\u0000hl\u0001\u0000\u0000\u0000ig\u0001\u0000"+
		"\u0000\u0000jk\u0005\u0007\u0000\u0000km\u0003\u0002\u0001\u0000lj\u0001"+
		"\u0000\u0000\u0000lm\u0001\u0000\u0000\u0000m\u0013\u0001\u0000\u0000"+
		"\u0000nr\u0005 \u0000\u0000oq\u0003\u0002\u0001\u0000po\u0001\u0000\u0000"+
		"\u0000qt\u0001\u0000\u0000\u0000rp\u0001\u0000\u0000\u0000rs\u0001\u0000"+
		"\u0000\u0000su\u0001\u0000\u0000\u0000tr\u0001\u0000\u0000\u0000uv\u0005"+
		"!\u0000\u0000v\u0015\u0001\u0000\u0000\u0000wx\u0003\u0018\f\u0000xy\u0005"+
		"#\u0000\u0000y\u0017\u0001\u0000\u0000\u0000z{\u0005\u0010\u0000\u0000"+
		"{|\u0005\u0013\u0000\u0000|\u0080\u0003\u0018\f\u0000}\u0080\u0003\u001a"+
		"\r\u0000~\u0080\u0003\u001c\u000e\u0000\u007fz\u0001\u0000\u0000\u0000"+
		"\u007f}\u0001\u0000\u0000\u0000\u007f~\u0001\u0000\u0000\u0000\u0080\u0019"+
		"\u0001\u0000\u0000\u0000\u0081\u0082\u0003\u001c\u000e\u0000\u0082\u0083"+
		"\u0007\u0001\u0000\u0000\u0083\u0084\u0003\u001c\u000e\u0000\u0084\u001b"+
		"\u0001\u0000\u0000\u0000\u0085\u008a\u0003\u001e\u000f\u0000\u0086\u0087"+
		"\u0007\u0002\u0000\u0000\u0087\u0089\u0003\u001e\u000f\u0000\u0088\u0086"+
		"\u0001\u0000\u0000\u0000\u0089\u008c\u0001\u0000\u0000\u0000\u008a\u0088"+
		"\u0001\u0000\u0000\u0000\u008a\u008b\u0001\u0000\u0000\u0000\u008b\u001d"+
		"\u0001\u0000\u0000\u0000\u008c\u008a\u0001\u0000\u0000\u0000\u008d\u0092"+
		"\u0003 \u0010\u0000\u008e\u008f\u0007\u0003\u0000\u0000\u008f\u0091\u0003"+
		" \u0010\u0000\u0090\u008e\u0001\u0000\u0000\u0000\u0091\u0094\u0001\u0000"+
		"\u0000\u0000\u0092\u0090\u0001\u0000\u0000\u0000\u0092\u0093\u0001\u0000"+
		"\u0000\u0000\u0093\u001f\u0001\u0000\u0000\u0000\u0094\u0092\u0001\u0000"+
		"\u0000\u0000\u0095\u0096\u0005\u0010\u0000\u0000\u0096\u009f\u0005\u001e"+
		"\u0000\u0000\u0097\u009c\u0003\u0018\f\u0000\u0098\u0099\u0005\"\u0000"+
		"\u0000\u0099\u009b\u0003\u0018\f\u0000\u009a\u0098\u0001\u0000\u0000\u0000"+
		"\u009b\u009e\u0001\u0000\u0000\u0000\u009c\u009a\u0001\u0000\u0000\u0000"+
		"\u009c\u009d\u0001\u0000\u0000\u0000\u009d\u00a0\u0001\u0000\u0000\u0000"+
		"\u009e\u009c\u0001\u0000\u0000\u0000\u009f\u0097\u0001\u0000\u0000\u0000"+
		"\u009f\u00a0\u0001\u0000\u0000\u0000\u00a0\u00a1\u0001\u0000\u0000\u0000"+
		"\u00a1\u00b2\u0005\u001f\u0000\u0000\u00a2\u00b2\u0005\u0010\u0000\u0000"+
		"\u00a3\u00b2\u0005\u000f\u0000\u0000\u00a4\u00b2\u0005\u000e\u0000\u0000"+
		"\u00a5\u00b2\u0005\u0011\u0000\u0000\u00a6\u00b2\u0005\u0012\u0000\u0000"+
		"\u00a7\u00b2\u0005\t\u0000\u0000\u00a8\u00b2\u0005\n\u0000\u0000\u00a9"+
		"\u00aa\u0005\u001e\u0000\u0000\u00aa\u00ab\u0003\u0018\f\u0000\u00ab\u00ac"+
		"\u0005\u001f\u0000\u0000\u00ac\u00b2\u0001\u0000\u0000\u0000\u00ad\u00ae"+
		"\u0005 \u0000\u0000\u00ae\u00af\u0003\u0018\f\u0000\u00af\u00b0\u0005"+
		"!\u0000\u0000\u00b0\u00b2\u0001\u0000\u0000\u0000\u00b1\u0095\u0001\u0000"+
		"\u0000\u0000\u00b1\u00a2\u0001\u0000\u0000\u0000\u00b1\u00a3\u0001\u0000"+
		"\u0000\u0000\u00b1\u00a4\u0001\u0000\u0000\u0000\u00b1\u00a5\u0001\u0000"+
		"\u0000\u0000\u00b1\u00a6\u0001\u0000\u0000\u0000\u00b1\u00a7\u0001\u0000"+
		"\u0000\u0000\u00b1\u00a8\u0001\u0000\u0000\u0000\u00b1\u00a9\u0001\u0000"+
		"\u0000\u0000\u00b1\u00ad\u0001\u0000\u0000\u0000\u00b2!\u0001\u0000\u0000"+
		"\u0000\r%18Bglr\u007f\u008a\u0092\u009c\u009f\u00b1";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}