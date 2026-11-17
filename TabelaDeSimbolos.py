"""
Tabela de símbolos com pilha de escopos (porte de TabelaDeSimbolos.dart).

* Escopo 0 = Global. Cada bloco/função empilha um novo escopo.
* Funções também ficam na tabela (tipo 'funct'); a assinatura
  (tipo de retorno + tipos dos parâmetros) é guardada à parte para
  permitir a checagem de chamadas.
"""


class TabelaDeSimbolos:
    def __init__(self):
        self._escopos: list[dict[str, str]] = [{}]   # pilha de escopos
        self._historico: list[dict[str, str]] = []   # {nome, tipo, escopo} p/ dump
        self._assinaturas: dict[str, tuple[str, list[str]]] = {}

    def entrar_escopo(self) -> None:
        self._escopos.append({})

    def sair_escopo(self) -> None:
        if len(self._escopos) > 1:
            self._escopos.pop()

    def existe(self, nome: str) -> bool:
        """True se `nome` está visível em algum escopo."""
        return any(nome in escopo for escopo in reversed(self._escopos))

    def adicionar(self, nome: str, tipo: str, descricao: str | None = None) -> bool:
        """Declara `nome` no escopo atual. False se já existir NESTE escopo.
        `descricao` (opcional) só muda o texto exibido no dump."""
        atual = self._escopos[-1]
        if nome in atual:
            return False
        atual[nome] = tipo
        self._historico.append({
            "nome": nome,
            "tipo": descricao or tipo,
            "escopo": "Global" if len(self._escopos) == 1
                      else f"Local (Nível {len(self._escopos) - 1})",
        })
        return True

    def get_tipo(self, nome: str) -> str | None:
        """Tipo do símbolo visível mais interno, ou None se não declarado."""
        for escopo in reversed(self._escopos):
            if nome in escopo:
                return escopo[nome]
        return None

    # ---- funções ---------------------------------------------------
    def adicionar_funcao(self, nome: str, retorno: str, params: list[str]) -> bool:
        desc = f"funct {retorno}({', '.join(params)})"
        if not self.adicionar(nome, "funct", desc):
            return False
        self._assinaturas[nome] = (retorno, params)
        return True

    def get_funcao(self, nome: str) -> tuple[str, list[str]] | None:
        """(tipo_retorno, [tipos dos parâmetros]) ou None se não for função."""
        if self.get_tipo(nome) == "funct":
            return self._assinaturas.get(nome)
        return None

    def dump(self) -> str:
        if not self._historico:
            return "Tabela de Símbolos vazia.\n"
        linhas = ["NOME\t|\tTIPO\t|\tESCOPO",
                  "------------------------------------------"]
        for item in self._historico:
            linhas.append(f"{item['nome']}\t|\t{item['tipo']}\t|\t{item['escopo']}")
        return "\n".join(linhas) + "\n"